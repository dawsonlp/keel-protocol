# Context establishment and continuity

This is part of the core contract. It defines the conditions under which a
conversation may admit messages and retain its interpretation. An explicitly
selected binding or deployment profile supplies the mechanism. The
[provisioned-context profile](profiles/provisioned-context.md) supplies a
concrete memory-only option; neither recovery nor a core incarnation field is
required.

## Meanings and ownership

| Concept | Meaning |
|---|---|
| Context | One participant's retained interpretation of its conversation: identities, authenticated messages, dispositions, references, turns, decisions and relevant delivery state |
| Admission scope | A profile-established association among the governed namespace, core revision, conversation actor/key, participants and the context that will interpret incoming traffic |
| Admission guard | The mechanism that permits traffic only under that association while the required context remains retained; it must also cover queued traffic |
| Establishment | Installing the association and required initial context before admitting conversation traffic; not accepting a work request or granting application authority |
| Continuation | Using the same established interpretation; a connection opening or credential renewal alone does not establish it |
| Retirement | Ending permission to admit new traffic into that scope, without changing historical acceptance, completing work or revoking a grant |
| Restoration | Reconstructing a retained interpretation through a separately specified recovery guarantee before reopening admission |

Core owns these meanings and the admission guarantees below. Infrastructure
chooses resource budgets, retention duration, retirement triggers, scheduling,
storage and recovery policy. A profile must state the trust and failure boundary
within which it supplies its guarantees, and which conditions end them. It must
not silently substitute another context after those conditions occur.

Each participant owns its required local state and admission guard. One peer's
retention does not restore the other's lost state. Failure detection need not be
instantaneous: a peer may still admit an already in-flight message into its own
valid retained scope before learning of the other's loss. That does not authorize
creating replacement state or claiming that the lost peer received a reply.

## Selecting a usable profile

Before conversation traffic, the participants must share an explicitly applicable
continuity profile alongside their core revision, binding, trust and authorization
configuration. Core conformance alone does not identify a compatible setup or
resumption mechanism. Profiles must define:

1. The authenticated participants, roles, namespace and conversation association,
   and how fresh establishment differs from continuation.
2. The required retained state, admission checks and treatment of traffic queued
   before a loss or retirement.
3. The enforceable failure/retirement boundary, allowed resumption if any, and
   refusal or binding-rejection outcomes.
4. How applicability is established and how admission fails when setup is absent,
   incomplete, expired, unavailable or no longer authorized.

A claimed profile cannot consist only of an assertion that state probably
survived. It needs an implementable setup and admission mechanism. Required
behavior cannot be carried only in ignorable metadata. An implementation may
support a different precisely specified profile satisfying this contract; it
need not implement all profiles. Its peers must actually select that profile.

The standard [provisioned-context profile](profiles/provisioned-context.md) uses
trusted deployment provisioning and the existing signed conversation UUID.
It has no remote bootstrap protocol and is usable when provisioning can securely
configure both endpoint adapters. Independently operated peers without that
facility need another explicitly defined compatible profile, not an assumed
default on a bare WebSocket.

## Establishment and admission

Establish the authorized scope and its initial interpretation before any
effectful conversation admission. Empty state must not by itself authorize a
new context. The profile may reserve a fresh key before the first `say` or
`approval`; reservation creates neither an accepted request nor a turn. Independent
closure markers and prospective stop suppression likewise require an established
scope; their exceptions concern missing messages inside it, not missing scope.

A receiver must enforce the following order and conditions:

1. Apply bounded framing/encoding checks and independently established route
   authorization. Check the delivery's profile/scope association before any
   retained-state response can disclose a match or miss. Untrusted payload
   fields can be bounded selectors but cannot establish an association.
2. Require the profile's admission guard and required local context to be valid.
   A missing record cannot turn continuation into fresh creation. An old signed
   frame cannot be relabeled into a newly established scope by an adapter.
3. Within that authorized scope apply the [exact retained-copy rules](messaging.md#exact-retained-copies-and-expired-credentials).
   Otherwise perform current authentication, addressing, authorization, structure,
   conflicting-ID and semantic checks. The actual authenticated principal,
   signed profile and addressed conversation must agree with the scope. Profile
   membership is not a substitute for a message signature or action permission.
4. At semantic admission, ensure the same guard and required context are still
   valid, consistently ordered with retirement. A frame queued earlier must not
   run under a replacement context or a newly reused connection label. If
   retirement/loss wins, reject that attempt without new acceptance or execution;
   if admission wins, retain its resulting facts under the applicable guarantee.

This is an observable ordering requirement, not a prescribed lock, actor queue,
storage engine or context representation. A check made before network delivery
or at socket receipt alone cannot protect later semantic admission.

The selected profile must prevent frames from a retired/lost scope from becoming
new work in replacement state, including first messages whose replies were lost.
It may use a bound fresh key, an authenticated channel association, retained
retirement information or another explicitly specified mechanism. It cannot
rely on complete erased state to recognize its own loss. Its failure boundary
must instead ensure that loss disables admission, or that an independent guard
continues to reject the old scope. Arbitrary undetected corruption outside that
boundary is not covered by a claim about controlled loss or retirement.

## Outcomes and retry eligibility

| Condition | Meaning and required treatment |
|---|---|
| Scope is established and local required state retained | Admit otherwise valid traffic under the ordinary core rules; exact retries retain their dispositions |
| Scope is valid but capacity cannot accept a particular new message | Use ordinary `busy` before acceptance; do not create a terminal disposition |
| Scope is absent, not ready, retired or invalid | Withhold sending or use the profile's generic binding rejection before semantic handling; do not create a context, reserve a message ID or issue a fabricated terminal semantic refusal |
| Continuity is not established from the sender's knowledge | Do not resume old traffic on the assumption that it is safe; preserve the uncertainty and use the selected profile's establishment/resumption procedure |
| Current trusted evidence confirms earlier acceptance | Keep that fact; neither transport failure nor retirement reverses it |

An invalid-scope rejection reports no execution outcome for the original request.
It is not `unknown` for a message reference inside an established context, nor
`busy` promising that the same scope remains usable after backoff. Actual unknown
references within an authorized live scope retain their existing core outcomes.

[Reserved diagnostics](diagnostics.md#receiving-and-associating-a-diagnostic)
retain the original independently captured route and scope association. Their
absent conversation field cannot revive a retired context or convert an old
conversation failure into a fresh actor-level control effect. An ambiguous
association selects no arbitrary scope. Control-response suppression does not
override an earlier required binding rejection.

An open connection, valid certificate, locally retained outbox, prior ack/result,
history page or earlier context-status response does not alone establish current
continuation. The receiver still checks the association at admission. Releasing
a sending slot under the notification and delivery rules also supplies no continuity or non-execution evidence.

No frame may be rewritten or re-signed under its old ID to cross the boundary.
A fresh context/key or new message ID does not authorize automatically repeating
uncertain application work. Applications may reconcile effects, inspect history
through an authorized contract, or explicitly request new work under their own
semantics. Core requires no UI, retry schedule, automatic reconciliation service
or global exactly-once guarantee.

## Retirement, retention and already admitted work

The profile must make its lifetime/retirement conditions available before they
are relied on. Within those conditions infrastructure may select retention and
retirement policy, including ending a scope to enforce resource limits. A promise
of a longer lifetime cannot be shortened while still claiming it is in force.
Turn completion, local notification release or an idle connection alone does not
implicitly retire a context; retirement must enact the profile's guard transition.

Retirement and new admission must be ordered. Invalidate admission before
discarding required context state or installing replacement state. Previously
queued frames keep their original guard association and cannot inherit a new
one. Once that scope is no longer usable, a best-effort notification to the peer
is not the protection: the receiver must actually reject its stale traffic.

Retirement is not application cancellation, rollback, a new terminal result,
approval withdrawal, permission revocation or proof of external-effect cessation.
Already admitted work may have executed or may continue under its application
contract. It must not be restarted merely by replaying the old frame into new
context state. Ending the scope may leave outcomes unknown; infrastructure must
not report completion or non-execution it cannot establish. Core prescribes no
policy for scheduling that remaining work.

Do not selectively remove retained duplicate/authentication records while
claiming the context remains live, or to force an eligible copy through fresh
expiry checks. A genuine retirement invalidates the defined admission scope.
If records are retained for inspection, their historical facts remain intact.
The selected live profile need not provide a return route after retirement;
separate authorized inspection/recovery may do so under its own contract. This
adds no history or disposition-query API and changes no retained-copy response-audience
requirement.

## Restoration and the effect boundary

Core requires no survival of context after restart. A profile that supports
retained-context reconnect or durable restoration must explicitly define that
capability and its failure boundary. Before enabling ingress it must establish
the same interpretation, including exact-message authentication and disposition,
selected response contracts, approvals, reference meanings and notification facts required
by the exchanges it claims to continue. Reading some old messages is insufficient.

An authorization to reconnect to a name, or possession of a still-valid token
whose context is absent, cannot recreate the lost context. If the guarantee
cannot be established, keep admission disabled and report unavailable/unknown
continuity through the profile. Establishing a fresh scope is a different action.

The core guarantee includes preventing stale-scope traffic from being
silently admitted as new work within the selected profile's failure boundary.
It does not guarantee that accepted work finishes, that a lost result is
recoverable, or that external effects occur exactly once. A crash between an
external action and its outcome record remains an application/effect-owner
problem. [Application recovery and reconciliation](../docs/network-development.md#history-and-application-recovery)
can strengthen those separate boundaries under the responsible service contracts.

## Conformance

[Continuity vectors](vectors/continuity.json) describe required outcomes and
the provisioned profile's cases. A complete implementation must exercise its
actual setup, queues, context guards, failure boundary and response routes.
Document/schema checks alone do not demonstrate this behavior.
