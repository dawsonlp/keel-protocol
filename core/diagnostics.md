# Verification diagnostics and control responses

This is part of the core contract. It defines the reserved `unverified`
recipient, receiving and associating verification diagnostics, and termination
of control-response exchanges. It adds no message kind, frame digest, attempt
identifier, setup protocol or recovery service.

A **semantic refusal** reports a disposition under ordinary core admission
rules. A **verification diagnostic** reports that a delivered frame failed
verification. Its echoed correlation was read from untrusted input and does
not prove rejection of the exact originally signed message. Neither a lost
reply nor a diagnostic can establish that an earlier copy did not execute.

## Control-response termination

`ack` and `refusal` are controls. Never send a core message in response to a
recognizable control, whether it is valid, invalid, expired, unmatched,
ambiguous, conflicting, or an exact retained copy. Controls occupy no sending
slot and have no acknowledgement or automatic retransmission obligation.
This does not suppress the valid control's defined local effect, such as
confirmation by an ack or backoff after an ordinary `busy` refusal.

Use bounded parsing to classify the frame's payload kind into a recognizable
control, a known core non-control, or an unclassifiable frame. Recognizable
controls follow the preceding no-reply rule and their validated local effects;
they are not unclassifiable merely because they are controls. Such untrusted
classification can suppress a reply, but cannot
authenticate the frame, authorize work, select a recipient, create a context
or reserve a message ID. Duplicate/ambiguous kind members, unreadable payloads,
unknown kinds, or any other inability to identify unambiguously either a control
or a known core non-control make the frame unclassifiable and do not authorize
a diagnostic reply. A receiver must not guess that an
unclassifiable frame was a request merely to respond to it.

For unclassifiable frames use the binding rejection, without a core response.
Admit no message, reserve no claimed sender ID and overwrite no retained disposition.
For the WebSocket binding, after its existing size/type handling, close the
delivery's original connection with generic **1008**, without identifying
close-reason details; if already closed, discard the frame. Never close or
mutate a replacement connection because an old queued frame failed.

For a recognizable invalid control, discard it without applying its claimed
control effect or returning a core response. Earlier applicable framing,
audience or continuity failures still require their binding outcomes. Local
logging, presentation and additional connection-retirement policy belong to
infrastructure; none may weaken those earlier guards. A failure retains its
specified classification even when no refusal is sent.

For a known non-control kind, apply the ordinary guards, verification and
admission checks. A failure uses the response defined by those rules when
permitted by the earlier guards. This distinction prevents ordinary control-response chains; it is not
a guarantee against arbitrary hostile traffic or deliberate frame rewriting.

## Sending a verification diagnostic

A frame failing a check in the [verification order](security.md#verification-order)
has not passed ordinary message admission. When a diagnostic is permitted,
send a fresh signed `refusal` only over that frame's incoming route, addressed
to `unverified` with no conversation. Do not trust a return route, sender,
namespace or authority asserted by the failed frame.

The route must already satisfy the [audience guard](bindings.md#response-audience-and-confidentiality)
and applicable original scope guard. Failure of either guard uses its uniform
binding outcome, not a diagnostic selected from retained state. Where fixed
independent binding policy permits a malformed-frame diagnostic, bounded
untrusted parsing still cannot create that permission. Never look up retained
history merely to decide whether to reveal a different error on an unassured
route. A well-formed scope mismatch in the provisioned profile retains its
generic 1008 outcome rather than a `not-addressed-to-me` diagnostic.

The reserved form contains exactly these payload fields:

| Field | Requirement |
|---|---|
| `version`, `id`, `kind`, `sent_at` | Ordinary core fields; `kind` is `refusal`; fresh ID and currently valid signing credential |
| `to` | Exactly `{"principal":"unverified"}` |
| `reason` | The first applicable verification failure, from the set below |
| `in_response_to` | Optional; echo a uniquely readable valid message UUID from the failed frame, otherwise omit it |

Allowed reasons are `malformed`, `algorithm-key-mismatch`, `certificate-invalid`,
`certificate-expired`, `key-not-certified`, `bad-signature`, `not-canonical`, and
`not-addressed-to-me`. `malformed` here means a verification-stage failure, not
an authenticated operation-input or lifecycle refusal. Processing stage determines
the distinction; the reason string alone cannot do so.

No other payload fields are allowed, including `detail`, `metadata`, `evidence`,
`caused_by` and `on_behalf_of`. Semantic reasons such as `busy`, `closed`,
`unknown` and `unsupported` cannot use this recipient. After successful ordinary
verification, a permitted semantic refusal is addressed to the authenticated
sender under the ordinary message rules. No other message kind may address
`unverified`, which is not a principal and cannot be certified.

An invalid or unclassifiable control receives no diagnostic under the previous
section. Generating a diagnostic reserves neither the rejected sender's claimed
ID nor a semantic disposition for its frame. Repeated deliveries of a rejected
non-control frame can produce fresh diagnostics; the diagnostics themselves are
not requests for another response or retransmitted application messages.

## Receiving and associating a diagnostic

The reserved form replaces only ordinary recipient matching. It does not waive
authentication, route authorization, continuity, structure or correlation checks.
`unverified` names no local participant and selects no conversation on its own.

1. Capture the delivery's actual route instance and independently established
   namespace, local recipient, expected peer and applicable request/scope
   association. Preserve this association through queuing. A URL, reused
   connection name, sender claim or echoed ID cannot establish it. Apply the
   current audience guard and all applicable original continuity guards before
   retained-state feedback or control effects. No-conversation payload shape
   does not exempt a diagnostic about conversation traffic from that boundary.
2. Within an independently established scope, apply the
   [exact retained-copy rules](messaging.md#exact-retained-copies-and-expired-credentials)
   before first-seen credential expiry. An eligible exact control copy receives
   no response and causes no repeated control transition, including no repeated
   attempt termination. An authentication-only observation is not such acceptance.
3. For a first-seen diagnostic, perform verification checks 1–7 normally with
   current credentials and governed naming authority. At check 8, admit the
   reserved-recipient candidate only through this path: it must be a `refusal`
   with exactly the reserved address, received from the expected authenticated
   peer on the independently authorized route. Then require the supported
   version and complete restricted payload shape and reason set above. A valid
   certificate for some other peer, TLS identity alone or mere knowledge of S
   supplies no exception. Failure causes no core reply or submission effect;
   an earlier guard failure still takes its binding outcome.
4. To affect an outgoing message, `in_response_to` must resolve uniquely to a
   retained local outbound attempt on that same captured route and original
   scope. The diagnostic's authenticated signer must equal that message's
   intended recipient. Match the established governed namespace and core
   profile too. Do not select the current slot, borrow an attempt from another
   connection, or choose one of several candidate scopes sharing an ID.
   Recheck the applicable original guard at this control-state update, ordered
   with retirement, just as for ordinary semantic admission.
5. Apply only the effect in the next section. The same rules apply when the
   sender of the attempted message is the conversation actor, including its
   notifications, approvals and owner closures. An `actor:` principal acting
   as requester follows requester rules in that conversation.

Absent, unknown or ambiguous correlation changes no submission, slot, turn,
approval or retained disposition. A diagnostic authenticated as coming from
the independently authorized peer may be exposed as a local notice under
infrastructure policy. This is not a reason to invent a request, infer an
outcome, or reply with `unknown`. Without an independently authorized peer/route
basis, it is not an authenticated peer notice for this interaction.

If no unique applicable original protocol scope can be established, the notice
cannot be admitted to an arbitrary conversation or acquire retained-control
eligibility there. Independent authority to expose an unassociated notice
cannot bypass a retired scope or authorize a message-specific effect. A binding
that multiplexes scopes must supply an unambiguous association for such effects
or leave the diagnostic unassociated. No new association field is introduced.

### Retained diagnostic identity

A diagnostic accepted as a scoped control has its own authenticated identity,
separate from its echoed target. Retain its exact bytes, successful verification
and exception basis, actual signer, independently known local recipient and
original request/scope and route association under the ordinary applicable
retention rules. Use that resolved local scope for control lookup; the literal
recipient `unverified` is not a global identity bucket. Never use the rejected
frame's unauthenticated claimed signer as the diagnostic's originating principal.

Retain an accepted diagnostic's original association and lack or presence of a
submission effect. A later outbound message cannot turn an earlier unassociated
notice or retained no-effect diagnostic into a refusal of that new message.
Eligible exact copies remain no-ops. Newly signed conflicting bytes with the
same scoped diagnostic ID cannot overwrite its earlier record; classify the
conflict as `malformed` without sending a control reply. Merely displaying an
unassociated notice supplies no scoped acceptance or retained authentication basis.

## Effect on sending and knowledge

A valid, uniquely associated verification diagnostic ends the identified
automatic attempt series. Its receipt is not the generic authenticated-peer
activity that restarts that same series. A reachability event alone does not
restart a series ended by this diagnostic. Any deliberate later attempt uses
the same original signed bytes and ordinary sending-slot and continuity rules;
the diagnostic is not permission to re-sign S or repeat uncertain work under a
new ID.

Correlation identifies the outbound message, not which physical retransmission
failed. A delayed diagnostic can end the currently running series for that same
message on the same eligible route/scope; it does not prove that the latest
attempt failed. Core adds no per-attempt identifier or freshness claim.

The diagnostic is neither confirmation nor a terminal semantic refusal of the
outgoing message. Unless other retained facts establish its disposition, its
outcome remains **not confirmed**. The peer authenticated its own report, not
the rejected input's claimed identity or the absence of earlier execution.
Preserve earlier acceptance/refusal facts, valid later confirmation and the
independent lifecycles of work, questions and approvals.

For a **requester submission**, ending attempts this way does not itself release
the occupied sending slot or authorize later queued submissions. Hold it until
ordinary confirmation, terminal semantic refusal, or explicit release by whoever
the requester acts for. A previously authorized implementation policy can make
that explicit release decision; core requires no human prompt or new approval
exchange. Stopping this attempt series and authorizing release are distinct facts.
A diagnostic concerning a separate stop slot cannot release the ordinary slot.

For a **conversation actor's outgoing notification**, the infrastructure retains
its existing policy discretion to end attempts and release the slot, including
after a diagnostic. That release does not establish delivery or change the turn,
question, approval or decision outcome. Neither role can use a diagnostic for
one message to release another message's slot.

## Conformance

[Diagnostic and control vectors](vectors/diagnostics.json) cover restricted
shapes, authentication, both sending roles, route/scope association, uncertainty,
retained copies, release boundaries and control-response termination. The schema
checks the reserved form; actual association, guards and local control effects
need implementation tests. These artifacts do not claim runtime conformance.
