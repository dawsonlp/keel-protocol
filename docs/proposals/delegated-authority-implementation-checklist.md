# Delegated authority implementation checklist

This checklist tracks the [revised extension proposal](delegated-authority-extension.md).
The protocol baseline is unreleased core/1 at
`5b24163897c8b13f0d570b3c4c2f21c51623c708`. The proposal records the agreed
direction and the design choices still open.

Mark an item complete when its decision, artifact, or test result is linked next
to the item. For runtime results, record the implementation revisions, selected
profiles, cases run and any limitations. Track repository checks, receiver tests,
interoperability and deployment evidence separately. Keep item IDs stable so
reviews and test results can refer to them.

## 0. Agreed direction

- [x] **DA-D01** Place verified representation in an optional Keel extension.
- [x] **DA-D02** Include multi-hop delegation and recursive permissioning in the
  vision from the outset. Preserve the differences between routing work, deriving
  authority and seeking approval during work.
- [x] **DA-D03** Write the revised proposal with the ownership boundaries, motivating
  scenarios and counterexamples for both direct and recursive authority.

## 1. Settle the initial profile

On 19 November 2026 the user approved the recommended provisioned direct grant
profile. It fixes one represented principal and requester direction per
conversation, uses bounded permission conferred by a resource authority and
checks offline validity with local denial and a deployment-set maximum lifetime.
See the [approved decisions](delegated-authority-initial-profile-decisions.md#selected-first-profile).
Revisit the recursive design check if a later profile changes proof or authority
association semantics.

- [x] **DA-P01** Agree on the initial use cases, profile scope and permission model.
  Define who can confer authority over each resource, how the receiver maps the
  request to the permitted action, and whether the subject must still hold the
  relevant rights at use time. [Permission decision](delegated-authority-initial-profile-decisions.md#permission-and-trust)
- [x] **DA-P02** Select trusted provisioning or a separately identified signed
  message contract. Specify how both peers establish support before use and how
  the selected authority binds to the request. Preserve assertion-only
  `on_behalf_of` and reject required delegated authority that cannot be established.
  [Provisioned authority association](../../extensions/delegated-authority/provisioned-direct-grant.md#authority-association-and-readiness)
- [x] **DA-P03** Choose subject isolation for turns and conversations. Set the rules
  for renewal, contributions, answers, targeted stop before and after the opening,
  and represented decisions. Preserve the protocol owners of turns and approvals.
  [Target authorization](../../extensions/delegated-authority/provisioned-direct-grant.md#action-and-target-checks)
- [x] **DA-P04** Select a validity and status model based on the acceptable
  revocation delay. Specify time bounds, clock assumptions, trusted status sources,
  and behavior when required status is stale or unavailable. Distinguish admission,
  queued effects, protected disclosure and exact-duplicate feedback.
  [Expiry, effects and disclosure](../../extensions/delegated-authority/provisioned-direct-grant.md#effects-expiry-and-disclosure)
- [x] **DA-P05** Agree on grant identity, issuer authority, holder proof, key
  renewal, rotation, compromise and retained verification. Define proof bounds and
  how first-seen artifacts differ from exact retained copies.
  [Signed artifact definition](../../extensions/delegated-authority/direct-grant.md)
- [x] **DA-P06** Check the design against an issuance-only actor and an A-to-B-to-C
  derivation. Show where a later verifier would check the root, exact parents,
  narrowing and ancestor status. Keep use and delegation scopes distinct and
  confirm that older receivers would reject unsupported derived authority.
  [Recursive design check](delegated-authority-initial-profile-decisions.md#da-p06-recursive-design-check)
- [x] **DA-P07** Record the proxy trust boundary. Identify what the worker learns
  from the proxy’s grant, what the proxy must enforce about incoming instructions,
  and whether any use case requires separate proof of a particular instruction.
  [Proxy trust boundary](delegated-authority-initial-profile-decisions.md#da-p07-proxy-trust-boundary).

## 2. Specify the direct-grant profile in `keel-protocol`

- [x] **DA-S01** Write the extension contract and the concrete proof profile as
  separate parts. Assign compatibility identities and define applicability, signed
  artifact representation, schemas, algorithms and processing bounds.
  [Extension and artifact index](../../extensions/delegated-authority/README.md)
- [x] **DA-S02** Specify setup, grant-to-request binding, retained associations and
  their loss or retirement. Specify authorization and disclosure checks for every
  affected message purpose, including exact copies and conflicting bytes.
  [Provisioned direct grant profile](../../extensions/delegated-authority/provisioned-direct-grant.md)
- [x] **DA-S03** Reconcile observable check order with core. Specify setup failure,
  observable refusals and control response behavior for malformed or unsupported
  proof, invalid scope, inadequate permission, and missing or stale status. The
  selected offline model uses local denial and expiry in place of remote status.
  [Admission and failure order](../../extensions/delegated-authority/provisioned-direct-grant.md#admission-and-failure-order)
- [x] **DA-S04** Create shared structural, cryptographic and behavioral vectors.
  Map the proposal’s `DA01`–`DA15` requirements to cases, with recursive cases
  assigned to the later profile and rejection of unsupported chains covered here.
  [Grant artifact cases](../../extensions/delegated-authority/grant-vectors.json)
  and [receiver traces](../../extensions/delegated-authority/receiver-vectors.json).
- [x] **DA-S05** Review normative prose, schemas and vectors together against the
  agreed decisions. Resolve disagreements with core explicitly. Run
  `python3 tools/check_repository.py` and record the specification revision that
  implementations will consume. [Specification snapshot and checks](#specification-snapshot-and-checks)

### Specification snapshot and checks

Profile `keel.provisioned-direct-grant.v1` uses the core baseline above and the
extension snapshot identified by the digest below. Pin the containing protocol
commit in each consumer’s conformance evidence. Use the digest to compare
earlier results from a local snapshot against the committed artifacts.

```sh
shasum -a 256 extensions/delegated-authority/{README.md,direct-grant.md,direct-grant.schema.json,grant-vectors.json,provisioned-direct-grant.md,receiver-vectors.json} | shasum -a 256
```

SHA-256 `f1ad0bee7798c56df02b695334e5fde76898c564a3c82abb9601007fd52d9284`.

- `python3 tools/check_repository.py` passed, covering local links, JSON and trace
  integrity. `git diff --check` passed and the core baseline was verified unchanged.
- Ajv 8.20.0 validated the Draft 2020-12 schema and 25 decoded structural cases.
  An independent Python `cryptography` 50.0.2 fixture check passed all 28 artifact
  cases, including Ed25519 and P-256 signatures and grant validity boundaries.
- The 22 receiver traces map to the 13 applicable proposal requirements. DA10
  and DA11 cover derived authority in the future chain profile. Runtime execution
  of the traces and interoperability remain tracked in sections 3 and 4.

## 3. Implement and demonstrate direct grants

Select two independent language implementations when their core endpoints can
exercise the agreed integration. Put protocol components in their language
repositories and proxy control, login, history and resource policy in the owning
application or deployment. Use the proposal’s acceptance cases as the test basis.

Python and TypeScript are implementing from the same specification and fixtures.
On 19 November 2026 the protocol-side review recorded the following progress.

| Project | Evidence | Remaining work |
|---|---|---|
| `keel-python` | At local HEAD `9e8fb3b` plus working-tree changes, six grant parsing and signature tests and ten approval receiver tests passed against this snapshot. The approval tests use a provisioned test route. | Pin an implementation revision. Complete the issuer authority, permission, holder, audience and validity checks, profile integration and receiver traces. |
| `keel-typescript` | The development plan records the profile selection, the verified snapshot and the core prerequisites. | Pin an implementation revision when the signed endpoints, approval handling and actual-channel provisioning can exercise the profile. |

**DA-I01** through **DA-I07** remain open. The Python result is component and
approval-slice evidence. The TypeScript result is design evidence. Each project
can use the shared artifact fixtures before running the profile receiver traces
and then pin its own implementation revision for interoperability.

- [ ] **DA-I01** Record the implementation repositories, revisions, owners and core
  prerequisites. Identify component responsibilities, interfaces, retained state
  and failure boundaries before changing the endpoint.
- [ ] **DA-I02** Implement artifact validation, trusted issuer and holder checks,
  permission applicability and status evaluation. Keep these separate from
  bindings, application policy and lifecycle ownership.
- [ ] **DA-I03** Integrate proof selection and verification with guarded admission,
  turns, approvals, retained copies and disclosure. Expose the admitted authority
  basis to the application’s effect checks. Run the applicable core receiver tests.
- [ ] **DA-I04** Run the shared extension vectors in each implementation. Exercise
  direct action without delegation infrastructure, assertion-only attribution,
  and failed required delegation with no fallback to the signer’s own authority.
- [ ] **DA-I05** Exercise authorization failures at real endpoints. Cover wrong
  issuer, key, subject, audience, action or resource, subject switching, stop before
  opening, expiry or revocation during queued work, unauthorized reply routes,
  duplicate disposition handling and retired scopes.
- [ ] **DA-I06** Run the UI actor, proxy and deterministic worker as separate
  endpoints. Verify legitimate worker replies under the worker’s identity. Give
  the proxy broader outward authority than the UI’s incoming control permission
  and verify that a valid but excessive UI instruction produces no protected effect.
- [ ] **DA-I07** Exchange signed artifacts between the independent implementations
  under the same profile and policy fixtures. Record matching dispositions,
  retained facts and observed effects. Assess deployment promises separately using
  the deployment’s actual trust and revocation arrangements.

## 4. Specify and demonstrate recursive delegation

Apply **DA-P06** during initial design. The remaining work in this section tracks
a separately selected recursive profile. Its evidence is separate from completion
of the direct-grant profile.

- [ ] **DA-R01** Agree on the chain profile’s scope and compatibility identity.
  Evaluate one selected leaf and one explicit path to a root. Define how older
  peers detect unsupported chain use and how direct grants keep their meaning.
- [ ] **DA-R02** Specify exact parent binding, authorized child issuance, subject
  continuity and how the permission contract determines narrowing. Include
  distinct use and delegation scopes, eligible holders and destinations, inherited
  conditions, and a decreasing depth bound.
- [ ] **DA-R03** Specify effective validity and status across ancestors, including
  unavailable dependencies, key lifecycle and revocation under the selected
  freshness rule. Define limits on chain depth, proof bytes and verification work.
- [ ] **DA-R04** Specify branching and accounting boundaries. Reject privilege
  splicing and unsupported shared quotas. If a later permission contract supports
  a shared allowance, identify its enforcement owner and failure semantics.
- [ ] **DA-R05** Produce normative text, schemas and shared fixtures. Cover a valid
  A-to-B-to-C path, issuance-only authority, parent substitution or omission, wrong
  child issuer, widened or removed constraints, ancestor expiry or revocation,
  exceeded depth, cycles and an older receiver rejecting a chain.
- [ ] **DA-R06** Implement the agreed recursive profile in selected language
  endpoints. Run its conformance cases and verify that direct-grant and core
  receiver behavior still satisfies their respective contracts.
- [ ] **DA-R07** Demonstrate multi-hop interoperability in coordinated and peer
  arrangements. Record the authority path and observed effects separately from
  work routing. Where practical, verify the same behavior with two provisioning
  arrangements to check for hidden dependence on a central service.
- [ ] **DA-R08** Demonstrate further permission requests during work. Verify that
  each approval retains its own owner and deadline, that upstream denial or expiry
  supplies no new permission, and that any resulting grant is checked before the
  protected effect. Leave escalation and workflow policy with the application.
