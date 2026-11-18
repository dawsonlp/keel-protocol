# Developing a networked application

Keel carries interactions among actors. Design the application in terms of work,
information and authority first, then assign those responsibilities to actors.
This guide uses a report-preparation network as an illustration, not a required
service architecture or a runnable SDK example.

## Define the application contracts

Suppose a coordinator prepares a report using a data actor, asks a person to
clarify its intended audience, and obtains permission before publishing it.
Identify the report/job independently of any protocol conversation. Define what
submission success means, which actor owns completion, and which operation
actually publishes the report.

For each operation, specify:

- Its meaning, permitted effects, inputs and successful output.
- Whether later contributions amend the input, add information or are declined.
- What a failed or stopped result says about effects already started.
- Current authorization and any required approval, including scope and expiry.
- Application work identity, duplicate-effect handling and reconciliation when
  the requester cannot determine the outcome.

Named operations can declare input and successful-output schemas under the
[embedded-schema profile](../core/schemas/README.md). Data can be any core-valid
JSON value, including arrays and scalars. Declared schemas require data to be
present; omission is distinct from null. Guidance must explain contribution and
effect semantics that schemas alone cannot capture. Required text can be fixed
descriptive text for deterministic operations.

## Assign roles and deploy endpoints

The coordinator is an answering actor for its client and a requester when it
calls the data actor. Those are separate conversations and response obligations.
A human interface can be a requester or decision maker without exposing an
answering service. Protocol infrastructure can fulfill receiving and delivery
obligations around a small application handler.

Before traffic, arrange:

1. Governed principal names, issuer/key naming authority and credentials under
   the [security profile](../core/security-profile.md).
2. Addresses, a shared binding, current action authorization and recipient-bound
   response routes. Signatures authenticate bytes, not the present carrier's
   right to receive replies; signing also does not encrypt content.
3. An explicitly selected continuity profile. For the
   [provisioned context profile](../core/profiles/provisioned-context.md), a trusted
   facility authorized by both endpoints installs matching scope descriptors,
   a fresh actor-issued conversation key and guards on the actual connection.
   Both guards must be ready and activated before conversation traffic.
4. Resource limits, scheduling and clock policy appropriate to the application.
   Apply the specified frame limits and admission/control rules consistently.

This is trusted deployment setup, not a public discovery or negotiation API.
A socket using the right subprotocol is insufficient by itself. Do not infer
endpoint readiness or continuity from a known URL or restored client file.

## Select meaning before preparing work

A description advertises current offerings; it does not bind later invocations
to a cached description. An admitted turn retains its selected contract. If a
prepared model tool, mechanical command or human interaction must keep a stable
meaning across deployment changes, explicitly select the optional
[provisioned interaction agreement](../extensions/interaction-agreements/provisioned-agreement.md).
Preserve the intended agreement from preparation through setup. A model alias
or UI label must not silently resolve to a different offering at admission.

## Conduct an exchange

This schematic sequence omits signed envelope fields. Implementations must build,
canonicalize and sign complete payloads under the normative definitions.

| Step | Protocol action | Application interpretation |
|---|---|---|
| Submit | Client sends a fresh `say` to the established coordinator context, with its operation and input | Request a particular response contract, not an unspecified permanent job lifecycle |
| Admit | Coordinator reports the opening's disposition with `taken` | The turn's contract has been selected; acceptance alone is not work completion or durable storage |
| Delegate | Coordinator opens a separate turn with the data actor | The child has its own response obligation; its result is input to the coordinator's work |
| Clarify | Coordinator issues a turn question; client answers with a `say` whose `in_response_to` names that question | The answer continues the original turn |
| Amend | Client sends a contribution naming the opening `say` | The selected contract decides whether to admit the amendment; it is not an independent invocation |
| Report | Coordinator may emit `progress` and eventually one terminal `result` | Progress is provisional; the result answers the selected contract |

A new `say` without contribution correlation requests an independent turn. An
endpoint cannot silently merge it into the current work. Within one conversation
there is at most one open turn; use separate conversations where independent work
must proceed concurrently. Do not block protocol controls while application work
runs. Results and questions can arrive before `taken`; retain submissions and
apply the [notification rules](../core/notifications.md) instead of using arrival
order as the actor's execution order.

## Obtain permission and enforce effects

Publishing permission can use an independent `approval` exchange, with its own
identity and deadline. Either conversation role may originate it. The originator
accepts the authorized, correctly bound decision and issues closure. A sent
`decide` is not yet evidence that its originator accepted it, and a closed
exchange is not itself a grant to execute.

Bind the decision to the exact requested action and enforce current authority at
the actual publishing boundary. Application policy defines grant scope, use
limits and expiry. Permission does not prove publication, and completing or
stopping a work turn neither withdraws an independent approval nor revokes
permission. Explicitly withdraw a pending approval when the application's work
dependency requires it. No portable scoped-grant wire format is supplied here.

## Stop work and report outcomes

A `stop` names the intended opening request's ID, even if that opening is still
in transit. Its acknowledgement confirms acceptance of the control; a matching
`stopped` result terminates the turn. Neither promises rollback, termination of
already-started external actions or cancellation of delegated jobs.

A network that promises cancellation of a report job must give that application
operation its own target, authority and outcome contract. It must remain
serviceable while work is running, using another conversation when necessary.
A successful job-submission operation can return a job identity while the job
continues; later status operations have their own turns.

## History and application recovery

Recovery is provided by responsible actors and client infrastructure using the
current protocol. No recovery extension is selected. Service contracts must
state what is retained, who may retrieve it and what a missing record means.

| Use case | Responsible component | Required application-level distinction |
|---|---|---|
| Client restarts after a result was produced | Client plus work owner or record actor | Look up an existing outcome without requesting the work again |
| User reloads a transcript | History actor and interface | Authorized historical data is not a restored live conversation |
| Client reads history in pages | History actor and reader | Define ordering, cursors, completeness, gaps and retention expiry |
| Saved request has no observed outcome | Client and effect/work owner | Exact saved bytes do not authorize retransmission after scope retirement; reconcile under the application contract |
| Effect occurs before its outcome is recorded | Effect owner and any record actor | Missing records do not prove non-execution; coordination or external reconciliation must supply any stronger promise |
| Long-running job survives worker restart | Work-owning actor | Preserve application state and reconcile effects; this does not automatically restore lost core turns |
| Reader inspects old signed artifacts | Evidence service and verifier | State historical authentication and disclosure assumptions; an old timestamp alone proves no earlier admission |

For example, after reconnecting the client establishes a fresh valid scope and
asks the responsible actor for the report job's outcome. The new result answers
that lookup and may carry the old artifact as data. It must not inject the old
result into the new context as live traffic for an unknown old turn. If the
outcome is unavailable, expose uncertainty or use an explicitly defined
reconciliation operation. A fresh request ID alone does not make repeating an
external action safe.

## Validate the network's promises

Test operation success and refusal, input amendments, independent approvals,
late first deliveries, exact retries, stop races, lost connections and uncertain
effects. Inject failure between external execution and recording, not just before
work begins. Verify history access authorization and incomplete pages. Test the
promised application behavior on top of conforming endpoints; distinguish its
results from [protocol implementation conformance](implementation.md).
