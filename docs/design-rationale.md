# Design rationale

This explains the current choices and their drivers. It is explanatory; exact
behavior remains in the [core definition](../core/README.md).

## A common interaction contract

Bounded computation, clarification and collaboration share a useful vocabulary:
request, admitted contribution, question, progress and terminal outcome. A
fixed-text request with structured data does not require natural-language
inference. Separate deployable components are not needed for every conceptual
responsibility.

Core therefore retains a common conversation and authority contract, with
obligations conditioned by contextual role. A participant need not originate
every interaction, but must handle applicable received traffic correctly. A
smaller substrate or limited participation profiles would add compatibility and
selection obligations without a demonstrated need in the selected scope.
Other actor service contracts can exist; actor naming does not make them core/1.

## Turns, commitments and authority have different owners

A turn provides one selected response obligation. Contributions can change its
inputs under that contract; an independent invocation requires its own turn.
A successful job-submission result can complete that operation while the accepted
application job continues. Delegated turns and model calls do not automatically
complete their parent's obligation.

Approvals ask for permission rather than work completion. Their originator owns
decision acceptance and closure regardless of conversation role. Work termination
does not implicitly withdraw approval or revoke permission. A stop names a
particular turn because delivery delay must not redirect cancellation to newer
work. Application effects and cancellation guarantees remain application-owned.

## Evidence and uncertainty

Transport arrival order cannot establish processing order. A result can arrive
before its admission report; a missing result does not mean failure. Explicit
references and retained facts establish only the relationships they support.
This permits correct implementations with different scheduling and storage
choices while preventing invented certainty.

A signed artifact identifies its signer under configured naming trust. It does
not prove the present carrier is entitled to receive protected replies. Exact
retained-copy recognition and authorized-route feedback are therefore separate.
Likewise a retained earlier authentication fact differs from admitting an unseen
expired message or proving a historical event solely from its timestamp.

## Explicit scope instead of implicit restoration

Retaining an address or opening another connection does not prove that both peers
still hold the state needed to interpret an old exchange. Explicit establishment
and retirement guards prevent stale traffic from becoming fresh work. The
provisioned context profile makes this concrete for controlled deployments using
memory-only state.

History retrieval and application recovery do not require reopening those old
exchanges. A responsible actor can answer a fresh lookup with retained outcomes.
The application owns recording, reconciliation and any gap between an external
effect and its record. The identified uses do not justify a recovery extension;
core retains its live-context boundary.

## Structured data and stable application meaning

Operation declarations describe an offering; an admitted turn retains its selected
contract. A cached description alone does not bind a future invocation. Core
allows general JSON data and a defined embedded-schema dialect without making
operation names universal compatibility identifiers.

Networks that need a stable promise during preparation and admission can select
the provisioned interaction-agreement profile. It preserves the requester's
intended agreement and retires the association before incompatible replacement.
This solves the selected controlled-deployment case without a registry or new
wire fields. Conditional invocation and exact declaration-evidence schemes remain
unselected proposals.

## Timestamp representation and application resolution

A restricted RFC 3339 representation gives independently implemented peers one
syntax to validate. UTC-only spelling avoids offset normalization decisions.
A six-digit fractional maximum admits microsecond distinctions while bounding
parsing and comparison and fitting Python's datetime precision; milliseconds
would discard distinctions useful to some applications. It is a supported range,
not a requirement to generate six meaningful digits for every event.

Years 0001–9999 and seconds 00–59 avoid year-zero and explicit leap-second labels
that complicate ordinary cross-language handling. These constraints do not make
every native parser sufficient: implementations must validate real dates, retain
exact microseconds and preserve signed spelling. A JavaScript millisecond date
representation alone cannot preserve every admitted value.

The protocol owns accepted representation and comparison. Applications own their
required resolution; deployments own clock accuracy, synchronization and behavior
around adjustments. Sub-microsecond application observations may have separate
fields, but cannot redefine a core deadline. No timestamp alone proves causal
order across machines.

## Related decisions

The [decision catalogue](historical/README.md) records selected outcomes, their
basis and the disposition of material alternatives by subject. It does not retain
the deliberation chronology or add requirements to this definition.
