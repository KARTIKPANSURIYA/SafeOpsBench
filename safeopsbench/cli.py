"""Rich command-line interface for tasks and repeated benchmarks."""

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from safeopsbench import __version__
from safeopsbench.agents.deterministic import (
    NaiveOrderAgent,
    RuleBasedSafeAgent,
    ScriptedCorrectAgent,
)
from safeopsbench.agents.random_agent import RandomToolAgent
from safeopsbench.config import Settings
from safeopsbench.core.environment import SafeOpsEnvironment
from safeopsbench.core.runner import run_agent
from safeopsbench.core.task import TaskDefinition, discover_tasks
from safeopsbench.core.validator import validate_tasks
from safeopsbench.metrics.scoring import aggregate

app = typer.Typer(help="Stateful enterprise agent safety benchmark.", no_args_is_help=True)
console = Console()


def _task(task_id: str) -> TaskDefinition:
    for task in discover_tasks():
        if task.id == task_id.upper():
            return task
    raise typer.BadParameter(f"Unknown task {task_id}")


def _agent(name: str, seed: int) -> Any:
    agents = {
        "scripted": ScriptedCorrectAgent,
        "rule-based-safe": RuleBasedSafeAgent,
        "naive": NaiveOrderAgent,
    }
    if name == "random":
        return RandomToolAgent(seed)
    if name not in agents:
        raise typer.BadParameter(f"Unknown agent {name}")
    return agents[name]()


def _write_run(
    environment: SafeOpsEnvironment,
    result: Any,
    agent: str,
    timestamp: str | None = None,
) -> Path:
    stamp = timestamp or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    root = Settings().results_dir / stamp / agent / environment.task.id / environment.run_id
    root.mkdir(parents=True, exist_ok=True)
    (root / "result.json").write_text(result.model_dump_json(indent=2))
    (root / "trajectory.json").write_text(environment.trajectory.model_dump_json(indent=2))
    (root / "final_state.json").write_text(json.dumps(result.final_state, indent=2))
    (root / "violations.json").write_text(
        json.dumps(
            [violation.model_dump(mode="json") for violation in environment.violations],
            indent=2,
        )
    )
    return root


@app.command()
def info() -> None:
    """Describe the benchmark."""
    console.print("[bold]SafeOpsBench[/bold]\nAgent quality is not equivalent to answer quality.")


@app.command("version")
def version_cmd() -> None:
    """Print the package version."""
    console.print(__version__)


@app.command("list-tasks")
def list_tasks() -> None:
    """List installed task definitions."""
    table = Table("ID", "Name", "Category", "Difficulty")
    for task in discover_tasks():
        table.add_row(task.id, task.name, task.category, str(task.difficulty))
    console.print(table)


@app.command("show-task")
def show_task(task_id: str) -> None:
    """Show a task definition."""
    console.print_json(_task(task_id).model_dump_json(indent=2))


@app.command("validate-tasks")
def validate_cmd() -> None:
    """Validate all task schemas and references."""
    console.print(f"[green]Validated {len(validate_tasks())} tasks.[/green]")


@app.command()
def doctor() -> None:
    """Check package, database, and task registry health."""
    tasks = validate_tasks()
    console.print(f"[green]OK[/green] Python/package/database/task registry ({len(tasks)} tasks)")


@app.command("seed-data")
def seed_data(output: Path = Path("safeopsbench.db")) -> None:
    """Create a persistent synthetic demonstration database."""
    from safeopsbench.db.seed import seed_session
    from safeopsbench.db.session import create_database

    engine, factory = create_database(f"sqlite+pysqlite:///{output}")
    session = factory()
    seed_session(session)
    session.close()
    engine.dispose()
    console.print(f"Seeded {output}")


@app.command()
def run(
    task_id: str,
    agent: str = typer.Option("rule-based-safe"),
    runs: int = typer.Option(1, min=1),
    seed: int = 42,
) -> None:
    """Run one task one or more times."""
    for index in range(runs):
        environment = SafeOpsEnvironment(_task(task_id), agent, seed + index)
        result = run_agent(environment, _agent(agent, seed + index))
        path = _write_run(environment, result, agent)
        console.print(
            f"{task_id} success={result.task_success} safe={result.safe_success} "
            f"unsafe_attempts={result.unsafe_action_attempts} result={path}"
        )
        environment.close()


@app.command()
def benchmark(
    agent: str = typer.Option("rule-based-safe"),
    runs: int = typer.Option(1, min=1),
    seed: int = 42,
) -> None:
    """Run all tasks and export detailed JSON and CSV evidence."""
    results = []
    table = Table("Task", "Success", "System Safe", "Unsafe Attempts", "Calls")
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    base = Settings().results_dir / timestamp / agent
    for task in discover_tasks():
        for index in range(runs):
            run_seed = seed + index
            environment = SafeOpsEnvironment(task, agent, run_seed)
            result = run_agent(environment, _agent(agent, run_seed))
            results.append(result)
            _write_run(environment, result, agent, timestamp)
            table.add_row(
                task.id,
                "✓" if result.task_success else "✗",
                "✓" if result.safe_success else "✗",
                str(result.unsafe_action_attempts),
                str(result.tool_calls),
            )
            environment.close()
    console.print(table)
    metrics = aggregate(results)
    base.mkdir(parents=True, exist_ok=True)
    (base / "summary.json").write_text(metrics.model_dump_json(indent=2))
    rows = []
    for result in results:
        row = result.model_dump(exclude={"final_state", "policy_violations", "critical_violations"})
        row["execution_duration"] = row.pop("execution_duration_seconds")
        rows.append(row)
    with (base / "summary.csv").open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    console.print(metrics.model_dump_json(indent=2))


if __name__ == "__main__":
    app()
