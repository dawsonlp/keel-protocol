# Provisioned direct grant profile

**Identity:** `keel.provisioned-direct-grant.v1`. This optional profile adds a
fixed delegated authority association to core/1 over
[`keel.provisioned-context.v1`](../../core/profiles/provisioned-context.md).
The core schema, signed message type and WebSocket subprotocol remain applicable.
The profile defines no new core message kind, field, refusal or setup wire format.

## Authority association and readiness

This profile applies only in the requester-to-actor direction of an explicitly
provisioned conversation. Both peers independently authorize the facility used
to set up the scope. Before provisioning, the requester selects the intended
exact [signed grant](direct-grant.md). The facility installs a matching immutable
association at both endpoints alongside the continuity descriptor. It includes
the profile identity, independently governed namespace, actual channel and local
guard, fresh conversation ID, recorded actor and requester roles, exact compact
grant, subject, holder/key, audience and understood permission contract.

Before reporting ready, both endpoints confirm their intended association,
including the exact artifact and selected permission contract. The receiving actor
validates the grant under current configured trust, verifies the audience is its
own actor principal and the holder is the recorded requester, and checks the
holder key against the certified key provisioned for requester signing. The
requester must be configured to sign protected messages with that key. Each signer
still authenticates under core. The grant issuer and provisioner may be different.
Provisioning cannot confer permission beyond a verified grant.

Any unsupported profile, mismatched descriptor, invalid grant or denied setup
leaves the scope unestablished. The control path reports setup failure to its
authorized participants without placing a core refusal on the message path.
Follow provisioned-context bilateral readiness and activation before enabling
sending. A receiver cannot silently establish ordinary core for a requester that
selected this profile. The signed conversation ID binds each ordinary core message
to the authority association by way of the established guard. It carries no grant
semantics in isolation. A valid artifact cannot open a scope from a received frame.

The existing interaction-agreement profile may also be selected. Its offering
constraints and this profile's permission constraints must both hold. Losing a
required association or its enforcement state retires the original scope under
the continuity procedure before discarding state. Renewal, replacement, a change
of holder key or subject, and new use after connection loss each require fresh
setup with a fresh conversation ID. A grant may be selected in more than one
fresh scope while applicable. Pending work, permissions granted by ordinary
approvals, and dispositions retain their original meanings. They do not move to
the new scope. Scope retirement proves no effect or cancellation outcome.

## Admission and failure order

1. Apply the core binding's bounded framing and independent route and disclosure
   checks and the provisioned-context guard. If the association is missing from
   a scope selected for this profile, treat it as missing required scope state.
   Use the generic binding outcome with no core disposition or new reservation.
2. Inside the valid scope, apply core's exact retained-copy path first when
   eligible. New grant use is unnecessary to report a prior disposition. Current
   authorization to disclose that disposition remains required. An exact copy
   cannot renew authority, reapply a decision, or retrieve an old result.
3. For first-seen messages, apply core signer authentication, context matching,
   version, structure, content-type and conflicting-ID checks before applying
   profile authorization. Preserve failures at those checks. Use core reference
   rules when a permission decision needs an exact target. An ambiguous reference
   cannot select authority. Normal core authorization and lifecycle tests still
   apply and must not be bypassed by a successful grant check.
4. For fresh protected requester actions, require the authenticated signer and
   certified message key to match the association's holder and thumbprint. The
   established subject supplies the representation selection. If an optional
   `on_behalf_of` is present on that action it must match exactly. Recheck the
   signed grant's current validity and configured issuing authority, and apply
   current local denials and resource policy. An expired, withdrawn, inadequate
   or otherwise unestablished grant or a subject or key mismatch is an ordinary
   `not-authorized` refusal of the protected request within the otherwise valid
   scope. Use only the normal permitted response path. The signer’s independent
   permissions cannot authorize a failed represented request in this scope.
5. Apply the action-specific permission checks below before any protected
   admission, including acceptance without execution and prospective suppression.
   Recheck the same guard and current authorization at the admission boundary,
   ordered with guard retirement and locally enforced authority changes. If an
   asynchronous check completes after retirement or expiry, it cannot admit the
   queued action on its old result. Capacity backpressure retains its core meaning.

Malformed or unsupported grant artifacts are rejected by setup and cannot appear
as authority fields in otherwise core messages. First-seen wire failures still
use the core [verification order](../../core/security.md#verification-order),
[structural checks](../../core/asking-contract.md#2-every-message), and
[control response rules](../../core/diagnostics.md#control-response-termination).
No invalid control causes a core reply.

## Action and target checks

The resource-owned permission contract must define exactly how to match the
selected offering and actual action/resources against the grant. Reject unknown
or incomplete permission interpretations. The receiver must check the actual
invocation or target, including when an offering has changed meaning without
changing its operation name. It must preserve the admitted operation,
represented subject and applicable constraints for future target resolution.

| Message or purpose | Required handling |
|---|---|
| Requester opening `say` | Check the proposed opening action and resources, including when a stop marker may suppress it. An unmatchable action cannot be admitted by treating it as harmless |
| Requester contribution or answer `say` | Resolve the eligible target under core. Apply permission for the exact action as a contribution or answer under the retained turn constraints. The association cannot change subject or expand the turn's authorized work |
| Requester `stop` | For a known eligible target require permission to stop that opening. For an unseen target, require permission covering every eligible opening that could arrive for that target under this scope, or independently established trusted facts that narrow the target enough to establish coverage. If coverage is unestablished, refuse `not-authorized` and install no marker. Once authorized, apply [core stop](../../core/asking-contract.md#44-stop) |
| Requester `approval` | Require permission to seek the described authorization. An `approval` starts its own originator-owned exchange and neither issues a grant nor proves execution |
| Requester `decide` | Require permission for that exact actor-originated approval and decision under its intended authority relationship. Apply [core approval target, deadline and binding checks](../../core/approvals.md#decision-and-terminal-state). A missing or invalid required reference cannot be reconstructed from the grant |
| Either peer's `closed`, `ack` or `refusal` | Apply ordinary ownership, correlation, authorization and disclosure rules. Grant expiry neither blocks a still-authorized owner action or control merely because it is expired nor permits another signer to take ownership |
| Actor's `taken`, `progress`, `question`, `result`, `approval` or `decide` | Actor acts under its own authority, with ordinary rules for the kind. No reverse-direction delegated permission follows from the requester grant. Require current disclosure before emitting protected content |
| `describe` and `description` | Actor-level traffic stays outside the authority association and follows its ordinary scope and rules |

For target-dependent checks, core's reference resolution and compatibility rules
determine the eligible target before any target-dependent permission match. For
example, a valid live grant cannot turn an unknown `decide` target into an
approval, and no grant authorizes closing another principal's approval. Neither
newly admitted work nor local scope renewal transfers anyone's lifecycle role.

## Effects, expiry and disclosure

Retain enough live state to distinguish the original signed message and actor,
represented subject, exact grant and verifying issuer key, permission contract,
applicable action/resource constraints and disposition. Implementation storage and
layout are replaceable. If required live interpretation state is lost, retire the
scope. Signed bytes or an old disposition alone give no fresh permission.

Grant expiry or local denial prevents fresh protected admission. It does not of
itself retire a still-authorized core route or undo an admitted turn. The account
of earlier admission survives within the applicable lifetime. At a protected
effect, the effect owner must enforce the resource contract and current grant
authorization for any effect that still depends on the grant. Specify in the
resource contract the enforcement and ordering of effect, expiry and known denial.
Never claim global instantaneous revocation or rollback from a late denial.

Evaluate disclosure independently. The receiver may report an eligible prior
disposition on a currently authorized route, limited to the core minimal control.
It must not send protected content on a route that has lost authority. Hold such
delivery under the binding's disclosure rules and retain delivery uncertainty.
Grant expiry does not create a terminal outcome or waive the actor's responsibility
for work already admitted. Use an independently authorized application interaction
for later protected retrieval. That interaction does not reopen an old scope.
