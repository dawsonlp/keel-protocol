# Decision catalogue

This collection records the decisions that shaped core/1: what was selected,
the reason, how the choice applies, and its limits. It retains decision knowledge,
not the deliberation log. Current specifications remain authoritative; these
records neither add requirements nor establish implementation conformance.

## Browse by subject

| Subject | Decision record | Principal outcome |
|---|---|---|
| Scope and compatibility | [Protocol scope and identity](scope-and-identity.md) | One common role-conditioned contract with explicit standalone core/1 identities |
| Work and authority | [Turns, contributions, cancellation and approvals](work-and-authority.md) | Separate response obligations, application commitments and independent permission exchanges |
| Security and evidence | [Identity, authentication, disclosure and effects](security-and-evidence.md) | Governed names and exact signed messages; authority, disclosure and effects keep separate owners |
| Delivery and continuity | [Evidence, context lifetime and diagnostics](delivery-and-context.md) | Preserve uncertainty and scoped identity; establish admission explicitly and retire stale scopes |
| Operations and agreements | [Declarations, structured data and application agreements](operations-and-agreements.md) | Interoperable data validation plus an optional provisioned application promise |
| Time | [Timestamp representation and precision](timestamp-representation.md) | Restricted UTC representation with up to six fractional digits and exact interpretation |
| Recovery | [History and application recovery ownership](recovery-and-service-ownership.md) | Responsible services use the existing protocol; no recovery extension selected |

Each subject has one home. Records cross-reference related subjects and their
current normative destinations rather than duplicating the detailed specification.
Filenames are stable descriptive identifiers; filenames and titles use the same
subject vocabulary as this catalogue.

## Find by term

| Term or former label | Look under |
|---|---|
| Actor participation, B01, protocol extraction, E02 | [Scope and compatibility](scope-and-identity.md) |
| Turn, contribution, stop, approval, application commitment, P01–P03, B02–B03 | [Work and authority](work-and-authority.md) |
| Namespace, issuer, expired retry, signature, grant, P04–P05, P10, security review | [Security and evidence](security-and-evidence.md) |
| Late report, duplicate, progress replacement, guard, diagnostic, P06–P07, P09 | [Delivery and continuity](delivery-and-context.md) |
| Operation schema, cached description, stable offering, P08, S02–S03, C01–C06 | [Operations and agreements](operations-and-agreements.md) |
| Precision, RFC 3339, microseconds, deadline representation, S01 | [Time](timestamp-representation.md) |
| Record service, missed result, history paging, restart, E01 | [Recovery](recovery-and-service-ownership.md) |

Former labels are lookup aliases only. They are not current work queues or a
second classification hierarchy.

## Unselected proposals

| Approach | Disposition | Decision context |
|---|---|---|
| Recovery extension and automatic conversation restoration | Superseded by service ownership | [Recovery](recovery-and-service-ownership.md) |
| Portable scoped-grant format | Not adopted | [Security](security-and-evidence.md) |
| Smaller shared substrate or limited participation profiles | Not selected for core/1 | [Scope](scope-and-identity.md) |
| Generic invocation preconditions, required-extension facility and exact declaration evidence | Deferred; no selected wire behavior | [Operations and agreements](operations-and-agreements.md) |

“Adopted” identifies a selected definition. “Not selected” or “not adopted” means
no implementation obligation was created. “Deferred” preserves a possible future
question without authorizing a mechanism. “Superseded” identifies an earlier
approach replaced by the stated decision. These distinctions prevent an archived
idea from appearing to be an unfinished core requirement.

## Collection policy

Retain title, subject, disposition, decision, concise basis, application and limits,
and relations to current authority and other decisions. Retain an earlier
alternative only when its disposition helps interpret the current boundary.
Implementation and deployment status belongs in the [current implementation guide](../implementation.md),
not in historical test-count snapshots.

Discussion transcripts, review iterations, agent/task metadata, intermediate
checklists, temporary paths, old checkout line references, repeated validation
reports and unadopted test artifacts have been removed. This is a curated decision
collection, not a complete archival record or a catalogue of every past proposal.
When a decision changes, preserve the material former outcome and its replacement
relationship; do not accumulate a new chronological log.

The organization adapts [Dublin Core's descriptive fields](https://www.dublincore.org/specifications/dublin-core/dces/)
for titles, subjects, descriptions and relations, and [IFLA's user tasks](https://repository.ifla.org/bitstreams/7d23aa55-1f85-490f-b500-6170285585a6/download)
for finding, distinguishing, selecting and exploring related material. This is
a small project-specific application of those principles, not a claim of formal
cataloguing-standard compliance. Scope and retention are deliberately limited to
information useful for understanding decisions.
