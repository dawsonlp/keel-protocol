# Delegated authority

The optional extension allows an authenticated actor to exercise a bounded
permission for a represented principal. The receiver establishes the authority
independently of message authentication and applies its current resource policy.
The signer remains accountable for the signed message. Conversation roles and
ownership of turns, questions and approvals continue to follow core/1.

Use a direct core conversation for an actor exercising its own permissions,
including when `on_behalf_of` merely describes who benefits from the work.
Authoritative representation requires explicit selection of the
[provisioned direct grant profile](provisioned-direct-grant.md). Its authority
association fixes the requester, represented principal, grant and receiving actor
at setup. The profile maintains the existing core message format.

## Ownership and scope

| Owner | Responsibility |
|---|---|
| Keel extension | Authority selection and verification, binding to the live scope, handling at admission and interaction with core responsibilities |
| Resource owner | Governs permission contract meaning, determines which issuers can confer it, maps requests to actions and resources, and enforces current effect and disclosure policy |
| Deployment | Establishes both peers' provisioning trust, issuer and actor credentials, authenticated channels, clocks and lifetime limits |
| Application | Defines proxy control, procurement of permissions, work delegation, approval escalation, recovery and protected history access |

A resource authority can confer limited permission for a term. The selected
profile supplies no subject-entitlement lookup, remote revocation service, or
accounting for single-use or shared quotas. The application must define and enforce
those guarantees separately if it relies on them. Core approvals remain independent
decision exchanges. A decision can authorize grant issuance under an application
contract. The accepted decision and a portable grant are distinct artifacts.

The direct profile accepts root-issued grants with no onward issuance right.
For a UI actor, proxy and worker, each receiving actor can validate a distinct
direct grant. A worker can verify the proxy's authority, and the proxy must
separately check the instruction it received from the UI. Request-specific proof
of human intent requires its own binding and verification contract.

The [multi-hop design proposal](../../docs/proposals/delegated-authority-extension.md#7-multi-hop-and-recursive-permissioning)
tracks future recursive authority. Its model separates the permission to use a
resource from permission to issue a narrower grant, with exact parent bindings
and ancestor restrictions. Derived proof requires a separately selected profile.

## Conformance artifacts

- [Provisioned direct grant profile](provisioned-direct-grant.md) defines scope,
  receiving obligations and applicability.
- [Signed direct grant](direct-grant.md) defines the exact artifact and trust checks.
- [Schema](direct-grant.schema.json) describes decoded protected header and claims.
- [Signed grant vectors](grant-vectors.json) cover artifact parsing, verification
  and validation. Per-case values override the named defaults. Keys are public test
  fixtures. A schema or signature pass alone never establishes permission.
- [Receiver traces](receiver-vectors.json) define setup, request and lifecycle
  acceptance cases. Adapt them to each runtime and observe state, emitted traffic
  and protected effects. Checking the trace file demonstrates artifact integrity.

The [implementation checklist](../../docs/proposals/delegated-authority-implementation-checklist.md)
tracks consumer implementations, interoperability and recursive profile work.
