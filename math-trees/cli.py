#!/usr/bin/env python3
"""
Derivata CLI - Command-line interface for generating math trees and expressions
"""

import os
import sys
import click


def get_latex_gen_dir():
    """Get the path to the latex_gen directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    return os.path.join(repo_root, 'latex_gen')


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Derivata - Generate arithmetic expressions and visualize them as LaTeX trees"""
    pass


@cli.command()
@click.option('-f', '--force', is_flag=True, help='Skip confirmation prompt')
@click.option('-n', '--dry-run', is_flag=True, help='Show what would be deleted without actually deleting')
def clean(force, dry_run):
    """Clean the latex_gen output folder."""
    latex_gen_dir = get_latex_gen_dir()
    
    if not os.path.exists(latex_gen_dir):
        click.secho("✓ latex_gen folder doesn't exist - nothing to clean", fg='green')
        return
    
    # Count files before deletion
    files = [f for f in os.listdir(latex_gen_dir) if os.path.isfile(os.path.join(latex_gen_dir, f))]
    file_count = len(files)
    
    if file_count == 0:
        click.secho("✓ latex_gen folder is already empty", fg='green')
        return
    
    # Confirm deletion if not forced
    if not force:
        if not click.confirm(f"Delete {file_count} file(s) from latex_gen?"):
            click.echo("Cancelled")
            return
    
    # Remove all files (or dry-run)
    deleted_count = 0
    errors = []
    
    for filename in files:
        file_path = os.path.join(latex_gen_dir, filename)
        try:
            if os.path.exists(file_path):
                if dry_run:
                    click.echo(f"  Would delete: {filename}")
                    deleted_count += 1
                else:
                    os.remove(file_path)
                    deleted_count += 1
        except Exception as e:
            errors.append(f"{filename}: {e}")
    
    if errors:
        click.secho("✗ Errors occurred:", fg='red')
        for error in errors:
            click.echo(f"  {error}", err=True)
        sys.exit(1)
    
    if dry_run:
        click.secho(f"✓ Dry run: would clean {deleted_count} file(s) from latex_gen", fg='green')
    else:
        click.secho(f"✓ Cleaned {deleted_count} file(s) from latex_gen", fg='green')


if __name__ == '__main__':
    cli()
