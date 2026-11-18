# Core payload schema

[keel-v1.schema.json](keel-v1.schema.json) defines the core asking payloads in
JSON Schema draft 2020-12. Every `$ref` is internal. There is no extension
schema dependency.

The `$id` is `urn:keel-protocol:core:1`, identifying standalone core/1.
Payloads use `version: 1` and the signed profile `keel-core-v1+jws`; see
[release status](../../README.md#protocol-identity-and-validation). There is no legacy-draft compatibility promise.

Apply [signature verification](../security.md#verification-order), then the
[structural check order](../asking-contract.md#2-every-message). A schema pass
does not establish authorization, valid transitions, ordering, or duplicate
handling. Core acknowledgement payloads carry no promise of durable acceptance.
An extension's stronger semantics must be established separately.

Conversation admission also requires the selected [continuity profile](../continuity.md)
and its active scope guard. Payload validity, a fresh ID or an initiating `say`
does not establish a new context. The provisioned profile constrains conversation
key allocation and channel association without adding payload fields; these
conditions cannot be checked from one JSON payload.

The payload envelope remains an object. `say.data` and `result.data` may contain
any JSON value within the [signed-JSON profile](../security-profile.md), including
arrays, strings, numbers, booleans and `null`. The selected operation narrows that
domain. Presence is distinct from value: `null`, `false`, `0`, `""`, `[]` and `{}`
are present values and must survive validation and serialization unchanged.
Omission is not a JSON value and must not be synthesized as `null`.

`in_response_to` has an
explicit turn-contribution or question-answer meaning for `say`; its absence
requests a new turn. The target's kind and state, operation compatibility,
contribution admission, and the opening contract's terminal output obligation
are semantic checks defined in [turns](../asking-contract.md#4-turns) and
[operations](../asking-contract.md#61-operations). They cannot be established
by validating one payload in isolation. Structural fixtures remain structural
even when their messages refer to other messages not included in that fixture.

`stop.turn` is a required UUID identifying the opening request. The optional
legacy `through` field is not accepted. Whether the target is open, closed,
unseen, or the wrong kind of message requires the semantic rules in
[stop](../asking-contract.md#44-stop). The schema defines no generic target
category or extension cancellation vocabulary. Ignorable metadata cannot
change the required meaning of a stop.

`approval.in_response_to` is optional: an approval may start an independent
exchange without an earlier message or work turn. When supplied, it is a
correlation reference, not a turn-membership declaration. `closed` may be sent
by either conversation role, but only for a question or approval that sender
originated. Its reason must agree with that request's kind and terminal state.
Authenticated ownership, decision acceptance, and closure-before-request
markers are semantic rules in [approval exchanges](../approvals.md); the
payload schema alone cannot establish them.

The [notification receiving rules](../notifications.md) require the actor's
reports to resolve to eligible locally issued inputs in the correct context.
They distinguish a missing `taken` from a missing opening request, and a valid
late report from a contradictory disposition. `progress.replaces` can name an
unseen predecessor without establishing its existence or reserving its ID.
Target kind, turn, cycles and terminal facts require semantic checks; the
schema cannot establish them from one payload. Payload shape alone does not
establish a valid notification relationship.

Refusal of a predecessor alone does not invalidate a new progress update or
authenticate an absent relationship. A required bare reference with multiple
permitted targets is `malformed`, even though both messages can have distinct
originator-scoped identities. These semantic checks and the rules for confirmed
acceptance/sending-slot release cannot be determined from payload shape alone.

## Core timestamp validation

Core `sent_at` and question/approval `deadline` follow the
[timestamp profile](../timestamps.md): UTC `Z`, years 0001–9999, seconds 00–59,
and an optional fraction of one to six digits. The `time` pattern enforces the
entire string, component ranges and microsecond limit. Actual Gregorian
month/day/leap-year validation is additionally required at structural checking;
for example, `2030-02-30T12:00:00Z` passes the pattern but is `malformed`.
This required check precedes supported-content checks, semantic admission,
acknowledgement and time arithmetic, while earlier guards, authentication and
version checks retain precedence. Invalid controls still receive no core reply.

Preserve all admitted fractional values in comparison and preserve original
signed strings. Do not round or truncate excessive precision, use native parser
normalization as validation, or add application-wide `format` assertion to obtain
this rule. The requirement applies to core timestamp fields; the embedded-schema
`format` policy below is unchanged. [Timestamp vectors](../vectors/timestamps.json)
distinguish schema acceptance, full calendar validation, exact comparisons and
receiving outcomes. The earlier nine-digit draft is deliberately narrowed;
year zero and explicit leap-second labels are not admitted.

## Reserved diagnostics and controls

`unverified` is not a principal. Only a verification-diagnostic `refusal` may use
the exact recipient object `{"principal":"unverified"}`, without a conversation.
Its payload has exactly `version`, `id`, `kind`, `sent_at`, `to`, `reason`, and
optionally `in_response_to`. The schema excludes `detail`, `metadata`, `evidence`,
`on_behalf_of`, `caused_by` and every other additional payload field, even when
that field is otherwise allowed on an ordinary refusal.

The reserved form permits only `malformed`, `algorithm-key-mismatch`,
`certificate-invalid`, `certificate-expired`, `key-not-certified`, `bad-signature`,
`not-canonical`, and `not-addressed-to-me`. These describe verification-stage
failure; `malformed` must not relabel a semantic refusal as a diagnostic.
`ack`, `describe`, `description` and other kinds cannot use this reserved
recipient. Ordinary principal/conversation refusals retain their existing shapes.

This structural restriction does not authenticate a diagnostic or associate it
with a submission. The [diagnostic and control rules](../diagnostics.md)
require the original authorized route, expected authenticated peer and applicable
scope. A submission effect also requires unique retained local attempt association.
Missing, unknown or ambiguous correlation cannot select the current sending slot.
A diagnostic reports a failed frame, not non-execution of the original signed
message or earlier copies. Ending attempts and authorized slot release remain
distinct. No control receives a core reply, including a structurally invalid one;
failure classification alone does not mean a refusal is sent in response.

Eligible exact retained controls keep their earlier handling before first-seen
authentication. Retirement and audience guards still precede retained-state
feedback. Payload validation alone cannot establish those conditions or runtime
control-response termination. Timestamp failures follow the same no-response
rules for controls; they cannot create a diagnostic response chain.

## Embedded operation schemas

This section defines the core interpretation of operation `input` and `output`.
It applies to producers and receivers of descriptions and to validation under a
selected operation contract. An outer payload-schema pass does not establish
these semantic requirements.

- **Dialect:** both fields contain an object-form
  [JSON Schema draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core).
  The root remains an object; boolean schemas are permitted at nested schema
  positions. An absent `$schema` means the fixed 2020-12 dialect. Every explicit
  `$schema` at a schema location must equal
  `https://json-schema.org/draft/2020-12/schema`. A different dialect is not a
  core operation schema, even if a local validator supports it.
- **Schema validity:** each embedded schema must satisfy the draft 2020-12
  meta-schema and this profile. Apply schema rules at schema locations, not to
  arbitrary instance data in `const`, `enum`, `default` or `examples`. Producers
  must not advertise invalid schemas; receivers refuse descriptions with invalid
  embedded schemas as `malformed`. The outer payload schema checks the root form
  and explicit root dialect only; it does not replace this validation.
- **References:** treat each `input` or `output` as a standalone schema document.
  Its references, including `$ref` and `$dynamicRef`, must resolve unambiguously
  to schema locations within that document under the 2020-12 rules. `$defs`,
  anchors and nested schema resources are allowed. No reference may depend on
  the containing description, the other field, another operation or an external
  resource. Missing or ambiguous targets make the declaration `malformed`.
  Never fetch schemas from the network while processing a description or request.
  A schema's `$id` names a resource; it does not authorize retrieval.
- **Assertion meaning:** use the standard 2020-12 vocabularies, including
  format-annotation. `format` does not add a core assertion. Content annotations
  do not require decoding or validating embedded content. Unknown keywords may
  annotate a schema but cannot impose required core validation behavior. An
  embedded `$vocabulary` does not replace the fixed dialect or activate custom
  assertions. Required application meaning must be stated in the application
  contract; a separately applicable agreement may impose additional application
  checks without redefining what matches this core schema profile.
- **Instance preservation:** validation tests the supplied value. It must not
  coerce types, insert `default` values, remove properties, or discard falsey
  values to obtain a match. The `default` keyword is an annotation. Core does
  not require proof that a schema has any satisfying instance; for example,
  `{"not": {}}` is valid and rejects every value.

When an opening operation declares `input`, `say.data` must be present and its
value must match that schema before opening the turn. Even an empty schema `{}`
requires the field to be present. Without `input`, opening `data` remains optional
and advisory under [operations](../asking-contract.md#61-operations). A successful
result under a selected `output` likewise requires present, matching `result.data`;
other terminal statuses are not constrained by that success schema. Contributions
and answers use the retained contribution rules, not the opening schema by default.
These requirements depend on the selected contract and cannot be inferred from
one `say` or `result` payload alone.

Within one `description.operations` array, operation names must be unique by exact
string equality, whether the repeated declarations are identical or conflicting.
Refuse duplicates as `malformed`. This is a semantic constraint beyond the outer
schema; ordinary `uniqueItems` would not detect two different objects with the
same name. Names in different descriptions need not be globally unique, stable
across deployments or governed by a core version convention.

Validator selection, compilation, caching and resource management belong to
implementations. Those choices must preserve the above observable interpretation;
library defaults are not an alternate protocol dialect. These requirements do not
make discovery evidence of future availability, authority or contract selection.

## Opaque application metadata

Application metadata is opaque. No model usage, construction, knowledge, query,
storage, checkpoint, or recovery types are required by this schema.
