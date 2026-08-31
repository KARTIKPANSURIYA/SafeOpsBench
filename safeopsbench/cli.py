"""Rich Typer command-line interface."""
import csv,json
from datetime import datetime,timezone
from pathlib import Path
from typing import Any
import typer
from rich.console import Console
from rich.table import Table
from safeopsbench import __version__
from safeopsbench.agents.deterministic import NaiveOrderAgent,RuleBasedSafeAgent,ScriptedCorrectAgent
from safeopsbench.agents.random_agent import RandomToolAgent
from safeopsbench.config import Settings
from safeopsbench.core.environment import SafeOpsEnvironment
from safeopsbench.core.runner import run_agent
from safeopsbench.core.task import TaskDefinition,discover_tasks
from safeopsbench.core.validator import validate_tasks
from safeopsbench.metrics.scoring import aggregate
app=typer.Typer(help="Stateful enterprise agent safety benchmark.",no_args_is_help=True);console=Console()
def _task(task_id:str)->TaskDefinition:
 for task in discover_tasks():
  if task.id==task_id.upper():return task
 raise typer.BadParameter(f"Unknown task {task_id}")
def _agent(name:str,seed:int)->Any:
 agents={"scripted":ScriptedCorrectAgent,"rule-based-safe":RuleBasedSafeAgent,"naive":NaiveOrderAgent}
 return RandomToolAgent(seed) if name=="random" else agents[name]()
def _save(env:SafeOpsEnvironment,result:Any,agent:str)->Path:
 root=Settings().results_dir/datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")/agent/env.task.id/env.run_id;root.mkdir(parents=True,exist_ok=True)
 (root/"result.json").write_text(result.model_dump_json(indent=2));(root/"trajectory.json").write_text(env.trajectory.model_dump_json(indent=2));(root/"final_state.json").write_text(json.dumps(result.final_state,indent=2));(root/"violations.json").write_text(json.dumps([x.model_dump(mode="json") for x in env.violations],indent=2));return root
@app.command()
def info()->None:console.print("[bold]SafeOpsBench[/bold]\nAgent quality is not equivalent to answer quality.")
@app.command("version")
def version_cmd()->None:console.print(__version__)
@app.command("list-tasks")
def list_tasks()->None:
 table=Table("ID","Name","Category","Difficulty")
 for t in discover_tasks():table.add_row(t.id,t.name,t.category,str(t.difficulty))
 console.print(table)
@app.command("show-task")
def show_task(task_id:str)->None:console.print_json(_task(task_id).model_dump_json(indent=2))
@app.command("validate-tasks")
def validate_cmd()->None:console.print(f"[green]Validated {len(validate_tasks())} tasks.[/green]")
@app.command()
def doctor()->None:
 tasks=validate_tasks();console.print(f"[green]OK[/green] Python/package/database/task registry ({len(tasks)} tasks)")
@app.command("seed-data")
def seed_data(output:Path=Path("safeopsbench.db"))->None:
 from safeopsbench.db.seed import seed_session
 from safeopsbench.db.session import create_database
 engine,factory=create_database(f"sqlite+pysqlite:///{output}");s=factory();seed_session(s);s.close();engine.dispose();console.print(f"Seeded {output}")
@app.command()
def run(task_id:str,agent:str=typer.Option("rule-based-safe"),runs:int=typer.Option(1,min=1),seed:int=42)->None:
 for i in range(runs):
  env=SafeOpsEnvironment(_task(task_id),agent,seed+i);result=run_agent(env,_agent(agent,seed+i));path=_save(env,result,agent);console.print(f"{task_id} success={result.task_success} safe={result.safe_success} calls={result.tool_calls} result={path}");env.close()
@app.command()
def benchmark(agent:str=typer.Option("rule-based-safe"),runs:int=typer.Option(1,min=1),seed:int=42)->None:
 results=[];table=Table("Task","Success","Safe","Violations","Calls","Status");stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ");base=Settings().results_dir/stamp/agent
 for t in discover_tasks():
  for i in range(runs):
   env=SafeOpsEnvironment(t,agent,seed+i);r=run_agent(env,_agent(agent,seed+i));results.append(r);_save(env,r,agent);table.add_row(t.id,"✓" if r.task_success else "✗","✓" if r.safe_success else "✗",str(len(r.policy_violations)),str(r.tool_calls),"PASS" if r.safe_success else "FAIL");env.close()
 console.print(table);metrics=aggregate(results);base.mkdir(parents=True,exist_ok=True);(base/"summary.json").write_text(metrics.model_dump_json(indent=2));
 with (base/"summary.csv").open("w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(results[0].model_dump()));w.writeheader();w.writerows([{k:(json.dumps(v) if isinstance(v,(list,dict)) else v) for k,v in r.model_dump().items()} for r in results])
 console.print(metrics.model_dump_json(indent=2))
if __name__=="__main__":app()
