# Task authoring

Copy a YAML task, choose a unique `Cddd` ID, declare public setup and event triggers, then express expected goals and constraints without embedding task-specific evaluator code. Refer only to registered tools and policies. Events support `before_tool`, `after_tool`, `after_n_steps`, `on_tool_name`, and timestamp fields; implemented fixtures include inventory reservation, account hold, approval resolution, stale/failure simulation. Run `uv run safeopsbench validate-tasks`. Gold actions are optional and never an answer key exposed to agents.
