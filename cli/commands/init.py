"""hca init - Initialize .claude in current project."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from cli.core.config import CLAUDE_DIR, COMPONENTS, DEFAULT_BRANCH, DEFAULT_SOURCE
from cli.core.deployer import DeployMode, Deployer
from cli.core.git_ops import GitOps

console = Console()


@click.command("init")
@click.option(
    "--source",
    "-s",
    default=DEFAULT_SOURCE,
    help="Source repository URL or local path",
)
@click.option(
    "--branch",
    "-b",
    default=DEFAULT_BRANCH,
    help="Source repository branch",
)
@click.option(
    "--backup",
    is_flag=True,
    help="Backup existing .claude before deploying (non-interactive)",
)
@click.option(
    "--merge",
    is_flag=True,
    help="Merge with existing .claude, preserving user additions",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force overwrite without any confirmation",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Preview operations without executing",
)
@click.option("--agents-only", is_flag=True, help="Only deploy agents")
@click.option("--commands-only", is_flag=True, help="Only deploy commands")
@click.option("--skills-only", is_flag=True, help="Only deploy skills")
@click.option(
    "--select",
    is_flag=True,
    help="Interactively select components to deploy",
)
@click.pass_context
def init_cmd(
    ctx: click.Context,
    source: str,
    branch: str,
    backup: bool,
    merge: bool,
    force: bool,
    dry_run: bool,
    agents_only: bool,
    commands_only: bool,
    skills_only: bool,
    select: bool,
) -> None:
    """Initialize Happy Coding Agent in the current project."""
    cwd = Path.cwd()
    claude_dir = cwd / CLAUDE_DIR
    verbose = ctx.obj.get("verbose", False)
    git_ops = GitOps()

    # Validate mutually exclusive options
    if sum([backup, merge, force]) > 1:
        console.print(
            "[red]Error:[/] Options --backup, --merge, and --force are mutually exclusive"
        )
        raise click.Abort()

    # 1. Check if current directory is a git repository
    if not git_ops.is_git_repo(cwd):
        if not Confirm.ask(
            "[yellow]Warning:[/] Current directory is not a git repository. Continue?",
            default=False,
        ):
            raise click.Abort()

    # 2. Determine components to deploy
    components = _determine_components(
        agents_only, commands_only, skills_only, select
    )

    if not components:
        console.print("[red]No components selected. Aborting.[/]")
        raise click.Abort()

    # 3. Determine deploy mode and handle existing .claude directory
    deploy_mode = DeployMode.OVERWRITE
    backup_path: Optional[Path] = None

    if claude_dir.exists():
        mode_choice, backup_path = _handle_existing_claude(
            claude_dir, backup=backup, merge=merge, force=force, dry_run=dry_run
        )
        if mode_choice == "abort":
            raise click.Abort()
        elif mode_choice == "merge":
            deploy_mode = DeployMode.MERGE

    # 4. Fetch source configuration
    console.print(f"\n[blue]Fetching configuration from:[/] {source} ({branch})")

    deployer = Deployer(source, branch, verbose=verbose)

    if dry_run:
        console.print("\n[yellow]Dry run mode - no changes will be made[/]")
        _preview_deployment(deployer, components, deploy_mode)
        return

    # 5. Execute deployment
    try:
        with console.status("[bold green]Deploying..."):
            result = deployer.deploy(cwd, components, mode=deploy_mode)
        _show_deployment_summary(result, backup_path)
    except Exception as e:
        console.print(f"[red]Deployment failed:[/] {e}")
        raise click.Abort()


def _determine_components(
    agents_only: bool,
    commands_only: bool,
    skills_only: bool,
    select: bool,
) -> List[str]:
    """Determine which components to deploy based on options."""
    if agents_only:
        return ["agents"]
    if commands_only:
        return ["commands"]
    if skills_only:
        return ["skills"]

    if select:
        # Interactive selection
        console.print("\n[bold]Select components to deploy:[/]")
        components = []
        if Confirm.ask("  Deploy agents?", default=True):
            components.append("agents")
        if Confirm.ask("  Deploy commands?", default=True):
            components.append("commands")
        if Confirm.ask("  Deploy skills?", default=True):
            components.append("skills")
        return components

    # Default: deploy all
    return COMPONENTS.copy()


def _handle_existing_claude(
    claude_dir: Path,
    backup: bool = False,
    merge: bool = False,
    force: bool = False,
    dry_run: bool = False,
) -> tuple[str, Optional[Path]]:
    """Handle existing .claude directory.

    Args:
        claude_dir: Path to existing .claude directory
        backup: Use backup mode (non-interactive)
        merge: Use merge mode (non-interactive)
        force: Force overwrite without confirmation
        dry_run: Preview mode

    Returns:
        Tuple of (mode_choice, backup_path)
        mode_choice: "backup", "merge", "overwrite", or "abort"
        backup_path: Path to backup directory if created, None otherwise
    """
    console.print("\n[yellow]Existing .claude directory found[/]")

    if dry_run:
        if merge:
            console.print("  Would merge with existing directory")
            return ("merge", None)
        elif backup:
            console.print("  Would backup existing directory before deploying")
            return ("backup", None)
        elif force:
            console.print("  Would overwrite existing directory")
            return ("overwrite", None)
        else:
            console.print("  Would prompt for handling strategy")
            return ("overwrite", None)

    # Non-interactive modes
    if force:
        shutil.rmtree(claude_dir)
        console.print("  [yellow]Removed existing .claude directory[/]")
        return ("overwrite", None)

    if backup:
        backup_path = _backup_and_remove(claude_dir)
        return ("backup", backup_path)

    if merge:
        console.print("  [blue]Will merge with existing configuration[/]")
        return ("merge", None)

    # Interactive prompt - show detailed options
    console.print("\n[bold]Choose how to handle existing configuration:[/]")
    console.print("  [cyan]backup[/]    - Save existing .claude to a backup, then deploy fresh")
    console.print("  [cyan]merge[/]     - Keep your additions, update source files")
    console.print("  [cyan]overwrite[/] - Remove existing and deploy fresh (no backup)")
    console.print("  [cyan]abort[/]     - Cancel operation")
    console.print("")

    choice = Prompt.ask(
        "Your choice",
        choices=["backup", "merge", "overwrite", "abort"],
        default="merge",
    )

    if choice == "abort":
        return ("abort", None)
    elif choice == "backup":
        backup_path = _backup_and_remove(claude_dir)
        return ("backup", backup_path)
    elif choice == "merge":
        console.print("  [blue]Will merge with existing configuration[/]")
        return ("merge", None)
    else:  # overwrite
        shutil.rmtree(claude_dir)
        console.print("  [yellow]Removed existing .claude directory[/]")
        return ("overwrite", None)


def _backup_and_remove(claude_dir: Path) -> Path:
    """Backup existing .claude directory and remove it.

    Returns:
        Path to the backup directory
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = claude_dir.parent / f".claude-backup-{timestamp}"

    shutil.move(str(claude_dir), str(backup_dir))
    console.print(f"  [green]Backed up to:[/] {backup_dir.name}")

    return backup_dir


def _preview_deployment(
    deployer: Deployer, components: List[str], mode: DeployMode = DeployMode.OVERWRITE
) -> None:
    """Preview what would be deployed."""
    console.print(f"\n[bold]Deploy mode:[/] {mode.value}")
    console.print("\n[bold]Components to deploy:[/]")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Component")
    table.add_column("Files/Directories")

    manifest = deployer.get_manifest()

    for component in components:
        items = manifest.get(component, [])
        table.add_row(component, ", ".join(items[:5]) + ("..." if len(items) > 5 else ""))

    console.print(table)

    if mode == DeployMode.MERGE:
        console.print("\n[dim]Merge mode will preserve your custom additions[/]")


def _show_deployment_summary(result: dict, backup_path: Optional[Path] = None) -> None:
    """Show deployment summary."""
    console.print("\n" + "=" * 50)
    console.print("[bold green]Deployment Complete![/]")
    console.print("=" * 50)

    # Show mode info
    mode = result.get("mode", "overwrite")
    console.print(f"\n[bold]Mode:[/] {mode}")

    if backup_path:
        console.print(f"[bold]Backup:[/] {backup_path.name}")

    # Main components table
    table = Table(show_header=True, header_style="bold")
    table.add_column("Component")
    table.add_column("Status")
    table.add_column("Files")

    for component, info in result["components"].items():
        status = "[green]OK[/]" if info["success"] else "[red]FAILED[/]"
        table.add_row(component, status, str(info["count"]))

    console.print(table)

    # Show merge statistics if applicable
    merge_stats = result.get("merge_stats", {})
    if merge_stats:
        console.print("\n[bold]Merge Details:[/]")
        for component, stats in merge_stats.items():
            console.print(f"\n  [cyan]{component}:[/]")
            if stats.get("updated"):
                console.print(f"    Updated: {len(stats['updated'])} items")
            if stats.get("added"):
                console.print(f"    Added: {len(stats['added'])} items")
            if stats.get("preserved"):
                console.print(
                    f"    [green]Preserved (your additions):[/] {len(stats['preserved'])} items"
                )
                for item in stats["preserved"]:
                    console.print(f"      - {item}")

    console.print(f"\n[dim]Version: {result['version']}[/]")
    console.print(f"[dim]Commit: {result['commit'][:8]}[/]")
    console.print("\n[bold]Next steps:[/]")
    console.print("  1. Review deployed configurations in .claude/")
    console.print("  2. Run 'hca status' to verify deployment")
    console.print("  3. Start using /feature-analyzer and other commands!")
