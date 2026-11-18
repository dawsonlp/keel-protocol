# Implementing core/1

This guide organizes the current engineering obligations without prescribing
packages, processes or storage. The [core specification](../core/README.md) and
selected profiles are authoritative. This repository supplies no implementation;
independent runtime conformance and consumer migration remain to be demonstrated.

## Implement the endpoint boundary

| Area | Implementation responsibility | Required evidence |
|---|---|---|
| Contract identity | Dispatch payload version, signed type, schema and binding as one core/1 contract | Reject incompatible earlier-profile traffic rather than silently translating it |
| Credentials and names | Apply the closed JOSE/certificate profile and explicitly configured issuer/key naming authority | Positive verification and all specified rejection cases, including naming collisions and forbidden algorithms |
| Canonical signing and exact identity | Produce the specified canonical bytes, retain original compact JWS, and distinguish conflicting bytes under one scoped identity | Canonicalization and signature fixtures; byte-equal retries through renewal |
| Admission and disclosure | Apply route and continuity guards before state-dependent feedback; independently authorize response recipients | Captured first frames and retries on unauthorized routes reveal no retained state or protected response |
| Retained authentication | Keep the complete trusted basis for eligible exact-copy handling; do not turn a stored artifact into invented historical proof | Expiry, renewal, lost-state, control and current-authority cases in their specified precedence |
| Turns and operations | Select and retain the admitted contract; validate operation data; distinguish independent openings, contributions and answers | Operation and turn traces, including falsey values, selected-contract retention and declined amendments |
| Approvals and effects | Implement independent originator-owned lifecycle, binding, deadlines and closure; keep actual effect authorization separate | Both conversation directions, competing decisions, withdrawal/expiry races and external-effect policy tests |
| Notifications and delivery | Retain references and dispositions; handle duplicates, reordering and incomplete knowledge without invented transitions | Late first deliveries, result-before-taken, progress replacement, identity conflicts and scoped retry cases |
| Stop and application cancellation | Target the opening request, including suppression before arrival; keep control processing serviceable | Delayed stop cannot select a newer turn; terminal protocol state does not falsely report rollback |
| Diagnostics and controls | Associate notices with the original attempted route and scope; prohibit core reply loops | Invalid controls, ambiguous association, old callbacks and unrelated notices cannot affect new traffic |
| Time | Validate full syntax and real dates, preserve up to six fractional digits and compare exactly across the year range | Timestamp validation, comparison and receiving vectors; actual clock behavior tested separately |
| Binding and continuity | Establish matching readiness and guards, retain required live state and retire admission before discarding it | Provisioning, disconnect, backend loss, queued-frame and replacement-context races |
| Application integration | Preserve protocol state outside application/model callbacks and make workload boundaries explicit | Mechanical and human/model flows obey the same receiving rules; application side effects remain policy-controlled |

Use the [schema guide](../core/schemas/README.md) for the payload and embedded
operation schemas. A general-purpose date parser, JSON Schema `format` handling
or transport authentication alone does not implement all required checks.
Follow the normative verification and admission order rather than combining
checks in an order that changes observable failures.

## Deployment responsibilities

Configure enrollment and trust bootstrap, issuer/key namespace authority,
credential renewal, key compromise response, action and disclosure policy,
confidentiality, resource limits and clocks. Specify the deployment's actual
failure boundary and limits; principal identity does not imply unrestricted
naming authority or permission to use every resource.

The provisioned-context profile requires a trusted facility independently
authorized by both endpoints, matching descriptors, actual-channel association,
a fresh actor-issued conversation key and bilateral readiness before traffic.
Connection loss retires that scope. A frontend connection cannot keep lost
backend interpretation state alive. Alternative profiles require their own
precise shared definitions; silently restoring traffic under the provisioned
profile's name is not permitted.

Human approval interfaces must present the action actually bound to the decision.
Model output is application input, not independent authority to execute. Multiple
logical actors hosted in one process are not automatically separate compromise
domains. Scheduling and resource controls must allow required controls to remain
serviceable while work is running.

## Integrating or replacing an existing implementation

Select core/1 explicitly; do not relabel legacy artifacts or rewrite saved signed
messages. Preserve unresolved submissions as evidence while applying the current
scope rules to retry eligibility. A persisted outbox, renewed credential or
successful reconnect cannot establish remote state retention.

Implement the application's history/outcome retrieval and effect reconciliation
through its responsible actors. Use fresh valid exchanges after an old scope
ends. Consumer service contracts, not a recovery extension, define retention,
completeness and application job resumption. The [network guide](network-development.md)
provides concrete cases. The obligations above remain current; inspect the actual
consumer source and test behavior before claiming its migration is complete.

## Validation and conformance evidence

Validation has distinct layers:

1. **Repository consistency:** run `python3 tools/check_repository.py` from any
   directory. It checks local links/anchors, JSON parsing and trace structure.
   Documentation links must resolve within this checkout or use explicit URLs.
2. **Structural and value validation:** exercise the payload schema with the
   declared draft and embedded-schema restrictions. Run real-date timestamp
   validation and exact comparisons as well as shape checks. Reject invalid
   values instead of repairing them.
3. **Cryptographic validation:** run canonicalization, signature, credential,
   approval-binding and retained-authentication fixtures from
   [security vectors](../core/vectors/security.json). Preserve fixture bytes.
4. **Receiver behavior:** adapt the [behavioral traces](../core/vectors/README.md)
   to the implementation, asserting its emitted responses, retained facts and
   effects at each step. Trace-file integrity alone does not execute them.
5. **Interoperability and deployment:** run independent peers, inject duplication,
   reordering, loss, expiry, scope retirement and unauthorized routes, then test
   the actual network's service and effect guarantees.

For each claim record the implementation revision, selected profiles, environment,
executed cases, failures and limitations. An optional profile's vectors apply only
when claiming that profile. No unadopted proposal traces are retained as
conformance artifacts.

Specification review is complete; runtime conformance is not established here.
This guide carries forward the outstanding security and migration responsibilities
without treating their earlier checklist completion counts as implementation evidence.
