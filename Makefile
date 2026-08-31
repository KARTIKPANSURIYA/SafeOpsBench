.PHONY: sync check test benchmark
sync:
	uv sync
test:
	uv run pytest
check:
	./scripts/run_all_checks.sh
benchmark:
	uv run safeopsbench benchmark --agent rule-based-safe
