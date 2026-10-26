# Electrical sanity checks

The circuit layer performs a deliberately conservative graph check before any page is
drawn. It catches declarations that are unambiguously wrong from connectivity alone:

- two terminals of one part assigned to the same net
- a bare wire directly joining `V+` and `GND`
- separate groups of parts with no shared net
- a controller whose shortest `V+` to `PITCH` path contains less than 10 kΩ of fixed resistance

For the controller rule, fixed resistors contribute their value and every variable or
non-resistive part contributes 0 Ω. This pessimistic calculation proves the documented
minimum even when an LDR or pencil track approaches zero resistance.

These checks do **not** simulate a circuit. They cannot prove current, voltage, timing,
stability, or electrolytic bias without a richer model. Those
properties remain design calculations and bench tests. Adding speculative rules here
would give false confidence.

An intentional teaching circuit can suppress one exact result with `Circuit(...,
allow={"same-net:R1"})`, `rail-short:W1`, or `disconnected`. Exceptions are visible in
the sheet's circuit declaration; unknown exception names fail validation. Prefer a
narrow part exception to the circuit-wide `disconnected` exception.
