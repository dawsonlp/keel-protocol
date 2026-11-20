# Product definition

## Vision

Enable independently built actors to cooperate through a small, explicit common
contract whose messages can be authenticated and whose outcomes remain correctly
interpretable despite delay, duplication, interruption and incomplete knowledge.
Applications should be able to combine deterministic computation, human decisions
and model-assisted work without changing the fundamental exchange semantics.

## Intended users and needs

| User | Need |
|---|---|
| Protocol implementer | A precise definition of signing, admission, roles, state and failure outcomes that another implementation can reproduce |
| Application author | Work requests, structured results, clarification, contributions, progress and permission exchanges with explicit meaning |
| Network operator | Governed identities, trusted setup, enforceable authority and clear responsibility for resource and continuity policies |
| Interface or agent author | Correlated evidence about what was accepted, decided or completed, without treating missing messages as definitive outcomes |

A small deterministic actor can offer one bounded operation. A coordinating actor
can call several actors and synthesize their results. A human interface can supply
information or authorize an action. These are application arrangements using one
common role-conditioned contract, not separate core participation profiles.

## What this project supplies

- A language-independent signed-message and credential profile.
- Conversation, turn, contribution, notification and independent approval semantics.
- Delivery, duplicate, refusal, diagnostic and context-lifetime rules.
- A concrete WebSocket binding and provisioned memory-only context profile.
- Payload schemas and structural, cryptographic and behavioral conformance artifacts.
- An optional provisioned agreement profile for stable application meaning.
- An optional provisioned direct grant profile for verified requester authority.

The current deliverable is a specification. It selects no programming language,
SDK, process model, database or actor hosting framework.

## Responsibility boundaries

| Owner | Responsibility |
|---|---|
| Core protocol | Shared message meanings, authentication/admission rules and live-context obligations |
| Endpoint infrastructure | Implement those rules, retain required live state, manage delivery and enforce scope guards |
| Application contract | Define operation meaning, outputs, amendments, effects, cancellation and work identity |
| Network and deployment | Choose participants, routes, trust governance, compatible profiles, resource policy and application agreements |
| Responsible service actors and clients | Provide any promised historical access, retained outcomes, job recovery or local saved-state behavior |

Discovery, factories, network membership, scheduling strategy, model orchestration,
job management, record services and storage design are outside the protocol.
Keel does not promise durable acceptance, eventual reply retrieval, automatic
restart resumption, global event ordering or exactly-once external effects.

## Success criteria and limits

Success means independently implemented peers interpret admitted messages and
failure evidence consistently under the same selected contract and profiles.
A result answers its particular operation contract; permission is distinguishable
from execution; missing evidence remains uncertainty; state loss cannot silently
turn old traffic into new work.

Schema validity, a listening socket or passing artifact checks does not establish
that success. It requires receiver behavior and cross-implementation testing.
Network reliability and application outcomes require additional evidence from
those responsible for providing them.
