"""hca status - Show deployment status."""

import json
from pathlib import Path
from typing import Dict, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cli.core.config import CLAUDE_DIR, COMPONENTS, get_metadata_path

console = Console()


def load_metadata(project_path: Path) -> Optional[Dict]:
    """Load metadata from a deployed project.

    Args:
        project_path: Path to the project

    Returns:
        Metadata dictionary or None if not found
    """
    metadata_path = get_metadata_path(project_path)
    if not metadata_path.exists():
        return None

    with open(metadata_path) as f:
        return json.load(f)


@click.command("status")
@click.option("--json-output", is_flag=True, help="Output as JSON")
@click.pass_context
def status_cmd(ctx: click.Context, json_output: bool) -> None:
    """Show Happy Skills deployment status."""
    cwd = Path.cwd()
    claude_dir = cwd / CLAUDE_DIR
    metadata = load_metadata(cwd)

    if json_output:
        if metadata:
            click.echo(json.dumps(metadata, indent=2))
        else:
            click.echo(json.dumps({"status": "not_deployed"}))
        return

    if not claude_dir.exists():
        console.print("[yellow]No .claude directory found.[/]")
        console.print("Run 'hca init' to deploy configurations.")
        return

    if not metadata:
        console.print("[yellow].claude directory exists but no HCA metadata found.[/]")
        console.print("This may be a manually created configuration.")
        _show_directory_contents(claude_dir)
        return

    # Show deployment info
    console.print(
        Panel.fit(
            f"[bold]Happy Skills[/]\n"
            f"Version: {metadata.get('version', 'unknown')}\n"
            f"Commit: {metadata.get('commit', 'unknown')[:8]}\n"
            f"Installed: {metadata.get('installed_at', 'unknown')[:10]}\n"
            f"Updated: {metadata.get('updated_at', 'unknown')[:10]}",
            title="Deployment Status",
            border_style="green",
        )
    )

    # Show components
    console.print("\n[bold]Deployed Components:[/]")
    table = Table(show_header=True, header_style="bold")
    table.add_column("Component")
    table.add_column("Status")
    table.add_column("Files")

    components = metadata.get("components", {})
    for comp in COMPONENTS:
        if comp in components:
            info = components[comp]
            status = "[green]Installed[/]"
            files = len(info.get("files", []))
        else:
            status = "[dim]Not installed[/]"
            files = 0

        table.add_row(comp, status, str(files))

    console.print(table)

    # Show source info
    console.print(f"\n[dim]Source: {metadata.get('source', 'unknown')}[/]")
    console.print(f"[dim]Branch: {metadata.get('branch', 'unknown')}[/]")


def _show_directory_contents(claude_dir: Path) -> None:
    """Show contents of .claude directory."""
    console.print("\n[bold]Directory contents:[/]")

    for item in sorted(claude_dir.iterdir()):
        if item.is_dir():
            count = len(list(item.rglob("*")))
            console.print(f"  [blue]{item.name}/[/] ({count} files)")
        else:
            console.print(f"  {item.name}")
