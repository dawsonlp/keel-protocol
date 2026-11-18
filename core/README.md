# Core protocol

The core defines observable participation in live signed conversations. It
defines application-independent message behavior and safe admission boundaries;
it requires no restoration of conversation state after loss.

The protocol specifies shared message meanings and the minimum observable
guarantees needed for correct interoperability. A participant's knowledge can
remain incomplete: missing messages do not establish an outcome, and receipt
order does not supply an otherwise absent actor order. Implementing infrastructure
is responsible for using those facts and limits correctly, including its state
representation, scheduling, presentation, delivery management and enforcement
mechanisms. Core selects no UI, model-dispatch workflow or total-order mechanism.
An infrastructure may supply stronger guarantees under an explicitly applicable
agreement; those guarantees do not become implicit core requirements. Freedom
of implementation does not change what an acknowledgement, result or closure
means, or the obligations of the contract it claims to implement.

| Concept | Meaning and identity |
|---|---|
| Actor | Within this core, a participant capable of engaging correctly with the protocol, named by an actor principal; the name alone does not establish protocol conformance |
| Principal | A governed identity: `actor:<name>` or `party:<id>`; explicitly authorized issuer/keys certify that participant's name |
| Credential | An issuer's time-limited certification of a principal and key under configured naming trust |
| Authenticated message | Exact signed bytes with an established signer, profile and addressed context; the observation can be retained independently of credential expiry |
| Authorization | Receiver/resource policy determining whether the requested action is permitted |
| Requester | A principal asking an actor; it may itself be an actor |
| Protocol contract | Messages and behavioral obligations under an explicitly identified core or extension profile |
| Operation declaration | An actor's advertised named request, guidance and optional input/output schemas; a description is not a binding to a later invocation |
| Turn contract | The response obligation selected when the actor admits an opening, retained for that turn |
| Offering agreement | An explicitly established application promise about available interaction meaning over a stated scope; optional beyond core |
| Conversation | An exchange addressed by an actor principal and a conversation UUID together |
| Conversation context | The live state used to interpret that conversation's messages, turns, decisions, and duplicates |
| Admission scope | An explicitly established association between authorized peers, a conversation and the binding conditions under which its messages may be handled |
| Continuity guard | The infrastructure mechanism that prevents traffic for an invalid or retired scope from entering replacement context state |
| Message | An immutable signed value with a UUID; retries preserve its entire original compact JWS |
| Turn | An exchange with one defined terminal response contract, opened by the actor's admission reported in `taken`, identified by its opening `say`, and ended by `result` |
| Notification | An actor-issued report of a request disposition or turn fact; receipt can establish knowledge after the transition it reports |
| Progress replacement | An explicit supersession relationship between progress messages of the same actor and turn; an unseen predecessor remains unresolved |
| Contribution | A later `say` admitted to a turn to supply information, answer a question, or propose an amendment under that turn's contract |
| Stop target | A fresh opening request's message UUID, carried in `stop.turn`; it can identify an open turn or a request still in transit |
| Approval | An independent request for authority identified by its message UUID, with at most one accepted decision in its context |
| Approval originator | The authenticated sender of the request; owns its deadline, decision acceptance, and closure irrespective of conversation role |
| Decision maker | A participant authorized to grant or deny the described permission; permission does not establish execution |
| Grant | Permission under an explicit application contract, with its own validity, scope and use limits |
| Effect | Actual execution or resource change; the effect owner enforces the applicable authorization and duplicate-effect policy |
| Evidence | An artifact whose claims require a stated verification basis; a retained local observation is not automatically portable historical proof |
| Binding | A way to carry signed frames to addresses and return responses |
| Acceptance | Taking responsibility for a message within the live context, without a core durability promise |
| Verification diagnostic | An authenticated peer report that a delivered frame failed verification; association can end retries without confirming or semantically refusing the original message |

A conversation belongs to one actor. An actor can have many conversations.
Equal conversation UUIDs at different actor principals do not identify the same
conversation. For the same pair of principals, different conversations must
nevertheless use different keys, including when actor and requester roles are
reversed. This makes bilateral message routing unambiguous within retained
contexts. Losing context does not prove that its earlier work was undone.

Principal names identify participants independently of network membership.
Trusting an issuer/key does not automatically authorize it to certify every
name. [Governed names](security.md#governed-names-and-issuer-authority) define
explicit naming authority, intentional issuer overlap, collision handling and
identity continuity; action authorization remains a separate receiver decision.

Every message names one recipient. A conversation message also names its
conversation. Correlation names a message in that context; `caused_by` can name
a message in another conversation. References establish no authority by themselves.

The actor has at most one open turn per context. Questions belong to that turn and close
when it closes. Approvals have their own lifecycle and can be pending without
a work turn. Correctness includes consistent acceptance,
ordering, duplicate handling, and accurate uncertainty within that context.
Matching a JSON Schema alone is insufficient.

The actor's actual turn state and a peer's knowledge are distinct. Valid
notifications can arrive before `taken` or after `result`; receipt adds facts
without repeating transitions or reopening work. Missing messages can leave
turn order, outcomes or a question's precise closure reason unknown. Explicit
progress replacement orders only the messages its valid relations connect.
[Receiving notifications](notifications.md) defines those mechanisms and their
limits; infrastructure selects its representation and policy.

Prior refusal of a progress predecessor does not by itself invalidate a fresh
update. Delivery confirmation follows validated evidence about identified inputs,
not a required separate ack frame. The actor's infrastructure may release a
notification's local retries without asserting delivery or changing its exchange.
Scoped identity does not disambiguate every bare reference; required lookups
with multiple permitted targets are refused rather than arbitrarily interpreted.

A turn may admit many contributions and produce a synthesized or aggregate
response. An independent invocation has its own response obligation; it is not
silently combined with an open turn. A `say` targets a contribution by naming
the turn's opening `say`, or answers a question by naming that question, in
`in_response_to`. Without that field it requests a new turn. The
[asking contract](asking-contract.md#4-turns) defines each disposition.

Whether an interaction accepts amendments is independent of whether its inputs
are structured or its implementation uses a model. A model call is internal
computation. A delegated actor's turn is a separate exchange. Neither completion
automatically completes the parent turn. Application commitments can span many
turns; each result answers only for its own response contract.

Operation names are unique within each description, but core does not require
their meaning to remain unchanged across descriptions or future turns. A
requester can know a reported outcome without knowing the selected output
declaration. [Contract selection and knowledge](asking-contract.md#62-contract-selection-and-requester-knowledge)
defines that distinction. Networks can select stronger named or unnamed
interaction promises through the optional
[provisioned agreement profile](../extensions/interaction-agreements/README.md).

`say.data` and `result.data` can carry any core-valid JSON value while the
message envelope remains an object. Declared input and successful-output schemas
require present data, distinct from null or an empty value. The shared
[embedded-schema profile](schemas/README.md#embedded-operation-schemas) fixes
validation meaning without selecting an implementation engine.

Core `stop` targets one identified turn, including suppression of its opening
request before arrival. It never selects another turn because that turn happens
to be open. A `stopped` result ends that response obligation without promising
rollback, cessation of already-started external effects, or cancellation of a
longer-lived application commitment. Application cancellation defines its own
target, authority, and outcome; see [stop](asking-contract.md#44-stop).

An approval can initiate a conversation or coexist with work turns. Its
originator orders decision acceptance, expiry, and withdrawal, and sends
`closed` in either conversation direction. Correlation supplies context without
creating a lifecycle dependency. Ending work cannot implicitly withdraw an
approval or revoke accepted permission. [Approval exchanges](approvals.md)
define explicit withdrawal, owner-issued closure, and delayed-request handling.

[Verification diagnostics](diagnostics.md) have a restricted `unverified` address
and require authenticated peer, original route/scope and unique attempt association
before changing retry state. They establish no non-execution or semantic refusal,
and do not themselves release requester slots. No core message is sent in reply
to a control; unclassifiable frames use the binding rejection. Infrastructure
owns local diagnostic presentation and authorized release policy.

## Required definition

Read [messaging](messaging.md), [security](security.md),
[credential/envelope validation](security-profile.md),
[the asking contract](asking-contract.md), [core timestamps](timestamps.md),
[approval exchanges](approvals.md),
[receiving notifications](notifications.md),
[verification diagnostics and control responses](diagnostics.md),
[context establishment and continuity](continuity.md),
[bindings](bindings.md), and the
[schema](schemas/README.md). The [core vectors](vectors/README.md) supply
specific conformance cases. No extension specification is needed to implement
or claim conformance to these core requirements.

Participants need the same core revision, a shared binding, compatible trust
anchors, permission to interact and an explicitly selected continuity profile
for conversation traffic. The [provisioned-context profile](profiles/provisioned-context.md)
provides a concrete memory-only choice for controlled deployments. Other profiles
must precisely implement the core admission requirements. A base participant is
conformant even when it provides no restart recovery or conversation-history access.

## Participation and conformance

Core/1 is one common conversation and authority contract, including asking,
approvals and their delivery and receiving rules. It is not a universal definition
of actor behavior. An actor principal identifies a participant; it does not select
or prove support for this contract. Separately identified service contracts can
use actor identities without being core/1 contracts.

Conformance belongs to the participant endpoint and is conditioned by its role
in each exchange. Application code and infrastructure may jointly fulfill that
contract; placing machinery in an adapter does not reduce the endpoint's
obligations. Core does not require each participant to originate every optional
interaction, but it must correctly handle applicable received traffic under the
required definition. There is no reduced asking-only, approval-only or bounded-only
core conformance profile.

| Role or scope | Required behavior |
|---|---|
| Both peers | Apply authentication, addressing, scope, acceptance/refusal, identity, duplicate and delivery rules |
| Answering actor | Honor the admitted turn contract, report input dispositions, handle applicable contributions and controls, and produce its terminal result |
| Requester | Retain the required submission context and interpret associated reports, questions and closures, including delayed delivery |
| Approval originator | Own decision acceptance, expiry, withdrawal and closure of its independent approval |
| Approval recipient/decision maker | Apply authorization and approval receiving rules; handle an accepted request through the signed decision exchange |

Requester and answering actor are contextual roles. An actor can request work
from another actor; this does not reverse the roles in its existing conversation.
A client need not expose its own answering service merely because it requests
work. Either conversation role may originate an approval, including without an
open work turn. An approval-only workload does not select a smaller core contract.

An operation need not ask questions, emit progress or request permission. It may
be a deterministic calculation with fixed descriptive text and structured data,
and may decline amendments under its selected turn contract. No model, human
interface or natural-language inference is required. Such an offering still has
the applicable turn, control and receiving obligations. An application promise
about which interactions an operation will originate does not negotiate reduced
protocol support.

Authorization policy may legitimately refuse a request, and a decision maker
may deny permission. Neither is a substitute for missing protocol support.
The [`unsupported` refusal](asking-contract.md#8-refusals) covers version,
content block type and named operation; it is not an opt-out from core approval
or notification handling. Descriptions and arbitrary metadata do not negotiate
participation profiles.

### Participation examples

| Example | Conformance consequence |
|---|---|
| A `sum` operation receives `say` with fixed text and structured `[2,3]`, reports admission and returns `result` with data `5` | A bounded deterministic operation uses the ordinary contract; meaningful text does not require inference |
| A bounded operation declines a later amendment | The contribution receives its defined disposition; it is not silently ignored or treated as new work |
| A mechanical requester receives a question or a result before `taken` | It follows the receiving contract using retained references, even if its usual workload returns only results |
| A participant initiates an approval without a work turn | Approval ownership and closure apply independently; this does not establish an approval-only profile |
| An authorized approval reaches an endpoint whose application never originates approvals | Optional origination does not permit an `unsupported` capability refusal; ordinary authorization and decision rules still apply |
| A record or locator endpoint uses another signed contract under an actor principal | Its identity alone establishes no core/1 conformance; mapping it to a core operation requires explicit preservation of its intended guarantees |

Existing [turn](vectors/turns.json), [operation](vectors/operations.json),
[notification](vectors/notifications.json) and [approval](vectors/approvals.json)
traces cover the underlying exchange rules. These examples clarify their
participation scope; they do not claim tested implementation interoperability.
History and application recovery guarantees belong to the responsible services;
see the [network guide](../docs/network-development.md#history-and-application-recovery).

## Context lifetime

Core guarantees apply while the state interpreting an exchange is retained.
Transport interruption can occur without state loss; reconnecting proves
neither that the state survived nor that it was lost. The same principal,
certificate, address, or conversation UUID is not proof of continuity.

The selected profile must prevent old-scope traffic from silently creating fresh
work in replacement state within its declared failure boundary. A missing context
is never sufficient authority to create one. Retire its admission guard before
discarding required state; queued frames remain associated with their original
guard. These requirements do not prove completion, non-execution or exactly-once
external effects. They require neither permanent message history nor detection
of arbitrary silent corruption or instantaneous remote failure.

The [continuity contract](continuity.md) defines establishment, admission and
retirement. Infrastructure chooses lifetime and resource policies. In the
provisioned profile, each authenticated connection receives a fresh actor-issued
conversation key, both endpoints prepare their receive guards before traffic,
and connection loss or local context retirement ends that scope. Reconnection
needs fresh setup; uncertain old work is not automatically resubmitted.

Stronger retained reconnection or restoration needs its own explicit profile
or extension. Core introduces no incarnation field or recovery API. Inside a
valid scope, an unknown question or approval cannot be reconstructed from a
response; a closure-before-request creates only its defined scoped marker.

Processes, databases, internal components, storage APIs, and durable logs remain
implementation choices. No factory, locator, knowledge service, or record
service is a prerequisite of core participation.
