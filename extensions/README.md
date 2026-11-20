# Optional profiles and extensions

Core conformance stands on its own. Additional behavior applies only when its
contract and scope are explicitly selected by the relevant participants.

| Specified optional profile | Purpose | Definition |
|---|---|---|
| `keel.provisioned-agreement.v1` | Preserve the requester's intended application agreement for a provisioned conversation | [Interaction agreements](interaction-agreements/README.md) |
| `keel.provisioned-direct-grant.v1` | Establish a requester's bounded authority for one represented principal in a provisioned conversation | [Delegated authority](delegated-authority/README.md) |

The core [provisioned context profile](../core/profiles/provisioned-context.md)
establishes live admission and retirement. The optional agreement profile adds a
stable application promise to that association; it does not add core wire fields.

An extension must not silently redefine ordinary core messages. A completed
extension needs explicit compatibility identity, applicability, support
establishment, required behavior and separate conformance evidence. Its presence
in a directory, an actor name or arbitrary metadata does not establish support.

Core `stop` targets one identified turn. Ordinary application cancellation can
be a named operation with its own meaning, target and authorization. Any future
extension that changes stop targets or core guarantees needs a separately agreed
contract and cannot fall back silently to core semantics.

No recovery extension is selected. History, missed-result access
and work recovery belong to network/application components using the current
protocol; see the [network guide](../docs/network-development.md#history-and-application-recovery).
Previously considered approaches have dispositions in the
[decision catalogue](../docs/historical/README.md#unselected-proposals), not listed
as pending requirements for implementation.

## Further delegated authority work

The [delegated-authority extension proposal](../docs/proposals/delegated-authority-extension.md)
describes the vision for multi-hop delegation and recursive permissioning.
The specified direct grant profile covers root-issued grants. Recursive proof
and per-request proof carriage require separate profile definitions.
