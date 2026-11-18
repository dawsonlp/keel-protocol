# Identity, authentication, disclosure and effects

**Disposition:** signed-message security adopted; portable scoped grants not adopted.
**Subjects:** identity; naming authority; authentication; authorization; evidence.

## Decision

Use certified signed messages, receiver-owned authorization and retained
authentication of exact artifacts. Apply a closed credential and envelope profile
rather than accepting unspecified JOSE variants. Canonical signed bytes and the
original compact JWS establish message identity; retries and credential renewal
must not rewrite an existing message or approval binding.

Retain governed `actor:<name>` and `party:<id>` principals. Each trusted issuer/key
has explicit authority over the names it may certify. Trust in an issuer alone
does not authorize the whole namespace. Deliberate overlap is a governance choice;
independent collisions cannot silently merge identities or permissions.

Keep authentication, current action authorization, permission and actual effects
separate. The effect owner enforces authority, including explicit deputy trust
and binding to the requested action where required. A signed reference or evidence
attachment does not itself confer authority, and attached evidence is not a fresh
request to execute.

## Exact retained artifacts and disclosure

A previously authenticated exact copy can retain its established disposition
after ordinary credential expiry, under the required live scope and verification
precedence. It does not gain a new effect or deadline. A fresh decision uses
current credentials and authority while binding the unchanged retained approval.

Recognizing bytes does not establish the carrier's right to receive a response.
Prior-disposition feedback requires an independently authorized route and current
disclosure policy. Eligible feedback is minimal; it does not replay cached results
or grants. Failed route guards must not reveal whether state was retained.

An unseen expired artifact does not acquire earlier authentication from its own
timestamp. Historical verification requires its own established evidence basis.
Retained local authentication is not automatically portable historical proof.

## Basis and limits

These distinctions prevent attribution from being mistaken for authority, exact
copies from becoming retrieval credentials, and stored messages from becoming
invented proof of an earlier event. Issuer-qualified wire identities and feedback
to any carrier of matching bytes were not selected.

Confidentiality, bootstrap, compromise response, resource protection and suitable
human/model interfaces have deployment owners. Signing does not encrypt content,
prove what a human saw or establish the truth of an actor's output. Logical actors
in one process are not automatically independent compromise domains.

Portable scoped grants were considered but no wire format, placement or extension
contract was adopted. Application-specific permission requirements remain valid;
a generic grant service is not a core prerequisite.

## Current authority and related decisions

[Security](../../core/security.md), [credential profile](../../core/security-profile.md),
[bindings](../../core/bindings.md) and [retained-copy handling](../../core/messaging.md#exact-retained-copies-and-expired-credentials)
are authoritative. See [work and authority](work-and-authority.md) for approval
ownership and [recovery ownership](recovery-and-service-ownership.md) for history.
