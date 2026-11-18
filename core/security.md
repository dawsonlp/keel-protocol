# Security

Every core message is signed. Receivers authenticate the signer, check the
recipient, and apply authorization before acting. The wire definition is in
[the asking contract](asking-contract.md).

## Security responsibilities

The core uses certified signed messages and receiver-owned authorization.
These responsibilities are independent of whether a participant is implemented
by deterministic code, a model, or a human-facing application.

| Concept | Meaning and owner |
|---|---|
| Principal | A participant's identity under the receiver's configured naming trust |
| Credential | An issuer's time-limited assertion binding that principal to a key |
| Authenticated message | Exact signed bytes whose signer, profile and addressed context have been established |
| Authorization | The receiving operation/resource owner's decision about the requested action |
| Approval exchange | An originator-owned request and decision lifecycle; see [approvals](approvals.md) |
| Grant | Authority conferred under an explicit application contract, including any validity and use limits |
| Effect | The resource change or other external action, governed by its effect owner |
| Evidence | An artifact and the claims a verifier can establish about it under stated trust |

Credential validity, approval decision deadline, grant validity, retained
duplicate state and evidence retention are different lifetimes. One does not
extend another by implication. Issuing a credential does not authorize the
issuer or subject to grant permissions over unrelated resources. An accepted
decision does not prove execution, content truth or independent human review.
Conversation admission additionally requires the selected profile's
[continuity guard](continuity.md). A valid credential, retained authentication
or earlier decision does not establish that a conversation scope remains usable.

## Principals and trust

A principal is a governed name, `actor:<name>` or `party:<id>`. Its authenticated
identity comes from its certificate's `sub`, not from a claim in the message
payload. Compare the entire principal string exactly, including its kind and
case. The issuer and keys establish who may certify that identity; they are
not additional components of its wire name.

Participants have signing keys and certificates. A receiver has configured
trust configuration binding issuer names, public keys and explicit naming
authority as defined below. Obtaining a certificate,
authenticating a person, distributing trust anchors, and protecting private keys
are deployment responsibilities. The core specifies the certificate presented
with a message; it specifies no sign-in service or key-holder interface.

A certificate is a signed JWT. Its header has `typ: "keel-cert+jwt"` and an
accepted signing algorithm. Its payload contains `iss`, `sub`, `iat`, `exp`,
and `cnf.jkt`. Times are JWT NumericDate values. `cnf.jkt` is the RFC 7638
thumbprint of the certified public JWK, using the RFC 7800 confirmation claim.
The reserved recipient `unverified` is not a principal and cannot be certified.
The [credential and envelope profile](security-profile.md) defines the closed
field sets, principal grammar, time rules and malformed-input behavior. A
generic JWT verifier without these profile checks is insufficient.

### Governed names and issuer authority

Within a governed namespace, each full principal name denotes one participant.
The deployment's naming governance assigns names and authorizes issuers to
certify them; receivers enforce that authority using authentically provisioned
trust configuration. Core requires these responsibilities, not a central
registry, federation service, naming prefix or configuration-file format.

For current certificate admission, a receiver must establish a permitted
association between all three of:

1. The exact certificate `iss` value.
2. The configured issuer public key that verifies that certificate.
3. The exact `sub` principal, within that issuer/key's explicitly authorized
   names or governed naming scope.

An issuer/key with no explicit naming authority may certify no principals.
Adding a trust anchor does not by itself authorize any names. A cryptographically
valid certificate outside the verifying issuer/key's authority fails as
`certificate-invalid`. Do not combine a signature verified by one key with the
subject scope of another key, even if both keys have the same issuer name.
Names or scopes may be represented by explicit local policy, but their meaning
must be unambiguous; matching a name's appearance alone grants no authority.

These rules apply equally to actor and party principals. For example, a
configuration can authorize Blue's issuer/key to certify `actor:blue.release`
and Green's to certify `actor:green.release`. Green's otherwise valid certificate
for Blue's actor must fail. A policy that intentionally authorizes both
issuer/keys for `party:ada` asserts that both certify the **same participant**.
It does not create two issuer-qualified identities or merge two independently
owned identities. Such overlap must be an explicit governance decision.

Network membership and action authority are separate from identity. Names such
as `actor:requirements`, `actor:learning-deployment` and `party:ada` need not
change. One participant may join several collaboration networks under the same
governed name. Dots, hyphens and other permitted name characters imply no
membership, hierarchy, delegated naming authority or resource permission.

Before joining independently governed namespaces, reconcile any equal names:
establish that they identify the same participant, allocate distinct names,
or keep the namespaces isolated. Do not infer shared identity from spelling.
A receiver serving isolated namespaces must separately scope trust, principal
resolution, authorization and retained state to their independently established
deployment/binding context. Core carries no namespace discriminator with which
to repair ambiguous routing; untrusted message claims cannot select a different
namespace to obtain authority.
For a single-namespace deployment this can be one fixed trusted context; no
global namespace identifier or additional wire field is required.

### Identity continuity and rotation

Changing a participant's message-signing key can preserve its principal when
the new key has a currently valid certificate from an issuer/key authorized for
that same participant's name. Replacing or adding an issuer key or issuer name
requires a deliberate trust-policy update that states its naming authority.
If old and new issuer/keys overlap, both are asserting the same governed
principal; neither renewal nor addition automatically revokes an older key.

Preserving that principal does not bypass current authorization or restrictions
bound to a particular key or credential. It does not rewrite an existing signed
message or change an approval's exact-byte binding. Retain the original
verification basis; use current policy for new messages, actions and disclosure.
Removing an issuer/key's naming authority blocks new admission under it but
does not erase the earlier observation that a message was accepted. Relevant
compromise information may still prohibit further use or disclosure under the
[retained-authentication rules](#retained-authentication).

A changed full principal name is a changed core identity. Core defines no
automatic alias, permission transfer, approval transfer or conversation merge.
An application/deployment migration must explicitly address those relationships;
historical signed messages retain their original names and bytes. Do not
repurpose a name for a different participant while continuing to interpret it
as the same governed principal. Reusing its spelling in a separate namespace
requires the isolation above, including permissions, pending exchanges, grants,
duplicate records and historical identity interpretation. Ending a conversation
alone does not make old permissions or signed evidence belong to a new owner.

## Signed bytes

A message uses JWS compact serialization, with three base64url parts separated
by dots: protected header, payload, and signature.

| Part | Required representation |
|---|---|
| Protected header | `typ: "keel-core-v1+jws"`, `alg`, public `jwk`, and `cert` containing the certificate JWT |
| Payload | UTF-8 JSON in exactly its RFC 8785 canonical form |
| Signature | `EdDSA` with Ed25519, or `ES256` with P-256; ES256 is 64-byte raw `r` followed by `s`, never DER |

Every verifier accepts both algorithms. Every signer uses one of them. The
algorithm must match the key type and curve.

Numbers follow I-JSON. Integral-valued numbers must lie within ±(2^53−1),
including values written with an exponent or fractional notation; larger ones
must be represented as strings. Non-finite numbers are invalid. Duplicate object
members are invalid. These constraints prevent different implementations from
assigning different values or canonical bytes to the same payload.

## Verification order

The table specifies first-seen authentication within an admissible binding
scope. Apply bounded input checks, the binding's uniform audience guard and,
for conversation traffic, the selected profile's
[continuity admission guard](continuity.md#establishment-and-admission)
before any state-dependent feedback. A missing or retired conversation
scope receives the profile's binding rejection without a core disposition,
message-ID reservation or replacement context. Within a valid scope,
[exact retained-copy recognition](messaging.md#exact-retained-copies-and-expired-credentials)
may resolve a known disposition under its narrow response-audience rule.
That path uses a previously established fact, not current authentication of a
new message. Otherwise the first failing table check determines the failure
classification. Whether to emit a refusal follows the binding and
[control-response rules](diagnostics.md#control-response-termination): invalid
controls receive no core reply, and unclassifiable frames use binding rejection.

| Order | Check | Reason |
|---|---|---|
| 1 | Outer framing, encoding, protected header and public key satisfy the closed profile; `typ` is `keel-core-v1+jws` | `malformed` |
| 2 | `alg` matches the key type and curve | `algorithm-key-mismatch` |
| 3 | The certificate satisfies its complete profile, including issuance-time sanity; its signature, issuer/key and subject naming authority are valid | `certificate-invalid` |
| 4 | Current clock is strictly before `exp + 30` seconds | `certificate-expired` |
| 5 | The certificate's `cnf.jkt` matches the message key's thumbprint | `key-not-certified` |
| 6 | The message signature verifies with that key and algorithm | `bad-signature` |
| 7 | The payload is exactly the canonical form of its JSON value | `not-canonical` |
| 8 | `to` names the intended recipient and, for a conversation message, the intended conversation; only the restricted [diagnostic path](diagnostics.md#receiving-and-associating-a-diagnostic) admits the reserved `unverified` address | `not-addressed-to-me` |

After all eight verification checks, check structure in the order specified by the
asking contract, including the [core timestamp checks](timestamps.md).
Authentication supplies identity; authorization decides
whether that identity may make this request. A valid signature alone is not
permission. Refuse unauthorized requests as `not-authorized`.
At semantic admission, the same conversation guard and required context must
still be valid, ordered with retirement. Earlier authentication cannot admit a
queued frame into replacement state.
Parsing, input-size and resource checks precede expensive unbounded work as
specified below. The [profile](security-profile.md#failure-classification)
assigns malformed encodings and claims to their verification steps.

The diagnostic exception replaces recipient matching only for its restricted
control form on an independently authorized expected-peer route. It waives no
other verification or structural rule, supplies no action authority, and cannot
bypass the original continuity guard because the payload lacks a conversation.
Its correlation and local effect require the separate checks in
[diagnostics](diagnostics.md#receiving-and-associating-a-diagnostic).

## Retained authentication

Successfully authenticating a particular message establishes a fact about those
exact bytes under the verification conditions then in force. Retain that fact
with the message's relevant live state. Ordinary certificate expiry does not
erase it. It is not a standing permission to accept another message from the
same key, a new signature under the same ID, or a first-seen expired frame.

The retained basis must identify the exact compact JWS, signed profile,
governed namespace and authenticated principal, issuer name and the issuer key
used to verify the certificate, certified message key, addressed recipient and
resolved context, and the successful verification conditions and local time.
For an accepted reserved diagnostic, retain its independently resolved local
recipient, original scope/route and exception basis under
[retained diagnostic identity](diagnostics.md#retained-diagnostic-identity);
`unverified` is not a principal or an arbitrary shared context.
Those conditions include the applicable issuer/key naming-authority basis.
A representation may reference equivalent trusted local state rather than copy
every value; it must preserve the same distinctions. Retain the disposition
separately: prior verification alone does not mean the message was accepted.
Context lookup and comparisons must not use a sender-asserted earlier time as
evidence of prior verification.

An approval originator retains its exact issued request and its valid issuance
basis when it creates the pending request. It checks the credential/key/profile
used for issuance and records its own principal and addressed peer/context.
This is knowledge of issuance, not proof the peer received or accepted it.
The decision maker independently authenticates the incoming request before
retaining it. Neither participant may substitute the other's unverified
assertion for its own required observation.

Keep this basis through the pending exchange and the relevant terminal and
duplicate-retention lifetime while claiming that context remains live. A
receiver unable to retain a new message's required state must refuse as `busy`
before acceptance within an otherwise valid scope. Loss or retirement of the
required context instead disables admission under the selected profile; it is
not ordinary backpressure. Core does not require durable storage or restoration
after loss; missing state cannot be reconstructed merely from an old decision
or an expired request. A stronger restoration profile must establish both exact
bytes and their trusted verification basis, with the other required context,
before reopening admission. Retiring a scope does not erase historical
acceptance where records remain, but neither does it provide a feedback route
through the retired scope.

New messages require current admission and authorization. Relevant trust or
compromise information may cause current policy to reject new uses of earlier
evidence or prevent a pending action. Retained authentication is an observation,
not irrevocable trust, cached permission, or a grant's revocation rule. The
[duplicate rules](messaging.md#exact-retained-copies-and-expired-credentials) determine the limited
handling of exact copies with a retained disposition.

## Approvals

An `approval` requests authority for the exact action it describes. Its message
UUID is the approval's identity. It carries `action`, `reason`, `risk`,
`deadline`, and `bound_required`. It is an [independent exchange](approvals.md),
whose authenticated originator owns its lifecycle regardless of conversation
role. Correlation with work neither transfers authority nor determines expiry.

A `decide` names that approval in `in_response_to`, carries `approve`, and may
carry a `note`. When `bound_required` is true, `request_digest` is required. It
is the base64url SHA-256 digest of the approval's exact JWS compact string.

First apply the binding's audience and conversation continuity guards, then
the exact retained-copy rule to an eligible repeated decision inside the valid
scope. It cannot become a new decision and its disclosure requires an authorized route.
For a new decision, apply ordinary verification and structural checks, scoped
identity-conflict handling and current authorization. Resolve its approval under the
[approval state rules](approvals.md#decision-and-terminal-state). An unknown
request within that established scope is `unknown`, a known message of another kind is `malformed`, and an
approval originated by someone other than this receiver is `not-authorized`.
Resolve the request in the addressed conversation and its intended authority
relationship. An already terminal owned approval is `closed`. Identical
accepted duplicates retain their established disposition. For a pending request,
use the originator's retained exact request and valid issuance basis. Do not
require its original credential to remain unexpired at decision time, replace
its certificate, or re-sign it. The incoming decision is a new message and must
pass current verification. Then check:

1. The decision names the approval, and any required or supplied digest matches
   its signed bytes. Refuse a mismatch as `wrong-request`, or a missing required
   digest as `unbound-decision`.
2. The decision's `sent_at` is no later than the approval's deadline, compared
   under the [exact timestamp rules](timestamps.md#exact-values-and-signed-identity).
   If it is later, refuse as `closed`. Invalid timestamps fail structural checking
   before this comparison. The approval owner also enforces the live deadline on
   its own clock; the sender's timestamp cannot reopen a closed approval.
3. The signer is authorized to decide, and no different decision has already
   been accepted in this context. Refuse as `not-authorized` or `closed`
   respectively. The decision cannot create or restore its own approval.

A repeated copy of the same decision follows normal duplicate handling; it
does not become a second decision. Preserve accepted approval and decision
state for the live context. Core makes no restart-survival promise. State loss
must disable old-scope admission under the selected profile, not turn an old
decision into fresh authority or a semantic refusal in replacement state. An
explicit restoration profile can strengthen this lifetime. No application-specific
approval policy is defined here.

Only the authenticated originator may issue `closed` for its question or
approval. Check ownership independently of the signer's conversation role;
knowledge of an id is not authority to close it. Within an established scope
whose admission guard remains valid, an unknown target can receive
only the scoped provisional marker defined by [owner-issued closure](approvals.md#owner-issued-closure).
It cannot establish a missing scope, close another principal's request or establish a grant. Closure
ownership and reason checks apply before recording the terminal state.

A decision's grant, its acceptance, and execution of the authorized action are
distinct claims. `closed: decided` alone proves neither a grant nor execution.
Request expiry limits decision acceptance; grant validity, use limits, and
revocation follow separately specified authorization semantics. Closure does
not retroactively revoke an accepted grant.
Retirement of its conversation admission scope likewise does not withdraw an
approval, revoke a grant or establish that admitted effects ceased.

## Evidence and acting for another principal

A message may carry `on_behalf_of` and signed core messages as `evidence`.
The authenticated signer remains responsible for the message. Naming another
principal does not authenticate that principal or confer its permissions.

Evidence remains byte-for-byte unchanged. Establish its signed profile, signer
and original recipient context independently of the enclosing message. Its
original recipient need not be the enclosing recipient. A verifier may inspect
the original address as evidence; it must not rewrite that address or pretend
the artifact was a new request to itself.

| Evidence case | Permitted basis and limit |
|---|---|
| First seen while its credential is currently admissible | Verify the original signature, certificate/profile and addressing context; this proves current admissibility, not its actual historical creation time |
| Exact artifact previously authenticated by this participant | Use the retained authentication under the applicable live context; do not infer fresh permission or portable historical proof |
| First seen after expiry or without an admissible authentication basis | It is unestablished evidence in core; report that limit rather than infer historical validity from `sent_at` |
| A stronger historical/receipt agreement explicitly applies | Apply that agreement's trust, time, access and failure rules; core defines no such receipt format or service |

Mathematical signature verification can succeed after credential expiry, but
alone does not establish pre-expiry existence or trustworthy historical use.
An untrusted receipt time does not supply that missing fact. If an operation
requires evidence whose authentication cannot be established, refuse the
requested authority as `not-authorized` without executing it; do not invent a
new approval or silently weaken the requirement. An inspection operation may
return an explicit unestablished-evidence assessment under its own contract.

Never process attached evidence as a new request. Authority inferred from it
remains subject to receiver policy and the declared application contract.
Core defines no portable scoped-grant format. Applications define the authority
required at the effect boundary; see the [network guide](../docs/network-development.md#obtain-permission-and-enforce-effects).

## Limits of the proof

A signature binds bytes to a certified key. It does not establish the truth of
the content, the quality of an actor's work, or what a user interface displayed.
Signing does not encrypt content. Compromised keys or trust anchors undermine
the identities they certify. Availability under hostile traffic is not supplied
by message signatures.

## Credential lifecycle and deployment obligations

A deployment must establish who may enroll each principal, how receivers obtain
authentic trust configuration, and who protects and may invoke signing keys.
A downloaded trust anchor does not authenticate its own source. Provider
endpoint configuration and authenticated transport, or another explicitly
trusted provisioning method, establish that source. Development certification
facilities are not production enrollment policies. Non-exportable keys limit
extraction but do not prevent misuse through an authorized signing interface.

Issuers set credential lifetime and renewal eligibility independently of
application deadlines. A long approval must not automatically extend a general
identity credential. Renewal may reuse a key; rotation changes a key. Neither
action alone invalidates an older credential. A sender uses a current credential
for a new message and retains the original signed bytes of existing messages.

The deployment must state its maximum intended response window after principal,
key or issuer compromise; how renewal is stopped; how relevant receivers learn
denials or revocation; and what happens during disconnection or status-check
failure. Core supplies credential expiry, not a revocation service or immediate
invalidation guarantee. Receiver policy may deny a principal while leaving its
other historical identity claims intact. Selective key/credential invalidation
requires an explicitly applicable rule. Short expiry bounds exposure only when
the attacker cannot keep obtaining fresh credentials.

Trust configuration updates must follow [identity continuity and rotation](#identity-continuity-and-rotation).
An issuer/key rotation is different from changing a principal's owner or name.
A policy change may prevent future actions without making an earlier acceptance
or effect cease to have happened.

Clocks used for admission and live deadlines must meet the declared operational
accuracy. A deployment relying on an authenticated session must also state how
existing and resumed sessions respond to expiry, revocation and policy changes.
An old session or retained verification fact does not bypass current action
authorization. Core selects no sign-in provider, key store, refresh protocol,
maximum certificate lifetime or mandatory online status dependency.

## Authorization and effects

The effect owner must enforce the authorization applicable to the actual action
and resource, or explicitly delegate that enforcement to a trusted deputy.
When enforcement is delegated, the deputy's signature identifies the requester;
it does not independently prove that the deputy followed its policy. An
executor requiring independent assurance must check authoritative policy/state
or a grant under a separately established authorization contract.

Applications must define approval action meaning precisely enough for their
intended use. Where automated enforcement depends on an exact candidate,
operation, resource or environment, bind and validate those identities under
that contract. Human-readable `action` content alone supplies no universal
machine-executable grant vocabulary. Use digest-bound decisions where the
authorization contract requires exact signed-proposal evidence. An unbound
decision remains a signed, context-correlated decision; it has a weaker
portable binding and must not be advertised as digest-bound evidence.

Permission validity, use limits, delegation and revocation belong to the grant's
contract. The effect owner checks those conditions at use and owns any required
use accounting. Consequential applications must declare whether duplicate
effects are prevented by authoritative operation state/idempotency, reconciled,
or left uncertain after state loss. An `ack`, signature, grant or recovered
conversation alone does not establish exactly-once external effects.

## Confidentiality, human and model boundaries

Signed content is readable to anyone possessing its frame. The sender and
deployment must establish a trustworthy mapping from the intended recipient to
the endpoint, validate its transport identity and trust any TLS termination.
A signed `to` prevents a conforming wrong recipient from accepting the request;
it does not prevent disclosure to an incorrectly selected endpoint. See the
[binding's response-audience rules](bindings.md).

Access to evidence, history or a message does not imply permission to disclose
it to another actor, a model provider or a different human. The application
owns that access/disclosure policy and storage protection. A human-facing
approval implementation must faithfully present the action it asks the person
to decide; the protocol does not prove what the interface displayed or the
person understood.

A reasoning integration owns permitted model inputs, available capabilities,
output validation and mediation of proposed actions. The actual effect boundary
must enforce its authority constraints independently of persuasive content.
An actor's signed model result establishes attribution, not correctness or
permission. Multiple actor names or signatures do not establish independent
review if their keys, host, operator or reasoning inputs share a compromise
boundary. Applications claiming independence must supply that protection.

## Resource limits and controlled failure

Bindings must enforce their frame-size bound before unbounded decoding or
cryptographic work. Receivers must bound parsing, cryptographic input sizes,
evidence verification work and retained state. Authentication does not exempt
a peer from admission, pending-exchange or expenditure limits. Deployment policy
owns traffic/connection budgets, concurrency and model/external-service spend.
The applicable binding or deployment must make its limits and failure behavior
available to its participants; core does not prescribe a scheduler or cache.

Malformed inputs must produce the defined controlled rejection, not escape as
an unhandled verification failure. Exhaustion must never count unchecked
evidence as valid. If a valid retained scope lacks capacity for a new message,
refuse as `busy` before acceptance. Already accepted state must not be silently evicted
while claiming its context and guarantees remain live. If state is lost, the
selected profile's admission guard must reject old-scope traffic before semantic
handling; `busy` or `unknown` cannot substitute for that boundary. Retirement
must invalidate admission before required state is discarded. Continuation
cannot be claimed without the applicable profile's required retained or restored
interpretation. Required history/retention claims must state
their failure boundary rather than assume unlimited storage.

## Standards used

| Standard | Purpose |
|---|---|
| RFC 7515 | JWS compact serialization |
| RFC 7518 and RFC 8037 | ES256 and Ed25519 signatures |
| RFC 8785 and RFC 7493 | Canonical JSON and interoperable JSON values |
| RFC 7519 | Certificate JWTs |
| RFC 7638 and RFC 7800 | Binding a certificate to a public key |
