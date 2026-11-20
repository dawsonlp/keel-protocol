# Keel protocol

Keel defines how independently implemented actors exchange authenticated messages,
request work, contribute information, ask questions and obtain authority. It is
usable by deterministic services, human-facing applications and model-assisted
actors. Applications define the work; Keel defines what their exchanges mean.

**Current definition: core/1, unreleased.** The specification, schemas and vectors
are provided here. This repository does not supply an actor implementation or
claim tested interoperability between implementations.

## Experiment with different networks

A central design driver is to make substantially different actor networks easier
to build and compare on a common protocol. Networks may use centralized
coordination, peer collaboration, hierarchies, temporary teams or dynamically
selected actors. They may differ in work allocation, knowledge retention, human
participation, application authority and recovery while preserving the shared
meaning of protocol exchanges.

Pluggable components serve this experimentation. Language implementations should
separate protocol obligations from replaceable mechanisms such as hosting,
transport, scheduling, storage and model access. Network composition and policy
belong to the assemblies that use those components. Explicit interfaces must
allow materially different approaches without embedding one network's assumptions
throughout the library; replacements still have to satisfy their contracts and
the applicable protocol rules.

The architectural test is whether substantially different networks can be
assembled without changing the protocol or rewriting unrelated components.
Cross-project conversations between actors are one use case among others. The
future `keel-local-network` is one planned assembly, not a universal network
architecture. This is a design objective whose achievement requires evidence
from implementations and experiments.

## Read by purpose

| Purpose | Start here |
|---|---|
| Work on the project as an agent | [Agent guidance](AGENTS.md) |
| Understand the product and its boundaries | [Product](docs/product.md) |
| Review the requirements driving the definition | [Requirements](docs/requirements.md) and [design rationale](docs/design-rationale.md) |
| Build a networked application | [Network development guide](docs/network-development.md) |
| Implement a conforming endpoint | [Implementation guide](docs/implementation.md), then the [core specification](core/README.md) |
| Establish a stable application agreement | [Optional interaction agreements](extensions/interaction-agreements/README.md) |
| Verify authority to represent another principal | [Optional delegated authority](extensions/delegated-authority/README.md) |
| Understand a previous decision or rejected approach | [Curated history](docs/historical/README.md) |

## Repository map

```text
core/                  Required protocol definition, profiles, schema and vectors
extensions/            Specified optional behavior and its conformance artifacts
docs/                  Current product, requirements, rationale and usage guidance
  historical/          Subject catalogue of decisions and their dispositions
tools/                 Repository consistency checks
```

The [documentation index](docs/README.md) explains authority and reading order.
The core normative text governs observable behavior; its schema describes
structure and its vectors provide conformance cases. Guides explain how to apply
those definitions and do not add wire requirements.

## Contract boundary

Core/1 is one common conversation and authority contract. Optional origination
of questions or approvals does not make applicable receiving rules optional.
Participants can place protocol machinery in shared infrastructure while keeping
application logic small.

Core acceptance and duplicate handling are scoped to a live context. The
[provisioned context profile](core/profiles/provisioned-context.md) provides a
concrete memory-only deployment arrangement; it requires trusted setup at both
endpoints and does not define public discovery or automatic peer negotiation.
Recovery, history, application jobs and external effects belong to the responsible
network/application components. They do not acquire stronger guarantees from an
ordinary acknowledgement, a reconnect or the presence of saved messages.

## Protocol identity and validation

| Surface | Identity |
|---|---|
| Signed message type | `keel-core-v1+jws` |
| Payload version | `1` |
| WebSocket subprotocol | `keel.core.v1` |
| Payload schema | `urn:keel-protocol:core:1` |
| Identity certificate type | `keel-cert+jwt` under the closed core credential profile |

Earlier draft identities are not interchangeable. The provisioned interaction
agreement and provisioned direct grant are [optional profiles](extensions/README.md).
History and recovery remain application responsibilities.

Run `python3 tools/check_repository.py` for local documentation links, artifact
structure and trace-integrity checks. These checks do not execute an actor or
prove cryptographic or behavioral conformance. The [implementation guide](docs/implementation.md)
describes the remaining validation obligations. License: [MIT](LICENSE).
