# Documentation

This directory describes the current purpose, requirements and use of Keel.
It does not require familiarity with earlier review identifiers or decisions.

| Document | Question answered |
|---|---|
| [Product](product.md) | What is Keel for, who uses it and what is outside its scope? |
| [Requirements](requirements.md) | Which observable needs drive the definitions, and where are they specified? |
| [Design rationale](design-rationale.md) | Why were these boundaries and representations chosen? |
| [Network development](network-development.md) | How do actors use the protocol to deliver an application? |
| [Implementation](implementation.md) | What must an endpoint implement and demonstrate? |

## Authority and reading order

1. Establish the product scope and application responsibilities.
2. Read the [core concepts and required definition](../core/README.md).
3. Follow the implementation or network-development guide for your role.
4. Select the [optional interaction agreement](../extensions/interaction-agreements/README.md)
   only when the network needs its stronger application promise.

Normative core contracts and explicitly selected profiles define conformance.
The schema alone cannot express all admission, state or calendar rules. Vectors
supply expected cases; checking their artifact structure is not running those
cases against an implementation. Current guides summarize and link the authority
rather than replacing it.

## Status

Core/1 is unreleased. The original protocol review is resolved at specification
level. Independent implementation conformance, consumer migration and deployment
validation remain outstanding; no SDK or running network is delivered here.

[The decision catalogue](historical/README.md) organizes material outcomes by
subject, with their rationale, limits, alternative dispositions and links to
current definitions. Deliberation logs and process metadata are not retained.
The implementation guide preserves outstanding engineering responsibilities.

## Delegated authority

The [optional extension](../extensions/delegated-authority/README.md) specifies
provisioned direct grants. The [proposal](proposals/delegated-authority-extension.md)
describes the broader vision for multi-hop delegation and recursive permissioning.

Track design decisions, specification work and implementation evidence in the
[delegated authority implementation checklist](proposals/delegated-authority-implementation-checklist.md).
