# History and application recovery ownership

**Disposition:** retain core/1; earlier recovery-extension approach superseded.
**Subjects:** recovery; history; retained outcomes; service ownership.

## Decision

Document the recovery use cases and assign them to responsible network/application
actors and client infrastructure using the existing protocol. The identified
needs do not justify a recovery extension, transparent restoration of old
conversations or stronger core acknowledgement semantics.

This replaces the earlier treatment of recovery as an optional extension awaiting
a mechanism. No such extension is selected or required to complete core. Its
candidate traces were proposals, not adopted conformance obligations.

## Basis and application

Existing consumers need to recover a missed result after client restart, catch up
history and reconcile paged records. These uses establish service needs, not a
requirement to restore lost protocol interpretation state.

A client can establish a fresh valid context and ask the responsible actor for a
retained outcome. The fresh result answers that lookup and may carry a historical
artifact as data. It does not inject an old result as live traffic for an unknown
turn. The service defines authority, retention, completeness and historical trust.

| Use | Owner and retained distinction |
|---|---|
| Missed outcome | Work owner or record actor; retrieving the outcome does not request execution again |
| Transcript catch-up and paging | History actor and reader; missing or incomplete records are not proof of non-execution |
| Saved submissions | Client infrastructure; saved signed bytes do not authorize resending across a retired scope |
| Long-running job restart | Work owner; application state and effect reconciliation do not automatically restore core turns |
| External effect before recording | Effect owner and collaborating record service; a record actor cannot recover information it never received |
| Historical signed evidence | Evidence service and verifier; old timestamps alone cannot prove earlier authenticated admission |

## Limits and consequences

Networks must define and test their actual service promises, including the gap
between an external effect and its record. A missing result or new message ID
cannot make repeating uncertain work safe. Core acceptance remains scoped to a
live context; a duplicate's minimal acknowledgement is not reply retrieval.

This scope decision closes the protocol question without claiming completed
consumer services, runtime recovery or migration. Any future proposal to change
core guarantees requires a separately demonstrated need and explicit agreement.

## Current authority and related decisions

The [network guide](../network-development.md#history-and-application-recovery)
contains current use and acceptance guidance; [implementation guidance](../implementation.md)
retains the outstanding engineering obligations. See [delivery/context](delivery-and-context.md)
for scope retirement and [security/evidence](security-and-evidence.md) for history trust.
