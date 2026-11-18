# Provisioned context profile

**Identity: `keel.provisioned-context.v1`. Status: normative deployment profile
for unreleased core/1.** It instantiates the [core continuity contract](../continuity.md)
using the existing signed conversation key and an explicitly provisioned channel.
It adds no core message kind, payload field, public setup endpoint or discovery
service. The WebSocket subprotocol remains `keel.core.v1`.

This profile is usable in controlled deployments with a trusted provisioning
facility authorized to configure both endpoint adapters. It is not automatic
interoperation between arbitrary remote peers merely supporting core/1. Each
endpoint must independently authorize that facility; authority over the actor
alone does not authorize configuration of the requester. Implementations may
instead select another precisely specified continuity profile.

## Scope and trusted inputs

One provisioned scope carries one conversation between one recorded actor and
one requester over one actual authenticated WebSocket connection. Either
principal may have an `actor:` identity, and message direction never swaps
their recorded conversation roles. Independent approvals and either-side
owner closures use that same scope.

The provisioning facility must install an identical agreed descriptor at both
endpoints containing:

| Input | Required value or association |
|---|---|
| Continuity profile | `keel.provisioned-context.v1`, explicitly selected |
| Core identity | Payload 1, `keel-core-v1+jws`, and `keel.core.v1` transport |
| Namespace | Independently governed namespace/trust domain for this exchange |
| Participants | Exact actor and requester principals, with recorded roles |
| Conversation | A newly allocated receiver-authorized UUID C |
| Channel | A trusted association to the actual authenticated connection and its endpoint adapters |
| Audience and authority | Current route authorization for both recipients and authority to provision this scope; ordinary message/action checks remain required |
| Lifetime | Memory-only context tied to this connection and its local guard; no reconnection or restart resumption under this profile |

The descriptor is a local configuration contract, not JSON accepted from an
untrusted frame. Implementations may represent it differently. Provisioning may
use trusted local control calls or an existing secure deployment facility, but
must establish the inputs and ordering below. Its delivery mechanism must not
allow a party to replay an old descriptor or bind it to an unrelated connection.
No remote provisioning wire format is defined or claimed interoperable here.

A URL, TCP address, reused connection name, arrival order or client claim alone
cannot identify the channel. The association must remain tied to the actual
connection instance and authorized peers. Trusted proxies/adapters must propagate
loss or replacement of required endpoint state; keeping their frontend socket
open cannot keep a lost backend context valid.

## Establishment procedure

Provisioning is control-plane setup with no application effects:

1. The conversation actor, or a facility authorized by it, allocates C as a fresh
   UUIDv4 using cryptographically secure randomness. Never accept an arbitrary
   requester-provided old key as fresh setup, reuse a previous allocation
   deliberately, or derive C only from a URL, participant name or resettable
   counter. Regenerate any collision with retained allocations. No permanent
   registry of every prior conversation is required.
2. Reserve C for the specified participants and actual connection. Install the
   descriptor and fresh empty context at both endpoints. The minimal context
   records its conversation identity/roles and is ready to retain all ordinary
   core facts. It contains no accepted request, turn or approval merely from setup.
3. Each endpoint validates its local configuration authority, descriptor, channel,
   namespace, role and current response-audience assurance. It installs a receive
   guard bound to that specific local context instance and reports readiness to
   the trusted facility. Local readiness alone does not permit admission. An
   absent/inconsistent input fails setup without admitting conversation messages.
4. Only after the facility confirms both receive guards ready may it activate
   them for admission. Activate both before enabling either endpoint to send
   conversation frames. This requires ordered readiness and activation, not
   simultaneous activation or a distributed transaction. If setup fails or
   the connection is lost, invalidate the allocation and guards. A repeated setup
   call cannot reset an active context or reenable a retired allocation; it may
   only observe the same still-live setup without mutation, or create a fresh C
   on a fresh connection under this procedure.

The facility conveys the authorized C to the requester adapter before it signs
an initiating `say` or `approval`. The signature therefore binds that message to
the allocated C. The actor's replies also sign C. A captured old JWS still names
its old conversation and cannot be transferred by changing an outer label.

The actor and requester may now exchange the ordinary core kinds permitted by
their roles. A `closed` or `stop` may precede its target inside this established
scope under the existing marker rules. Setup does not bypass unknown-reference,
authorization, deadline or duplicate checks.

## Local guard and admission

Each endpoint uses these conceptual states; no particular representation is
required:

| State | Conversation behavior |
|---|---|
| Preparing | Scope not ready; withhold sending and admit no conversation frames |
| Active | The exact connection association, authority and required local context remain valid; ordinary core admission is permitted |
| Retired | Admission permanently disabled for this allocation; no message or setup replay can recreate it |

For each delivery, retain the association to the guard that received it. Require
the configured namespace/profile, authenticated sender, signed recipient and
signed conversation C to match the descriptor. Use bounded untrusted selectors
only to reject or choose an already configured guard; they confer no authority.
The configured actor/key remains fixed even for reverse-direction approvals.

Before interpreting retained IDs or disclosing a disposition, apply current
audience authorization and the scope check. Then apply retained exact-copy handling
or current first-seen verification as appropriate. Immediately before accepting
the message for semantic handling, require that the same guard is active and
still owns the same retained context. Order this decision with retirement. A
mailbox entry, callback or buffered frame must not look up a newly installed
context by a reused channel name and execute there.

An empty-context lookup is never a creation request. A new context exists only
through the establishment procedure; C remains fixed for its guard's lifetime.
A missing/replaced required context invalidates the guard. A receiver cannot
keep the allocation active while discarding earlier accepted/refused messages
or their required interpretation. If capacity is insufficient for a new message
while the active context is intact, refuse that message as ordinary `busy`.

## Failure and retirement

Either endpoint may retire its local scope according to its infrastructure policy.
It must invalidate admission before discarding required context state or installing
a replacement. Connection loss, local restart, detected loss/replacement of required
state, or loss of the provisioned authorization also retires the local guard.
Close the associated connection and disable outgoing conversation traffic. No idle
timeout or retention duration is selected by this profile beyond its connection
and state boundary; applicable base-binding rules still apply.

Queued but unadmitted frames are rejected under their captured retired guard.
If admission already occurred before retirement, keep that historical fact wherever
records remain; later failure cannot undo its consequences. Work/effects may still
be in progress. Retirement neither creates a terminal result nor cancels an
application job, withdraws an approval or revokes permission. Required application
handling of unfinished work remains its own contract.

The peer may not observe the failure immediately. Until it does, it may admit an
in-flight frame into its own still-valid old context. It must never admit that
frame into replacement state. The profile claims no instantaneous remote failure
detection and no detection of arbitrary silent corruption. It requires trusted
adapters to fail closed on the defined loss/replacement events, rather than
silently reconstructing empty state under the old guard.

## Binding outcomes

For a conversation frame delivered with missing/not-ready/retired setup, the
wrong conversation/channel association, or failed independent audience authority,
use the same generic binding rejection: close that connection with WebSocket
code **1008** if it remains open; otherwise discard the queued frame under its
retired guard. Send no core disposition or identifying close-reason details,
and perform no new semantic handling. Do not reserve its ID or change an earlier
accepted/refused disposition. Do not look up historical copies merely to decide
whether to reveal a different rejection. This is not a terminal `refusal` for
the signed message and establishes no past execution outcome.
Apply this action only to the delivery's original connection/guard; a queued
old frame must never close or mutate a newly provisioned replacement connection.

Ordinary framing failures retain the base binding's size/type rejection. Within
a valid scope, ordinary authenticated semantic failures still use their core
reasons, including `unknown` for a missing required message reference and `busy`
for capacity. Scope failure must not be mislabeled as either one.

A well-formed recipient or conversation selector conflicting with the descriptor
gets the generic scope rejection, as does an authenticated signer outside its
participants; this takes precedence over an addressing or role diagnostic.
The restricted [reserved diagnostic](../diagnostics.md#receiving-and-associating-a-diagnostic)
is routed by its captured independently authorized original association, rather
than treating the literal `unverified` address as a participant or a conflicting
conversation recipient. It must still satisfy that original guard; omission of
C cannot make a retired conversation's diagnostic into fresh actor-level traffic.
Missing or malformed addressing fields on an otherwise active, independently
authorized channel instead follow ordinary first-seen verification and structure
checks. They cannot establish a scope, authorize a retained-state disclosure or
reach semantic admission. A bounded untrusted selector may reject a mismatch;
it cannot establish identity or make a missing guard valid.

An exact retained copy inside an active authorized scope uses the retained exact-copy rule,
including ordinary credential expiry. A duplicate cannot reopen work. This
profile provides no old-scope feedback route after retirement; preserved facts
may be inspected only through another explicitly authorized contract. Retiring
or rejecting a route does not erase those facts or grant authority to selectively
discard records while keeping the context live.

## Reconnect, non-conversation traffic and limits

A new WebSocket connection has no authorization to resume the old conversation.
It needs fresh provisioning and a fresh C. An old outbox must not be forwarded
automatically, rewritten to C, or re-signed under its old message IDs. Choosing
new IDs is also not automatic authority to repeat uncertain application work.
Preserve unresolved outcomes and application drafts; use explicit reconciliation
or a new authorized application request where its contract permits it.

Retained-context reconnection and restart restoration require another selected
profile specifying those capabilities. They are not silent options on this
profile identifier. A deployment can support both profiles and select one per
scope; switching profiles does not mutate existing signed messages or establish
continuity by itself.

Non-conversation `describe`, `description` and their controls retain their
separate actor-level request scope and ordinary `dedup-window` rules. They may
use a separately authorized actor-level connection, or be explicitly segregated
on the same connection by the adapter. They neither allocate C nor activate,
resume or prove continuity of a conversation. They retain ordinary signature,
addressing, audience and confirmation checks. Reserved diagnostics follow the
[core diagnostic rules](../diagnostics.md), including unique original-route/scope
association before any submission effect. A multiplexed or ambiguous correlation
cannot select a conversation arbitrarily. Invalid/diagnostic control frames
cannot act as setup or continuity evidence. No control receives a core reply;
earlier scope failure still requires this profile's binding outcome.

This profile needs no durable storage, historical query, per-retired-conversation
tombstone or recovery service. Its fresh C and invalidated channel/guard prevent
re-entry; trust in correct provisioning and guard enforcement is indispensable.
It does not promise indefinite retention, reply delivery, finished work or
exactly-once external effects. Supporting arbitrary remote provisioning would
require a separately specified setup protocol; it is not implied here.

## Conformance

The [continuity vectors](../vectors/continuity.json) cover setup, bilateral state
loss, retirement/admission races, stale frames on fresh channels, confidentiality
and separation from application effects. Claim this profile only after testing
the actual provisioning authority, adapters, queue paths and failure boundary.
Protocol artifacts alone are not an implementation of this profile.
