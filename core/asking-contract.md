# The asking contract

This draft defines core conversations using message version `1`, including
work turns and independent [approval exchanges](approvals.md). It builds on
[messaging](messaging.md) and [security](security.md). This is the unreleased
standalone core/1 contract; its signed and binding identities are defined in
[version and extensions](#9-version-and-extensions).

The [schema](schemas/keel-v1.schema.json) specifies payload structure.
[Vectors](vectors/README.md) specify structural, security, delivery, turn, stop,
approval and notification behavior for concrete cases.

## 1. Parties and identifiers

| Thing | Form | Notes |
|---|---|---|
| **Principal** | `party:<id>` or `actor:<name>` | Exact governed name from the signer's certificate (`sub`), certified by an explicitly authorized issuer/key. The name implies no network membership or action permission. See [naming authority](security.md#governed-names-and-issuer-authority). |
| **Actor address** | `actor:<name>` | What a client asks |
| **Conversation key** | A UUID in canonical form, of any version | Allocated fresh by the authority designated in the selected continuity profile; a profile may constrain its generation. Do not reuse it for a different conversation between the same two principals, even with reversed roles. Neither side derives application meaning from it. A conversation is always its actor and key together. See [context routing](messaging.md#conversation-context-routing) and [establishment](continuity.md). |
| **Message id** | A UUID in canonical form | Fresh for each message; retries preserve exact bytes and ID. Originator scope, collision avoidance and ambiguous references follow [message identity](messaging.md#message-identity-and-reference-resolution). |
| **Times** | [Core timestamp profile](timestamps.md): RFC 3339 UTC, years 0001–9999, seconds 00–59, optional 1–6 fractional digits | For example, `2026-10-26T18:04:05.123456Z`. Validate actual dates and preserve microsecond distinctions. |

## 2. Every message

Every message is a signed JWS (security.md). Its payload is a JSON object in canonical form. Numbers are I-JSON. These fields are common to every kind:

| Field | Required | Meaning |
|---|---|---|
| `version` | yes | The core contract version this message follows: `1`. |
| `id` | yes | The message id |
| `kind` | yes | One of the kinds below |
| `sent_at` | yes | The sender's clock, under the [timestamp profile](timestamps.md). Supplies no processing order or general freshness authority; approval decisions also have the explicit deadline consistency check in section 5. |
| `to` | yes | `{ "principal": <principal>, "conversation": <key> }`. `conversation` is left out only for the requests in section 6, which aren't about one conversation; the reserved refusal recipient also has no conversation. |
| `in_response_to` | per kind | Ordinarily the id of an earlier message in the same conversation, except for section 6 responses. A reserved diagnostic instead echoes an untrusted UUID from a failed frame; [diagnostic association](diagnostics.md#receiving-and-associating-a-diagnostic) resolves its original scope without proving that exact message was rejected. For `say`, section 4.1 restricts the target to a turn's opening `say` or a question. |
| `caused_by` | no | `{ "actor": <actor address>, "conversation": <key>, "message": <id> }`: the message, in another conversation, that led to this one. It records a causal reference; it grants no authority. |
| `metadata` | no | An object. Receivers ignore unknown keys. Application extensions should use namespaced keys. The core defines no application metadata keys. |
| `on_behalf_of` | no | A principal this message is sent for, vouched for by its signer |
| `evidence` | no | An array of signed documents, attached unchanged: core messages used as evidence |

A receiver classifies a message with **unknown fields at the top level** as `malformed`, so that no two implementations read it differently. Optional annotations belong in `metadata`; required additional behavior needs an explicitly applicable contract (section 9). The [control-response rules](diagnostics.md#control-response-termination) suppress core replies to controls and unclassifiable frames; classification is not always an instruction to send a refusal.

**Checking a message's structure.** After verification, a receiver checks the payload in this order, using the first reason that applies. Send a refusal only when the binding and [control-response rules](diagnostics.md#control-response-termination) permit it:
1. `version` isn't one it supports: `unsupported`.
2. The payload doesn't match the schema for its kind (unknown kind, unknown or missing field, wrong type), or a core timestamp fails the [whole-string and calendar checks](timestamps.md#validation-and-receiving-order): `malformed`.
3. A content block has a type other than `text`: `unsupported`.

**Content** is an array of blocks. This version defines one: `{ "type": "text", "text": <string> }`. A block of any other type is refused (`unsupported`).

**Data** on `say` and `result` is any core-valid JSON value: object, array,
string, number, boolean or null. The message envelope remains an object and
the canonical-JSON and numeric restrictions apply throughout. An absent `data`
field differs from a present `null`, `false`, `0`, `""`, `[]` or `{}`. Preserve
the actual value; do not insert defaults, coerce it or omit it by truthiness.
Section 6.1 defines when an operation requires its presence and validation.

**Size.** A message is at most `message-limit` (messaging.md, parameters). A larger one is refused as `malformed`.

## 3. Kinds within a conversation

### Sent by the asker

| Kind | Fields | Meaning |
|---|---|---|
| `say` | `content` (non-empty); `in_response_to` optionally; `operation` and `data` optionally | Without `in_response_to`, requests a new turn. Naming a turn's opening `say` proposes a contribution to that turn; naming a question supplies an explicit answer. Section 4.1 defines admission and refusals. An opening request's `operation` selects its response contract and `data` supplies its structured input. Contributions retain that contract; section 6.1 defines their permitted input. `content` supplies the request or contribution in words. |
| `stop` | `turn` (required): the opening `say` id, which may not have arrived | Stops only the identified turn, or prevents its opening request from starting a turn. Never selects whichever turn happens to be open. Section 4.4 defines targeting, dispositions, and the boundary with application cancellation. |

### Sent by the actor

| Kind | Fields | Meaning |
|---|---|---|
| `taken` | `in_response_to`: the `say`; `as`; `turn`: the id of the `say` that opened the turn, unless `as` is `not-acted-on`; `question`: the question answered, when `as` is `answer` | Reports the actor's semantic disposition: `new-turn` opened a response obligation; `added-to-turn` admitted a contribution; `answer` admitted an answer to the named question; `not-acted-on` started no work and applied no contribution. Sent for every `say` that wasn't refused. It is distinct from acceptance acknowledged by `ack`; receiving a report does not repeat that transition. |
| `progress` | `in_response_to`: the turn; `content`; `replaces` optionally: the id of an earlier progress message in the same turn | Provisional output or a status update. `replaces` declares supersession under [progress replacement](notifications.md#progress-replacement), including unresolved predecessors and branches; arrival order supplies no replacement. It is not a terminal result or, by itself, an independently consumable structured deliverable. |
| `question` | `in_response_to`: the turn; `content`; `deadline` optionally | Needs an answer from the asker |
| `result` | `in_response_to`: the turn; `status`; `content`; `data` optionally (any JSON value, required for success with a declared output schema) | **Ends the actor's turn and reports that terminal outcome.** Receipt establishes it for the requester even if earlier notifications are missing. `status` is one of: `succeeded` (done as asked); `failed` (couldn't be done, because something went wrong); `needs-clarification` (can't go on without more from the asker); `stopped` (the identified turn ended by `stop`, with the limits in section 4.4); `denied` (not done, because an approval it needed was denied, or expired). |

### Sent by either side

| Kind | Fields | Meaning |
|---|---|---|
| `approval` | `in_response_to` optionally: an earlier message for correlation; `action` (content: exactly what would be done); `reason` (content); `risk` (`low`, `medium` or `high`); `deadline`; `bound_required` (boolean) | Starts an independent request for authority, identified by its message id. It may initiate a conversation without a work turn. Its originator owns the lifecycle defined in [approval exchanges](approvals.md). |
| `decide` | `in_response_to`: the `approval` (required); `approve` (boolean); `note` optionally; `request_digest` (required when `bound_required` is true) | Supplies the authorized grant or denial for acceptance by the approval's originator while the request is pending. `request_digest` is SHA-256 of the approval's exact JWS compact string, in base64url. |
| `closed` | `in_response_to`: a question or approval; `why` | Issued only by that request's originator. For questions, `why` is `answered`, `expired`, or `withdrawn`; for approvals, `decided`, `expired`, or `withdrawn`. It reports terminal state, not permission or execution. [Owner-issued closure](approvals.md#owner-issued-closure) defines ownership and out-of-order delivery. |
| `refusal` | `in_response_to`: the refused message, if it could be read; `reason`; `detail` optionally for ordinary refusals | A semantic refusal means the request will not be accepted. A verification diagnostic reports rejection of a delivered frame, without proving non-execution of the original message. The reserved form forbids detail and other annotations; section 8 and [diagnostics](diagnostics.md) define association, delivery effects and no-response rules. |
| `ack` | `in_response_to`: the acknowledged message | The receiver accepted it within the live context; no core durability promise (messaging.md). |

## 4. Turns

- **At most one turn is open at the actor per conversation.** The actor opens it by taking a fresh request as `new-turn`, reports that admission in `taken`, and closes it with `result`. Its id is the opening `say`. The requester's incomplete knowledge may cover several turns without establishing which is now active.
- **One turn has one terminal response contract.** The opening request establishes it. Multiple admitted `say` messages may contribute to fulfilling or amending the effective request. The result can synthesize or aggregate several contributions under that contract.
- **A turn has one terminal result.** Retransmitting that result follows normal message identity and duplicate rules. Another internal computation or delegated result cannot close it again.
- **Questions belong to their identified turn.** When the actor closes the turn, it closes its still-open questions as `withdrawn`. Receipt of a result establishes that none remains open, but does not identify which questions were answered, expired or withdrawn. Approvals have an independent lifecycle; closing a turn does not implicitly close them, even when correlated to it.
- **Status is derived, never guessed.** Distinguish turn and question facts from each approval's state. Approvals may be pending while no turn is open. A client derives knowledge from messages within an established live context; [receiving notifications](notifications.md) defines late facts, unresolved references and contradictions without selecting an implementation representation or policy.

### 4.1 Requests, contributions, and answers

A sender intending to contribute to a particular turn sets `in_response_to`
to that turn's opening `say` id. To answer a question it names the question
instead. An untargeted `say` always requests a new turn, even if the sender
believes another turn is still open. Conversation history can inform the new
request without using `in_response_to` to name a previous result.

First apply the [retained-copy rules](messaging.md#exact-retained-copies-and-expired-credentials),
including their response-audience guard. A new `say` must pass current
verification, authorization, structural, conflicting-ID and stop-suppression
checks. If not already handled or suppressed, resolve its target under
[reference disambiguation](messaging.md#message-identity-and-reference-resolution).
An opening and a question with the same UUID are distinct possible targets;
if both match, refuse as `malformed` without choosing a contribution or answer,
even if one candidate is already closed. Otherwise:

| Target | Interpretation |
|---|---|
| No `in_response_to` | A fresh request, independent of any open turn |
| Opening `say` of the open turn | A proposed contribution to that turn |
| Open question in the open turn | A proposed answer to that question |
| Opening `say` of a known closed turn, or a known closed question | Refuse as `closed`; do not open or join another turn |
| Unknown message id in this context | Refuse as `unknown`; do not reconstruct a turn or question |
| Any other known message, including a non-opening `say`, `progress`, or `result` | Refuse as `malformed` |

Next check the operation and input rules in section 6.1. For a valid request,
contribution, or answer, its disposition is:

| Situation | Disposition |
|---|---|
| Fresh request, no turn open | Accept and send `taken` as `new-turn` |
| Fresh request, a turn open | Accept for handling and send `taken` as `not-acted-on`; do not execute, queue, or merge it into the open turn |
| Targeted contribution or answer admitted under the turn's contract | Accept and send `taken` as `added-to-turn` or `answer`, naming the original turn; an admitted answer also closes its question as `answered` |
| Well-formed contribution or answer the actor declines to apply | Accept for handling and send `taken` as `not-acted-on`; an unanswered question remains open |

Acceptance follows the ordinary acknowledgement rules. `not-acted-on` is a
terminal disposition for that message id: a duplicate must not execute after
the turn later closes. A requester seeking a fresh invocation can send a new
request after closure, or use a different conversation for independent
concurrent work. An open turn alone is not a reason to return retryable `busy`
for an independent request; inability to handle the message still follows the
ordinary `busy` rule.

A contribution naming the turn does not implicitly answer an open question.
Only an admitted answer naming that question closes it. A targeted contribution
cannot silently become a different operation invocation or attach to a newer
turn. Repeating `operation` does not ask for an additional execution.

### 4.2 Contributions and completion

Admitting a contribution makes it part of the effective request. The terminal
response must account for it, or explain why the requested change could not be
applied. The actor must not report unqualified success against an obsolete
request after admitting a relevant correction. Admission does not promise
perfect interpretation, undo prior effects, or grant new authority; existing
accepted permission grants still authorize only their described actions.

Contribution admission and completion are ordered within the live context. If
admission occurs first, the result must reflect that disposition. If completion
occurs first, a new contribution targeting the closed turn is refused as
`closed`. An already admitted duplicate retains its established disposition;
it is not a new late contribution. Internal cancellation, buffering, restart,
and model invocation are implementation choices.

### 4.3 Communication patterns

| Pattern | Response obligation |
|---|---|
| Bounded request | One initial input and result; the contract may decline amendments |
| Incremental information or steering | Several admitted contributions inform or amend one response |
| Clarification | A question and its explicit answer continue the original turn |
| Accumulating questions or a composite operation | The declared response contract accounts for the constituent questions or outcomes; unrelated operation schemas are not implicitly combined |
| Delegation and synthesis | Child exchanges have their own turns; their results can contribute to the parent's response |
| Progressive output | The actor issues provisional `progress` before its terminal `result`; delivery may reverse that order |

These patterns are independent of whether the actor uses models, deterministic
code, or both. A structured reasoning operation can decline amendments; a
deterministic interactive operation can accept them. Model output chunks and
model-call completion are internal events, not automatic protocol results.

A bounded offering selects a response pattern, not a reduced protocol profile.
It may use fixed descriptive text with structured data and decline amendments,
while its endpoint still fulfills the applicable
[participation and receiving obligations](README.md#participation-and-conformance).

When an actor asks another actor, the child request belongs to that recipient's
conversation and has its own response contract. Its result does not itself
complete the parent's turn. The parent interprets and validates returned
material as required by its own contract. If it sends that material onward,
it issues a new addressed message under its own identity; an original signed
message can remain unchanged as `evidence`. Causal references and evidence
do not transfer authority. The core specifies no delegation strategy.

Application commitments can span several turns. For example, an operation that
accepts a job may successfully return its job reference; later operations can
inspect or advance that job. The acceptance turn's success does not mean the
job is complete. Application work identities and lifecycle rules remain owned
by the application contract.

### 4.4 Stop

**The core target is an identified turn.** `stop.turn` is required and names
the asker's opening request: a `say` without `in_response_to`, in the addressed
conversation. It uses the same identity as `taken.turn` and a result's
`in_response_to`. The opening request may still be in transit, so a turn need
not yet exist. The target is not a conversation, latest contribution, question,
application job, or set of descendants. References grant no cancellation
authority; normal authorization applies.

First apply the [retained-copy rules](messaging.md#exact-retained-copies-and-expired-credentials),
including their response-audience guard. For a new `stop` that passes current
verification, authorization, structural and conflicting-ID checks, resolve
`turn` within the live context:

| Target state | Disposition |
|---|---|
| Known message that is not a fresh `say` from this asker in this conversation | Refuse as `malformed` |
| Opening request of the matching open turn | Accept and `ack` the stop; close that turn with one `result` whose `status` is `stopped` |
| Opening request of a known closed turn | Refuse as `nothing-to-stop`; retain its existing result |
| Known fresh request already disposed of without opening a turn | Refuse as `nothing-to-stop`; retain its existing disposition |
| Message id not yet known | Accept and `ack` the stop; retain prospective suppression for that opening request |

Check target eligibility before its turn state. A target already known to belong
to another asker or conversation is invalid; core does not require a lookup
outside the retained context to establish this.

**No disposition affects a different turn.** A delayed stop for S1 cannot stop
S2, even when S2 is open. A duplicate accepted stop receives its established
acknowledgement without being applied again. A new stop id for an already
closed target receives `nothing-to-stop`.

Prospective suppression is scoped to the named opening request from this asker
in this conversation. If that request arrives and passes verification,
authorization, and structural checks, accept it and send `taken` as
`not-acted-on`, without a turn or result. Do not execute or queue it, even after
another turn closes. A repeated stop for an unseen target can be acknowledged
while preserving the same suppression. A suppression marker is not a received
message or an opened turn. If the named message later proves to be a
contribution, answer, or other kind, the marker does not suppress it: apply its
ordinary rules. A known such message is an invalid target for a new stop.
Under section 4.1, a contribution naming the suppressed opener is `unknown`
while that opening message is unseen, and `malformed` once it is known to have
been taken as `not-acted-on`: no turn was opened to receive contributions.

Stop acceptance, contribution admission, and turn completion are ordered within
the context. Completion does not wait for delivery or acknowledgement of the
result. If completion wins, the stop cannot replace that result. If the
stop wins, the actor must cease advancing that turn, withdraw its open questions,
and issue the `stopped` result; no later computation or child
reply may produce a second result or reopen it. Later new contributions and
answers to that closed turn are refused as `closed`; already admitted duplicates
retain their established dispositions. The result describes known partial work
and outstanding effects when relevant, without claiming more than is known.

An approval is not a turn and cannot be targeted by `stop.turn`. A work contract
can require the approval's originator to explicitly withdraw a still-pending
request when work is abandoned; [approval cancellation](approvals.md#work-permission-and-cancellation)
defines that boundary. Turn closure alone cannot withdraw an independent
approval or revoke an accepted grant.

An `ack` for the stop confirms acceptance of this control request. It does not
acknowledge the targeted `say`, prove that a turn existed, or establish that all
work has ceased. For an opened turn, the `stopped` result reports its termination;
for a suppressed opening request, `taken: not-acted-on` reports that request's
disposition. Missing replies can still leave the requester uncertain.

Retain target, suppression, and terminal state for the live context. Core does
not require their survival across state loss. Suppressing an unknown target in
a new context cannot establish that it never executed in an earlier context.

#### Application cancellation

Core stop ends the identified response obligation and prevents further
advancement of that turn. It does not undo completed effects, guarantee that an
already-started external action has ceased, or establish that delegated actors
are quiescent. An implementation can interrupt local computation or issue child
stops, but core prescribes no cancellation strategy or transitive guarantee.

Longer-lived jobs, workflows, deployments, and other application commitments
have their own identities and cancellation contracts. Where cancellation is
offered, its operation must define the target, authority, scope, treatment of
in-progress and completed effects, and what its response establishes. For
example, accepting a cancellation request and confirming that all affected work
has ceased are different outcomes. A successful turn that accepted a job stays
successful when a later operation cancels that job.

Such an operation is an ordinary fresh `say`, with its own turn and result. If
another turn is still open in the conversation, use a separate conversation;
otherwise the fresh request receives `not-acted-on` under section 4.1. An actor
offering cancellation must remain able to handle that operation while the
targeted application work runs. Core introduces no application cancellation
vocabulary; section 9 defines the boundary for additional protocol targets.

### 4.5 Receiving notifications

Actor transitions and the requester's observation of them are distinct.
[Receiving turn notifications](notifications.md) defines admission and correlation
for `taken`, `question`, `progress` and `result`, including late first deliveries.
Valid reports can arrive before `taken` or after the turn's result. They add
facts without reopening work or changing an unrelated turn. A result closes
knowledge of the turn while its questions' exact closure reasons can remain
unknown. `replaces` supplies a specific progress relationship; neither it nor
arrival order supplies a total order of turns or output.

Implementing infrastructure chooses representation, presentation, scheduling
and resource policy within these meanings. Core does not select an active turn
from incomplete evidence or require a UI, model workflow or history service.

## 5. Deadlines

`sent_at` and question/approval `deadline` use the shared
[timestamp validation and exact comparison rules](timestamps.md). Invalid
timestamps fail structural checking before admission or timer arithmetic.
Applications may choose coarser values; every receiver preserves all admitted
microsecond distinctions. Clock accuracy and scheduling remain deployment
responsibilities.

- **The originator owns a request's deadline** and measures it on its own clock. A still-open question expires when its deadline is reached; its originator sends `closed` with `why: "expired"` and refuses later new answers as `closed`. An approval's originator orders its decision acceptance, expiry, and withdrawal under [approval exchanges](approvals.md#decision-and-terminal-state). An expired approval supplies no grant; it does not automatically end a work turn.
- **Decision verification** also checks that the decision's `sent_at` is no later than the deadline. That is a consistency check, not how the deadline is enforced. The [security contract](security.md#approvals) distinguishes the retained original request from the newly authenticated decision; request-certificate expiry does not itself expire the approval.


## 6. Describing an actor

`describe` is addressed to the actor principal with no conversation key. The
actor answers with `description`, naming the request in `in_response_to`.
For initial handling the response is the acknowledgement; no separate `ack`
is sent. The requester retries the exact unanswered request after `ack-timeout`.
An eligible [retained duplicate](messaging.md#exact-retained-copies-and-expired-credentials)
receives only a fresh minimal `ack` on an authorized route. It confirms earlier
acceptance, not delivery or currency of a description. A new ID requests a
current description; this is safe because `describe` has no application effect.

| Response field | Meaning |
|---|---|
| `name` | The actor principal |
| `summary` | Text describing what it offers |
| `algorithms` | Both `EdDSA` and `ES256` |
| `honored_request_metadata` | Names of request metadata keys it understands |
| `operations`, optional | Named requests and their input/output declarations |

A description is signed like every message. It describes this actor now; a
cached description does not promise that an operation is still available or
authorized later, or that the same operation name will retain its meaning for
future turns. A fresh description also cannot remove the interval before an
invocation is admitted. Bare principal, operation name and conversation key
do not select a historical declaration. Describing is not a prerequisite to
invocation; stronger offering agreements have their own explicit scope.
There is no search, record-query, conversation-enumeration,
or counting capability in the core description.

A newly received description must identify a retained `describe` addressed to
its authenticated actor in the applicable non-conversation request scope; its
`name` must equal that requested actor principal. A required unknown request
is `unknown`; a known wrong request kind or inconsistent `name` is `malformed`.
The response must come from the requested actor, otherwise `not-authorized`.
Earlier authentication, addressing and route checks still apply. Only a valid
description confirms that request; signature verification alone does not make
its advertised operations or schemas valid.

### 6.1 Operations

An operation declaration makes structured input interpretable across independent
participants. It does not specify which application operations an actor offers.

| Field | Required | Meaning |
|---|---|---|
| `name` | yes | The value used in a `say`'s `operation` |
| `guidance` | yes | When and how to ask; permitted contributions and their interpretation/validation, including whether amendments are supported; whether the operation may ask questions or request approval |
| `input` | no | A self-contained, object-form JSON Schema draft 2020-12 under the [embedded-schema profile](schemas/README.md#embedded-operation-schemas), for the opening request's `data` |
| `output` | no | A schema under the same profile for the turn's successful terminal `result.data` |
| `effects` | no | `false` declares that asking again as a new request is harmless; otherwise assume it may have effects |
| `examples` | no | Illustrative requests in words |

Within one description, operation names must be unique by exact string
equality. Identical duplicate declarations are invalid too. Refuse the whole
description as `malformed`; do not choose first/last or merge entries. This is
local uniqueness, not global allocation or stability across descriptions.

For a fresh request, a supplied operation must be known or it is refused as
`unsupported`, with nothing done. With `input`, `data` must be present, is binding
and must match before a turn opens, even when the schema is `{}`. Refuse absent
or mismatching data as `malformed`, with `detail` only
on a route authorized for that information under [bindings](bindings.md#response-audience-and-confidentiality).
Without `input`, the actor interprets `content`; any initial `data` is a hint.
Having an input schema makes no assertion about the implementation technique.

The operation selected when the turn opens, together with its input, output,
and contribution rules, governs that turn until it closes. Later descriptions
do not retroactively change this contract. When `output` is declared, a
successful terminal result must contain `data` matching it, even for `{}`.
Without `output`, result data is optional. A non-success result may describe
what it left done; the success schema and its presence requirement do not apply
to that description. The actor's obligation does not depend on whether the
requester knows which declaration was selected (section 6.2).

A contribution or answer inherits the opening request's operation. It may omit
`operation` or repeat that same name, even if the actor no longer advertises
the operation for new requests. Compare with the retained operation first.
Another supplied name is `unsupported` if unknown, or `malformed` if it names
a different known operation. This also applies to introducing a named operation
into a turn opened without one. A contribution cannot change the output
contract. An independent invocation uses a fresh request instead.

`guidance` must state which contributions are supported and how their content
and optional `data` are interpreted and validated. The opening `input` schema
is not automatically a schema for every contribution. No field merge, input
replacement, or rerun is implied by another `say`. If full input replacement
is permitted, the replacement must match the selected `input` schema. Other
structured amendments require explicit contribution rules; absent such rules,
contribution `data` is a hint, not a binding replacement of the opening input.
A contribution violating declared input requirements is refused as `malformed`
with `detail` subject to the same response-audience rule. A well-formed contribution the actor declines receives
`taken: not-acted-on`. For unnamed interactions, the actor's description must
state the corresponding contribution rules; senders cannot assume amendment
support from the absence of an operation name.

Producers and receivers must apply the shared [embedded-schema profile](schemas/README.md#embedded-operation-schemas),
including meta-validation, dialect and self-contained reference rules. Invalid
declarations make the whole description `malformed`. Network retrieval and
automatic value conversion are prohibited. Core selects no schema engine and
requires no proof of schema satisfiability. Application owners are responsible for meaningful,
usable declarations. An actor may advertise only operations the requester is
authorized to use; the advertisement grants no later action authority.

Where the operation depends on approval, its contract must also state whether
the permission request remains needed after the work turn ends and who
withdraws it if work is abandoned. Neither a correlation reference nor an
operation's completion creates an implicit approval-lifecycle dependency.

### 6.2 Contract selection and requester knowledge

The actor must retain the contract it selected when admitting a turn. The
requester need not know that complete contract merely because it knows the
operation name, has a cached description, or receives `taken`. None of those
messages binds an invocation to a particular earlier description. Core fixes
the accepted turn's obligation; it does not impose a deployment version policy
or an unchanging offering for all future turns in a conversation.

A requester applies contract-specific checks only where retained agreement or
evidence establishes that contract's applicability to the identified turn.
A cached or newly fetched description alone is insufficient. An otherwise
valid result can establish the actor's reported terminal outcome and confirm
the opening request even when the selected output declaration is unknown;
that does not establish independently verified application/schema compliance.
When the applicable output is known, absent or mismatching data on a successful
result is `malformed` and cannot confirm the request. Later evidence cannot
retroactively erase an accepted report or its disposition. See
[notification contract knowledge](notifications.md#contract-knowledge).

Applications and networks can establish stronger offering agreements for named
or unnamed interactions. Their owners define the meaning and compatibility
promise, requester adapters preserve the intended agreement, and hosting
infrastructure enforces it at actual admission/dispatch. The optional
[provisioned agreement profile](../extensions/interaction-agreements/README.md)
specifies one controlled-deployment approach. Context continuity alone supplies
no such promise. Core adds no expected-contract field, contract-mismatch
refusal, registry, version syntax or required-extension container.

## 7. Delivery

Establish the [continuity profile and scope](continuity.md) before conversation
traffic, then apply the [messaging rules](messaging.md) per conversation. A submission is
accepted when its actor takes responsibility within the live context. A
notification is sent with its identity and sending state retained for its
active delivery attempts. Its signed recipient identifies the principal
for whom it is intended.

Within one sending session, hold later submissions until acceptance of the
current one is confirmed, it is semantically refused, or it is explicitly released by whoever the
requester acts for. Exhausting attempts reports not confirmed and leaves later
submissions held. Within established context continuity, resume eligible paused
attempts when the binding becomes reachable or an authenticated message arrives
from the actor. A [verification diagnostic](diagnostics.md#effect-on-sending-and-knowledge)
ends its associated automatic attempt series; its receipt or reachability alone
cannot restart that series. Diagnostic termination is not explicit release of a
requester slot. Explicit release by whoever the requester acts for, including an
already authorized implementation policy, stops local retries and releases the
slot without undoing prior acceptance. Core requires no human prompt.

Confirmation can come from a separate acknowledgement or a validated semantic
report under [confirmation and sending slots](messaging.md#confirmation-and-sending-slots).
For example, a valid result confirms its opening request without waiting for
its `ack` or `taken`. Only the specifically confirmed messages release their
slots; a result does not confirm an outstanding contribution, answer or stop.

A `stop` may be sent beside an in-flight `say` in the same conversation,
including a contribution or answer. At most one additional stop may occupy
a sending slot in that session at a time; explicit release follows
the ordinary uncertainty rules. Its target is always the opening request,
not the in-flight contribution or answer. It has its own
identity and retries; its acknowledgement does not acknowledge the `say` or
release that message's sending slot. A stop for one turn does not suppress an
unrelated in-flight request. Later ordinary submissions remain held until both
messages have had acceptance confirmed, been terminally semantically refused, or
been explicitly released. A diagnostic for one slot cannot release the other.

Sending a stop withdraws unsent queued submissions only if they are the targeted
opening request or are known to belong to that turn. Unrelated queued requests
remain queued under the ordinary sending rules. Local withdrawal does not
recall a message already sent or prove its non-execution. Retrying an already
sent submission uses the exact original JWS and preserves the applicable sending slots;
retries never become new requests.

The receiver recognizes exact retained copies under the messaging rule, including
after original-credential expiry, without creating another turn, decision, or
execution. Its fresh minimal acknowledgement/refusal requires an independently
authorized recipient route; no cached application content is returned by that
rule. A terminal semantic refusal ends retries;
`busy` waits for backoff and consumes no attempt. Acknowledgements and refusals
receive no core response, including when invalid or unmatched, under the
[control-response rules](diagnostics.md#control-response-termination).

The actor may end notification attempts and release the sending slot under its
infrastructure's policy, including before attempts run out or during repeated
`busy`, with the scope and limits in [delivery and uncertainty](messaging.md#delivery-and-uncertainty).
This changes delivery attempts, not the message's disposition or exchange state.
The core provides no catch-up query or eventual-delivery guarantee. A result
that was missed can leave the requester with an unknown outcome. Reconnecting
does not establish context continuity or authorize automatic resubmission of
uncertain work. Retire admission before discarding required context, and reject
old-scope traffic under its original guard. The concrete
[provisioned profile](profiles/provisioned-context.md) requires fresh setup on a
new connection; it supplies no automatic continuation. See
[context loss](messaging.md#context-loss).


## 8. Refusals

| Reason | Meaning |
|---|---|
| `malformed` | Invalid payload, missing or unknown fields, an unknown kind, excessive size, input that fails its declared requirements, an invalid target kind, a notification or closure contradicting established facts, invalid progress replacement, or a contribution attempting to select a different known operation |
| `algorithm-key-mismatch`, `certificate-invalid`, `certificate-expired`, `key-not-certified`, `bad-signature`, `not-canonical`, `not-addressed-to-me` | The first failing [verification check](security.md#verification-order) |
| `not-authorized` | The authenticated principal may not make this request, supply this decision, or close another originator's request |
| `unknown` | A required correlation reference names no message or approval known in the live context; prospective `stop.turn` suppression, [closure before the request](approvals.md#closure-before-the-request), and an unresolved [progress predecessor](notifications.md#progress-replacement) are explicit exceptions |
| `closed` | A targeted turn, question, or approval is closed, or a question/approval deadline has passed |
| `wrong-request` | A decision names the wrong approval or carries the wrong digest |
| `unbound-decision` | A required approval digest is missing |
| `nothing-to-stop` | The targeted opening request is known to have ended or to have been disposed of without opening a turn; a different open turn is unaffected |
| `unsupported` | An unsupported version, content block type, or named operation |
| `busy` | The receiver cannot accept the message within the live context now; retry with the same id after backoff |

`busy` is the only retryable refusal and does not acknowledge acceptance. It is
sent directly, does not enter the conversation's accepted state, and does not
consume a sending attempt. An authenticated, properly correlated semantic refusal
ends attempts for that submission. A properly associated verification diagnostic
also ends its automatic attempt series, but is not confirmation or semantic
refusal and does not itself release a requester slot. Preserve established facts;
otherwise the submission remains not confirmed. The diagnostic reports a failed
frame whose echoed ID was untrusted, not proof about the exact original bytes or
absence of earlier execution. [Diagnostics](diagnostics.md) defines receiving
association and the role-specific release rules.

A permitted diagnostic for an unverifiable known non-control frame has no
authenticated recipient. Address its restricted minimal form to `unverified`,
with no conversation, only on the original independently authorized route.
No other kind can use that recipient. Only verification-stage reasons are
permitted; no detail, metadata, evidence or other additional fields are allowed.
An unverifiable frame cannot become an authorized request or reserve its claimed
sender's ID. [Sending diagnostics](diagnostics.md#sending-a-verification-diagnostic)
and [receiving them](diagnostics.md#receiving-and-associating-a-diagnostic) define
the full exception. Never send a core response to recognizable controls; use
the binding rejection for unclassifiable frames. Earlier guards retain precedence.

## 9. Version and extensions

Every core payload in this standalone core/1 draft has `version: 1`. A different or missing
version is classified as `unsupported`. A known version with an unknown kind or
top-level field is `malformed`. Emitting a core refusal remains subject to the
binding and control-response rules; an unknown kind uses the unclassifiable-frame
binding outcome rather than generating a diagnostic chain.

This payload is signed with protected `typ: "keel-core-v1+jws"`; its schema
identity is `urn:keel-protocol:core:1`, and the WebSocket binding selects
`keel.core.v1`. These jointly identify this standalone definition. The generic
source-project `keel+jws`, legacy asking/version 2, and earlier draft profiles
are different contracts. No compatibility with them is required. Selecting a
binding or changing external metadata cannot reinterpret their signed bytes as
this core. Optional inspection of old artifacts must retain their original
contract identity and must not admit them as new core/1 work.

Unknown metadata keys are ignored. Metadata must not redefine core field or
message meanings or carry requirements whose omission would change the
requested action. In particular, a metadata target cannot turn `stop` into
job cancellation, descendant cancellation, or a stronger cessation guarantee.
`honored_request_metadata` is not negotiation of required cancellation semantics.

The core defines one stop target category, an identified turn; it has no open
target-kind registry. An extension can define another category only through an
explicitly identified and versioned contract, with support and applicability
established before use. That contract must define target identity, authorization,
scope, effects, outcomes, and refusal behavior, with its own schema and vectors.
Required semantics that are unsupported must be refused, never ignored or
silently downgraded to core turn stop. An unrecognized top-level field in a core
payload remains `malformed`; an unsupported contract version is `unsupported`.
No extension negotiation wire mechanism is defined by this draft.

Additional services require their own contracts; sharing the signed-message
format does not add their kinds to the asking contract. Application operations
can supply cancellation semantics without extending core stop.

This is a pre-release draft. Changes to fields, kinds, or behavior must update
the text, schema, and vectors together. A published compatibility identity must
not identify conflicting definitions. No implementation may silently amend it.
