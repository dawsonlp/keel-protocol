# Operation declarations, structured data and application agreements

**Disposition:** core rules and optional provisioned agreement adopted; generic
invocation conditions and declaration-evidence mechanisms deferred.
**Subjects:** operations; schemas; compatibility; application agreements.

## Decision

Descriptions advertise current offerings; they do not bind later invocations to
a cached declaration. Each admitted turn retains its selected response contract.
The actor's retained contract and the requester's knowledge of it are distinct.
Operation names must be unique within one description, without a universal
promise of unchanged meaning across descriptions or future turns.

Allow any core-valid JSON value in request/result data while retaining an object
envelope. Declared input and successful-output schemas require present data;
omission, null and falsey values are distinct. Use the defined Draft 2020-12
embedded-schema profile with object roots, permitted nested booleans, local
references and annotation-only `format`. Validator defaults, coercion or
property removal must not silently change admission meaning.

For controlled deployments needing stable application meaning, specify the
optional `keel.provisioned-agreement.v1` profile. The requester retains the
agreement used during preparation; setup establishes that intended agreement
at both endpoints or fails. The host preserves its meaning for the association
and retires the paired scope before incompatible replacement. The profile adds
no core wire field, public setup protocol or registry.

## Basis and application

Structured values support deterministic and model-assisted operations without
mandatory wrappers. One schema interpretation prevents implementation-dependent
acceptance. Application compatibility remains with the contract owner rather
than being inferred from a name, alias or matching schema.

The optional agreement supports prepared mechanical requests, cached model tools
and human interaction modes whose meaning must survive preparation-to-admission
delay. It preserves a selected application promise without making that stronger
promise mandatory for every core participant.

## Alternatives and limits

Universal permanent operation naming, semantic-version syntax, mandatory
registries and declaration hashing were not selected. Transparent expected-contract
conditions on arbitrary invocations, a generic required-extension facility and
exact declaration-evidence mechanisms remain deferred. Unknown metadata does
not implement them; no generic contract-mismatch refusal was added.

An agreement establishes neither current authority nor execution, availability,
recovery or exactly-once effects. No implementation package or mandatory network
service was selected to own its machinery.

## Current authority and related decisions

[Asking](../../core/asking-contract.md), [schema rules](../../core/schemas/README.md)
and the [optional agreement profile](../../extensions/interaction-agreements/provisioned-agreement.md)
are authoritative. See [scope](scope-and-identity.md) for participation and
[delivery/context](delivery-and-context.md) for the association's lifetime.
