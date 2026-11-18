# Messaging

The core defines behavior within a live conversation context. It requires
neither durable storage nor reconstruction of state after failure.
Conversation admission requires an explicitly established scope and active
guard under [context establishment and continuity](continuity.md).

## Participants and messages

An actor's state is private. Other participants affect it through messages.
A participant's local transitions must be consistent with processing messages
one at a time in its accepted order. Conversations may progress independently. Waiting for
work must not prevent handling a `stop`, contribution, answer, approval, decision,
or owner-issued closure. Processing a contribution need not interrupt an internal computation;
its effect on the turn follows the asking contract.

A message is an immutable value with an identifier and no live-object references.
A retry preserves its entire original JWS compact string, including protected
header, payload and signature. Renewal cannot rewrite an existing message;
re-signing the same payload under its old ID is conflicting reuse. `sent_at` does not establish processing
order or identify duplicates. Addresses are opaque and may be supplied directly.

## Message identity and reference resolution

Allocate a fresh UUID for each new message and never reuse it for different
bytes in the originating principal's applicable message scope. When allocating,
also avoid IDs of authenticated messages already known to have originated from
the peer in that conversation. An unresolved reference is not such a message
and reserves no ID. This requires
no global registry or coordination with unseen allocations. Received messages
remain scoped by originator as defined under [duplicates](#acceptance-and-duplicates);
equal UUIDs from different originators are not by themselves an identity match.

Where a reference requires a target lookup, use the field's specified context,
originator role and permitted target kinds. A fixed-originator reference such
as `progress.replaces` cannot resolve to another principal's message. If more
than one permitted target remains, refuse the new message as `malformed` before
acting. Do not select by iteration order, target state, or an implicit preference
for one kind. For example, `say.in_response_to` cannot choose between the
requester's opening and the actor's question when both share its UUID, even
if one is already closed. A known wrong-kind message does not add a permitted
candidate; an unknown reference still follows its own rule and exceptions.

Preserve a reference's established interpretation and disposition. Later
discovery of another scoped message cannot retarget earlier accepted work or
change an exact duplicate's outcome. A new late notification reports its
identified earlier disposition under its own role/target fields and consistency
rules; it is not fresh admission of the input it names. Do not infer that a
collision now known was already known at the earlier admission. No new wire
field or ordering requirement follows from this rule.

## Transport assumptions

Frames may be lost, duplicated, delayed, or reordered. Correctness within the
context must not rely on the transport preventing these conditions. A stronger
transport is allowed. [Bindings](bindings.md) define how frames are carried.

## Conversation context routing

The selected continuity profile must establish the context and authorize its
identity before conversation traffic is admitted. An initiating payload or an
empty lookup is not setup authority. Its designated creator must choose a fresh UUID that is not reused for a
different conversation between the same two principals, regardless of which
participant is the conversation actor. In particular, two actors asking one
another in separate conversations must use distinct keys. A conversation's
recorded actor and key remain fixed; reversing message direction does not
reverse that identity.

Apply the profile's scope guard before retained-state feedback or semantic
admission. After authenticating the peer and checking the recipient, resolve
the peer and conversation key to that established context. A single match uses
its recorded conversation actor, regardless of the incoming message kind. In a
freshly established empty context, a valid initiating `say` or `approval` begins
an exchange with the configured actor. A `closed` received before its initiating approval may
establish only the provisional state specified by [owner-issued closure](approvals.md#closure-before-the-request)
in that addressed context; it does not reconstruct an approval or grant.
Likewise, a `stop` for an unseen opening request can retain only its scoped
prospective suppression in the addressed actor's context, as specified by
[stop](asking-contract.md#44-stop).
These marker exceptions require an established scope; they cannot provision or
revive one. Other messages cannot create missing requests or turns by reference.

If conflicting retained contexts make that routing ambiguous, refuse as
`malformed` before applying the message. Do not choose by the currently open
turn, message kind, or transport connection alone. A colliding first message
can be indistinguishable from traffic in one existing context, so this rule
depends on the creator's fresh-key obligation; it does not claim that every
collision can be detected from the payload. The profile may supply an authorized
connection-to-context association; an open socket alone does not supply one.
Missing or retired scopes fail the profile guard, rather than being treated as
new contexts or unknown references. Context loss still proves no execution outcome.

## Acceptance and duplicates

An `ack` means the receiver accepted the message and responsibility for handling
it in the current context. It does not promise that state or responsibility
survives a process failure. Acceptance may be held in memory. If the receiver
cannot accept a message under these rules, it refuses as `busy` rather than
acknowledging it.

Acceptance for handling is distinct from admission to a turn. For a `say`,
`taken` reports the semantic disposition. An `ack` alone does not establish
that an amendment was admitted or that an independent invocation started.
For a notification, acknowledgement establishes its handling under the
[receiving rules](notifications.md), not that reported work is still open or
that an unseen progress predecessor exists and can be superseded.

Retain exact accepted messages and terminal semantic refusals, their
[authentication basis](security.md#retained-authentication), and their established
dispositions for the lifetime of the context. Scope each lookup to the
[governed namespace](security.md#governed-names-and-issuer-authority), signed
core profile, local recipient, authenticated originating principal, resolved
conversation actor/key (or the non-conversation request scope), and message ID.
An ID alone is neither an identity match nor authority to read a response.
Different signed bytes in the same scope/ID are `malformed`, even if their
decoded payloads match. Preserve the original record when rejecting a conflict;
[controls receive no reply](diagnostics.md#control-response-termination).
Accepted reserved diagnostics use their independently resolved local recipient
and original scope under [retained diagnostic identity](diagnostics.md#retained-diagnostic-identity),
never a global `unverified` bucket or the rejected frame's claimed sender.

An identical repeated accepted message does not start another turn, decision
or execution. A terminal semantic refusal stays terminal even if the operation,
policy or other condition that caused it changes; a fresh attempt uses a new
message ID. This includes authenticated, addressable requests refused after
authentication when their message/context identity can be established. `busy`
does not establish a terminal disposition or acceptance. Verification failures
do not reserve an unauthenticated principal's IDs, overwrite an existing
disposition or undo earlier work.

The corresponding minimal acknowledgement or terminal refusal reports the
established disposition only on a currently authorized recipient route, as
defined below. Disclosure of any cached content, and selection of a
route for later content, separately obey [response audience](bindings.md#response-audience-and-confidentiality).
A change in access policy may prohibit disclosure without changing whether
earlier acceptance or execution occurred. Duplicate protection for messages
outside a conversation lasts at least `dedup-window`.

Retain a notification's exact JWS and sending state while retrying it.
The core does not require persisting notifications before sending. `ack` and
`refusal` are controls; neither receives a core response, even when invalid or
unmatched. Unclassifiable frames follow the diagnostic contract's binding outcome.

## Exact retained copies and expired credentials

Duplicate recognition and permission to return information are separate checks.
Apply the binding's uniform route/disclosure guard and, for conversation traffic,
the selected profile's scope guard before any response that
could reveal a retained-state match or miss. After bounded frame/encoding checks,
a receiver checks for an eligible exact copy in
its own trusted retained state before applying first-seen credential expiry.
When an eligible record is retained, the receiver must use the rule below;
it cannot discard that record or apply fresh expiry first to avoid the rule.
The following order is normative for a retained-copy response:

1. Find a candidate in the independently established governed namespace,
   intended local recipient's current core profile and
   retained context/request scope. An index or digest is only a lookup aid:
   compare the complete original compact JWS byte-for-byte. Neither an ID nor
   a payload match is sufficient. Use the stored signer and resolved context,
   not an unverified claim about either. Ambiguous context matches must not
   select an arbitrary record.
2. Require the original successful authentication basis and an accepted or
   terminal semantic-refusal disposition. Prior `busy`, an authentication-only
   observation, an unassured delivery rejection, or a lost/untrusted record
   does not qualify. Locally issuing a request does not qualify as having
   received that request. Do not construct state merely to qualify this copy.
3. Recognize the established disposition without re-executing the message,
   admitting work, reopening an exchange, or granting fresh authority. Ordinary
   expiry of its original certificate does not erase this fact. This exception
   admits no new signature from an expired credential and does not change the
   original approval deadline. Exact `ack` and control-refusal copies receive
   no response and cause no second control transition. This includes an accepted
   reserved diagnostic under its retained local scope and exception basis; its
   exact copy cannot repeat attempt termination or acquire a new target.
4. Before revealing any prior disposition, independently establish the route's
   authority to receive that feedback for the original sender in this context,
   and apply current disclosure/trust policy. The old message, its certificate
   or possession of its bytes supplies no current route assurance. Authorization
   to perform a new action is not required merely to report a past disposition;
   authorization to inspect that disposition is required. If route assurance or
   disclosure authorization fails, use the same generic binding rejection as
   other unauthorized deliveries: this WebSocket profile closes with 1008,
   sends no core disposition, and leaves the retained state unchanged.
5. On an authorized route, generate a new minimal `ack` for prior acceptance,
   or a new minimal `refusal` with the retained terminal reason. Use a fresh
   message ID, current `sent_at` and currently valid signing credential; correlate
   to the original request and address its original sender/context. Do not replay
   an expired signed response, detailed refusal, result, grant, evidence or other
   content as this disposition response. Generating a new control report does
   not retry or replace an existing signed message.

These rules apply to retained conversation and non-conversation messages within
their applicable retention lifetime and authorized admission scope. A profile
does not have to provide a route after retirement; the provisioned profile does
not. It cannot selectively clear required records while keeping that scope live
to avoid this rule. For an accepted `describe`, a duplicate's
minimal `ack` confirms only earlier acceptance, not delivery or currency of its
description. A new `describe` with a new ID requests a current description.
Other fresh queries or stronger reply recovery require their own applicable
contracts; this rule adds no status or history operation.

Without an eligible exact match, and subject to those same route/disclosure
and applicable scope guards, use full current
[first-seen admission](security.md#verification-order). An expired first delivery
is `certificate-expired` regardless of its claimed `sent_at`. A fresh currently
authenticated frame that reuses a scoped ID with different signed bytes is
`malformed`; failed authentication cannot poison that ID. Earlier local issuance
alone cannot make an unseen expired incoming frame an admitted copy.

Never turn an unassured retry into a new return route for queued or future
content. Failure to return a disposition does not undo past acceptance or
execution. The response-audience rule prevents explicit disposition disclosure;
core does not promise constant-time processing or eliminate traffic/timing side
channels. Deployments needing stronger traffic-analysis protection must supply it.

## Order and correlation

For work turns, the conversation's actor orders the transitions it owns.
For an independent approval, its originator orders decision acceptance, expiry,
and withdrawal, even when the originator is the conversation's requester.
Neither participant's receipt order supplies a global order for the other's
transitions. Owner-issued messages communicate those transitions; missing
messages can leave the peer's knowledge incomplete.

[Receiving turn notifications](notifications.md) distinguishes actor transitions
from learning about them. A valid late report can add facts about a terminal
turn without reopening it. Its required live references and established
dispositions constrain admission; a missing `taken` does not prevent a result
for a known eligible opening request. Explicit progress replacement supplies
only the relationships it actually establishes, not an order for every update.

A submission comes from the requester; a notification comes from the actor.
Timestamps and sending order do not override accepted order. A delayed submission
can arrive after a later one if the requester explicitly released the earlier
submission's sending slot.

The actor orders contribution admission and turn completion within the same
context. Once a contribution is admitted, completion must account for it under
the turn's response contract. An obsolete internal computation cannot silently
complete the turn against the earlier request. A contribution received after
its target closes follows the asking contract's `closed` rule; arrival timing
does not turn it into a new invocation.

Within one sending session, at most one message per direction occupies the
ordinary sending slot. Acknowledgements and control refusals do not hold that
slot. One additional `stop` may occupy a separate sending slot beside a `say`
in the same conversation, including a contribution or answer.
The [asking contract](asking-contract.md#7-delivery)
defines this exception and preserves each message's independent delivery state.

Approval, decision, and closure messages use ordinary sending slots. A pending
approval is exchange state, not an occupied sending slot once its request is
acknowledged. Local expiry or withdrawal can take effect before its `closed`
message can be delivered. [Approval exchanges](approvals.md) define the owner
and how an overtaking closure is retained without creating a grant.

## Delivery and uncertainty

A sender learns acceptance from an authenticated acknowledgement or response
that establishes it under [confirmation](#confirmation-and-sending-slots).
A semantic refusal can establish that the receiver will
not accept this request. Silence, timeout, and state loss establish neither
execution nor non-execution. A refusal of an invalid frame cannot undo earlier
work accepted from another copy.

A message may be confirmed, refused, or not confirmed. Exhausting attempts
reports `not confirmed`, never failed or cancelled. The message might still
arrive and be acted on. Stopping retries does not withdraw accepted work.

A [verification diagnostic](diagnostics.md#effect-on-sending-and-knowledge)
can end the uniquely associated automatic attempt series without confirming or
semantically refusing the original message. It does not release a requester
slot by itself; the existing authorized release rule still applies. Preserve
any established disposition, otherwise report not confirmed. Diagnostic receipt
or reachability alone cannot restart that ended series. A deliberate later
attempt must retain the original bytes, sending-slot and continuity conditions.

A protocol `stop` names the opening request of one turn. Its acknowledgement
confirms acceptance of the stop, without confirming the opening request's
delivery or application-wide cancellation. Its target and prospective
suppression rules are defined in [stop](asking-contract.md#44-stop).

Retry with the same id after `ack-timeout`. `busy` waits for `backoff` without
consuming an attempt. Hold retries without consuming attempts while the binding
cannot reach the peer. Retry only within the context's established continuity;
an open transport connection alone does not establish that continuity.

The conversation actor's infrastructure may end local delivery attempts for
one of its outgoing non-control messages and release that sending slot under
its own policy, including before attempt exhaustion or during repeated `busy`.
This applies to the actor's role in the recorded conversation, not merely an
`actor:` principal. An actor acting as requester in another conversation follows
the requester-submission release rule in [asking](asking-contract.md#7-delivery).

Release establishes no acceptance, terminal refusal, non-delivery or withdrawal.
Without established confirmation/refusal the message remains `not confirmed`;
an already accepted copy remains accepted. The turn, question, approval or
decision lifecycle does not change merely because delivery attempts stop.
Ordinary originator/deadline responsibilities still apply. Any resumed attempt
uses the original exact signed bytes, the ordinary sending slot and established
context continuity; a released message gets no extra concurrent sending slot.
This permission does not remove obligations to issue required reports. No
priority scheduler, compulsory timeout or eventual-delivery promise is selected.

After releasing a notification slot, the actor may proceed to later messages.
Core-only participants
must not rely on subsequent replay, polling, or eventual delivery of that
notification. A missing result can remain unknown.

## Confirmation and sending slots

Confirmation records evidence of acceptance for handling, not receipt of a
particular `ack` frame. Apply the response's authentication, addressing, scoped
correlation, structure and semantic admission/consistency checks before using
it as confirmation. A refused, ambiguous or merely inspected response establishes
no such confirmation. An admitted report establishes only the messages below:

| Validated accepted report | Outgoing messages confirmed |
|---|---|
| `ack(X)` from X's intended receiver in its addressed context | X |
| `description` from the requested actor naming a retained `describe` in its non-conversation request scope | That `describe`, under asking section 6 |
| Consistent `taken(X)` with any permitted disposition | Its identified `say` X; `not-acted-on` confirms handling, not turn admission |
| Actor `question`, `progress` or `result` for eligible opening S | S; the report establishes that S opened |
| `taken(C, added-to-turn, S)` or `taken(A, answer, Q, S)` | C or A respectively, and opening S |

Reserved diagnostics confirm none of these messages and do not establish
terminal semantic refusal. Missing or ambiguous diagnostic correlation must not
select an outstanding input; [diagnostic association](diagnostics.md#receiving-and-associating-a-diagnostic)
is separate from this confirmation table.

Contract-dependent validation follows [requester knowledge](notifications.md#contract-knowledge).
An unknown output declaration does not prevent an otherwise valid result from
confirming S; that confirmation does not assert unverified schema or application
compliance. A result known to violate its applicable contract is refused and
supplies no confirmation.

A question retained solely under a prior closure marker with an unseen parent
does not reconstruct or confirm that missing opening. Its limited acceptance
follows the closure exception, not the eligible-opening rows above.

Stop retrying and release any sending slot held by each thus-confirmed outgoing
message, just as for a valid separate acknowledgement. Retain the actual evidence;
do not fabricate a received `ack`. A late confirmation can update an earlier
released input's disposition but cannot release another message's slot.

A result for S, including `stopped`, does not confirm a particular contribution,
answer or stop. `closed(Q, answered)` establishes the reason, not the identity
of an admitted answer; `closed(P, decided)` likewise does not confirm a particular
decision. The absence of other locally known candidates is not proof that none
exists. A correlation, causal reference or evidence attachment alone is not a
confirmation. Ending delivery attempts by local policy and learning acceptance
are separate events. Other contracts can define additional specific evidence
under their own semantics; they cannot silently change these core meanings.

## Context loss

State loss can end a context and its unfinished exchanges. The core does not
require restarting work, restoring duplicate recognition, recovering decisions,
or retrieving missed replies. Previously issued acknowledgements report earlier
acceptance; they are not durable commitments.

The [continuity contract](continuity.md) requires rejection of traffic whose
scope is no longer valid, before it can be admitted into replacement state.
It does not require restoring that state, and supplies no exactly-once guarantee
for external effects. A peer must not automatically turn an uncertain old request
into a new request on the assumption that it did nothing. Within a retained valid
context, duplicate handling and approval closure still apply fully.

Only after establishing a valid admission scope, required unknown live correlation references are refused as `unknown`, with
the limited exceptions specified by core. An authorized `closed` may precede its
question or approval; retain it under the [closure-before-request rule](approvals.md#closure-before-the-request).
This creates no request, turn, decision, or grant. An old `decide` cannot create
an approval or reopen one. `stop.turn` explicitly permits
prospective suppression of an unseen opening request; this creates no turn and
proves nothing about execution in a lost context. A progress message may name
an unseen `replaces` target under [progress replacement](notifications.md#progress-replacement),
but still requires a known eligible opening. This unresolved declaration creates
no predecessor message, identity reservation or reconstruction of lost state.
A stale frame naming a retired conversation fails its profile guard before any
of these reference rules. A fresh message in a properly established new scope
can encounter an unknown old ID without reviving the old conversation. Stronger
continuation or restoration requires an explicitly applicable profile or extension.

## Parameters

| Parameter | Meaning |
|---|---|
| `ack-timeout` | Wait before retrying an unanswered message within its context |
| `attempts` | Attempts met with silence before reporting not confirmed |
| `backoff` | Delay following `busy`, unless its `detail` specifies a delay |
| `dedup-window` | Minimum duplicate-response retention outside conversation state |
| `frame-limit` | Maximum UTF-8 bytes in a signed frame; default 1 MiB |
| `message-limit` | Maximum UTF-8 bytes in a signed message; default 768 KiB and no greater than `frame-limit` |

Retry and retention values must be positive and compatible with the interaction's
deadlines. No database, cache, checkpoint, or restart parameter is part of core.
