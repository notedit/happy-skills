#!/usr/bin/env python3
"""
Happy Skills CLI - Deploy .claude configurations to any git project.

Usage:
    hca init          Initialize .claude in current project
    hca update        Update deployed configurations
    hca status        Show deployment status
"""

import click

from cli import __version__
from cli.commands import init, status, update


@click.group()
@click.version_option(version=__version__, prog_name="hca")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Happy Skills - Deploy Claude configurations to your project."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


cli.add_command(init.init_cmd, name="init")
cli.add_command(update.update_cmd, name="update")
cli.add_command(status.status_cmd, name="status")


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
