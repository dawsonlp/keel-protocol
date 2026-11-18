# Current requirements

These requirements explain the drivers for core/1. They summarize the approved
contract; the linked normative definitions supply exact rules and precedence.
They do not introduce an additional protocol version or a new checklist of
unimplemented specification work.

| ID | Driver and required outcome | Definition and evidence |
|---|---|---|
| R01 | Independently built peers need one explicit compatibility identity and shared message vocabulary; incompatible drafts must not be silently mixed | [Core](../core/README.md), [binding](../core/bindings.md), [schema](../core/schemas/README.md) |
| R02 | Attribution must survive forwarding or retention of signed artifacts; trusted issuers may certify only their governed names | [Security](../core/security.md), [credential profile](../core/security-profile.md), authentication vectors |
| R03 | Authentication, current authorization, permission and external execution must remain distinguishable; captured bytes must not authorize disclosure on a new route | [Security](../core/security.md), [bindings](../core/bindings.md), security vectors |
| R04 | An admitted opening must select one terminal response contract; contributions can enrich that turn without silently invoking independent work | [Asking](../core/asking-contract.md), turn and operation vectors |
| R05 | Structured deterministic operations and interactive work must share the contract without requiring a model or human; role-applicable receiving remains required | [Participation](../core/README.md#participation-and-conformance), operation vectors |
| R06 | Declarations must provide interoperable input/output validation while leaving application meaning and cross-invocation compatibility with their owners | [Operation schemas](../core/schemas/README.md), operation vectors, optional [agreement profile](../extensions/interaction-agreements/provisioned-agreement.md) |
| R07 | Permission exchanges must work independently of work turns, preserve originator ownership and distinguish decision acceptance from grant use | [Approvals](../core/approvals.md), approval vectors |
| R08 | Delayed stop requests must identify the intended work; protocol termination must not imply rollback or recursive application cancellation | [Stop](../core/asking-contract.md#44-stop), stop vectors |
| R09 | Duplicates, reordered reports and missed messages must not repeat actions, reopen terminal work or manufacture a total order | [Messaging](../core/messaging.md), [notifications](../core/notifications.md), delivery and notification vectors |
| R10 | Context loss or replacement must not let old traffic create fresh work; conversation admission requires an explicitly established scope | [Continuity](../core/continuity.md), [provisioned context](../core/profiles/provisioned-context.md), continuity vectors |
| R11 | Retained authenticated bytes must keep their identity across credential renewal; recognizing an exact old copy must not authorize new actions or uncontrolled disclosure | [Retained copies](../core/messaging.md#exact-retained-copies-and-expired-credentials), security and authentication vectors |
| R12 | Invalid delivery should yield useful bounded diagnostics without response loops or false confirmation of the original message | [Diagnostics](../core/diagnostics.md), diagnostic vectors |
| R13 | Timestamps must have unambiguous interoperable syntax and exact comparison, while clock quality and application timing remain separately owned | [Timestamps](../core/timestamps.md), timestamp validation and comparison vectors |
| R14 | Networks must be able to provide historical access and recover application work through ordinary service interactions without making recovery mandatory or redefining core acceptance | [Core lifetime](../core/README.md#context-lifetime), [application recovery guidance](network-development.md#history-and-application-recovery) |

## Constraints

Core/1 is a common conversation and authority contract. It does not define all
possible actor protocols. Conformance is by endpoint and contextual role, not
by implementation package or the spelling of an actor identity.

The wire timestamp profile accepts UTC `Z`, years 0001–9999, real Gregorian dates,
seconds 00–59 and optional one-to-six fractional digits. All receivers must retain
and compare the whole admitted value; applications choose the resolution they
emit. More digits do not establish better clocks or physical event order.

The concrete provisioned-context profile requires trusted setup at both endpoints
and retires its scope on connection loss or local context retirement. It is not
a public discovery, negotiation or reconnect-restoration protocol.

Application agreements and extensions must be explicitly applicable before a
participant relies on their stronger promise. No generic capability registry,
operation-version syntax, declaration hash convention, recovery extension or
scoped-grant format is required or selected by core.

## Acceptance evidence

The [implementation guide](implementation.md#validation-and-conformance-evidence)
maps the requirements to validation layers. Artifacts establish a reproducible
specification target. Runtime conformance requires observing the endpoint's
behavior, including negative cases and failure boundaries. Application guarantees
require their own tests; passing core cases does not establish them.
