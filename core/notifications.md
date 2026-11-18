# Receiving turn notifications

This is part of the core contract. It defines receipt of actor-issued `taken`,
`question`, `progress` and `result` in a retained conversation context, including
late first deliveries. [Asking](asking-contract.md) defines the actor's work
transitions; [messaging](messaging.md) defines delivery and duplicate identity.

## Facts and incomplete knowledge

A notification reports a fact about its identified request or turn. Receiving
it does not repeat the actor's transition. The actor has at most one open turn;
the requester can nevertheless have incomplete knowledge of several requests.
That uncertainty is not evidence of concurrent actor turns or of any particular
terminal outcome. Arrival order and `sent_at` do not establish an otherwise
unknown actor order or which turn is presently active.

A known locally issued untargeted `say` can support a report even when its
`taken` has not arrived. It is an eligible opening request if its retained facts
do not establish that it was refused or not acted on. The request is not itself
proof of a turn; a valid admission report (`taken: new-turn`, `added-to-turn`
or `answer`), question, progress or result identifying that turn establishes
that the actor opened it. A result also establishes its terminal outcome.
No missing notification needs to be invented or awaited. These facts can
[confirm identified submissions](messaging.md#confirmation-and-sending-slots)
without receiving a separate `ack`; they do not confirm every input in the turn.

An `ack` of a `say` establishes acceptance for handling, not turn admission.
A stop acknowledgement does not establish whether the opening was suppressed,
whether it executed, or whether its result has been delivered. A locally
released sending slot, lost reply or display choice establishes none of those
facts. A positive admission report cannot override an established incompatible
semantic disposition.

Infrastructure chooses how to represent knowledge, schedule actions, expose
history and uncertainty, and manage local resources. Core requires the message
meanings and receiving outcomes below, not a UI, model-dispatch policy, graph
store, complete-history requirement or notification sequence number. Stronger
ordering or recovery guarantees require an explicitly applicable agreement.

## Admission and correlation

First apply the binding's audience guard and the selected profile's
[continuity admission guard](continuity.md#establishment-and-admission), before
any retained-state feedback. Within that valid scope, apply the
[exact retained-copy rules](messaging.md#exact-retained-copies-and-expired-credentials).
An eligible duplicate retains its established disposition regardless of later
turn state. A first delivery must pass current authentication, authorization,
addressing, structure and conflicting-ID checks. Knowing its turn does not
admit a previously unseen expired signature.
The same guard and required context must still be valid at semantic admission,
ordered with retirement; a queued late report cannot enter replacement state.

Resolve references within the governed namespace, signed profile, local
recipient and recorded conversation, with the correct originating principal
for each referenced message. The report must come from that conversation's
actor; otherwise refuse as `not-authorized`. An ID or conversation key alone
cannot borrow another principal's request or confirmation state.

| New report | Required retained reference and consistency |
|---|---|
| `taken: new-turn` | `in_response_to` is the requester's untargeted `say` S; `turn` equals S |
| `taken: added-to-turn` | `in_response_to` is the requester's contribution C targeting opening S; `turn` equals S |
| `taken: answer` | `in_response_to` is the requester's answer A targeting actor question Q; `question` equals Q and `turn` equals Q's opening S |
| `taken: not-acted-on` | `in_response_to` is the requester's `say`; it reports no admission of that input and requires no `turn` |
| `question`, `progress`, `result` | `in_response_to` is the requester's eligible opening S, not a contribution, question or another notification |

Where required by the table, the eligible opening and, for an answer report,
the question must be known. `taken: not-acted-on` requires only its own `say`,
not that input's target. A missing `taken` is not a missing opening.
Refuse a required unknown live reference inside that established scope as `unknown`. Apply
[reference disambiguation](messaging.md#message-identity-and-reference-resolution)
where a reference can name more than one permitted target. Refuse a known wrong kind, inconsistent target, or
contradiction of an established semantic disposition as `malformed`. Resolve
the identified turn, not whichever turn a component currently displays.

Two limited exceptions retain their own meanings:

- [Owner closure before a question](approvals.md#closure-before-the-request)
  permits retaining that question already closed without requiring an unseen
  parent turn. It does not license a known inconsistent parent or create a turn.
- A progress `replaces` target can be unresolved under the rules below. This
  does not waive the known-opening requirement for that progress message.

Neither exception establishes a conversation scope or bypasses its admission
guard. Missing or retired scope receives the selected profile's binding
rejection before these reference rules, not an `unknown` semantic refusal.

An unloaded reference in a history view is not proof that the live protocol
context lacks it. Conversely, a history artifact cannot reconstruct lost live
state merely by naming it. Optional restoration follows its explicitly
applicable profile and establishes the required interpretation before reopening
admission. A retained report or confirmation alone is not current continuity
evidence.

## Late facts and terminal state

### Contract knowledge

Distinguish the actor's selected turn contract from the requester's knowledge
of it. Apply a particular output schema only when retained agreement or
evidence establishes its applicability to this turn. A cached or newly fetched
description, the operation name, and `taken` alone do not bind the turn to that
declaration. Do not reject a result solely for disagreeing with such an
unbound advertisement, or invent a selected declaration from its data.

If the applicable output is established, a successful result must contain
`data` matching it; otherwise refuse it as `malformed`, without confirmation
or admission of a terminal fact from that invalid report. This presence rule
also applies to an unconstrained `{}` output schema. Non-success results do
not have to match the success schema.

If the selected declaration remains unknown, admit an otherwise valid,
consistent result under the ordinary rules, including before `taken`. It
establishes the actor's reported terminal outcome and confirms its eligible
opening, while application/schema compliance can remain unverified. Acceptance
is not a claim to have performed an unavailable check. The actor must still
honor its actual selected contract. A later discovered mismatch does not erase
prior acceptance, confirmation or execution; local handling of that additional
evidence is infrastructure policy.

These knowledge rules also apply to declaration-specific interpretation of
other reports. They waive no known contradiction, structural requirement,
authentication, authority, correlation or continuity check. See
[contract selection](asking-contract.md#62-contract-selection-and-requester-knowledge).

### Receiving a valid late report

Accept and acknowledge a new report that satisfies the above rules and is
consistent with retained facts, even when its `taken` is missing or its turn
is already known to have ended. Retain it under the ordinary context rules.
If unable to accept the required responsibility, use `busy` before acceptance.
An acknowledgement confirms handling of the report, not that its work or
question is still open.

| Situation | Required meaning and outcome |
|---|---|
| Result for eligible S arrives before `taken(S)` | Accept the result; S has the reported terminal outcome without a preliminary `taken` |
| Compatible question or progress for eligible S arrives before `taken(S)` | Accept the observed fact about S; do not infer that S is still active now |
| Compatible `taken` arrives after S's result | Accept the reported disposition without reopening S or admitting the input a second time |
| Question Q for known terminal S arrives for the first time | Accept Q with its turn already terminal; Q is not an open protocol question |
| Progress for known terminal S arrives for the first time | Accept provisional information about S; it cannot replace S's terminal result or affect another turn |
| Delayed result for S arrives while another turn N is known | Apply it only to S; it neither closes nor reopens N |
| Several eligible turn reports lack terminal information or established order | Preserve their established facts and the remaining uncertainty; do not choose the active turn or invent results from arrival order |

The infrastructure decides how these facts affect presentation, scheduling or
whether to attempt another message. A new answer received by the actor for a
closed question still receives `closed` under asking. Permitting an attempted
answer, displaying the old question, or initiating a new application inquiry
does not reopen the old protocol exchange.

### Question state and closure reason

A known terminal result means none of that turn's questions remains open.
It does not identify which were answered, expired or withdrawn before the
actor finished. Preserve any established owner reason; otherwise the precise
reason remains unknown. Do not manufacture an owner-issued `closed: withdrawn`
from incomplete receiver knowledge.

A compatible delayed owner closure can establish that missing reason. A
valid `taken: answer` establishes that its named answer was admitted and the
named question was answered, even when the turn's result arrived first.
These are reports of earlier actor transitions, not new answers after closure.
The actor's obligation to withdraw its actually still-open questions when it
ends a turn remains unchanged.

### Consistency and repeated reports

Apply only contradictions established by retained facts, without inventing
missing order, messages or outcomes:

Known local causal facts also constrain consistency. If the requester first
created an input only after observing its turn's result, a subsequent report
cannot truthfully describe that input's admission before completion. Refuse
that inconsistent admission as `malformed`. Do not infer this ordering merely
from `sent_at`, missing messages or transport arrival order; no new clock or
event-log representation is required.

- For one `say`, a new `taken` agreeing with an established disposition is
  acknowledged without another transition. Different `as`, `turn` or `question`
  meanings for that same input are `malformed`. An earlier acknowledgement
  alone does not select a `taken` disposition.
- Established `not-acted-on` or terminal semantic refusal of an opening cannot
  coexist with a report that the actor opened or completed that turn. Refuse
  the inconsistent new notification as `malformed`, in either arrival order.
  `busy` and verification failures are not such terminal semantic evidence.
- One question admits at most one answer. `taken(A, answer, Q)` conflicts with
  an established different admitted answer or explicit owner expiry/withdrawal
  of Q. Refuse the inconsistent notification as `malformed`. Conversely an
  incompatible subsequent owner closure follows the same consistency rule in
  [approvals](approvals.md#owner-issued-closure).
- `closed(Q, answered)` does not identify the admitted answer. It is compatible
  with `taken(A, not-acted-on)` when A need not be the answer that resolved Q.
- One turn has one terminal result message. An identical retained copy follows
  normal duplicate handling. Any additional result ID for that turn is
  `malformed`, even when its status/content matches; a new ID is not a retry.
- A new control refusal cannot undo already established acceptance or terminal
  facts. This consistency rule creates no response to a control refusal.

Preserve prior accepted messages and dispositions when refusing a contradiction.
A refusal or later-discovered inconsistent claim cannot make earlier acceptance
or execution cease to have happened. Core specifies no new local fault-reporting
or shutdown policy.

## Progress replacement

`replaces` declares that this progress supersedes the identified earlier
progress of the same actor in the same turn. It changes that relationship,
not either message's bytes or acceptance identity. Unrelated progress is
additive information; receipt order is not an implicit replacement mechanism.
The declaration reports the actor's output relationship, not a new work action.

Resolve the target in this actor's message scope within the governed namespace
and conversation. The same ID from another originating principal, namespace
or conversation neither resolves nor invalidates it.

For a new progress message P whose opening is otherwise eligible:

| Target knowledge | Disposition |
|---|---|
| No `replaces` | Accept P as progress with no supersession assertion |
| Target is an accepted progress message of this actor in this turn | Accept P and establish the replacement, unless doing so would create a cycle |
| Target is not yet known in the applicable message scope | Accept P with an unresolved replacement declaration; do not claim target existence or authenticate/reserve its ID |
| Trustworthy retained facts establish another kind or another turn | Refuse P as `malformed`, independently of whether the target was accepted or refused |
| Target is terminally refused, without independently established wrong-kind/turn facts | Accept otherwise valid P; its declaration has no superseding effect over that target or its predecessors |
| P names itself, or acceptance would establish a replacement cycle | Refuse P as `malformed` |

Prior `busy`, failed authentication or an unassured delivery does not make an
unknown target terminally refused. The resource/retention rules for accepting
messages still apply; no separate graph representation is required.

Refusal alone is not proof that the actor's new output is invalid. Retain the
predecessor's refusal without admitting it, reserving another identity or
traversing its outgoing replacement declaration. A subsequent accepted progress
can replace P normally; refusal must not propagate through otherwise valid new
updates. P still requires its own current authentication, authorization and
admission. Use only target facts actually established by the retained validation
basis: malformed or unsupported bytes do not supply validated kind/turn facts
merely because those fields can be read. A refused target whose kind/turn could
not be established remains non-superseded; do not invent missing facts.

### Resolution of an unseen target

An accepted unresolved declaration cannot reserve another message's identity
or dictate its admission. When a candidate target arrives, apply its own
authentication, correlation, consistency and admission checks. Consider all
replacement relations that accepting that candidate would establish, including
earlier unresolved declarations that would then resolve. If accepting a progress
candidate would establish a cycle, refuse the candidate as `malformed` before
acknowledging it.

If the target is accepted as a progress of the same actor and turn, the
declaration establishes supersession even though the target arrived later.
If the target instead proves to be the wrong kind, another turn's progress,
or terminally refused, the declaration has no superseding effect. Accept an
otherwise valid target under its ordinary rules; the prior declaration cannot
invalidate it. Keep P's earlier acceptance and bytes unchanged, but do not
treat its invalid relationship as established. Send no retroactive refusal
of an already acknowledged P merely because its declaration cannot be resolved.
Handling or displaying that inconsistency locally is implementation policy.

This distinction concerns different knowledge states: an independently known
wrong-kind/turn target
prevents new admission; a target discovered invalid later cannot reverse past
acceptance. An acknowledgement of P never asserted that an unseen predecessor
existed or that the replacement relationship was already established. Mere
terminal refusal of a predecessor does not block the successor in either order.

### Chains, branches and uncertainty

Established valid replacement relations are transitive: if C replaces B and
B replaces A, a later arrival of A does not restore it over B or C. Transitivity
uses established relations only. An unresolved or invalid relation contributes
no superseding edge, and an unseen message supplies no invented outgoing link.

Two messages replacing the same predecessor do not order each other. Both
relationships can be valid; core selects no winner between those successors.
Likewise, unlinked progress messages remain incomparable under this mechanism.
An implementation can group, select or summarize information under its own
policy, but that choice is not an additional actor-issued replacement or proof
that the chosen message is the actor's latest state.

Replacement never substitutes for a result, reopens a turn, closes a question
or affects an independent approval. It supplies no global or conversation-wide
sequence, delivery completeness, recovery or persistence guarantee.

## Conformance

[Notification vectors](vectors/notifications.json) cover these receiving rules.
Different representations and infrastructure policies can conform when they
preserve the same message meanings, required wire outcomes and permitted
uncertainty. Tests of these artifacts are distinct from driving the rules
through an actor implementation.
