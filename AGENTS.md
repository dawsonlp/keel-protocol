# Agent guidance

## Purpose and authority

This repository defines the language-independent Keel protocol. Build actors and
networks against its current definitions. Keep protocol semantics, implementation
mechanisms and application responsibilities distinct.

Read in this order for the task at hand:

1. [Product](docs/product.md) and [requirements](docs/requirements.md): purpose,
   scope and drivers. Establish the application's vision and requirements before
   selecting its architecture.
2. [Core](core/README.md), its required contracts and explicitly selected profiles:
   authoritative protocol behavior. Use the current schema and vectors alongside
   the prose; schema validity alone does not establish conformance.
3. [Design rationale](docs/design-rationale.md), [implementation guide](docs/implementation.md)
   and [network guide](docs/network-development.md): current explanation and use.
4. Actual source and tests in the implementation repository being changed.

If current prose, schema or vectors disagree, report and resolve the inconsistency;
do not silently select whichever behavior an implementation already has. Discuss
architecturally significant changes with the user before adopting them. Routine
implementation choices within agreed requirements need no new protocol decision.

## Preserve freedom to experiment with networks

The common protocol is the stable basis for experimenting with substantially
different actor networks. Orthogonal, pluggable components serve that purpose;
they must support more than alternative implementations of one predetermined
network architecture.

Keep three concerns explicit:

- **Protocol obligations:** shared meanings and observable behavior that every
  applicable implementation must preserve.
- **Replaceable mechanisms:** hosting, transport, scheduling, storage, model
  access and other implementation choices behind specified component contracts.
- **Network choices:** actor composition and relationships, coordination,
  work allocation, knowledge retention, human participation, application authority
  and recovery policy within the protocol's constraints.

Do not make a central coordinator, project ownership model, persistence service,
model provider or collaboration workflow an implicit library dependency. A
concrete assembly may choose any of these. Its choices must remain explicit and
replaceable at their owning boundaries. Interfaces alone are insufficient if
consumers still depend on one implementation's hidden state or policy assumptions.

Evaluate proposed component boundaries against contrasting network arrangements,
such as centralized coordination and peer collaboration. Ask whether those
networks can use the same protocol and reuse unaffected components. Specify what
a replacement must preserve, including ownership, errors and lifecycle; verify
substitution through observable contracts rather than identical internals. Do
not weaken protocol obligations to make an experiment appear compatible, or
claim arbitrary network compatibility without evidence.

Treat cross-project actor discussion as one use case among others. Treat the
future `keel-local-network` as one planned assembly, not the architecture all
networks must adopt. Derive shared requirements from concrete use cases and
counterexamples; do not add generic machinery solely to anticipate every possible
network. These principles do not authorize implementing the future network.

## Historical information: background only

Do not use `docs/historical/` as a source of requirements, implementation instructions,
current status or authority. Do not read it as part of routine task initialization.
Consult the [decision catalogue](docs/historical/README.md) only when useful to ask:
**has this idea already been examined, and what was its disposition?**

Use any answer as background, then check the current definition and actual need.
An unselected or superseded idea does not become a backlog item or permission to
implement it. Historical rationale does not override current requirements. Do
not reconstruct deleted review logs or bring process metadata back into the
current documentation. If a former decision merits reconsideration, identify the
new evidence and proposed change explicitly.

## Repository responsibilities and destinations

| Repository | Responsibility | Expected workspace location |
|---|---|---|
| `keel-protocol` | Current contracts, profiles, schemas, vectors and language-independent guidance | This repository |
| `keel-python` | Python 3.15 project established; component specification and uv bootstrap, runtime implementation pending | `../keel-python/` |
| `keel-typescript` | Planned TypeScript implementation with independently testable components | `../keel-typescript/` |
| `keel-rust` | Planned Rust implementation with independently testable components | `../keel-rust/` |
| `keel-local-network` | Future local actor network; collaboration, durability and application recovery belong here | `../keel-local-network/` |
| `keel` | Existing component designs and source to inspect and adapt | `../keel/` |

`keel-python` has been created; TypeScript and Rust remain planned destinations.
Repository existence is not a claim of a completed runtime or conformance. Locate
the actual checkout and read its `AGENTS.md`, current design and tests before work.
These relative paths are workspace navigation hints, not runtime dependencies.
Do not create repositories, publish packages or copy whole trees merely because
they appear here; carry out the work authorized by the user's task.

`keel-local-network` is future planning only; implementation is not currently
authorized. Its agreed initial scope is one local machine, with model-assisted
and human collaboration from the first release. Its recovery promise is limited
to actor/process crashes, not machine restart or local-storage loss/corruption.
Durable work acceptance, retained outcomes and application recovery belong to
the network's responsible actors and infrastructure, without strengthening core
acknowledgements or restoring retired protocol conversations implicitly. Component
architecture, storage, orchestration strategy and implementation language remain
to be agreed before building. It will consume the language implementations rather
than duplicate their protocol machinery.

Keep network-specific orchestration, application actors and domain services in
their owning application/network projects. This repository may explain their
use of Keel but must not acquire their implementation or service requirements.

## Use the components in `keel` deliberately

Inspect these locations in the existing `keel` checkout:

| Design or source | What to examine |
|---|---|
| `docs/reference/actor-parts.md`, `library-structure.md`, `kernels.md`, `shapes.md` | Responsibilities and interfaces among actor parts |
| `docs/building/a-new-actor-type.md`, `a-component.md` | How behavior and replaceable components compose |
| `packages/libraries/python/src/keel/` and `packages/libraries/typescript/src/` | Codec, identity, client, hosting interfaces, contract handlers, facilities and shapes |
| `hosting.py` / `hosting.ts` within those library roots | Boundary between kernels and hosted handlers |
| `packages/kernels/python/` and `packages/kernels/typescript/` | Scheduling, live state, delivery and host integration |
| `packages/bindings/` | Transport adapters and fault-injection seams |
| `packages/libraries/python-models/` and `packages/libraries/python-agents/` | Separation of provider-neutral model access from actor integration |

Read actual code rather than inferring behavior from a component name. The older
`keel` reference and canon govern that checkout's own work; they are not authority
over this standalone core/1 specification. Its code includes record-before-ack,
automatic recovery, historical query and other legacy assumptions. Do not import
those as core obligations, reuse legacy wire identities or assume existing tests
establish current conformance. Preserve useful separations while adapting behavior
to the current protocol. Rust should express equivalent responsibilities through
appropriate Rust interfaces, not mechanically copy another language's class tree.

## Orthogonal implementation principles

Before substantial language implementation, document each component's purpose,
owned state, interfaces, dependencies, failure boundary and conformance tests.
Use the existing component model as a starting point; agree material changes.
Conceptual separation does not require one package or process per responsibility.

| Responsibility | Boundary to preserve |
|---|---|
| Codec, schemas and exact time values | Representation and validation without transport, model or application logic |
| Identity, signing and trust | Key/credential handling and naming authority distinct from action policy and response disclosure |
| Binding | Frame transport and actual-route context; no independent reinterpretation of turns or grants |
| Endpoint/kernel | Guarded admission, ordering of state transitions, retained live facts, timers and delivery; no application scheduling strategy or mandatory durable record service |
| Contract handlers | Turn, contribution, approval, notification and control semantics through explicit host interfaces |
| Behavior and shapes | Application work behind an interaction adapter; work cannot override protocol lifecycle or block required controls |
| Facilities and client interfaces | Explicit capabilities for asking other actors, clocks and services; no hidden access to unrelated actor state |
| Assembly/deployment | Select concrete components, credentials, routes, profiles and policy at a composition boundary |
| Model adapters, if used | Provider access, context construction, retry policy and presentation remain separate from protocol semantics |

Assign each state transition one authoritative owner; adapters must not duplicate
competing state machines. Dependencies should point to explicit interfaces, with
concrete implementations selected by composition. Make clocks, transport and
external effects controllable for tests. Replace a binding without rewriting
behavior; change a model provider without changing the protocol; support a bounded
deterministic actor without requiring model, discovery or record services.

Share normative fixtures and semantic expectations across the three languages.
Do not require identical internal representations or APIs, and do not fork the
meaning of core messages to suit a language's libraries. Pin or otherwise identify
the protocol revision used by each implementation and report discrepancies back
to this repository.

## Build an actor that implements the protocol

1. Define its application offering: operation meaning, inputs, successful outputs,
   amendments, effects, authority and cancellation promises. Separate application
   work identity from protocol turn identity. Choose bounded or interactive work
   according to requirements; neither requires a model.
2. Select a language implementation and compose the required endpoint components.
   Implement core/1 identity consistently across payloads, signatures, schema and
   binding. Do not claim conformance for only the message kinds the application
   normally originates; applicable receiving obligations still hold.
3. Configure governed principals, issuer/key naming authority, credentials, action
   authorization and recipient-bound response routes. Apply the specified guards
   and verification order. A valid signature does not authorize reply disclosure
   to whoever carried its bytes.
4. Establish an explicitly selected continuity profile before conversation traffic.
   The provisioned profile requires independently authorized setup at both peers,
   a fresh actor-issued conversation key, actual-channel association and bilateral
   readiness. Retire admission before losing required state; reconnecting alone
   supplies no continuity.
5. Connect application behavior through the handler/shape boundary. Preserve the
   admitted turn contract, explicit contribution targets, one terminal response,
   independent approval ownership and correctly targeted stop. Keep controls
   serviceable while work or model calls are running. Application code enforces
   the actual effect and any stronger cancellation promise.
6. Preserve exact signed bytes and scoped identity. Receive delayed notifications
   from retained facts, not arrival order. Validate real dates and compare the
   full admitted timestamp precision. Keep historical artifacts separate from
   fresh live admission; do not invent acceptance or execution from missing data.
7. Test the actual receiver and a working client exchange, then failure cases:
   duplication, conflicting bytes, delayed first delivery, expired credentials,
   unauthorized routes, stop/approval races and retired contexts. A schema pass
   or a running listener is insufficient. Use the current vectors and the
   [implementation validation layers](docs/implementation.md#validation-and-conformance-evidence).

The protocol supplies no portable scoped-grant format or recovery extension.
Application permission and service recovery contracts must be explicit when used.

## Design and implement a network

Start with the network's purpose, required outcomes and conceptual model: entities,
identities, relationships, ownership and constraints. Establish those meanings
before choosing processes, workflow or deployment. Define what evidence counts
as success and what uncertainty the application must expose.

1. Assign work, information, authority and external effects to responsible actors.
   Specify their service contracts and collaborations. Do not assume every actor
   needs a model, a central coordinator, its own process or the same storage.
2. Define application jobs and commitments independently of turns. A successful
   submission can accept a job without completing it. Delegation creates another
   actor's exchange; the coordinator remains responsible for its own outcome.
3. Arrange trust governance, addresses, bindings, setup authority, resource budgets
   and failure boundaries. Configure each actual pair's admission and response
   audience. Discovery or membership services are network choices, not core setup.
4. Decide which application meanings must remain stable during preparation and
   admission. If needed, explicitly select the provisioned interaction-agreement
   profile and preserve the requester's intended agreement. Do not treat a cached
   description, operation alias or metadata field as that guarantee.
5. Define permission and effect enforcement, human participation and cancellation.
   Inspection access is not execution authority. A decision permits only its
   described action; work completion, revocation and job cancellation remain
   separate. Use fresh independent conversations where concurrent obligations or
   serviceable application cancellation require them.
6. Assign historical access, retained outcomes and job recovery to responsible
   actors and client infrastructure. Specify retention, completeness and trust.
   Reconcile uncertain effects through fresh valid exchanges after scope loss;
   never assume saved outboxes or a new message ID make repeated work safe.
7. Implement the agreed network in its application repository using the language
   libraries. Keep domain logic, model policies and service storage outside the
   shared protocol machinery. Record unresolved assumptions instead of making
   an application preference into a new core requirement.
8. Test the network's promises across real component boundaries, including a crash
   between an external effect and its record, unavailable actors, partial history,
   revoked authority and interrupted human interaction. Demonstrate the intended
   application outcome separately from protocol conformance.

The [network development guide](docs/network-development.md) provides a concrete
workflow and recovery cases. Choose an architecture from these requirements;
there is no universal actor-network topology selected by Keel.

## Keep changes reviewable

- Inspect current files, repository instructions and working-tree changes before
  editing. Preserve unrelated work and distinguish observed behavior from plans.
- Put current drivers in product/requirements documentation, exact behavior in
  the normative contracts and usage in the guides. Keep instructions and links
  current when repository locations or component responsibilities change.
- Update schema, vectors and prose together when an approved protocol change
  requires it. Preserve signed fixtures unless the change explicitly requires
  regenerated fixtures and their independent verification.
- Run `python3 tools/check_repository.py` for repository consistency. Run the
  relevant implementation's actual tests for code changes. Distinguish artifact
  checks, receiver tests, cross-language interoperability and deployed outcomes.
- Report the implementation revision, selected profiles, executed checks and
  remaining limitations. Do not present specification completion as a working
  actor, finished network or published language package.
