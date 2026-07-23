# Saved Search Alerts User Stories

## Saved Search Management

### SSM-01: Save the current search (TBD)

**Priority:** Critical

#### Problem Statement

As a returning customer, I want to save my current search so that I can revisit it without rebuilding the same filters.

Customers currently repeat the same setup whenever they return. Saving the search reduces repeated work and creates the foundation for optional alerts.

#### Flow

A signed-in customer runs a search and selects the option to save it. They provide a recognizable name and see confirmation that the search is available from their account.

#### Acceptance Criteria

1. Given a signed-in customer is viewing search results, when they save the current search with a valid name, then they see confirmation that the search was saved.
2. Given a signed-in customer has saved a search, when they open their saved searches, then they see the saved name and can reopen the matching results.
3. Given a customer is not signed in, when they try to save a search, then they are prompted to sign in before continuing.
4. Given a signed-in customer enters a name already used by another saved search, when they try to save it, then they see guidance to choose a different name.

#### Out of scope

- Editing filters after the search is saved.
- Enabling notifications during the initial save flow.

#### Missing details

1. Confirm whether the number of saved searches should be limited.

#### Design

TBD

### SSM-02: Remove a saved search (TBD)

**Priority:** High

#### Problem Statement

As a returning customer, I want to remove a saved search so that my list contains only searches I still use.

#### Flow

A customer opens their saved searches and chooses one to remove. They confirm the action and the search disappears from the list.

#### Acceptance Criteria

1. Given a customer is viewing their saved searches, when they confirm removal of a saved search, then it no longer appears in the list.
2. Given a saved search has notifications enabled, when the customer removes it, then they see confirmation that its notifications will also stop.

#### Design

TBD
