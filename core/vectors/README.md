# Core conformance vectors

[security.json](security.json) gives inputs and expected results for canonical
JSON, message verification, approval binding, and payload structure. Signed
fixtures use the standalone `keel-core-v1+jws` profile and payload version 1;
an unchanged earlier-profile specimen explicitly expects rejection. Public test
keys and primitive canonicalization inputs are preserved. Structural cases distinguish the
required `stop.turn` shape from invalid untargeted or legacy `through` payloads.
They also include approval initiation without a correlation reference and
closure addressed in the opposite conversation direction; sender ownership
still requires semantic checks.

Its `retained_approvals` artifact separates four executable observations:
the request authenticates before expiry; first seeing it after expiry fails;
a fresh decision authenticates after that expiry; and the decision binds the
unchanged request before its deadline. These cryptographic observations support
the retained-state rule; they do not execute stateful admission or response
authorization in an actor.

[diagnostics.json](diagnostics.json) specifies the restricted reserved-recipient
exception and control-response termination. Its cases cover first-seen verification,
authenticated peer and unique original-route/scope association, both conversation
roles, unassociated notices, retained no-effect controls, requester release and
notification policy. They distinguish attempt termination from semantic refusal
and preserve uncertainty about earlier copies. No core reply is permitted to a
recognizable control; unclassifiable frames take the binding outcome. The reserved
shape fixtures in security.json test only structure; these semantic traces require
an implementation adapter and do not claim runtime conformance.

[timestamps.json](timestamps.json) defines the UTC microsecond profile's
`validation_cases`, exact `comparison_cases` and receiving `cases`.
`schema_valid` records the outer time definition only; `valid` additionally
requires Gregorian calendar checks. Full structural validation must reject
impossible dates even when the pattern accepts them. Comparison cases require
the complete admitted value, including near the year-range endpoints; equivalent
values do not authorize rewriting signed strings. Behavioral traces cover
deadline boundaries, earlier-check precedence, retained copies, invalid controls
and application-data scope. These traces require an implementation adapter;
artifact validation does not execute runtime admission or establish clock accuracy.

[delivery.json](delivery.json) gives core behavioral traces. It includes
memory-only acceptance, duplicates within a retained context, missed replies
that remain unknown, state loss without automatic continuation, and refusal of
decisions for unknown approvals. Durable acceptance and restart resumption are
not conditions of passing this core suite.

[continuity.json](continuity.json) specifies the core establishment/admission
boundary and concrete `keel.provisioned-context.v1` profile. Cases cover trusted
setup, bilateral readiness, fresh conversation keys, channel and queued-frame
guards, retirement races, asynchronous peer failure, route privacy, exact-copy
feedback, uncertain outboxes, and the separate scope of optional restoration.
Ordinary behavioral traces presuppose an established valid scope unless they
explicitly exercise establishment or its failure. An old frame for a retired
conversation fails the guard; an unknown reference inside a valid new scope
follows the ordinary message rules. These are abstract adapter cases, not
evidence of an implemented provisioning facility or runtime.

Cases explicitly marked as isolated semantic checks exercise the named receiving
rule without claiming that a complete admission pipeline can reach it. For example,
a foreign signer fails the provisioned profile's scope guard before a notification
role check could return `not-authorized`. Likewise cryptographic/structural fixtures
test their stated layer, not provisioning. An implementation must honor earlier
applicable guard failures; a layer-specific expectation cannot override them.

[turns.json](turns.json) specifies fresh requests, targeted contributions,
explicit answers, declined inputs, and closure races. It covers the stable
response contract selected by an opening request, composite responses, and
the distinction between model calls, child turns, and the parent turn.
References in these traces name messages in the retained live context; the
traces require semantic checking beyond standalone schema validation.

[operations.json](operations.json) specifies description association, exact-name
uniqueness, the limits of cached advertisements, selected turn contracts and
requester knowledge. It covers general JSON data, required presence, falsey
values, the shared embedded-schema profile, contribution boundaries and exact
duplicate precedence. A report can confirm an opening while application/schema
compliance remains unverified; a known contract violation cannot confirm it.
These are core traces. The optional
[agreement vectors](../../extensions/interaction-agreements/vectors.json)
separately cover stronger application promises established through provisioning.

[stops.json](stops.json) specifies identified-turn cancellation, suppression
before an opening request arrives, completion and contribution races, duplicate
handling, and scoped sending behavior. It distinguishes protocol termination
from application cancellation and from effects that may still be in progress.

[approvals.json](approvals.json) specifies independent permission exchanges,
both conversation directions, originator-owned decisions and deadlines, and
explicit withdrawal without revocation. It covers owner authorization, closure
reasons, closure overtaking its question or approval, duplicate and contradictory
terminal reports, and independence from work-turn completion and stopping.

[notifications.json](notifications.json) specifies receipt of actor reports
before `taken`, after turn completion and across incomplete knowledge of several
turns. It covers required live references, actor/recipient scope, exact retries
versus late first deliveries, conflicting dispositions, question closure reasons
and progress replacement. Replacement cases distinguish unseen predecessors,
later-invalid claims, scoped IDs, chains, branches and cycles. The traces require
the same meanings and wire outcomes without selecting a UI, scheduling policy,
internal graph or mandatory recovery service. They are abstract conformance
cases, not evidence that a runtime implements these rules.

The notification and delivery cases distinguish refused predecessors from independently
invalid relationships, policy release during `busy` from confirmation, and
validated acceptance evidence from merely correlated reports. They also cover
ambiguous cross-originator references without imposing global ID allocation or
reinterpreting already accepted work. [Delivery traces](delivery.json) include
early notification release and the existing direct-description confirmation.

[authentication.json](authentication.json) specifies retained exact-message
authentication, expiry during pending approvals, fresh decision credentials,
renewal/rotation, conflicting signed bytes, lost state, historical-evidence
limits, current authority and confidential response audiences. Its 40 abstract
cases include exact retained copies, fresh minimal disposition controls, uniform
route/disclosure rejection for known and unknown frames, and principal naming
governance. Naming cases cover actor and party names, constrained issuer
authority, unauthorized collisions, deliberate overlapping issuers, trust-anchor
addition, key-specific authority, key/issuer rotation, membership, renaming and
isolated reuse of a name's spelling. Ending a conversation alone cannot repurpose
a governed principal or transfer old permissions and evidence. The traces also
separate retained authentication facts from current naming, action and
disclosure policy after an issuer-policy change. These are behavioral traces
requiring an implementation adapter; artifact checks do not establish runtime
conformance. The naming scenarios prescribe no issuer-qualified principal,
mandatory network prefix, runtime configuration format or federation service.

The `jcs` cases exercise the RFC 8785 primitive only; they do not assert whole
core-message admission. Integral-valued numbers outside the core bound can
therefore appear in a canonicalization specimen while remaining invalid in a
core frame. Test issuer subject sets are explicit fixture policy, not a
universal namespace configuration API.

Each implementation must reproduce applicable expected results. Test clocks,
trust anchors, and public fixture private keys are test context only. Never use
those keys to identify a real participant.

The traces can be driven by an implementation adapter without prescribing
internal architecture or storage APIs. They have not been executed against
actor implementations. Vectors cover examples; the [core definition](../README.md)
also applies. Extension conformance is claimed separately.
