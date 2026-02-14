#!/usr/bin/env python3
"""
Derivata CLI - Command-line interface for generating math trees and expressions
"""

import os
import sys
import click

# Add math-trees to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'math-trees'))

from generate_arithmetic_tree import generate_arithmetic_tree_latex


def get_gen_dir():
    """Get the path to the gen directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    return os.path.join(repo_root, 'gen')


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Derivata - Generate arithmetic expressions and visualize them as LaTeX trees"""
    pass


@cli.command()
@click.option('-f', '--force', is_flag=True, help='Skip confirmation prompt')
@click.option('-n', '--dry-run', is_flag=True, help='Show what would be deleted without actually deleting')
def clean(force, dry_run):
    """Clean the gen output folder."""
    gen_dir = get_gen_dir()
    
    if not os.path.exists(gen_dir):
        click.secho("✓ gen folder doesn't exist - nothing to clean", fg='green')
        return
    
    # Count files before deletion
    files = sorted([f for f in os.listdir(gen_dir) if os.path.isfile(os.path.join(gen_dir, f))])
    file_count = len(files)
    
    if file_count == 0:
        click.secho("✓ gen folder is already empty", fg='green')
        return
    
    # Confirm deletion if not forced
    if not force:
        # Show up to 4 files
        files_to_show = files[:4]
        click.echo(f"Delete {file_count} file(s) from gen:")
        for i, filename in enumerate(files_to_show, 1):
            click.echo(f"  {i}. {filename}")
        if file_count > 4:
            click.echo(f"  ... and {file_count - 4} more")

        if not click.confirm("Continue?"):
            click.echo("Cancelled")
            return
    
    # Remove all files (or dry-run)
    deleted_count = 0
    errors = []
    
    for filename in files:
        file_path = os.path.join(gen_dir, filename)
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
        click.secho(f"✓ Dry run: would clean {deleted_count} file(s) from gen", fg='green')
    else:
        click.secho(f"✓ Cleaned {deleted_count} file(s) from gen", fg='green')


@cli.command()
@click.option('-t', '--target', type=int, default=42, show_default=True, 
              help='Target value for the arithmetic expression')
@click.option('-d', '--depth', type=int, default=2, show_default=True,
              help='Depth of the expression tree (number of operation levels)')
@click.option('-o', '--output', type=str, default='tree.tex', show_default=True,
              help='Output filename (in gen folder)')
@click.option('--no-pdf', is_flag=True, help='Skip PDF compilation')
def generate(target, depth, output, no_pdf):
    """Generate an arithmetic expression tree."""
    
    if depth < 0:
        click.secho("✗ Depth must be non-negative", fg='red')
        sys.exit(1)
    
    if not output.endswith('.tex'):
        output = f"{output}.tex"
    
    try:
        click.echo(f"Generating arithmetic expression tree:")
        click.echo(f"  Target value: {target}")
        click.echo(f"  Depth: {depth}")
        click.echo(f"  Output: {output}")
        click.echo()
        
        generate_arithmetic_tree_latex(
            target_value=target,
            depth=depth,
            output_filename=output,
            compile_pdf=not no_pdf
        )
        
    except Exception as e:
        click.secho(f"✗ Error generating tree: {e}", fg='red')
        sys.exit(1)


if __name__ == '__main__':
    cli()
