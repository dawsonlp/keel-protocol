# Interaction agreements

**Specified optional profile: `keel.provisioned-agreement.v1`.**
The [normative profile](provisioned-agreement.md) establishes the requester's
intended application agreement alongside a fresh provisioned conversation.
It introduces no core field, message kind, public setup protocol or registry.
Core conformance does not require this additional promise.

## When to use it

A network may need prepared requests to retain their intended meaning until
admission: a model tool prepared from a particular offering, a mechanical command
bound to a deployment contract, or a human conversation promised to be
explanation-only. A cached core description or unchanged operation name alone
does not supply that guarantee.

The application owner defines the meaning and compatible changes. The network
selects the agreement; the requester retains the agreement used in preparation;
the host and trusted provisioning facility establish it at both endpoints.
The facility must be independently authorized by both parties.

## What the profile promises

- Setup establishes the intended agreement, not a silently substituted current offering.
- The agreement is bound to the roles, fresh conversation, actual connection and
  guards of `keel.provisioned-context.v1`.
- The host preserves its promised meaning for that association or retires the
  paired scope before incompatible replacement.
- Admission, exact retries, selected turn contracts, approval ownership and
  retired-scope handling retain their core meanings.

This profile does not guarantee deterministic outputs, schema-equivalent
application meaning, current effect authority or recovery across connection loss.
It supplies no remote negotiation protocol for arbitrary peers.

## Implement and validate

Read the [profile definition](provisioned-agreement.md) and its
[conformance traces](vectors.json), together with the
[core provisioned-context profile](../../core/profiles/provisioned-context.md).
The [network guide](../../docs/network-development.md#select-meaning-before-preparing-work)
explains application use. Schema and trace artifact checks do not prove runtime
agreement enforcement.

Conditional invocation and exact declaration-evidence mechanisms are not selected.
Their disposition is recorded in the [decision catalogue](../../docs/historical/operations-and-agreements.md);
they impose no additional profile obligations.
