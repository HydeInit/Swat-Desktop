from __future__ import annotations

import argparse
import dataclasses
import json
import sys

from swat_cli import doctor, profile

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


def run_profile_list(args: argparse.Namespace) -> int:
    try:
        profiles = profile.load_profiles()
    except profile.ProfileError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([dataclasses.asdict(p) for p in profiles], indent=2))
    else:
        for p in profiles:
            print(f"{p.id:20} {p.name}")
    return 0


def run_profile_show(args: argparse.Namespace) -> int:
    try:
        p = profile.find_profile(args.profile_id)
    except profile.ProfileError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(dataclasses.asdict(p), indent=2))
    else:
        print(f"{p.name} ({p.id}, v{p.version})")
        print(p.description)
        if p.host_packages:
            print(f"\nHost packages: {', '.join(p.host_packages)}")
        if p.environment:
            print(f"\nContainer environment: {p.environment}")
        if p.recommended_apps:
            print(f"\nRecommended apps: {', '.join(p.recommended_apps)}")
        if p.checks:
            print(f"\nVerification commands: {', '.join(p.checks)}")
    return 0


def run_profile_apply(args: argparse.Namespace) -> int:
    print(
        "swat profile apply is not implemented yet - profiles can be listed "
        "and inspected, but nothing installs anything yet.",
        file=sys.stderr,
    )
    return 1


def run_profile_remove(args: argparse.Namespace) -> int:
    print(
        "swat profile remove is not implemented yet - nothing has been "
        "applied by this tool, so there's nothing to remove.",
        file=sys.stderr,
    )
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="swat", description="SWAT system tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor", help="run read-only system diagnostics")
    doctor_parser.add_argument("--json", action="store_true", help="output results as JSON")
    doctor_parser.set_defaults(func=run_doctor)

    profile_parser = subparsers.add_parser("profile", help="inspect development profiles")
    profile_subparsers = profile_parser.add_subparsers(dest="profile_command", required=True)

    list_parser = profile_subparsers.add_parser("list", help="list available profiles")
    list_parser.add_argument("--json", action="store_true", help="output results as JSON")
    list_parser.set_defaults(func=run_profile_list)

    show_parser = profile_subparsers.add_parser("show", help="show details for one profile")
    show_parser.add_argument("profile_id", help="profile id, e.g. 'core'")
    show_parser.add_argument("--json", action="store_true", help="output results as JSON")
    show_parser.set_defaults(func=run_profile_show)

    apply_parser = profile_subparsers.add_parser("apply", help="apply a profile (not implemented yet)")
    apply_parser.add_argument("profile_id")
    apply_parser.set_defaults(func=run_profile_apply)

    remove_parser = profile_subparsers.add_parser("remove", help="remove a profile (not implemented yet)")
    remove_parser.add_argument("profile_id")
    remove_parser.set_defaults(func=run_profile_remove)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
