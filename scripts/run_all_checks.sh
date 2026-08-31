#!/usr/bin/env bash
set -euo pipefail
uv run ruff check .
uv run ruff format --check .
uv run mypy safeopsbench
uv run pytest --cov=safeopsbench
uv run safeopsbench validate-tasks
