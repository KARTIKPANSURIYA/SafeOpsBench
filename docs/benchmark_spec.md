# Benchmark specification

Task schema `0.1` encodes public request and role, initial state, deterministic events, expected goal, reusable final-state constraints, and optional debugging gold trajectories. The agent sees only the request, tool descriptions, latest result, global policy context, and step number.

SafeOpsBench complements agent benchmarks by emphasizing persistent transactional state, business invariants, authorization, concurrent changes, side-effect safety, recovery, and enterprise policy. This is conceptual positioning, not a literature or novelty claim.

Goals are task-dependent: `requires_approval`, `blocked`, and `insufficient_inventory` may be successful outcomes. Exact trajectory equality is not scored. Gold trajectories estimate minimum calls and assist validation. Identical code, task data, and seeds produce equivalent decisions; wall-clock timestamps and UUID artifact identifiers differ.
