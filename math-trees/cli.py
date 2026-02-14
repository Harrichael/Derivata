#!/usr/bin/env python3
"""
Derivata CLI - Command-line interface for generating math trees and expressions
"""

import argparse
import os
import shutil
import sys


def get_latex_gen_dir():
    """Get the path to the latex_gen directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    return os.path.join(repo_root, 'latex_gen')


def cmd_clean(args):
    """Clean the latex_gen folder."""
    latex_gen_dir = get_latex_gen_dir()
    
    if not os.path.exists(latex_gen_dir):
        print(f"✓ latex_gen folder doesn't exist - nothing to clean")
        return 0
    
    # Count files before deletion
    files = [f for f in os.listdir(latex_gen_dir) if os.path.isfile(os.path.join(latex_gen_dir, f))]
    file_count = len(files)
    
    if file_count == 0:
        print(f"✓ latex_gen folder is already empty")
        return 0
    
    # Confirm deletion if not forced
    if not args.force:
        response = input(f"Delete {file_count} file(s) from latex_gen? [y/N] ")
        if response.lower() not in ['y', 'yes']:
            print("Cancelled")
            return 1
    
    # Remove all files (or dry-run)
    deleted_count = 0
    errors = []
    
    for filename in files:
        file_path = os.path.join(latex_gen_dir, filename)
        try:
            if os.path.exists(file_path):
                if args.dry_run:
                    print(f"  Would delete: {filename}")
                    deleted_count += 1
                else:
                    os.remove(file_path)
                    deleted_count += 1
        except Exception as e:
            errors.append(f"{filename}: {e}")
    
    if errors:
        print(f"✗ Errors occurred:")
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1
    
    if args.dry_run:
        print(f"✓ Dry run: would clean {deleted_count} file(s) from latex_gen")
    else:
        print(f"✓ Cleaned {deleted_count} file(s) from latex_gen")
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Derivata - Generate arithmetic expressions and visualize them as LaTeX trees',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s clean              # Clean the latex_gen folder (with confirmation)
  %(prog)s clean -f           # Clean without confirmation
  %(prog)s clean -n           # Dry run - show what would be deleted
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Clean command
    parser_clean = subparsers.add_parser('clean', help='Clean the latex_gen output folder')
    parser_clean.add_argument('-f', '--force', action='store_true', 
                             help='Skip confirmation prompt')
    parser_clean.add_argument('-n', '--dry-run', action='store_true',
                             help='Show what would be deleted without actually deleting')
    parser_clean.set_defaults(func=cmd_clean)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Show help if no command specified
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
