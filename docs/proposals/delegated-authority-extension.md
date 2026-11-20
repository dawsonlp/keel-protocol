# Proposal: delegated authority extension

**Status:** design proposal, not an adopted extension, wire format or conformance
target. **Date:** 18 November 2026. **Baseline:** unreleased core/1 at
`5b24163897c8b13f0d570b3c4c2f21c51623c708`.

The [provisioned direct grant profile](../../extensions/delegated-authority/provisioned-direct-grant.md)
now defines the selected initial scope. This proposal records the original core
baseline and the broader design direction, including recursive authority.

This proposal develops the agreed direction of an optional Keel extension for
authenticated representation and delegated authority. Multi-hop delegation and
recursive permissioning are part of its vision from the outset; their wire
profiles and implementation are not yet selected. Concrete recommendations below
remain subject to agreement before normative specification or implementation.

The motivating proposal was written in the sibling `keel-typescript` checkout at
`docs/proposals/authenticated-representation-and-delegated-authority.md` for a
human UI actor and a proxy whose lifetime is independent of the UI. This document
restates the requirement independently and revises its proposed placement in
mandatory core. Reading that checkout is not required to understand this proposal.

## 1. Vision and intended outcome

Enable independently implemented actors to exercise explicitly bounded authority
for other principals, and, when expressly permitted, delegate narrower authority
through further actors. Every recipient should be able to establish the actual
signer, represented principal, applicable authority and limits without assuming
one network topology, identity provider, model, coordinator or permission service.

An authority path may contain several grants, while work and approvals follow
their own collaborations. These relationships must remain distinguishable.
Delegation must preserve accountable identities and constrain authority at every
step; it must not transfer protocol ownership, turn permission into execution, or
claim that a human personally reviewed an action.

The first interoperability target can be direct grants. Its concepts and component
boundaries must also accommodate bounded recursive delegation without changing
the meaning of an existing grant, weakening core, or replacing application actors.
Ease of later implementation means reusing these meanings and verification
boundaries, not accepting unspecified chain fields now.

Success requires independent endpoints to agree on allowed and refused requests
under the same selected profile, permission contract and trust configuration.
It does not mean identical local policies or universal recognition of issuers.

## 2. Placement and responsibility boundary

The extension belongs in `keel-protocol` because authority interpretation interacts
with signed requests, admission, contributions, decisions, duplicates and protected
responses. Its requirements apply only to participants selecting its contract.
A direct-acting core endpoint needs no delegation verifier or authority service.

| Owner | Responsibility |
|---|---|
| Core | Authenticated principal, assertion-only `on_behalf_of`, receiver authorization, signed identity, lifecycle ownership, delivery and continuity |
| Delegated-authority extension | Authoritative representation, proof-to-request association, required receiver checks, authority associations within exchanges, failures and compatibility |
| Concrete proof profile | Artifact representation, algorithms, issuer/holder binding, direct or derived proof structure, validity/status model and bounded validation |
| Application/resource contract | Permission meaning, resources, request/effect mapping, acceptable narrowing, grant-use accounting and effect/cancellation promises |
| Deployment and authority services | Enrollment, login/consent, trust roots, issuance policy, key custody and any status or issuance service API |
| Endpoint implementation | Enforce selected contracts through explicit interfaces; retain required live facts; control verification work, clocks and external effects |
| Network/application | Composition, control permissions, approval escalation, human participation, history, recovery and distribution of work |

The artifact definition should be a separate part of the extension specification
here, with the Keel integration stated separately. This does not require another
repository, package or process. A future non-Keel consumer may justify extracting
a general artifact specification; no such consumer is established by this use case.

Issuance and status services need their own contracts if standardized. They may
use ordinary Keel operations or another explicitly selected protocol. This
extension does not make either service, a registry, a database or a central
authority an implicit dependency of core participation.

## 3. Current contract and compatibility constraints

The current [security definition](../../core/security.md),
[credential profile](../../core/security-profile.md),
[asking contract](../../core/asking-contract.md), and
[extension rules](../../extensions/README.md) remain authoritative:

- Authentication identifies the certified signer. `on_behalf_of` neither
  authenticates its named principal nor confers that principal's permissions.
- `evidence` contains unchanged signed core messages, not arbitrary grant tokens.
- Unknown core payload fields and extra credential members are invalid. Metadata
  cannot carry requirements whose omission changes the requested action.
- A grant does not establish a conversation, restore retired state, authorize an
  arbitrary reply route, or transfer question/approval closure ownership.
- No scoped-grant extension or extension-negotiation wire protocol is selected.

Old signed assertions must never be retrospectively upgraded into verified
delegations. Supporting core/1 does not establish support for this proposal.
The revision, signed contract, binding selection and any provisioned association
must identify the behavior actually enforced. No proposed field is valid merely
because it appears in this document.

## 4. Conceptual model

The following are meanings and relationships, not JSON member names or class APIs.

| Concept | Meaning and constraints |
|---|---|
| Signer | Principal authenticated for the current message; remains accountable for it |
| Represented principal | Principal for whom authority is invoked; may be a human, organization or actor under governed naming |
| Grant holder | Principal authorized to exercise or further delegate specified authority; distinct from its signing key |
| Authority root | Receiver-recognized basis allowing an issuer to confer particular permissions for particular subjects/resources; not implied by certificate-issuance trust |
| Grant issuer | Principal signing a grant, authorized either by an accepted root basis or an explicitly validated parent delegation |
| Grant | Immutable authorization with identity, subject, holder, use scope, delegation scope and validity/status conditions |
| Grant identity | Issuer-scoped identity within the independently established governed namespace; exact signed artifact identity is retained separately |
| Use scope | Actions, resources, receiving audiences and conditions the holder may exercise itself |
| Delegation scope | Authority the holder may confer, permitted delegates and destinations, and limits on further derivation; no issuance right is inferred from use scope |
| Permission contract | Resource-owned definition of an action and its restrictions, applicability and permitted narrowing |
| Parent relationship | Exact authority dependency from one derived grant to its authorizing grant; not a causal message reference |
| Authority basis | Explicitly selected direct grant or supported derivation proof, with trusted root and applicable permission/status contracts |
| Authority association | Retained binding of a protected exchange to its represented subject and relevant authorization constraints; not a permanent cached permission |
| Authorization decision | Receiver's decision for this action using the validated authority basis and current applicable policy |
| Status authority | Authority entitled to establish grant status, subject to a selected freshness and failure contract |
| Request-specific authorization | Evidence permitting a particular instruction/effect; distinct from reusable delegated authority |

One principal can hold many grants and represent different subjects. One grant
can have several derived children when its delegation scope permits that.
One work request can cause several exchanges without creating any new grant.
An independently rooted grant does not become a child because it serves related
work. For the initial profile, each represented request selects one direct grant.
For the proposed later chain profile, it selects one leaf and one explicit path
to a root. Combining independent paths or jointly required grants is a separate
composition problem, not implicit union of privileges.

### Attribution, representation and authority

Three cases must be distinguishable:

1. A acts under A's own authority, without claiming a represented subject.
2. A attributes work to H using `on_behalf_of`, but uses A's own permissions.
3. A explicitly invokes verified delegated authority for H under this extension.

The third case requires an unambiguous signed or established-scope selection.
Failure of its required proof cannot silently fall back to the second or first.
The current weaker meaning of `on_behalf_of` remains valid outside that selection.

Being H does not by itself give H authority to grant access to W's resources.
W must recognize the root's authority for the stated subject, permissions and
resources. Naming trust, subject consent and resource authority are distinct.

## 5. Concrete arrangements and trust boundaries

### Human UI and independently living proxy

H authenticates through UI actor U. U signs a control request to proxy P for H.
P signs a separate work request to worker W for H. Each pair establishes its own
authorized conversation; W replies as W.

This can use two independent grants: U may control specified P operations for H,
and P may request specified W operations for H. P checks U's instruction before
using its own outward authority. A U grant for reading history cannot authorize
P to publish merely because P possesses a publication grant.

W's verification of P's grant proves neither U's incoming authority nor H's
approval of that exact request. This arrangement trusts P to enforce its control
boundary. If W needs independent evidence of the originating instruction, a
request-specific authorization contract must supply and bind it. A complete
delegation chain also does not, by itself, prove human intent for each invocation.

P's single-human restriction applies to control and protected access. It does not
require W's legitimate results or closures to claim that W represents H. UI
disconnection, sign-out and proxy revocation have separately specified effects;
an independent P grant is not automatically revoked by loss of U's connection.

### Recursive delegation across cooperating actors

An authority recognized by W grants A permission to review a document collection
for organization O and to delegate specified review authority. A grants B a
subset for collection X, with permission to delegate a further subset. B grants
C read-only review of document x at W, with no further delegation.

C signs its request to W as C, representing O. W checks the selected path and
its restrictions. A and B need not be online for each request if the explicitly
selected verification/status model permits offline use. They need not be central
coordinators, and the work's conversation path need not match the grant path.

The same model must accommodate an actor authorized only to allocate permissions:
A can have authority to grant B access without having permission to read the
resource itself. Therefore child authority is bounded by the parent's explicit
**delegation scope**, not necessarily its own use scope.

### Further permission during work

C discovers that review would require a write. Its read grant supplies no write
authority. C may ask an appropriate authority through an independent approval
exchange. That authority may itself need another decision before issuing or
authorizing a grant. Each approval retains its own originator, deadline, accepted
decision and closure; no recursive approval lifecycle is inferred from correlation.

If the required authority is obtained, its exact scope and request association
must be established before the write. The application decides whether to amend
existing work or make a fresh request under its operation contract. A newly
authorized write does not retroactively authorize an earlier effect.

The extension defines how resulting authority is proved and used. Which authority
to ask, human escalation, recursion budgets, deadlock avoidance, and cancellation
of dependent approval requests belong to the collaborating application's contracts.

## 6. Requirements for the extension

These are proposed extension requirements, not additions to current core.
Derivation requirements apply when claiming a recursive profile. A direct-only
profile must reject unsupported derived authority; it need not validate chains.

| ID | Required outcome | Observable counterexample |
|---|---|---|
| DA01 | Preserve signer, represented subject and protocol owner separately | H's name cannot let U close an approval owned by P |
| DA02 | Explicitly select authoritative representation; reject failed proof without fallback | Invalid H authority cannot execute under P's broader independent privileges |
| DA03 | Bind grant use to the certified actor/key, recipient and exact request selection | A copied artifact or substituted audience cannot authorize another actor's request |
| DA04 | Verify root and derived issuance authority separately from naming trust | A trusted identity certifier cannot invent resource permissions |
| DA05 | Apply explicit action/resource meaning and receiver policy | Renaming an operation or changing its meaning cannot expand a read grant into write |
| DA06 | Retain subject and constraints for protected exchange actions | A grant for Bob cannot silently amend or stop Alice's work |
| DA07 | Preserve scope, duplicate and response-audience rules | Revocation or reconnection cannot cause a duplicate effect or disclose cached content to a new carrier |
| DA08 | Define validity, status freshness and actual enforcement boundaries | Admission before expiry does not imply unlimited permission for later effects |
| DA09 | Distinguish work routing, grant derivation and approval dependencies | A causal message trail cannot substitute for a validated authority path |
| DA10 | Make recursive issuance explicit and monotonically restricted | A child cannot exceed its parent's delegable authority or reset remaining depth |
| DA11 | Preserve ancestor restrictions and status dependencies | Omitting an ancestor or choosing stale status cannot make a derived grant usable |
| DA12 | Bound proof size, depth and verification work | A cycle, ambiguous path or token-supplied URL cannot induce unbounded recursion or lookup |
| DA13 | Keep aggregate accounting with an explicit owner | Two children cannot each spend a shared allowance merely because their individual limits fit it |
| DA14 | Preserve direct participation and replaceable mechanisms | A deterministic direct actor needs no human login, issuer service or delegation parser |
| DA15 | Preserve evidence limits and confidentiality | Verified authority proves neither personal human review nor delivery; proofs are not automatically public |

## 7. Multi-hop and recursive permissioning

Multi-hop work routing, recursive delegation of authority, and recursively seeking
approval are all within the vision. They are separate relationships. The extension
owns the second and the authority consequences of the others; it does not select
a collaboration workflow.

### Proposed derivation invariants

A later chain profile should enforce these invariants at each parent-child edge:

1. Authenticate the child issuer and establish that it is the parent holder
   entitled to issue that child, including the applicable key binding. Validate
   the root's separately configured authority; do not trust a self-declared root.
2. Bind the child to the exact parent artifact and its contract identity. A grant
   ID alone must not allow mutable replacement or substitution under that ID.
3. Preserve the represented subject. Changing subject requires separately
   established authority, not an implicit step in the same derivation.
4. Check child use scope against the parent's delegable actions, resources,
   audiences, permitted holders and conditions. Check any child delegation scope
   against the parent's permitted onward delegation, including remaining depth.
5. Preserve inherited restrictions through every later derivation. A child cannot
   remove a mandatory approval condition, relax a status rule, extend an inherited
   validity bound, or turn nondelegable authority into delegable authority.
6. Verify every required ancestor and its status under the selected contract at
   the relevant use boundary. Missing or unestablished dependencies supply no
   authority. A receiver cannot simply check the leaf signature.
7. Apply current receiver/resource policy and any separately required subject
   entitlement. A valid path is an authorization input, not a command to permit.

Receiving audiences for use and permitted destinations of future grants are
distinct. For example, authority to control P does not imply authority to call W,
but an explicit delegation scope may permit issuing a grant usable at W even
when the parent has no direct-use audience W. This distinction is necessary for
permission brokers and prevents an incorrect audience-subset rule from making
recursive delegation unusable.

Permission narrowing must be decidable under the identified permission contract.
An initial chain profile should require a compatible contract throughout the path;
unknown conditions or unsupported narrowing are refused. Arbitrary text, JSON
Schema inclusion, and operation-name similarity are not general authority proofs.
Cross-contract translations would need explicit authorized semantics.

### Bounds, branches and shared limits

The proposed first recursive profile uses a single-parent path, not arbitrary
multi-parent proof graphs. Several children of one grant form branches, but an
invocation selects a complete supported path. It cannot splice permissions from
separate branches. Reject cycles and repeated grant identities on that path;
reappearance of a principal alone is not proof of an authority cycle. Enforce
explicit depth, artifact-count, byte and verification-work bounds before expensive
processing. Exceeding a bound fails validation; truncating a path does not make
the remaining suffix an independently trusted root.

Monotone narrowing is not sufficient for shared quotas. If a parent authorizes
ten total releases, two children each limited to ten do not preserve that total.
Global use limits, single-use grants and allocation among descendants require
an accountable enforcement/reservation owner with defined concurrency and failure
semantics. The initial profile should not claim these guarantees. A chain profile
must reject unsupported shared-limit semantics rather than treat them as ordinary
per-request predicates or assume a mandatory distributed ledger.

An ancestor's revocation makes dependent authority unusable when that fact must
be recognized under the selected freshness contract. Independently rooted grants
remain independent. A new root grant is a new authorization decision; it must not
be presented as preserving the restrictions or revocation lineage of an old path.

### Compatibility from the first profile

The direct-grant profile represents a root-issued grant with no onward issuance
right. It is a bounded case of this model, not a declaration that all grants must
forever have independently trusted issuers. The later chain profile must accept
only explicitly supported proof forms and preserve all inherited restrictions.
An earlier receiver rejects unsupported chain use; it never ignores ancestors.

Keep request authorization dependent on an explicit validated authority basis,
not on a hard-coded rule that every leaf issuer appears in a root trust list.
Keep key authentication, authority-path validation, permission applicability and
status evaluation separable. These are conceptual boundaries; no plugin API,
package layout or general proof engine is selected by this proposal.

## 8. Initial profile and remaining mechanism choices

Recommend the first portable profile support one represented principal, one
selected direct grant, a holder bound to both actor principal and signing key,
explicit receiving audiences, understood permission parameters and no onward
issuance. Do not invent compound permissions to conceal a need for unsupported
grant composition; an application can issue an explicitly adequate grant or
refuse that request.

Use a separately typed signed artifact. Its semantic content includes contract
identity, issuer-scoped grant ID, issuer, subject, holder/key, use scope, absence
of delegation rights, validity and selected status rules. Reuse established
cryptographic mechanisms where appropriate, with disjoint credential, message
and grant validation rules. This document selects neither claim names nor JOSE
headers. Later profiles need exact parent binding and delegation scope; do not
add ignored placeholders for those semantics to the initial profile.

### Grant meaning and current entitlements

The permission contract must distinguish authority conferred for a bounded period
from authority to exercise rights the subject must still hold at use time. The
latter requires an authoritative basis for the subject's current rights with
defined freshness and unavailable-state behavior. The former still remains subject
to current receiver policy and its selected revocation rules. Neither implies
the union of signer and subject privileges. The initial normative profile must
select a supported model or explicitly identify the required permission-contract
model before accepting a grant; receivers cannot silently choose different ones.

### Proof-to-request binding

| Candidate | Strength | Required boundary |
|---|---|---|
| Provisioned authority association | Can preserve the existing core envelope in controlled deployments | Both peers establish the intended subject, selected proof and extension applicability before traffic; signed conversation identity binds requests to that immutable association |
| Explicit extended message contract | Supports portable per-request proof selection | A distinct compatible signed contract/schema and support selection must bind the proof, subject, recipient and request together |

Favor a dedicated authority container with an embedded bounded proof for the
portable target, avoiding a mandatory lookup service. This is a design preference,
not permission to add a field to core/1. Compare its compatibility cost with the
provisioned alternative before selecting the initial integration profile.

A provisioned variant must specify association replacement, loss and retirement;
it cannot attach new authority retrospectively to old signed traffic. Replacing
an association must not silently continue old turns in a fresh conversation.
Per-request grants also require explicit renewal/replacement rules for exchanges.
Proof encoding and scope establishment are separate choices: portable artifacts
can be installed during trusted provisioning as well as carried in requests.

No initial profile should repurpose `evidence`, identity certificates or ignorable
metadata. Support must be established before relying on required semantics. If an
integration needs a core compatibility change, propose it explicitly with its
schema and vectors; optional delegation does not imply optional core correctness.

## 9. Association with work and approvals

At admission of a represented opening, retain its subject, selected authority
basis, permission meaning and action/resource constraints with the turn. A later
contribution, answer or stop must be authorized for that identified exchange.
A valid grant for another subject cannot take it over. Authority renewal for the
same subject is not automatically valid either: the replacement must explicitly
cover the requested action and preserve the admitted work's constraints.

For the initial profile, recommend refusing subject changes within a turn. A new
represented subject uses a new independently authorized exchange. Whether the
profile fixes one subject for an entire conversation or allows separate turns
for separate subjects remains an explicit design choice. The latter requires
careful isolation of retained state and disclosure, not just per-message checking.

Core permits a targeted stop before its opening arrives. Before accepting such
a stop under represented authority, the receiver must independently establish
that authority for the unseen target, for example through a fixed-subject scope
and an applicable stop permission. If it cannot, it must refuse under the
selected authorization rules rather than install a suppression marker on the
strength of an arbitrary subject claim. The normative design must reconcile this
with core stop precedence and test it in both arrival orders. Missing work cannot
become a way for Bob's authority to suppress a later opening for Alice.

Approval authority is associated with its own exact request. A work grant does
not automatically authorize deciding, issuing grants, reading history or closing
another principal's exchange. Correlation with a turn does not inherit authority
or lifecycle. A decision accepted under an application's issuance contract may
authorize creating a grant; `closed: decided` alone is never a portable grant.

| Message purpose | Required authority interpretation |
|---|---|
| New represented work or proxy control | Current basis for this signer, subject, receiver and actual operation |
| Contribution, answer or targeted stop | Authority for the named exchange and action, preserving its subject and constraints |
| Represented approval decision | Permission to decide this exact request, plus ordinary originator acceptance and binding checks |
| Result, progress or owner closure | Authenticated protocol role and ownership; applicable disclosure policy, without requiring the worker to represent the human |
| Acknowledgement, refusal or diagnostic | Existing control and audience rules; no recursive responses to invalid controls |
| Historical/context retrieval | Fresh read/disclosure authority under that service's contract |

Revocation does not change an established terminal disposition or create a new
terminal result. It also does not authorize abandonment of core obligations.
The selected contract must define how required completion/control reporting and
protected-content restrictions coexist, including when delivery must be held and
uncertainty exposed. It cannot solve this by requiring a fresh human grant on
every response or by disclosing protected content unconditionally.

## 10. Validity, status and effects

Human login, actor credentials, issuer verification, grants, cached status,
approval deadlines, conversation scopes and application jobs have distinct
lifetimes. The initial profile is incomplete until these interactions have
specified observable outcomes.

| Status model | Honest guarantee and cost |
|---|---|
| Validity-bound offline use | A grant may be used until expiry unless disqualifying information is already known; no immediate remote-revocation guarantee |
| Authoritative status with bounded age | Every required dependency needs status within the declared age; unavailable or stale status prevents new protected action |

Recommend considering bounded offline validity first only if the motivating
deployment accepts the resulting revocation delay. Otherwise a concrete status
contract is necessary. These are explicitly selected alternatives, never silent
fallback modes. Grant duration, clock tolerance, freshness, status authenticity
and failure behavior remain open decisions. Cached status cannot promise
instantaneous revocation during a partition.

For derived grants, effective validity and status incorporate every inherited
dependency. A long-lived leaf cannot extend a short-lived parent's authority.
Issuance-time validity alone does not make descendants independent of later
ancestor revocation under the selected model.

Require an admissible issuer authentication basis when first establishing an
artifact; its claimed issuance timestamp alone is insufficient after credential
expiry. A profile must separately specify continued use of retained verification,
issuer-key rotation and compromise. Any portable historical issuance proof would
need its own contract. A receiver that first encounters a chain must establish
each required artifact's basis; another endpoint's unverified assertion that it
checked the chain earlier does not suffice.

Holder key rotation requires a newly bound grant or an explicitly specified
rebinding mechanism. Certificate renewal does not extend grant validity. A retry
preserves its exact signed request and proof bytes; replacing an expired proof
under the same message ID is not an exact retry. A fresh ID does not establish
that repeating an unresolved external effect is safe.

Authorization at admission is not a promise of authority for every later effect.
The application/effect contract must identify the enforcement boundary, how
queued work is treated and what ordering it provides against revocation. A local
authoritative effect owner may order these events; a remote cached observation
does not provide the same guarantee. Revocation neither rolls back past effects
nor automatically stops jobs or recursively cancels downstream work.

## 11. Receiver behavior and failures

The normative design must reconcile exact precedence with current core vectors.
The proposed integration preserves this sequence and separation:

1. Apply bounded framing, independently assured response audience and continuity
   guards. A grant never establishes a missing or retired scope.
2. Apply eligible exact-retained-copy handling under current disclosure policy.
   This recognizes an old disposition, not fresh delegated permission or an effect.
3. Authenticate a new message's actual signer and validate its selected contract
   and structure in the defined order. Unsupported extension behavior is not
   silently interpreted as ordinary core work.
4. Establish its authority selection and the target exchange association. Validate
   the selected proof, issuer/root authority, holder/key, subject, audiences,
   permission applicability, validity and status. A chain profile checks every
   required edge and inherited restriction within its processing bounds.
5. Apply current receiver/resource policy and the request's actual constraints.
   Admit only while the original guard remains valid, ordered with retirement.
   Retain the basis needed to interpret admitted work and later targeted messages.
6. Enforce subsequent effects and disclosure under their explicit contracts.

| Failure | Required direction; exact wire mapping remains to be specified |
|---|---|
| Existing authentication/scope failure | Preserve the earlier core/binding outcome and response restrictions |
| Malformed authority structure | Reject at the selected profile's defined structural step |
| Wrong holder/subject/audience, unauthorized issuer, inadequate permission, expired/revoked authority | No delegated action; ordinarily `not-authorized` where an authenticated core refusal is applicable |
| Missing or stale required status | No new protected action; record authority as unestablished, not falsely revoked |
| Unsupported proof/profile or permission semantics | Reject without fallback; setup and wire classification need explicit compatibility rules |
| Invalid control | Preserve no-core-reply behavior; avoid diagnostic loops |

Do not fetch keys, parents, policies or status from arbitrary token-supplied URLs.
Any resolution uses independently authorized sources, bounded work and explicit
failure rules. Minimize proof disclosure: grants can reveal identity, resource
names and authority relationships. Forwarding content or showing history does
not automatically authorize forwarding its attached proofs. Retained decision
bases need no global audit database or compulsory durable history.

## 12. Conformance evidence and counterexamples

Normative prose, schemas, cryptographic fixtures and receiver traces must be
produced together after the remaining decisions. The following are acceptance
cases to develop, not existing executable vectors or evidence of conformance.

| Area | Required cases |
|---|---|
| Participation | Direct actor without delegation services; assertion-only attribution; explicit represented request; failed proof with no own-authority fallback |
| Trust and identity | Valid but unauthorized issuer; wrong subject namespace; wrong actor/key/audience; reused grant ID with different bytes; key rotation |
| Permission meaning | Read/write and resource separation; changed operation meaning; unsupported permission contract; explicit subject-entitlement dependency |
| Proxy boundary | UI exceeds control permission while proxy holds stronger authority; worker accepts proxy authority without falsely claiming proof of human instruction |
| Exchange association | Bob grant targets Alice turn; stop before opening under wrong or unestablished subject authority; same-subject replacement exceeds original constraints; independent approval authority; late worker reply without human grant |
| Lifecycle and disclosure | Expiry/revocation during queued work; duplicate before/after revocation; protected reply on unauthorized route; retired scope; first-seen expired issuer evidence |
| Status and availability | Fresh/stale/unavailable status; exact time boundaries; no offline fallback from a fresh-status profile; effect/check race |
| Recursive authority | Valid A-to-B-to-C derivation; missing/substituted parent; unauthorized child issuer; subject change; widened resource/audience; removed condition; inherited expiry/revocation |
| Delegation semantics | Issuance-only authority; nondelegable leaf; reset depth; cycle; principal reappearance without grant cycle; unsupported chain at direct-only receiver |
| Composition and budgets | No privilege union across paths; sibling overspending cannot claim shared-budget conformance; new root distinguished from derived authority |
| Recursive approval | Separate approval owners and deadlines; upstream denial/expiry grants nothing; work completion does not implicitly withdraw other approvals |
| Resource and confidentiality bounds | Oversized/deep proof; untrusted URL; hidden restrictions; no proof disclosure merely because an artifact is signed |

First demonstrate separate U, P and W endpoints with a deterministic worker
recording protected effects. Include valid signatures with insufficient authority
and show absence of the prohibited effect, not just a refusal message. Then test
independent language implementations using the same artifacts and policy fixtures.

Before adopting a recursive profile, demonstrate a valid multi-hop path and the
failure cases above in both coordinated and peer arrangements. Exercise two
authority-provisioning arrangements where practical to expose hidden dependence
on a central service. Direct-only conformance must not be reported as chain
conformance; repository checks establish neither.

## 13. Decisions and staged delivery

The agreed direction is an optional extension with multi-hop and recursive
permissioning in its vision. The following decisions remain for normative design:

| Decision | Proposed direction or alternatives |
|---|---|
| Initial support | One subject and one direct grant; no onward issuance; preserve the recursive model |
| Grant meaning | Explicit permission contract; settle conferred authority versus dependency on current subject rights |
| Message integration | Compare provisioned immutable association with a separately identified extended message contract; favor an embedded proof for the portable target |
| Exchange isolation | Fixed subject within a turn; decide whether initial conversations also fix one subject |
| Lifetime/status | Select one complete initial model with concrete limits, trusted sources and unavailable-state behavior |
| Trust and key lifecycle | Specify issuer authentication, retained verification, rotation, compromise and exact artifact identity |
| Recursive proof | Later single-parent paths with explicit delegation scope, inherited restrictions, bounded depth and ancestor status; no implicit graph composition |
| Failure behavior | Complete precedence, setup failure and wire outcomes without weakening existing core semantics |

Recommended delivery sequence:

1. Review this conceptual model and resolve the initial profile decisions against
   the human-proxy scenario and the recursive counterexamples.
2. Specify the extension and its direct-grant proof/integration profile with
   compatibility identity, schemas and shared positive/negative fixtures. Keep
   prospective recursive requirements clearly separate from supported conformance.
3. Implement and test independent endpoints under that agreed contract, including
   direct core participation with no delegation dependency.
4. Specify and validate recursive delegation under a separately selected profile,
   reusing the same authority concepts and application boundaries. Implement it
   when authorized and justified by the required network behavior.

No production protocol identity, schema, grant service, runtime component or
network implementation is introduced by this proposal. Core conformance remains
independent of all proposed delegation profiles.

## 14. Standards context

Use existing security mechanisms where their contracts fit; do not confuse a
standard token format with a complete Keel authorization contract.

- [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693.html#section-1.1) distinguishes
  delegation from impersonation. Its nested actor claims describe actor history;
  they do not provide the parent-grant validation defined as a requirement here.
  Adopting the identity distinction does not select OAuth token exchange.
- [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html#section-3.8) supplies
  relevant JWT validation guidance: issuer/subject and audience checks, explicit
  typing and mutually exclusive rules for different token kinds.
- [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662.html#section-4) explains the
  freshness cost of caching authorization status. Referencing it does not select
  its introspection service as a required Keel component.

These precedents inform design review. They do not establish security or
interoperability of a mechanism that has not yet been specified and tested.
