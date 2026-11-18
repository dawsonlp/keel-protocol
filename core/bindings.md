# Bindings

A binding carries complete signed frames to opaque addresses and returns
responses. It names the contract and revision it carries and declares its frame
limit. Participants must share a binding and the same core definition to
interoperate. Conversation traffic also needs an explicitly selected
[continuity profile](continuity.md#selecting-a-usable-profile). Resolving or distributing
addresses is outside the core.

A binding must not alter a message. Its sender may lose contact without knowing
whether a frame arrived. It must expose reachability so retries can be held
while delivery is unavailable. Loss, duplication, delay, and reordering must
preserve the [messaging rules](messaging.md).

Both conversation roles can send approvals and owner-issued closures. Direction
or message kind alone therefore cannot identify the conversation actor. Apply
the [context-routing rules](messaging.md#conversation-context-routing), including
fresh keys for distinct conversations between the same pair of principals.
An open connection alone supplies no additional context discriminator. A selected
profile can provision an authorized association to that actual connection.

If a deployment serves isolated governed namespaces, the applicable namespace
must be independently established by its trusted deployment/binding context
before resolving principal names or retained state. An issuer claim or an
otherwise ambiguous actor address cannot select another namespace. See
[governed names](security.md#governed-names-and-issuer-authority).

Return routes belong to the binding. A permitted diagnostic for an unverifiable
known non-control frame is sent only on its independently authorized incoming
route, addressed to `unverified`. The [diagnostic contract](diagnostics.md)
defines its restricted shape, receiving exception and attempt association.
Never trust a return route asserted by an unauthenticated payload. Controls
receive no core reply; unclassifiable frames use binding rejection.

Only an authenticated message establishes a peer's principal. An acknowledgement
from an unrelated principal cannot confirm the intended receiver's acceptance.
The binding must not substitute a transport connection's identity for the
certificate in the message.

## Response audience and confidentiality

Authenticating signed bytes identifies their signer; it does not establish who
currently controls the connection that delivered a copy. TLS server
authentication protects delivery to that server, but does not by itself bind
the client connection to the message's certified principal.

Before sending application content, cached results, evidence, detailed refusals
or queued/new notifications, the binding/deployment must establish that the
route is authorized to receive them for their signed recipient. This may come
from an explicitly provisioned trusted endpoint, authenticated client/session
mapping, or another agreed binding-level audience guarantee. Such assurance
governs disclosure, not permission to bypass message signatures or action
authorization. The address mapping and any TLS termination must be trusted.

Do not register or replace a confidential return route merely because a frame
was validly signed, matched a retained ID, or arrived on an open connection.
This applies to first-seen captured frames as well as retries. Without audience
assurance and current disclosure authorization, do not reveal a retained
disposition, even in a minimal control. A minimal control carries only
the normal signed envelope/payload identity fields, optional request correlation,
and `ack` or a refusal reason; it has no `detail`, content, evidence, metadata
or application data. It reports no cached result or grant. Returning even this
limited information is subject to the applicable disclosure policy and the
[exact retained-copy rule](messaging.md#exact-retained-copies-and-expired-credentials).

Perform the route/disclosure guard and the selected conversation scope guard
before selecting any state-dependent response. Scope establishment and admission
follow [the continuity contract](continuity.md#establishment-and-admission).
Untrusted bounded sender/context selectors may select an already configured
route policy; they must never establish identity or grant access. A route that
fails this guard gets the same generic rejection whether the presented frame
is an eligible retained copy, first-seen, or expired: this WebSocket profile
closes with 1008 and sends no core disposition. Do not reveal a retention hit
by returning `certificate-expired` for the miss and a different response for
the hit. Input framing/size rejection remains separately allowed. This rule
does not promise constant-time processing or hide network traffic patterns.
After authentication or trusted retained-copy lookup, require the actual signer,
profile and context to agree with that independently assured route policy.
A selector must not borrow another principal's or context's audience assurance.
Where fixed independent binding policy already assures a route, permitted
malformed-frame diagnostics may use it; parsing untrusted selectors never
creates that assurance.

If required response-audience assurance cannot be established, reject that
delivery at the binding boundary before admitting a new exchange that would
require protected content. For this WebSocket profile, close with code 1008.
This is not a terminal semantic refusal of the signed message: do not reserve
its ID, create an accepted context, or overwrite a retained disposition. A
captured first-seen copy on an unassured route must not poison later delivery
from an authorized route. Connection failure alone still proves no outcome
to the sender. If assurance is subsequently lost, hold protected outbound traffic
and report delivery uncertainty; do not reroute it to an unverified connection.
An explicitly authorized retrieval/recovery operation also needs this assurance.
Core selects no new challenge message, public handshake, or identity service.
The [provisioned-context profile](profiles/provisioned-context.md) specifies
trusted setup at both endpoints without adding a core message kind.

## Diagnostic routes and control failures

A diagnostic's absent conversation field does not establish a new actor-level
route or bypass a guard for its original conversation traffic. Capture the
actual connection and independently authorized peer/local recipient and scope
association when the frame arrives. Keep that association through callbacks and
queuing; an echoed ID cannot supply another route or revive a retired scope.
The [receiving rules](diagnostics.md#receiving-and-associating-a-diagnostic)
require unique association before any outgoing-message effect. An unassociated
notice cannot acquire that effect by borrowing the current sending slot.

Never send a core reply to recognizable `ack` or `refusal`, even when invalid.
Only if bounded parsing can identify neither a recognizable control nor a known
core non-control kind is the frame unclassifiable. Use generic WebSocket 1008
for that case after the existing size/type rules, without a core response or
identifying close-reason details. If its original connection is already closed,
discard the queued frame. Earlier audience/continuity failures keep their
required binding outcomes. Apply rejection only to the captured original route,
never a replacement connection. Other handling and presentation of recognizable
invalid controls is local policy within these constraints.

## WebSocket profile

This profile supplies one concrete transport for independent implementations.
It must be paired with an applicable continuity profile for conversation admission;
the subprotocol alone does not select one. Other bindings need an equally precise
shared definition.

| Property | Rule |
|---|---|
| Address | A configured WebSocket URL; actors do not require any particular URL path |
| Subprotocol | `keel.core.v1`, selecting standalone core/1; the definition remains unreleased |
| Transport security | TLS is required except on loopback |
| Message boundary | One text message carries exactly one JWS compact string, at most `frame-limit` UTF-8 bytes |
| Unsupported data | Close a binary message or invalid frame type with code 1003 |
| Excess size | Close a message exceeding `frame-limit` with code 1009 |
| Controls and unclassifiable frames | No core replies to recognizable `ack`/`refusal`; generic 1008 for unclassifiable frames after size/type handling, under [control-response termination](diagnostics.md#control-response-termination) |
| Return route | The connection on which the frame arrived |
| Reachability | The connection is open; while it is unavailable, hold retries without consuming attempts |
| Authentication | Apply current verification to first-seen messages and the exact retained-copy rule to eligible duplicates; the handshake grants no application authority |
| Response audience | Establish recipient-bound route assurance before protected outbound content; a bare server-authenticated WebSocket plus a valid request signature is insufficient |
| Conversation admission | Explicitly establish a compatible continuity profile and its scope; apply its guard before retained-state feedback and semantic handling |

A requester may reconnect with backoff. Reconnection alone establishes only
transport reachability, not retained conversation state. Retries with the same
identifiers remain valid only within established context continuity. Core makes
no promise of reattachment, missed-reply replay, or resumption after state loss.
Do not automatically resubmit uncertain work on the assumption that it failed.

The concrete `keel.provisioned-context.v1` profile binds one freshly allocated
conversation to one actual authenticated connection. Its scope ends on connection
loss or local retirement; a new connection requires new provisioning and a fresh
conversation key. It rejects absent, unready or retired scopes with generic 1008
and no core disposition or ID reservation. A profile that supports retained
reconnection or restoration must define its own precise establishment and
admission mechanism; it cannot be silently substituted under this profile name.

Either side may send a WebSocket ping. Close an idle connection if it has no
traffic and no reply to a ping for 60 seconds. Connection failure is evidence
about reachability, not evidence that a request was not performed.
