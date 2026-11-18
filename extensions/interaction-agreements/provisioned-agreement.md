# Provisioned interaction agreement profile

**Identity: `keel.provisioned-agreement.v1`. Status: normative optional deployment
profile for unreleased core/1.** It adds an application agreement to a conversation
established under [`keel.provisioned-context.v1`](../../core/profiles/provisioned-context.md).
Both profiles must be explicitly selected for this scope. Core conformance does
not require this profile. It adds no core field, message kind, refusal reason,
setup wire format or discovery service; the WebSocket subprotocol stays
`keel.core.v1`.

This profile is for controlled deployments whose endpoints independently authorize
a shared provisioning facility. It supports prepared mechanical requests, cached
model tools and unnamed human interactions whose intended meaning must survive
the interval between preparation and admission. Arbitrary remote peers need a
separately specified establishment arrangement; supporting core/1 alone is
insufficient.

## Agreement and responsibilities

An **agreement** is an application owner's promise about the interpretation and
permitted behavior of an offering. It may cover several operations and turns,
including unnamed interaction. Its identity is scoped to its governing authority;
a bare string, model tool alias, actor principal or conversation key does not
establish agreement identity or meaning.

| Responsibility | Required promise |
|---|---|
| Application contract owner | Defines the offering's meaning, constraints and what changes remain compatible with that promise |
| Network/deployment owner | Selects this profile, authorized participants, offerings and support policy |
| Requester adapter | Retains the intended agreement on which preparation relied and verifies that setup establishes that agreement |
| Actor host | Admits behavior consistent with the established agreement and each accepted turn's selected contract |
| Trusted provisioning facility | Establishes the same applicable agreement and scope at both independently authorizing endpoints |

These are logical responsibilities, not required processes, services or repositories.
The authority governing an agreement is distinct from a certificate issuer's
authority over principal names and from permission to execute an operation.

The agreement must define the named-operation contracts it promises and the
meaning of unnamed interaction within the offering. It must cover contributions,
successful outputs, permitted effects and any approval dependencies on which
participants rely. It may refer to separately defined application contracts.
Core question, approval, stop and delivery meanings remain unchanged. An agreement
can promise that ordinary unnamed chat is explanation-only, for example, without
making every core conversation explanation-only.

The owner defines compatibility against this promise. Different code, model,
prompt, deployment or declaration presentation may satisfy the same agreement.
Matching schemas alone do not prove semantic compatibility. This profile requires
neither deterministic outputs nor universal version ordering, a registry, semantic
version syntax or declaration hashing.

## Retain intent before setup

Before requesting setup, the requester must retain the agreement it actually
relied on when preparing the interaction. For a cached model tool, the adapter
must preserve the association from the offered tool to its actor, operation and
intended agreement through the model's selection. For a mechanical driver this
may come from authorized configuration; for a human interface it may be the
declared interaction mode. An alias must select an unambiguous target.

An ordinary cached core description does not by itself supply this stronger
promise. Its relationship to an agreement must come from an independently trusted
application/deployment arrangement. The requester cannot acquire a missing
preparation-time guarantee by labeling whatever the host currently offers as the
intended agreement after preparation.

The requester may deliberately prepare anew against a different offering. That
is a new application choice, not automatic reinterpretation of an existing draft,
tool decision or signed request. Reconsidering an offering also grants no authority
to repeat earlier work with an unresolved outcome.

## Trusted setup inputs

Alongside every input required by the provisioned-context profile, install the
following association at both endpoints:

| Input | Required value or association |
|---|---|
| Agreement profile | `keel.provisioned-agreement.v1`, explicitly selected |
| Governing authority | An authority each endpoint accepts for the agreement's identity and meaning |
| Intended agreement | The requester's retained selection, resolved to the same applicable application promise at both endpoints |
| Offering coverage | The named and unnamed interaction contracts promised in this scope, including any applicable conditions or limits |
| Scope association | The exact actor/requester roles, governed namespace, fresh C, actual authenticated connection and both local context/guard instances from provisioned setup |
| Enforceability | The host's commitment that behavior admitted under this association satisfies that agreement and its accepted turn contracts |
| Lifetime | This association lasts only while its paired context guard and agreement applicability remain valid; no in-place substitution or resumption |

This is a trusted configuration contract, not a JSON object accepted from an
untrusted frame. Implementations may exchange references or complete definitions,
but must establish their authority, resolution and applicability. An arbitrary
caller label or two equal labels with different meanings is insufficient. A
mutable lookup must not silently replace the promise retained for an active
association.

Setup must establish the requester's intended agreement. A compatible implementation
may honor that agreement even if its current advertisement is different. If the
host cannot honor it, setup cannot establish this association. Selecting the host's
current agreement without the requester's deliberate new choice is prohibited.

## Establishment and activation

1. Validate the intended agreement and each endpoint's authority to use the
   provisioning facility. Resolve and retain the agreed promise at both endpoints.
   A missing, unsupported, ambiguous or inconsistent input leaves setup unestablished.
2. Allocate and install the fresh C, actual connection association, empty contexts
   and receive guards exactly as the provisioned-context profile requires. Bind
   the agreement to those particular instances; it cannot be attached later to
   an already active conversation as though it governed earlier messages.
3. Each endpoint reports readiness only when both its continuity requirements
   and agreement association are ready. The actor host must be ready to enforce
   the promised behavior at admission. Neither local readiness nor acceptance by
   only one endpoint enables traffic.
4. Only after both endpoints are ready may the facility activate the paired
   guards and agreement associations. Activate both before enabling either sender.
   This is ordered activation, not a requirement for simultaneous updates or a
   distributed transaction. All failure and idempotent-observation rules from
   the provisioned-context profile apply.

Before activation, failed setup admits no conversation work and returns no core
contract-mismatch refusal. The setup arrangement must report locally that the
association was not established; it may disclose authorized diagnostics through
its own trusted control path. Once traffic has been enabled, later loss is scope
retirement and may leave work uncertain. It must not be presented as evidence
that no earlier request was admitted.

The requester signs ordinary conversation messages only after learning the
authorized C and established association. Signing C ties traffic to that
association through trusted setup; the bytes of C alone carry no application
meaning. Non-conversation `describe`/`description` retain their separate core
scope and cannot establish or replace this association.

## Admission and retained obligations

At each endpoint, the agreement association and its paired continuity guard
must remain applicable through semantic admission. Capture them with queued
frames; order admission with retirement so a frame cannot enter a replacement
offering through a later lookup. The actor host must choose behavior consistent
with the established agreement when it admits a fresh request. No architecture
for dispatch, storage, model execution or deployment synchronization is mandated.

Core admission and delivery rules still apply. A named operation unavailable in
this offering receives the ordinary `unsupported` refusal. Invalid declared input
receives `malformed`; capacity and authorization failures retain their existing
meanings. This profile creates no generic precondition-failure refusal and does
not repurpose one. The agreement supplies no implicit availability, completion,
permission or exactly-once effect guarantee.

The accepted turn retains its selected response contract under the core turn contract. The broader
agreement must not be replaced during that turn or between turns under the same
association. The receiver may make implementation changes compatible with the
agreement and the retained turn contract. It must not substitute incompatible
meaning for delayed contributions, answers or new openings.

Within an active authorized scope, eligible exact retained copies use the core
retained-copy disposition before any fresh-operation availability or input/precondition
checks. A retired operation does not undo prior acceptance, and a terminal refusal
stays terminal. An agreement reference supplies no authentication exception and
no right to retrieve sensitive cached replies. Current audience and scope checks
still precede retained-history disclosure.

## Ending the association

Ending an application promise does not inherently retire a continuity guard. **This
profile explicitly couples them:** before ending agreement applicability,
discarding its required association, or admitting incompatible replacement
behavior, invalidate the paired local continuity guard and agreement admission
together. Close that actual connection and disable outgoing conversation traffic
under the provisioned-context retirement rules. Conversely, continuity retirement
ends this agreement's applicability to new admissions on that local scope.

Loss of the required agreement state or its enforcement basis requires the same
retirement. Keeping the socket or the core context alive is insufficient. A live
continuity guard alone cannot preserve an ended agreement. An implementation must not
claim a scope failure merely because a per-request agreement check disliked a
message while leaving the scope active.

For traffic arriving after this actual retirement, the provisioned-context binding
outcome applies: close the original connection with generic WebSocket code 1008
if it remains open, otherwise discard under the captured retired guard. Send no
core disposition or identifying close-reason details, reserve no presented ID,
and reveal no retained-history distinction. Never close or mutate a replacement
connection because an old queued frame arrived.

The peer may not immediately observe retirement and may still admit an in-flight
message into its own valid old scope. Any such admission remains governed by the
old agreement. This profile promises neither instantaneous remote detection nor
detection of arbitrary silent corruption. Trusted endpoints must enforce the
defined loss, replacement and retirement boundary.

An incompatible offering requires a new deliberate agreement selection, fresh C
and fresh actual connection, with the entire establishment procedure repeated.
An announcement cannot change the meaning of old signed frames. Neither the
old C nor its signed messages may be rebound to the replacement. There is no
resume or restoration mode under this profile identity.

Retirement does not undo accepted work, revise an old disposition, manufacture a
terminal result, cancel an application job or withdraw an approval. Preserve
facts and unresolved outcomes wherever records remain. The retired scope provides
no retained-copy feedback route; inspecting retained records needs another authorized
contract. A new agreement, C or message ID does not authorize repeating uncertain
work. Application reconciliation or explicitly authorized new work remains
separate.

Retirement also does not release previously admitted work from the meaning or
constraints under which it was accepted. Whether that work continues or is
cancelled follows its application contract; loss of the reply path is not
permission to complete it under an incompatible replacement agreement.

## Conformance and limits

The separate [agreement vectors](vectors.json) cover intent preservation, bilateral
setup, named and unnamed interactions, lifetime enforcement, retained copies and
retirement races. Implementations claiming this profile must also satisfy the
core and provisioned-context requirements. Test the actual provisioner, requester
adapters, hosting dispatch and queue paths; these artifacts are not runtime
conformance evidence.

No additional payload schema is necessary because this profile introduces no wire
representation. A deployment must supply the trusted setup implementation and
application definitions before using it. Conditional per-invocation wire support
and exact declaration-evidence formats remain [separate proposals](README.md).
