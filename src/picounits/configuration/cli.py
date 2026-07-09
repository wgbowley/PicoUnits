"""
Filename: cli.py

Description:
    Simple command line tool to generate the '.picounits'
    automatically to working directories
"""


from __future__ import annotations

import argparse
from pathlib import Path

from picounits.configuration.picounits import DEFAULT_CONFIG


def generate(args: argparse.Namespace | None = None) -> None:
    """ Generates the '.picounits' file in working directories """
    _ = args

    target = Path.cwd() / ".picounits"
    if target.exists():
        print(f"Warning: .picounits already exists at {target}")
        reply = input("Overwrite? (y/N): ").strip().lower()

        # Asks the user if they want to overwrite past file
        if reply == "n":
            print("Aborted. No changes made.")
            return

    try:
        target.write_text(DEFAULT_CONFIG.strip() + "\n", encoding="utf-8")
        print(f"Successfully created .picounits at:\n   {target}")
        print("\n You can now edit it to switch to custom symbols (t/l/m)")
        print(" or change the dimension order.")
        print(" picounits will automatically use your settings in this project!")

    except OSError as e:
        print(f"Failed to write .picounits to {target}: {e}")
        return

    # Asks the user if they want to see the configuration structure
    reply = input("   Show the generated config now? (Y/n): ").strip().lower()

    if reply == "y":
        print("\n--- Generated .picounits content ---")
        print(DEFAULT_CONFIG)
        print("------------------------------------")


def main(args: argparse.Namespace | None = None) -> None:
    """ Adds the argparse argument """
    parser = argparse.ArgumentParser(
        prog="picounits", description="picounits — flexible, project-aware units for Python"
    )

    # Adds the `generate` argument for `picounits`
    subparsers = parser.add_subparsers()
    gen_parser = subparsers.add_parser(
        "generate",
        help=("Create a default .picounits config file in the current directory"),
        description=(
            "Generate a ready-to-use .picounits file with helpful"
            "comments " "and both SI defaults and common alternatives."
        )
    )

    gen_parser.set_defaults(func=generate)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        # If there is no functions to execute, prints help and exits
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
