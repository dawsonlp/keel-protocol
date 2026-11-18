# Approval exchanges

This is part of the core contract. It defines an independent exchange using
`approval`, `decide`, `closed`, and the ordinary acknowledgements and refusals.
It uses the [asking payloads](asking-contract.md#3-kinds-within-a-conversation),
[messaging](messaging.md), [context continuity](continuity.md), and [security](security.md). It introduces no separate
contract version, transport, or durability requirement.

Originating approvals is optional for an application. Correctly handling
applicable received approvals is part of
[core conformance](README.md#participation-and-conformance), even when its usual
workload is bounded request/result. Authorization refusal and permission denial
retain their ordinary meanings; neither advertises a reduced protocol profile.

## Identity and responsibility

An approval is a request for authority to perform its described action. Its
identity is the originating `approval` message id within its conversation.
The authenticated sender is its **originator**. The originator owns that request's
deadline, accepts its decision, and issues its closure. The **decision maker**
must be authorized to grant or deny the requested authority. Neither role is
determined by having an `actor:` rather than a `party:` principal, or by being
the requester rather than the answering actor in a work conversation.

An `approval` may be the first message in a conversation with an actor. It
omits `in_response_to` when there is no earlier message to reference. No `say`,
`taken`, or open work turn is required. The conversation's identity remains its
actor and UUID in both directions, even when the requester owns the approval.
The selected continuity profile must establish its admission scope before that
first message; the approval cannot create or reconstruct its own context.
Approval acceptance does not open a work turn or promise a work `result`.
The [context-routing rules](messaging.md#conversation-context-routing) require
distinct keys for distinct conversations between the same two principals,
including conversations with their roles reversed.

An approval can also be sent in an existing conversation. Several independent
approvals may be pending, with or without an open work turn. Each has its own
identity and disposition. A pending approval alone is not a reason to refuse
another otherwise valid request as `busy`; actual inability to accept still
uses the ordinary `busy` rule.

If present, `in_response_to` supplies correlation to a known earlier message in
the same conversation. `caused_by` can record a cause in another conversation.
Neither field attaches the approval to a turn, transfers authority, or creates
a cancellation dependency. A reference to a known closed turn does not attach
the approval to a newer turn. An unknown optional correlation reference is
refused as `unknown`, except where a previously received closure already
determines the request's disposition as described below.

## Decision and terminal state

The originator retains the request as pending when it sends it. An `ack` of
the approval establishes acceptance for handling by the recipient; it grants
no permission. The recipient sends its signed `decide` with `in_response_to`
naming the approval. `approve` carries the grant or denial. When required, the
request digest binds the decision to the approval's exact signed bytes.

Retain the original compact JWS and the [issuance/authentication basis](security.md#retained-authentication):
the originator knows its own valid issuance; the decision maker establishes
its own authentication on receipt. Ordinary expiry of that request's signing
credential does not expire the pending approval or change its digest. A new
decision uses currently admissible credentials and current decision authority.
A renewed certificate can sign that new decision or a new closure; it cannot
replace the certificate inside the existing request. A key change is permitted
only under the applicable identity and authorization policy.

The originator serializes decision acceptance, expiry, and withdrawal for that
approval. The conversation actor's receipt order does not replace the
originator's ordering when these are different participants. Apply the
[continuity admission guard](continuity.md#establishment-and-admission) before
retained-state feedback or semantic handling. Within that valid scope, apply the
[exact retained-copy rule](messaging.md#exact-retained-copies-and-expired-credentials)
to an eligible repeated message; apply current verification, structural and
authorization checks to a new decision. Then use these state transitions:

| Approval state or event | Required behavior |
|---|---|
| No known approval for a new `decide` inside the established scope | Refuse as `unknown`; do not reconstruct a request |
| The decision names a known message of another kind | Refuse as `malformed` |
| The referenced approval was not originated by this receiver | Refuse as `not-authorized`; receiving or retaining someone else's request does not make this participant its owner |
| Pending, with a valid authorized decision accepted before the deadline | Retain that one decision, acknowledge it, and issue `closed` for the approval with `why: decided` |
| Pending when its deadline is reached on the originator's clock | Become expired and issue `closed` with `why: expired` |
| Pending when the originator withdraws it | Become withdrawn and issue `closed` with `why: withdrawn` |
| Already decided, expired, or withdrawn; a different decision arrives | Refuse as `closed`; retain the terminal disposition |
| An identical previously accepted decision arrives again | Preserve acceptance; issue only a fresh minimal acknowledgement on a currently authorized recipient route, without another decision or closure transition |

Resolve the request in the addressed conversation and require the receiver to
be its retained originator. Check the decision maker's authorization for that
request and its intended authority relationship. Another signer is acceptable
only if explicitly authorized by the originator's policy for that request;
correlation and `on_behalf_of` do not supply that authority themselves.

Apply the [security checks](security.md#approvals) to the decision's signer,
binding, and time. A timely `sent_at` does not make a decision acceptable after
the originator's deadline or withdrawal. The peer's clock cannot expire the
originator's request. At decision processing, the originator must compare its
current clock to the deadline even if an expiry callback has not run. Apply
[timestamp validation and exact comparison](timestamps.md); do not round a
deadline to the local clock's sampling interval or truncate received microseconds.
At or after the deadline, a still-pending request expires and the decision is refused
as `closed`. If the originator cannot retain an accepted decision and
its responsibility for closure within the live context, it must refuse as
`busy` before acceptance.

Both a grant and a denial end the exchange with `closed: decided`; the decision
itself distinguishes them. An expired or withdrawn request supplies no grant.
Once a decision is accepted, later expiry or withdrawal cannot replace it.
The originator retains the request, accepted decision if any, and terminal
disposition and required verification basis for the live context. Reusing the
request id with different signed bytes is `malformed`, even if the decoded
payload is unchanged. Seeking a different permission or replacing an issued
approval requires a new request id with its own lifecycle. Replacement does
not implicitly withdraw the earlier request; the originator explicitly
withdraws it when that is intended.

## Owner-issued closure

`closed` is sent by the originator of the named question or approval, regardless
of conversation role. A receiver checks that authenticated ownership, the
conversation, and the intended peer before applying it. A known target owned
by another principal is `not-authorized`. A known target of another message
kind, or a reason incompatible with the target, is `malformed`.

| Target | Permitted `why` values |
|---|---|
| Question | `answered`, `expired`, `withdrawn` |
| Approval | `decided`, `expired`, `withdrawn` |

A closure records the originator's terminal disposition; it cannot create a
grant, substitute for a signed decision, or establish action execution.
`closed: decided` alone does not identify which decision was accepted or prove
that `approve` was true. A decision maker must distinguish sending a decision
from learning that the originator accepted it. An acknowledgement of that
decision confirms its acceptance.

Apply normal duplicate handling first. A new closure id reporting the same
established terminal reason is acknowledged without another transition. A
contradictory reason is `malformed`; preserve the original disposition. In
particular, an accepted decision cannot later be overwritten by an expiry or
withdrawal. A recipient's unacknowledged outgoing decision alone does not
establish an accepted decision, so a subsequent valid `closed: expired` or
`closed: withdrawn` can still report the originator's outcome.

For a question, a valid `taken: answer` establishes the admitted answer and the
reason `answered`. An incompatible owner expiry or withdrawal is `malformed`
in either arrival order. `closed: answered` alone does not identify which
answer was admitted. A turn's result establishes that its questions are no
longer open, but supplies no precise closure reason; a compatible delayed
closure can establish that missing fact. See [question state and closure reason](notifications.md#question-state-and-closure-reason).

### Closure before the request

Transport can deliver closure before the question or approval it names. Within
an established scope whose admission guard remains valid, for an otherwise
valid, authorized `closed` with an unknown target, acknowledge it and
retain a provisional terminal marker. Scope that marker by conversation
identity, authenticated closure sender, intended peer, and target message id.
It asserts closure only of a request originated by that sender for that peer.
It creates no received request, turn, decision, or authority.
This exception concerns a missing message, not a missing context; it cannot
bypass the continuity guard or establish a scope from stale traffic.

When a matching question or approval later arrives, apply the
[retained-copy rules](messaging.md#exact-retained-copies-and-expired-credentials)
first. A new message must pass current verification, authorization, structural
and conflicting-ID checks. Check that its kind agrees
with the retained closure reason and, for a question, any known parent-turn
facts, then retain and acknowledge it as already closed. Do not treat it as an open request or
reopen it; a new answer or decision cannot resolve it again.
This terminal handling precedes ordinary request admission and correlation
lookup, so a missing parent alone does not prevent retaining a closed question.
For a question, it must not reconstruct a missing turn or admit a known
inconsistent parent. An independent approval has no parent turn; its optional
correlation does not acquire the question's turn-eligibility requirement.
Presentation and whether to attempt a message remain infrastructure policy;
such attempts do not change the request's terminal disposition.

A later message with that scoped id but an incompatible kind or closure reason
is `malformed`; it does not erase the marker. A message from another principal,
to another peer, or in another conversation is not suppressed by the marker.
Apply that message's ordinary rules, including normal identity checks. Known
wrong-owner closures cannot create a marker for someone else's request.

This rule applies equally to questions and approvals because `closed` names
both. Other late-notification behavior follows [receiving notifications](notifications.md),
not an inferred exception to their required live references.

## Work, permission, and cancellation

Approvals have an independent lifecycle. Completing or stopping a work turn
does not automatically close an approval, even in the same conversation or
when the approval's `in_response_to` names that turn. Turn questions still
close when their turn closes.

Where work depends on approval, its operation or application contract must
state whether that permission request remains needed after the work turn ends
and who withdraws it if the work is abandoned. The originator enacts withdrawal
by closing a still-pending request. A declared dependency is implemented by
that explicit action, not inferred from timing, correlation, or ignorable
metadata. `stop.turn` never targets an approval exchange.

A permission grant is distinct from execution and completion. The grant's
scope and conditions belong to the described authorization; it grants no
broader action or authority by implication. The request's decision deadline
does not automatically set the validity period of an accepted grant. Revocation,
grant-use limits, and external effects require their own authorization or
application semantics. Closing a request is not a mechanism for undoing an
accepted grant or an action already performed.

Retiring the conversation scope is likewise not approval withdrawal, grant
revocation, cancellation or evidence that admitted work stopped. The
[retirement rules](continuity.md#retirement-retention-and-already-admitted-work)
govern admission; the application contract still governs permission use and
already admitted effects. A retained decision is not proof that conversation
traffic can continue after retirement.

A denied or expired approval prevents treating that request as permission.
Whether dependent work ends as `denied`, takes another permitted path, or
reports another outcome follows that work's response contract. The approval
exchange itself sends no work `result`.

## Delivery and loss

Each non-control message follows the ordinary acknowledgement and retry rules.
Pending approval state does not occupy a sending slot after its message is
acknowledged. `closed` has no special delivery bypass: it can wait behind an
in-flight message, or be sent after the sender explicitly releases that slot
under the ordinary uncertainty rules. Local expiry or withdrawal takes effect
at the originator even while its closure is waiting for delivery.

The [actor-role notification release policy](messaging.md#delivery-and-uncertainty)
also applies to ordinary approval, decision and closure delivery in that
direction. The requester role retains its separate release ownership rule.
Releasing an attempt neither withdraws an approval nor revokes, denies or
accepts a decision. Resolving an exchange does not by itself confirm reception
of every related frame; the exact [confirmation rules](messaging.md#confirmation-and-sending-slots)
still apply. For example, `closed: decided` identifies no particular decision.

Acceptance of a granting decision (`approve: true`) is sufficient for the
originator to use the permission under its application contract; it need not
wait for acknowledgement of the closure. Lost messages can nevertheless leave
the peer uncertain about that
acceptance. Silence is neither a grant nor a denial from the decision maker.

Duplicate decisions and closures do not require replay of missed messages or
new closure identities. Retries of an existing closure keep its original
identity. Retain pending and terminal state, including provisional closure
markers, for the live context. Core requires no survival or reconstruction
across state loss, but the selected profile must disable admission to the lost
scope. Old decisions and closures then encounter its binding rejection, not an
`unknown` refusal or a newly created terminal marker in replacement state.
`unknown` and prospective closure markers remain applicable to missing messages
inside an authorized live scope. Stronger restoration requires an explicitly
applicable profile that reestablishes the required interpretation before
admission; historical records alone do not establish that continuity or prove
what executed.

## Example

Release is handling deployment job J42 and asks Authority for permission to
release build b17 to production. In a separate conversation with Authority:

| Sender → recipient | Message |
|---|---|
| Release → Authority | `approval P`: exact action, reason, risk, deadline, `bound_required: true`; no `in_response_to` |
| Authority → Release | `ack`, `in_response_to: P` |
| Authority → Release | `decide D`, `in_response_to: P`, `approve: true`, digest of exact signed P |
| Release → Authority | `ack`, `in_response_to: D`, after accepting the valid decision while P is pending |
| Release → Authority | `closed K`, `in_response_to: P`, `why: decided` |
| Authority → Release | `ack`, `in_response_to: K` |

P, D, and K stand for message UUIDs. All messages are signed. Release owns P's
lifecycle although Authority is the actor associated with this conversation.
If deployment proceeds, its result belongs to Release's original work turn.
The permission exchange neither performs that deployment nor reports success.
