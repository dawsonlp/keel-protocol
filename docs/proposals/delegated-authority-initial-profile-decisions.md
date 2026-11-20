# Initial delegated authority profile decisions

**Status:** recommended profile approved by the user on 19 November 2026. This
document records the basis for the decisions in the
[implementation checklist](delegated-authority-implementation-checklist.md)
against the [revised proposal](delegated-authority-extension.md) and core/1 at
`5b24163897c8b13f0d570b3c4c2f21c51623c708`.

The [normative profile](../../extensions/delegated-authority/provisioned-direct-grant.md)
defines the selected behavior and the
[artifact contract](../../extensions/delegated-authority/direct-grant.md) defines
the exact representation and verification limits.

## Selected first profile

Use a signed direct grant that both peers select when provisioning a fresh
conversation. The grant authorizes a named requester, bound to its signing key,
to exercise specified authority for one subject at one receiving actor. The
authority association fixes that subject and exact grant for the life of the
conversation. An actor may represent other subjects in separately provisioned
conversations. An ordinary core conversation remains available for direct action
and attribution-only `on_behalf_of`.

This is the shortest path to interoperable grant verification for the controlled
UI–proxy–worker deployment. The grant is portable between authorized verifiers
that recognize its issuer, permission contract and audience. Trusted provisioning
installs the grant, using the existing signed conversation ID to bind traffic to
it. A future separately identified message contract can carry proof per request
when peers need that flexibility. The provisioned approach requires both peers to
authorize the provisioning facility and needs a fresh conversation for each grant
replacement. Per-request proof carriage requires its own signed compatibility
identity, schema, support selection and subject isolation rules. See the
[provisioned context](../../core/profiles/provisioned-context.md) and
[core extension rules](../../core/asking-contract.md#9-version-and-extensions).

| Checklist item | Recommended choice | Consequence to review |
|---|---|---|
| **DA-P01** Permission model | A receiver-recognized resource authority confers bounded permission for the term. The receiver still applies current local policy. The first profile supplies no subject-entitlement lookup or proof composition. | Human consent and issuer signature are distinct from authority over a worker’s resources. A deployment needing live subject-entitlement checks needs a contract that defines them. |
| **DA-P02** Message integration | Install an immutable authority association alongside `keel.provisioned-context.v1` at both endpoints. Keep the signed core envelope. | Shared provisioning is a prerequisite for this integration. A portable artifact alone cannot establish an authorized conversation or reply route. |
| **DA-P03** Exchange isolation | Fix one subject, one grant and one authorized direction per conversation. The requester can exercise the grant at the conversation actor. Worker responses and closures use their own authenticated roles. | A second represented direction needs its own conversation or a later profile. Refreshing a grant requires fresh setup. Work in the old conversation retains its original constraints. |
| **DA-P04** Validity and status | Use expiry-bounded offline validation with receiver-enforced local denials, explicit configured maximum lifetime and no remote status dependency. | A disconnected receiver can continue accepting covered requests until expiry unless it already knows a disqualifying fact. Select a fresh-status profile first if the target deployment cannot accept this delay. |
| **DA-P05** Identity and verification | Separate typed signed artifact, issuer-scoped ID, exact artifact binding, explicitly configured issuer key authority, and requester principal plus certified message key binding. | A holder key change requires a new grant and scope. Same-key certificate renewal neither renews the grant nor rewrites a signed request. |

## Decisions in observable terms

### Permission and trust

The issuing principal and verifying key must be explicitly trusted for the
subject, receiving actor and named permission contract, including the limits
they may confer. Naming certification and permission issuance use independent
trust rules. A grant selects one permission contract and its bounded parameters.
The receiver must map the actual selected operation and resources to that meaning
and enforce current resource policy. Unknown contracts and inadequate scope deny
the requested authority. The initial contract covers reusable permissions.
Accounting for shared quotas or one-time use requires a separately defined owner
and enforcement contract. [Core security](../../core/security.md).

### Setup, direction and renewal

The requester selects the intended authority before setup. Both endpoints install
the same profile, namespace, subject, requester/actor roles, permission contract
and exact grant association for the actual channel and fresh conversation ID.
The independently authorized facility confirms bilateral readiness before traffic.
The receiving actor verifies the grant’s authority during setup and checks its
applicable use conditions again at request admission. A matching
`on_behalf_of` can accompany a represented action, but selection comes from the
established scope. Missing or inconsistent setup fails before work. A conflicting
subject claim on a fresh protected message within an established scope is denied.
There is no fallback to the requester’s independent privileges in that scope.

The grant applies to requester actions the permission contract covers. A requester
may decide an actor-originated approval only when explicitly authorized for that
exact approval and within ordinary core acceptance rules. Ordinary controls,
role-owned reports and closures keep their original sender, ownership and
disclosure checks. New grant material never replaces the association in place.
Retirement precedes disposal or loss of required association state. Renewal
opens a fresh scope, and neither pending turns nor accepted approvals move there.
An old authorized connection can still report old outcomes while retained under
its original applicable rules. [Provisioned context](../../core/profiles/provisioned-context.md),
[approvals](../../core/approvals.md).

### Targeted actions and status

An amendment, answer or stop must match the scope’s subject, original work
constraints and an explicit action permission. For an unseen opening, a fixed
subject alone does not establish stop authorization. Accept prospective stop only
if the applicable stop permission covers every eligible opening that could arrive
for that target in the fixed scope, or if authorized retained target facts already
establish coverage. Otherwise refuse without a marker. Test both arrival orders,
including an allowed prospective stop followed by an authorized opening. The
profile uses ordinary core dispositions after authorization. [Core stop](../../core/asking-contract.md#44-stop).

Evaluate validity with the receiver’s current clock and exact protocol time
comparisons. Recommend an inclusive start and exclusive expiry, with fleet clock
accuracy a declared deployment assumption. Require receivers to enforce their
configured maximum grant lifetime and known disqualifications, including local
grant or issuer-key denial. Establish an acceptable maximum for the intended
deployment before claiming it meets revocation requirements. An expired grant
blocks new delegated admission, including new represented decisions. Expiry alone
does not retire a still-authorized core route or erase retained dispositions.
The effect owner rechecks applicable authority at the protected action boundary
as the resource contract requires. Disclosure, including after expiry, requires
its own current authorization. An exact copy can receive only eligible historical
feedback under the core rules and cannot reexecute. [Core timestamps](../../core/timestamps.md),
[retained copies](../../core/messaging.md#exact-retained-copies-and-expired-credentials).

### Issuer and holder evidence

Use a distinct signed artifact type with closed validation rules. Reuse core
canonical JSON and the core signing algorithms where applicable. Authenticate
the issuer through receiver-configured issuer/key authority, with no implicit
grant authority from a core identity certificate. Define the normative byte and
structure bounds before emitting fixtures. Keep the stable grant ID and exact
signed artifact identity separate. Match the holder key and principal to the
actual authenticated signer for new protected requests. Keep current grant and
issuer policy checks even when cryptographic verification is retained. Reject an
unknown or retired signing key for fresh grant use unless a future explicit trust
rule covers it. Do not promote retained authentication into historical proof for
another verifier. [Core security profile](../../core/security-profile.md).

## DA-P06 Recursive design check

The candidate supports the proposal’s recursive model as a separate future
profile. The initial artifact type expresses a root-issued grant with zero
onward authority. Its closed shape rejects derived fields. The provisioned
association explicitly selects the proof profile, so an unsupported chain profile
cannot activate the direct-only scope. A later profile can bind a scope to the
exact selected leaf and path with the same conversation mechanism, or carry proof
in a compatible extended message contract.

Use this review case. A root recognized by W grants A issuance authority over
collection X for subject O, with depth two and a condition that access is
read-only. A has no direct read permission. A issues a grant to B authorizing
one further issuance for document x in X. B issues C a leaf grant to read x at W.
At W, first authenticate the root, then verify each exact parent relationship and
holder-to-child-issuer key binding. Check both child use and onward scope against
what its parent could confer. Check inherited subject, allowed recipients, time
bounds and ancestor status. Only C’s certified key can present the bound leaf
for that action. The receiver still applies resource policy before reading x.

If B substitutes document y, drops a condition or omits its parent, the path
fails. If A’s grant becomes unusable under the selected status contract, the
dependent grants cannot authorize fresh use. A direct-only endpoint rejects the
different proof kind or profile selection before use. The chain check depends on
the parent’s delegation scope, so A’s lack of a direct-use audience or permission
does not prevent valid issuance. These outcomes follow the proposed design.
They remain receiver acceptance cases for the eventual implementation. See the
[recursive model](delegated-authority-extension.md#7-multi-hop-and-recursive-permissioning).

## DA-P07 Proxy trust boundary

Use three separately authenticated actors and two independently issued grants.
The UI may invoke specified proxy controls for H. The proxy may request
specified operations from the worker for H. The proxy checks the actual UI
instruction, subject and resources before issuing its downstream request. A UI
grant limited to history cannot induce a publication even if the proxy has a
publication grant. The worker verifies the proxy’s authority and applies its own
resource policy. That proof establishes who is authorized to ask for the action
and for whom. A request-specific record of what the UI or human authorized would
require its own proof and binding. The initial scenario uses the proxy’s control
boundary, with no independent worker proof of any particular human instruction
established as a requirement. An application requiring that assurance needs to
specify it before relying on the proxy. [Motivating arrangement](delegated-authority-extension.md#human-ui-and-independently-living-proxy).

## Receiver cases for the specification

Use these traces when turning the decisions into shared fixtures under **DA-S04**.
Observe the disposition or binding outcome, changes to retained state, and whether
the protected effect occurred. These are scenario sketches for the candidate design.

| Case | Expected observation under the candidate | Proposal requirements |
|---|---|---|
| Direct actor uses its own permission, with or without attribution | Ordinary core policy applies without consulting grant infrastructure | DA01, DA02, DA14 |
| Both peers provision a grant for document x, then the requester asks to read x | The receiver uses the authenticated requester, fixed subject and current resource policy to admit the read | DA01, DA03, DA05 |
| The parties disagree on grant bytes or support, or the issuer key has only naming authority | Setup fails before traffic, with no new work or prior-disposition feedback | DA02, DA03, DA04 |
| A correctly signed request claims another subject or asks for document y | Deny delegated work even if the signer independently has that permission | DA02, DA05, DA06 |
| A stop arrives before its opening, with authorization covering every eligible target | Retain suppression for the named opening. A later valid opening receives `taken` as `not-acted-on` | DA06, DA07 |
| A stop arrives before its opening with insufficient target authority | Refuse without retaining suppression. A later valid opening follows ordinary admission | DA06, DA07 |
| A grant expires or is denied locally after admission and before the protected effect | Preserve earlier admission. Apply the resource contract at the effect, and separately apply current disclosure policy to replies | DA07, DA08 |
| An eligible exact copy arrives after expiry on an authorized route | Report the retained disposition under the core rules. A delivery without audience authorization supplies no feedback. Neither repeats the effect | DA07, DA08, DA15 |
| A valid grant is presented on a retired scope, or setup receives an oversized or derived proof | No work. Scope failure uses the binding outcome. Unsupported or oversized proof fails setup within its processing bounds | DA02, DA07, DA09, DA12 |
| A UI history grant is used to try to induce publication by its more privileged proxy | The proxy rejects before making the downstream call. An independently authorized worker result can still be received and disclosed according to policy | DA05, DA09, DA15 |
| A work grant is offered as authority to decide a separate approval | Apply the approval’s own action permission, target binding, owner and deadline | DA01, DA06, DA09 |

Carry DA10, DA11 and the shared-budget case in DA13 into the recursive profile.
During direct-grant work, verify that unsupported derivation and quota conditions
cannot be silently discarded. See the [proposal conformance cases](delegated-authority-extension.md#12-conformance-evidence-and-counterexamples).

## Consumer readiness

Python and TypeScript are candidates for independent conformance. The inspected
Python checkout, at `9e8fb3b` with additional local work, has encoding and
signature primitives, in-process actors and a signed answering slice in
`src/keel_python/session.py`. Its session limits actor-side reception to `say`,
`stop` and controls, and requester-side reception to `taken`, `result` and
controls. The core approval receiver obligations needed by the extension are
still a prerequisite. The TypeScript folder contains design and a development
checklist, with signed WebSocket exchange and receiver coverage still pending
there. The Rust checkout was absent. Recheck each consumer’s actual source,
ownership and core receiver evidence before completing **DA-I01**. Shared
artifacts can be specified after profile agreement while consumer work progresses
in its owning repositories.
