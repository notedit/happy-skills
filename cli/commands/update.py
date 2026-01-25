"""hca update - Update deployed configurations."""

import json
from pathlib import Path
from typing import Dict, Optional

import click
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

from cli.core.config import (
    CLAUDE_DIR,
    COMPONENTS,
    DEFAULT_BRANCH,
    DEFAULT_SOURCE,
    get_metadata_path,
)
from cli.core.deployer import Deployer

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


@click.command("update")
@click.argument("component", required=False)
@click.option("--dry-run", is_flag=True, help="Preview update without applying")
@click.option(
    "--force", "-f", is_flag=True, help="Force update, ignore local changes"
)
@click.option("--source", "-s", help="Override source repository")
@click.option("--branch", "-b", help="Override source branch")
@click.pass_context
def update_cmd(
    ctx: click.Context,
    component: Optional[str],
    dry_run: bool,
    force: bool,
    source: Optional[str],
    branch: Optional[str],
) -> None:
    """Update deployed Happy Skills configurations.

    COMPONENT: Optional specific component to update (e.g., 'agents', 'skills')
    """
    cwd = Path.cwd()
    metadata = load_metadata(cwd)

    if not metadata:
        console.print("[red]No HCA deployment found.[/]")
        console.print("Run 'hca init' first to deploy configurations.")
        raise click.Abort()

    # Use stored source or override
    update_source = source or metadata.get("source", DEFAULT_SOURCE)
    update_branch = branch or metadata.get("branch", DEFAULT_BRANCH)

    console.print(f"[blue]Checking for updates from:[/] {update_source}")

    # Determine components to update
    if component:
        if component not in COMPONENTS:
            console.print(f"[red]Unknown component:[/] {component}")
            console.print(f"Available: {', '.join(COMPONENTS)}")
            raise click.Abort()
        components = [component]
    else:
        components = COMPONENTS.copy()

    # Create deployer and check for updates
    deployer = Deployer(update_source, update_branch)

    try:
        remote_manifest = deployer.get_manifest()
    except Exception as e:
        console.print(f"[red]Failed to fetch remote configuration:[/] {e}")
        raise click.Abort()

    # Compare with local
    local_components = metadata.get("components", {})
    updates_available = False

    table = Table(show_header=True, header_style="bold")
    table.add_column("Component")
    table.add_column("Local")
    table.add_column("Remote")
    table.add_column("Status")

    for comp in components:
        local_files = len(local_components.get(comp, {}).get("files", []))
        remote_files = len(remote_manifest.get(comp, []))

        if comp == "skills":
            # Skills are directories, count them differently
            remote_files = len(remote_manifest.get(comp, []))

        if remote_files != local_files:
            updates_available = True
            status = "[yellow]Update available[/]"
        else:
            status = "[green]Up to date[/]"

        table.add_row(comp, str(local_files), str(remote_files), status)

    console.print("\n[bold]Component Status:[/]")
    console.print(table)

    if not updates_available:
        console.print("\n[green]All components are up to date![/]")
        return

    if dry_run:
        console.print("\n[yellow]Dry run - no changes applied[/]")
        return

    if not force:
        if not Confirm.ask("\nProceed with update?", default=True):
            raise click.Abort()

    # Execute update
    try:
        with console.status("[bold green]Updating..."):
            result = deployer.deploy(cwd, components)

        console.print("\n[bold green]Update complete![/]")
        console.print(f"Version: {result['version']}")
        console.print(f"Commit: {result['commit'][:8]}")

    except Exception as e:
        console.print(f"[red]Update failed:[/] {e}")
        raise click.Abort()
