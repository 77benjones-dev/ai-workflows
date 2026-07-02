#!/usr/bin/env python3
"""Local Sonos control for Codex.

This intentionally uses the LAN UPnP/SOAP path through SoCo rather than the
OpenClaw sonoscli binary or Sonos cloud APIs.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any, Iterable

import soco
from soco import SoCo
from soco.exceptions import SoCoException, SoCoUPnPException


@dataclass
class Options:
    timeout: float
    scan: bool
    interface: str | None
    json_output: bool


def print_result(data: Any, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2, sort_keys=True, default=str))
        return
    if isinstance(data, list):
        for row in data:
            if isinstance(row, dict):
                print(" | ".join(f"{key}: {value}" for key, value in row.items()))
            else:
                print(row)
        return
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
        return
    print(data)


def discover(options: Options, *, include_invisible: bool = False) -> list[SoCo]:
    zones = soco.discover(
        timeout=options.timeout,
        include_invisible=include_invisible,
        interface_addr=options.interface,
        allow_network_scan=options.scan,
        scan_timeout=0.5,
        min_netmask=24,
    )
    if not zones and not options.scan:
        # Some networks filter SSDP multicast. Retrying with a local network
        # scan keeps routine commands usable while still allowing --ip fallback.
        zones = soco.discover(
            timeout=options.timeout,
            include_invisible=include_invisible,
            interface_addr=options.interface,
            allow_network_scan=True,
            scan_timeout=0.5,
            min_netmask=24,
        )
    return sorted(zones or [], key=lambda zone: (safe_name(zone), zone.ip_address))


def safe_name(zone: SoCo) -> str:
    try:
        return zone.player_name
    except Exception:
        return "(unknown)"


def zone_summary(zone: SoCo) -> dict[str, Any]:
    info: dict[str, Any] = {}
    try:
        info = zone.get_speaker_info()
    except Exception:
        pass
    return {
        "name": safe_name(zone),
        "ip": zone.ip_address,
        "uid": getattr(zone, "uid", ""),
        "model": info.get("model_name", ""),
        "visible": getattr(zone, "is_visible", None),
        "coordinator": getattr(zone, "is_coordinator", None),
        "household": getattr(zone, "household_id", ""),
    }


def find_zone(name: str | None, ip: str | None, options: Options) -> SoCo:
    if ip:
        return SoCo(ip)
    if not name:
        zones = discover(options)
        if not zones:
            raise RuntimeError("No Sonos speakers found. Try --ip <speaker-ip> or --scan.")
        return zones[0]
    for zone in discover(options, include_invisible=True):
        if safe_name(zone).casefold() == name.casefold():
            return zone
    raise RuntimeError(f"No Sonos speaker named {name!r} found. Run discover to list rooms.")


def coordinator(zone: SoCo) -> SoCo:
    # Sonos transport commands are accepted by the group coordinator; routing
    # them here makes play/pause/queue actions work even when the named room is
    # a grouped satellite.
    try:
        return zone.group.coordinator
    except Exception:
        return zone


def current_track(zone: SoCo) -> dict[str, Any]:
    try:
        track = zone.get_current_track_info()
    except Exception:
        track = {}
    return {
        "title": track.get("title", ""),
        "artist": track.get("artist", ""),
        "album": track.get("album", ""),
        "position": track.get("position", ""),
        "duration": track.get("duration", ""),
        "uri": track.get("uri", ""),
    }


def status(zone: SoCo) -> dict[str, Any]:
    transport: dict[str, Any] = {}
    try:
        transport = coordinator(zone).get_current_transport_info()
    except Exception:
        pass
    group_members = []
    try:
        group_members = [safe_name(member) for member in zone.group.members]
    except Exception:
        pass
    return {
        **zone_summary(zone),
        "volume": zone.volume,
        "mute": zone.mute,
        "state": transport.get("current_transport_state", ""),
        "group_coordinator": safe_name(coordinator(zone)),
        "group_members": group_members,
        "track": current_track(coordinator(zone)),
    }


def require_int(value: str, *, minimum: int = 0, maximum: int = 100) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < minimum or parsed > maximum:
        raise argparse.ArgumentTypeError(f"must be between {minimum} and {maximum}")
    return parsed


def run_discover(args: argparse.Namespace, options: Options) -> Any:
    zones = discover(options, include_invisible=args.include_invisible)
    return [zone_summary(zone) for zone in zones]


def run_status(args: argparse.Namespace, options: Options) -> Any:
    return status(find_zone(args.name, args.ip, options))


def run_transport(args: argparse.Namespace, options: Options) -> Any:
    zone = coordinator(find_zone(args.name, args.ip, options))
    action = args.transport_action
    getattr(zone, action)()
    return status(zone)


def run_volume(args: argparse.Namespace, options: Options) -> Any:
    zone = find_zone(args.name, args.ip, options)
    if args.volume_action == "get":
        return {"name": safe_name(zone), "volume": zone.volume, "mute": zone.mute}
    if args.volume_action == "set":
        zone.volume = args.level
    elif args.volume_action == "up":
        zone.volume = min(100, zone.volume + args.step)
    elif args.volume_action == "down":
        zone.volume = max(0, zone.volume - args.step)
    elif args.volume_action == "mute":
        zone.mute = True
    elif args.volume_action == "unmute":
        zone.mute = False
    return {"name": safe_name(zone), "volume": zone.volume, "mute": zone.mute}


def run_group(args: argparse.Namespace, options: Options) -> Any:
    zone = find_zone(args.name, args.ip, options)
    if args.group_action == "status":
        return {
            "name": safe_name(zone),
            "coordinator": safe_name(coordinator(zone)),
            "members": [safe_name(member) for member in zone.group.members],
        }
    if args.group_action == "join":
        target = find_zone(args.target, None, options)
        zone.join(target)
    elif args.group_action == "unjoin":
        zone.unjoin()
    elif args.group_action == "solo":
        zone.unjoin()
    elif args.group_action == "party":
        zone.partymode()
    return {
        "name": safe_name(zone),
        "coordinator": safe_name(coordinator(zone)),
        "members": [safe_name(member) for member in zone.group.members],
    }


def run_favorites(args: argparse.Namespace, options: Options) -> Any:
    zone = coordinator(find_zone(args.name, args.ip, options))
    favorites = zone.music_library.get_sonos_favorites()
    rows = [{"index": i + 1, "title": fav.title, "uri": fav.resources[0].uri if fav.resources else ""} for i, fav in enumerate(favorites)]
    if args.favorite_action == "list":
        return rows
    if args.index < 1 or args.index > len(favorites):
        raise RuntimeError(f"Favorite index must be between 1 and {len(favorites)}.")
    zone.clear_queue()
    zone.add_to_queue(favorites[args.index - 1])
    zone.play_from_queue(0)
    return status(zone)


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Print machine-readable JSON.")
    common.add_argument("--timeout", type=float, default=argparse.SUPPRESS, help="Discovery timeout in seconds.")
    common.add_argument("--scan", action="store_true", default=argparse.SUPPRESS, help="Fallback to network scan when SSDP multicast fails.")
    common.add_argument("--interface", default=argparse.SUPPRESS, help="IPv4 address of the local interface to use for discovery.")

    parser = argparse.ArgumentParser(description="Control local Sonos speakers from Codex.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--timeout", type=float, default=5.0, help="Discovery timeout in seconds.")
    parser.add_argument("--scan", action="store_true", help="Fallback to network scan when SSDP multicast fails.")
    parser.add_argument("--interface", help="IPv4 address of the local interface to use for discovery.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser("discover", parents=[common], help="List Sonos speakers on the LAN.")
    discover_parser.add_argument("--include-invisible", action="store_true", help="Include bridges and stereo-pair satellites.")
    discover_parser.set_defaults(func=run_discover)

    def add_target(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--name", help="Room/player name, e.g. Kitchen.")
        subparser.add_argument("--ip", help="Speaker IP if discovery fails.")

    status_parser = subparsers.add_parser("status", parents=[common], help="Show room state, volume, group, and current track.")
    add_target(status_parser)
    status_parser.set_defaults(func=run_status)

    for action in ("play", "pause", "stop", "next", "previous"):
        transport_parser = subparsers.add_parser(action, parents=[common], help=f"{action.capitalize()} a room/group.")
        add_target(transport_parser)
        transport_parser.set_defaults(func=run_transport, transport_action=action)

    volume_parser = subparsers.add_parser("volume", parents=[common], help="Get or change room volume.")
    add_target(volume_parser)
    volume_subparsers = volume_parser.add_subparsers(dest="volume_action", required=True)
    volume_subparsers.add_parser("get")
    set_parser = volume_subparsers.add_parser("set")
    set_parser.add_argument("level", type=require_int)
    up_parser = volume_subparsers.add_parser("up")
    up_parser.add_argument("step", nargs="?", default=5, type=require_int)
    down_parser = volume_subparsers.add_parser("down")
    down_parser.add_argument("step", nargs="?", default=5, type=require_int)
    volume_subparsers.add_parser("mute")
    volume_subparsers.add_parser("unmute")
    volume_parser.set_defaults(func=run_volume)

    group_parser = subparsers.add_parser("group", parents=[common], help="Inspect or change grouping.")
    add_target(group_parser)
    group_subparsers = group_parser.add_subparsers(dest="group_action", required=True)
    group_subparsers.add_parser("status")
    join_parser = group_subparsers.add_parser("join")
    join_parser.add_argument("target", help="Room name to join.")
    group_subparsers.add_parser("unjoin")
    group_subparsers.add_parser("solo")
    group_subparsers.add_parser("party")
    group_parser.set_defaults(func=run_group)

    favorites_parser = subparsers.add_parser("favorites", parents=[common], help="List or play Sonos favorites.")
    add_target(favorites_parser)
    favorites_subparsers = favorites_parser.add_subparsers(dest="favorite_action", required=True)
    favorites_subparsers.add_parser("list")
    open_parser = favorites_subparsers.add_parser("open")
    open_parser.add_argument("index", type=int)
    favorites_parser.set_defaults(func=run_favorites)

    return parser


def normalize_global_args(argv: list[str]) -> list[str]:
    global_flags = {"--json", "--scan"}
    global_value_flags = {"--timeout", "--interface"}
    moved: list[str] = []
    rest: list[str] = []
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in global_flags:
            moved.append(arg)
            index += 1
        elif arg in global_value_flags and index + 1 < len(argv):
            moved.extend([arg, argv[index + 1]])
            index += 2
        else:
            rest.append(arg)
            index += 1
    return moved + rest


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    raw_argv = list(argv) if argv is not None else sys.argv[1:]
    args = parser.parse_args(normalize_global_args(raw_argv))
    options = Options(args.timeout, args.scan, args.interface, args.json)
    try:
        print_result(args.func(args, options), as_json=args.json)
        return 0
    except (RuntimeError, SoCoException, SoCoUPnPException, OSError) as exc:
        print(f"sonos error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
