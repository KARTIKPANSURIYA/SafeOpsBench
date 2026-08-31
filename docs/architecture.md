# Architecture

`SafeOpsEnvironment` is the composition root: it creates a private SQLAlchemy engine/session, seeds task overrides, controls deterministic events, dispatches registered tools, enforces RBAC and policies, checks invariants before commit, and records trajectory plus audit evidence. Provider-neutral `Agent` observations expose globally documented policy context and tool schemas but never hidden expected states. Evaluation is constraint- and state-based, not exact gold-action matching. Protocols and registries allow new domains, tools, agents, and verifiers without modifying the execution loop.

Transactions prevent partial side effects. Controlled events—not threads—make TOCTOU experiments repeatable. Canonical SHA-256 snapshots omit timestamps and runtime metadata. Rule-based risk labels are infrastructure for future uncertainty, constraint, permission, and irreversibility risk research; v0.1 invents no learned coefficients.
