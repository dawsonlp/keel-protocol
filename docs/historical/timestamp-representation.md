# Timestamp representation and precision

**Disposition:** adopted for core timestamps.
**Subjects:** timestamps; precision; interoperability; deadlines.

## Decision

Use a restricted RFC 3339 UTC representation with uppercase `T` and terminal `Z`,
years 0001–9999, real proleptic Gregorian dates, seconds 00–59 and an optional
fraction of one to six decimal digits. Reject offsets, year zero, explicit leap
second labels, impossible dates and excessive precision rather than repairing,
normalizing or rounding them into accepted values.

Every receiver must preserve and compare the complete admitted value across the
whole year range. Equivalent fractional values do not permit rewriting signed
spelling or bytes. Whole seconds and milliseconds remain valid producer choices.

## Basis and application

The protocol defines a bounded interoperable representation; applications choose
the resolution they need and deployments provide suitable clocks. Milliseconds
would discard distinctions useful to some time-sensitive applications.
Microseconds provide additional useful range while fitting Python datetime
precision and remaining implementable across languages. Native parser acceptance
is not sufficient proof of conformance, and a millisecond-only date type cannot
preserve every admitted value.

Restricting years and leap-second labels avoids requiring special calendar or
leap-table handling in the shared wire contract. Calendar validation and exact
comparison still require more than a shape-only schema check.

## Limits

Precision is not accuracy, synchronization or physical event order. No timestamp
supplies uniqueness, total ordering, general freshness or delivery confirmation.
Originators enforce their own deadlines under the lifecycle rules; credential
validity and grant duration remain separate. A coarse clock does not authorize
rounding away a deadline distinction.

Applications may carry finer event timestamps under their own data contracts,
but cannot use them to silently redefine core deadline semantics. Deployment
policy owns clock adjustments and timing guarantees.

## Current authority and related decisions

[Core timestamps](../../core/timestamps.md) defines validation and comparison;
[design rationale](../design-rationale.md#timestamp-representation-and-application-resolution)
explains the current tradeoff. See [work and authority](work-and-authority.md)
for deadline ownership and [security](security-and-evidence.md) for credential time.
