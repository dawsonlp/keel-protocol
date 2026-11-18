# Core timestamps

This is the normative timestamp profile for core message `sent_at` and
question/approval `deadline`. It defines a restricted
[RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html#section-5.6) UTC
representation, validation and comparison. The protocol defines which values
every receiver must handle; applications choose the resolution their interactions
need, and deployments supply suitable clocks. This profile does not require a
particular programming language, parser, clock service or internal representation.

## Representation

A timestamp has exactly this form:

```text
YYYY-MM-DDTHH:MM:SS[.ffffff]Z
```

The brackets denote an optional fraction, not literal characters. If present,
the fraction contains **one to six decimal digits**; it need not contain six.

| Component | Required value |
|---|---|
| Year | Four ASCII digits, `0001` through `9999` |
| Date | A real date in the proleptic Gregorian calendar |
| Hour | `00` through `23` |
| Minute and second | `00` through `59` each |
| Fraction | Absent, or a dot followed by one to six ASCII digits |
| Separators and zone | Literal hyphens, colons, uppercase `T`, and terminal uppercase UTC `Z` |

Month, day and clock components contain exactly two digits. No whitespace,
trailing characters, offsets, lowercase alternatives, expanded year, year zero,
`24:00:00` or leap-second label `:60` is permitted. A seventh fractional digit
is invalid even when it is zero. Reject invalid values; do not normalize an
impossible date, clip a component, round an excessive fraction or repair syntax.

Validate the day against its month and year. February has 29 days exactly when
the year is divisible by four, except century years not divisible by 400.
Thus `2000-02-29` is valid and `2100-02-29` is invalid. The
[payload schema](schemas/keel-v1.schema.json) checks component ranges and syntax;
its day range alone does not establish a real calendar date.

The representable resolution is one microsecond, not a promise of clock
accuracy. Whole-second and millisecond values remain valid. Producers may
choose a coarser resolution when it meets their application contract. An
application must not describe a rounded external expiry as preserving that
expiry exactly. Every receiver must preserve and interpret the entire admitted
range and precision, regardless of the resolution it normally generates.

This is a civil-time profile with ordinary seconds `00–59`; it cannot identify
an inserted leap second distinctly. It does not prescribe clock smearing,
repetition or stepping, or require leap-table acquisition. Calendar validation
does not certify that every label denotes an actual UTC instant during a leap
adjustment. Deployments must make their clock behavior suitable for their timing
requirements. No timestamp comparison supplies physical event order across
clock adjustments or across independently running clocks.

## Validation and receiving order

Apply whole-string syntax, component-range and real-calendar checks as part of
step 2 of the [structural check order](asking-contract.md#2-every-message).
Invalid `sent_at` or `deadline` makes the payload `malformed`, even if an outer
JSON Schema validator accepts its shape. Perform these checks before semantic
admission, acknowledgement of acceptance, deadline scheduling or time arithmetic.
A failed parse must not enter a comparison as `NaN`, a default value or a
normalized date. Adding a JSON Schema `format` annotation alone does not satisfy
this obligation.

The existing precedence remains: binding audience and continuity guards,
eligible [exact retained-copy handling](messaging.md#exact-retained-copies-and-expired-credentials),
first-seen authentication/addressing, then supported payload version, then
structure including timestamps, then supported content type and semantic
checks. An earlier failure keeps its existing outcome. A valid signature does
not make an invalid timestamp acceptable. An eligible exact retained copy uses
its established disposition; a new timestamp spelling under the same message
ID is not such a copy.

Failure classification is separate from response emission. Follow
[diagnostic and control-response rules](diagnostics.md#control-response-termination):
an invalid timestamp on a recognizable control receives no core response, and
earlier binding rejection cannot be bypassed by timestamp error feedback.

## Exact values and signed identity

Compare valid timestamps by their complete date, time and fractional value.
An absent fraction is zero; shorter fractions are right-padded with zeros for
value comparison. For example:

```text
2030-01-01T12:00:00.1Z      = 2030-01-01T12:00:00.100000Z
2030-01-01T12:00:00.1234Z   < 2030-01-01T12:00:00.1235Z
2030-01-01T12:00:00.123456Z < 2030-01-01T12:00:00.123457Z
```

No admitted distinction may be lost through truncation, rounding, limited
floating-point precision or conversion through a coarser timestamp type. Raw
lexical comparison of strings with different fraction lengths is insufficient.
Implementations choose their representation; validated calendar components with
an integer microsecond fraction, or an exact seconds/fraction pair, are examples.
All values through year `9999` must remain exact, not only dates near the present.

Value equality does not change signed identity. Preserve original timestamp
strings and signed bytes; never rewrite `.1` as `.100000` in a retained message.
The two strings can denote equal values while their messages have different
canonical bytes and signatures. Existing message-ID, exact-retry and approval
digest rules still apply.

## Deadlines, clocks and scope

The [originator owns its deadline](asking-contract.md#5-deadlines). At decision
processing it compares its current clock reading with the valid retained deadline;
at or after the deadline a pending approval expires, even if a timer callback
has not run. The decision's `sent_at <= deadline` check is an additional
consistency condition: equality there is permitted, but it cannot override
owner-clock expiry, withdrawal or an already accepted decision.

Use the complete available clock reading in deadline comparison. The wire's
microsecond limit does not require reducing a finer local clock reading to
microseconds or rounding a deadline to the clock's sampling interval. A coarse
clock can still preserve an exact timestamp value; whether it can enforce the
application's timing requirement is a deployment responsibility. Encoding more
digits does not improve its accuracy, resolution, synchronization or scheduling.

`sent_at` does not establish processing order, message uniqueness, delivery
confirmation or general freshness. Core adds no maximum message age and no
general `deadline >= sent_at` rule. A well-formed past deadline follows the
existing lifecycle rules rather than becoming malformed. Credential `iat`/`exp`
NumericDates and their separate allowance remain governed by the
[security profile](security-profile.md); that allowance does not extend a
question or approval deadline.

These rules apply to the named core fields, not arbitrary strings inside
`data`, `metadata` or application schemas. Applications may define finer event
timestamps there under their own contracts. They cannot use those fields to
silently redefine a core deadline. Operation-schema `format` remains
[annotation-only](schemas/README.md#embedded-operation-schemas). Display,
local time conversion, synchronization, clock behavior and application timing
guarantees remain outside the representation contract.

[Timestamp vectors](vectors/timestamps.json) cover validation, comparison and
receiving outcomes. The [timestamp rationale](../docs/design-rationale.md#timestamp-representation-and-application-resolution)
explains the selected precision and interoperability tradeoffs. Artifact checks
do not establish runtime timing guarantees or implementation conformance.
