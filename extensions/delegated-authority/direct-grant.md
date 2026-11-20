# Signed direct grant

**Artifact identity:** `keel-direct-grant-v1+jws`. **Decoded schema identity:**
`urn:keel-protocol:direct-grant:1`. The artifact is used by the optional
[provisioned direct grant profile](provisioned-direct-grant.md).

## Representation

A grant is an immutable JWS compact ASCII string of at most **16 384 bytes**.
Reject larger inputs before splitting or decoding. The protected header contains
exactly `typ` (the artifact identity above) and `alg` (`EdDSA` or `ES256`). Both
header and claims must be exact RFC 8785 JSON, using the encoding, compact framing,
JSON value restrictions, key types and signature representations in the
[core credential profile](../../core/security-profile.md#encoding-and-cryptographic-input).
Every verifier supports both algorithms. Use only the matching configured key.
Verify the exact received compact signing input. Reject an unsupported header,
noncanonical part, invalid signature, unknown member or extra compact part.

The claims object contains exactly these members. The
[schema](direct-grant.schema.json) describes shapes. Validate exact lexical values,
canonical encoding, calendar dates, bounds and trust as specified here.

| Claim | Meaning and validation |
|---|---|
| `iss` | Exact governed issuer principal, `party:` or `actor:` |
| `id` | Canonical lowercase RFC-variant UUID of version 1–8, scoped to issuer in the configured namespace |
| `subject` | Exact governed represented principal, `party:` or `actor:` |
| `holder` | Exact governed requester principal of kind `actor:` |
| `holder_jkt` | RFC 7638 SHA-256 thumbprint of the holder's core public JWK. Canonical unpadded base64url encoding of exactly 32 bytes |
| `audience` | Exact governed principal of the one receiving actor |
| `permission` | Object with exactly `contract` and `parameters`. `contract` is an exact string of 1–128 ASCII characters from `[A-Za-z0-9._:/@+-]`, resolved in the receiver's governed configuration. `parameters` is a JSON object understood in full by that contract |
| `not_before` | Inclusive start of the grant's use interval, in the core timestamp profile |
| `expires_at` | Exclusive end of that interval, in the core timestamp profile. Strictly later than `not_before` |

Limit nesting in claims to **16** object or array levels, with claims at level 1.
Enforce this bound during parsing or with a parser that cannot exhaust unbounded
stack before detecting it. Canonical verification and permission interpretation
must apply only to bounded data. The permission contract must bound its own work
and reject unknown parameters, criteria or accounting semantics. No parameter can
extend the proof profile, confer onward issuance rights or direct verification
to an untrusted discovery endpoint. A derivation path is a different proof type.

## Verification and authority

1. Apply the size and structural limits, the protected-header checks and the
   claims schema. Apply real calendar and exact-value checks under the
   [timestamp profile](../../core/timestamps.md). Reject a noncanonical
   `holder_jkt`, including a valid-length string with nonzero unused bits.
2. In the independently established namespace, select candidate issuer keys by
   exact `iss` and the supported algorithm. Candidates come only from current
   deployment configuration and the deployment must bound how many it installs
   for an issuer. Verify the signature and identify exactly one distinct authorized
   verifying key. Reject an absent or ambiguous match.
   Its own rule must authorize this subject, audience, permission contract and
   every conferred parameter. Later setup also checks the holder and policy for
   the particular conversation. Naming certification confers no grant authority.
   A signature verified by one key cannot use another key's issuance rule.
3. Compare time with the receiver's current clock. Require
   `not_before <= now < expires_at` and require the interval length to be at most
   the receiver's configured positive maximum grant lifetime. Apply both checks
   exactly, with full microsecond precision. The core credential allowance of
   30 seconds applies only to core credentials. Deployments must document clock
   accuracy and a maximum lifetime consistent with their revocation tolerance.
4. Apply current local disqualification, including denial of the grant ID,
   issuer/key or holder/key. No remote status lookup is required. Offline
   verification can continue up to expiry in the absence of known local denial.

The issuer key is authenticated through configured issuer/key authority, without
an enclosing identity certificate. Validation establishes current use only.
Claims contain no issuance timestamp. A receiver cannot infer historical
issuance validity from the use interval. Reusing retained signature verification
requires exact grant bytes and the original verifying key. Recheck its current
authorization, grant interval and current local denials for every new protected
admission. An explicitly retained old key can remain authorized during rotation.
Removing its authority or denying the key prevents new protected use.

An issuer must never issue different compact bytes for the same grant ID in its
namespace. If a verifier has authenticated different bytes for that identity,
it must reject the conflicting artifact for setup and prevent new protected use
of that identity wherever the conflict is known. This requires no permanent global
registry. Never replace established bytes within a live scope. A denial keyed by
issuer and ID covers all spellings of that identity. Authority remains subject to
the independent route, message identity and lifecycle checks of the integration
profile.
