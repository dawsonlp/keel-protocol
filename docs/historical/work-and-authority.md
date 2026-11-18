# Work, contributions, cancellation and authority

**Disposition:** adopted for core/1.
**Subjects:** turns; contributions; stop; approvals; application commitments.

## Decision

One admitted opening selects one terminal response contract. Contributions may
add information, answer a question or amend inputs under that contract. A fresh
uncorrelated `say` requests independent work; it cannot silently join an open
turn. A contribution identifies the opening request, while an explicit answer
identifies the question. Unknown or closed targets do not create fresh work.

A selected operation may decline amendments. Model calls and delegated actor
turns remain internal work or separate exchanges; their completion does not
implicitly complete the parent turn. A successful job-submission result may
establish an application commitment that continues beyond that protocol turn.

A `stop` identifies the opening request, including a request still in transit.
Its acceptance and the turn's terminal `stopped` result are distinct facts. Stop
must not select whichever newer turn happens to be open when it arrives.

Approvals are independent exchanges, not work-turn state. Either conversation
role may originate them, including without an open turn. The originator owns
decision acceptance, deadline enforcement, withdrawal and closure. A sent
decision is not proof of its acceptance; permission is not proof of execution.

## Basis and application

Explicit targets preserve meaning under delay. One selected response obligation
makes incremental and composite work interpretable without conflating it with
multiple invocations. Independent authority ownership lets either participant
seek permission without pretending that permission is a work result.

An admitted contribution must be accounted for; late arrival cannot reopen a
terminal exchange. Work termination does not implicitly withdraw an approval or
revoke a grant. When an application dependency requires withdrawal, the originator
must perform it explicitly while the approval remains pending.

## Alternatives and limits

Protocol stop does not promise rollback, cessation of already-started external
effects, descendant cancellation or termination of a durable application job.
Those guarantees require application contracts with their own targets, authority
and outcomes. No additional application lifecycle was added to core.

## Current authority and related decisions

[Asking](../../core/asking-contract.md), [approvals](../../core/approvals.md) and
[notifications](../../core/notifications.md) define the transitions.
[Delivery and context lifetime](delivery-and-context.md) explains delayed evidence;
[security and evidence](security-and-evidence.md) separates permission from effects.
