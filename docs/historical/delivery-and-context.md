# Delivery evidence, context lifetime and diagnostics

**Disposition:** adopted for core/1 and its provisioned-context profile.
**Subjects:** delivery; duplicates; notifications; continuity; diagnostics.

## Decision

Interpret delivery using retained identities, references and established facts,
not arrival order. A valid result or question may arrive before `taken` for a
known opening. Missing reports do not establish failure, execution order or the
actor's current turn. Late reports can add knowledge without repeating a
transition or reopening terminal work.

Progress replacement establishes only its explicit valid relationships. Unknown
predecessors remain unresolved; they do not reserve another sender's identity.
Refusal alone does not invalidate a later update. Required ambiguous references
are refused rather than guessed. Exact duplicates preserve established
dispositions; conflicting bytes under the same scoped identity remain conflicts.

Explicitly establish a conversation's authorized scope before admission and
retire its guard before discarding required interpretation state. A missing
context is not permission to recreate one from traffic. A known principal, live
socket, saved outbox or historical record alone proves no current continuity.

The concrete `keel.provisioned-context.v1` profile uses trusted provisioning at
both endpoints, a fresh actor-issued conversation key, actual-channel association
and bilateral readiness before traffic. Its memory-only scope ends on connection
loss or local retirement. Reconnection requires fresh setup, not automatic replay.

## Diagnostics and controls

Verification diagnostics require authenticated association with the original
attempt, authorized route and scope before affecting retry state. They do not
confirm semantic acceptance or prove non-execution. Controls receive no core
reply; unclassifiable frames follow the binding rejection rules. Old callbacks
cannot act on a replacement connection or borrow its scope.

## Basis and limits

Delay, duplication and interruption leave different participants with incomplete
knowledge. The protocol preserves these distinctions while infrastructure chooses
representation, retry scheduling, presentation and local resource policy.
Local release of a retry or sending slot does not establish delivery.

Admission guards prevent stale work within the selected profile's failure
boundary. They do not guarantee accepted work finishes, results remain retrievable
or effects occur exactly once. No universal restoration mechanism, incarnation
field or permanent history service was introduced.

## Current authority and related decisions

[Messaging](../../core/messaging.md), [notifications](../../core/notifications.md),
[diagnostics](../../core/diagnostics.md), [continuity](../../core/continuity.md) and
the [provisioned context](../../core/profiles/provisioned-context.md) define the
rules. See [recovery ownership](recovery-and-service-ownership.md) for service
responsibilities after scope loss, and [security](security-and-evidence.md) for
retained authentication and response audiences.
