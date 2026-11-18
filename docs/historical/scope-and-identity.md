# Protocol scope and compatibility identity

**Disposition:** adopted for core/1.
**Subjects:** protocol scope; participation; compatibility.

## Decision

Core/1 is one common conversation and authority contract. It includes asking,
independent approvals and the delivery, security and receiving obligations needed
to interpret them. Conformance belongs to the endpoint and is conditioned by its
role in each exchange. Deterministic services and human/model collaboration use
the same contract; no model or human interface is required.

Optional origination does not make applicable receiving rules optional. A simple
application may delegate protocol machinery to infrastructure without reducing
the endpoint's obligations. Actor principal names identify participants but do
not establish core conformance or make asking universal to all actor protocols.

The first standalone definition uses payload version `1`, signed type
`keel-core-v1+jws`, WebSocket subprotocol `keel.core.v1`, schema identity
`urn:keel-protocol:core:1` and certificate type `keel-cert+jwt` under its closed
credential profile. Earlier draft identities are not interchangeable. Core/1
remains unreleased.

## Basis and application

The selected scope supports both bounded service operations and interactive work.
Other service contracts can exist without requiring this core to define every
kind of actor participation. One compatibility identity makes the conformance
claim explicit. Application meaning, network composition and implementation
placement retain separate owners.

Core supplies shared observable semantics, not a required UI, scheduling strategy,
storage engine or hosting framework. Infrastructure chooses its mechanisms while
preserving the contract's facts and uncertainties.

## Alternatives and limits

A smaller common substrate with independent interaction contracts and a family
of limited participation profiles were not selected. Either would require a
concrete scope need plus explicit support, selection and compatibility rules.
Separate conceptual responsibilities do not require separate repositories or
processes. No compatibility obligation to unreleased legacy drafts was retained.

## Current authority and related decisions

[Core participation](../../core/README.md#participation-and-conformance) and
[protocol identities](../../README.md#protocol-identity-and-validation) govern
implementation. [Recovery ownership](recovery-and-service-ownership.md) explains
why retained service outcomes do not require a broader core contract.
