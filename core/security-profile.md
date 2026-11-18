# Credential and signed-envelope profile

This is part of the core contract. It specifies the exact representations and
validation conditions used by the [security verification order](security.md#verification-order).
The core's signed type and compatibility identity are stated in
[signed bytes](security.md#signed-bytes) and [version and extensions](asking-contract.md#9-version-and-extensions).
This document defines no issuance service or credential-status protocol.
It also supplies no conversation-establishment or restoration mechanism. The
selected [continuity profile](continuity.md#selecting-a-usable-profile) must
establish a valid admission scope independently of credential validity.

## Closed representations

This profile permits only the members listed below. Unknown members in the
protected headers, credential claims, confirmation object or public JWK are
invalid; they are not extension metadata. In particular, `crit`, `b64`, `jku`,
`x5u`, `kid`, `aud`, `nbf` and private key members are not supported in these
objects. Reject them rather than silently ignore possible restrictions.
A different credential/profile contract must be explicitly identified and
supported before using additional semantics. Core payload `metadata` keeps
its separate ignorable-annotation rule.

| Object | Exact permitted members and conditions |
|---|---|
| Message protected header | `typ`: the core signed type; `alg`: `EdDSA` or `ES256`; `jwk`: public JWK below; `cert`: nonempty compact certificate JWT string |
| Certificate protected header | `typ`: `keel-cert+jwt`; `alg`: `EdDSA` or `ES256` |
| Certificate claims | `iss`: nonempty string matching a configured issuer; `sub`: a principal that issuer is authorized to certify; `iat`, `exp`: times below; `cnf`: confirmation object |
| Confirmation object | `jkt`: canonical unpadded base64url of exactly 32 bytes, the SHA-256 RFC 7638 thumbprint of the certified public JWK |
| Ed25519 public JWK | `kty`: `OKP`; `crv`: `Ed25519`; `x`: canonical unpadded base64url of exactly 32 bytes |
| P-256 public JWK | `kty`: `EC`; `crv`: `P-256`; `x`, `y`: canonical unpadded base64url of exactly 32 bytes each, encoding a valid point on that curve |

Principal grammar is the [payload schema's principal definition](schemas/keel-v1.schema.json):
`^(party|actor):[A-Za-z0-9._@+-]{1,128}$`. The subject must be a string matching
that entire grammar, with no leading/trailing characters or newline. Do not
use a regex mode in which `$` permits a match before a final newline.
`unverified` is a restricted response destination, never a
certifiable principal. Trust configuration binds issuer names to permitted
keys and explicit naming authority under [governed names](security.md#governed-names-and-issuer-authority);
it is not discovered from arbitrary URLs in a frame. Certificate admission
requires one permitted issuer-name, verifying-key and subject association.
An absent subject-authority rule permits no names; another key's subject scope
cannot complete the association. Naming-authority failure is `certificate-invalid`.
Multiple configured keys for one issuer may be checked within the deployment's
resource bounds; a successful check must preserve which authorized key and
naming scope established it. This adds no `kid` header or other wire field.

The certificate's algorithm must be accepted for its configured issuer key.
The message algorithm must match its public key: Ed25519 uses `EdDSA`; P-256
uses `ES256`. Neither symmetric algorithms nor `none` are accepted. Both
supported algorithms must be verifiable; a signer may use either.

## Encoding and cryptographic input

Both compact objects have exactly three nonempty parts separated by two dots.
Each part uses the base64url alphabet without padding, whitespace or alternate
encodings. Decoding and canonical re-encoding must reproduce the part exactly.
Empty, extra or malformed parts fail the applicable framing check.

JSON must be valid UTF-8 with no duplicate object members, invalid Unicode
scalar strings, nonfinite numeric values or integral-valued numbers outside
±(2^53−1), including exponent or fractional notation whose parsed numeric value
is an integer. Such values must be represented as strings in message data.
The bound applies to the parsed numeric value, not the spelling of its JSON
token; implementations must not disagree based on integer/float runtime types.
Booleans are not numeric dates. A JSON header or certificate-claims
value must be an object. Certificate/header JSON need not be RFC 8785 canonical;
the transmitted bytes remain the signing input. The core message payload must
be exactly the RFC 8785 canonical encoding of its JSON value. Its structural
requirements are checked after authentication as defined by asking.

JWS signing input is the ASCII protected-header part, a dot, and the payload
part. Both signature forms are exactly 64 decoded bytes. Ed25519 verification
follows RFC 8032/8037. ES256 uses raw 32-byte unsigned `r` followed by 32-byte
unsigned `s`, checked by P-256 ECDSA/SHA-256; DER encoding is not accepted.
An invalid signature or decoded signature length fails signature verification;
invalid base64url framing fails earlier. Do not treat a verifier exception as
successful validation or allow it to escape the defined controlled rejection.

The certificate's public-key binding uses RFC 7638's required public members
only. This closed JWK profile permits exactly those members. A valid certificate
signature and matching subject are insufficient if its thumbprint does not
match the message key. A copied public certificate cannot certify another key.

## Credential times

`iat` and `exp` must be finite JSON numbers, not strings, booleans or null.
They are JWT NumericDate seconds. Require `exp > iat` and `iat <= now + 30`.
The latter is an explicit core issuance-time sanity rule, not an assertion that
generic JWT `iat` has not-before semantics. Fail these profile conditions as
`certificate-invalid`.

For a first-seen message, accept the expiry condition only while
`now < exp + 30`. At equality or later, return `certificate-expired`.
This is the fixed clock allowance for credential admission; it does not add
30 seconds to an approval's decision deadline. Issuers may impose tighter
issuance lifetime rules through deployment policy, but a receiver must not
silently claim a larger core expiry allowance.

Use the receiver's current clock for admission. A sender's `sent_at` cannot
backdate credential validity. [Retained authentication](security.md#retained-authentication)
and exact duplicate disposition are separate from admitting a first-seen frame.

## Failure classification

Apply the security document's ordering, including the binding's audience guard
and the applicable conversation continuity guard before retained-state feedback
or semantic admission. Invalid scope uses its profile's binding rejection,
without a core disposition or message-ID reservation; it is not an unknown
message reference. Within the valid applicable scope, a later verification
failure must not replace the first applicable reason. In particular:

| Fault | Classification |
|---|---|
| Outer compact framing/base64url, protected-header syntax/type/member set, unsupported outer type/algorithm, malformed public JWK or invalid P-256 point | `malformed` |
| Otherwise valid supported public key paired with the other accepted message algorithm | `algorithm-key-mismatch` |
| Nested certificate framing, JSON, member sets, type, claims, time sanity, issuer/naming authority, issuer-key algorithm or certificate signature | `certificate-invalid` |
| Otherwise valid credential at or after `exp + 30` | `certificate-expired` |
| Valid credential certifies a different message key thumbprint | `key-not-certified` |
| Well-framed message whose signature fails, including wrong decoded length or DER ECDSA | `bad-signature` |
| Signed payload with invalid JSON/Unicode/numbers/duplicate members or noncanonical RFC 8785 bytes | `not-canonical` |
| Otherwise authenticated payload not addressed to the intended recipient/context | `not-addressed-to-me` |

Malformed certificate input always belongs to the certificate check, rather
than escaping as an outer parser error. Invalid deployment trust configuration
must fail closed as configuration failure; it cannot broaden accepted issuers,
subjects or algorithms. Payload-version, schema, authorization and lifecycle
checks follow the applicable core rules. Exact retained duplicates have the
narrow handling described in [messaging](messaging.md#exact-retained-copies-and-expired-credentials).
That handling remains inside the valid applicable scope; retained authentication
does not reopen a retired context or make an expired first-seen frame admissible.
After the applicable binding guards pass, an absent or wrong-type `to`, missing
intended principal, or mismatched required conversation fails addressing as
`not-addressed-to-me` before payload schema validation. This fixes the result
even if the payload has other structural
faults. Reserved `unverified` responses follow the explicit
[diagnostic receiving exception](diagnostics.md#receiving-and-associating-a-diagnostic);
the value cannot satisfy ordinary principal addressing or bypass the original
route/scope guard. First-seen diagnostics still require all other verification
and restricted structural checks. Eligible exact controls retain exact-copy precedence.

These failure classifications do not require a reply to invalid controls.
[Control-response termination](diagnostics.md#control-response-termination)
forbids core replies to recognizable `ack`/`refusal`, while retaining their valid
local effects. It uses binding rejection for frames that bounded parsing can
identify as neither a recognizable control nor a known core non-control kind.
No failed frame
can establish identity, reserve its claimed sender's ID or create a context.

## Standards basis

The closed field sets, issuance-time sanity rule and fixed allowance above are
Keel profile choices. JWS defines protected signing input and critical-header
handling; JWT defines expiry; JWT best practices require distinct, unambiguous
validation rules for token uses. These standards do not define Keel permissions
or approval lifetimes.
[RFC 7515](https://www.rfc-editor.org/rfc/rfc7515.html#section-4.1.11),
[RFC 7519](https://www.rfc-editor.org/rfc/rfc7519.html#section-4.1.4),
[RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html#section-3.12)
