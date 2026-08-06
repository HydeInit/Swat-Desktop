from __future__ import annotations

import argparse
import dataclasses
import json
import sys

from swat_cli import doctor

# Exit codes: 0 = all checks passed, 1 = warnings only, 2 = at least one
# error, or the check itself could not run.
STATUS_EXIT_CODES = {"ok": 0, "warn": 1, "error": 2}
STATUS_SYMBOLS = {"ok": "OK", "warn": "WARN", "error": "ERROR"}


def run_doctor(args: argparse.Namespace) -> int:
    results = doctor.run_all()

    if args.json:
        print(json.dumps([dataclasses.asdict(r) for r in results], indent=2))
    else:
        for result in results:
            print(f"[{STATUS_SYMBOLS[result.status]:5}] {result.name}: {result.message}")

    return max((STATUS_EXIT_CODES[r.status] for r in results), default=0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="swat", description="SWAT system tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor", help="run read-only system diagnostics")
    doctor_parser.add_argument("--json", action="store_true", help="output results as JSON")
    doctor_parser.set_defaults(func=run_doctor)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
