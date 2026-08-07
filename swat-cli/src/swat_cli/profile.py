"""Development profile loading and inspection - reads and validates profile
YAML files against profiles/schema.json. Read-only: no packages installed,
no containers created."""

from __future__ import annotations

import dataclasses
import json
import os
from pathlib import Path

import jsonschema
import yaml

# Repo-layout-relative default (swat-cli/src/swat_cli/profile.py -> repo
# root -> profiles/), which is what an editable dev install resolves to.
# Overridable via SWAT_PROFILES_DIR since this assumption won't hold once
# swat-cli is actually packaged/installed - that path decision is for
# when this gets wired into the ISO, not this prototype.
DEFAULT_PROFILES_DIR = Path(__file__).resolve().parents[3] / "profiles"


class ProfileError(Exception):
    pass


@dataclasses.dataclass
class Profile:
    id: str
    name: str
    description: str
    version: int
    host_packages: list
    environment: dict
    recommended_apps: list
    checks: list

    @classmethod
    def from_dict(cls, data: dict) -> "Profile":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            version=data["version"],
            host_packages=data.get("host_packages", []),
            environment=data.get("environment", {}),
            recommended_apps=data.get("recommended_apps", []),
            checks=data.get("checks", []),
        )


def _profiles_dir() -> Path:
    override = os.environ.get("SWAT_PROFILES_DIR")
    return Path(override) if override else DEFAULT_PROFILES_DIR


def load_schema(profiles_dir: Path | None = None) -> dict:
    directory = profiles_dir or _profiles_dir()
    schema_path = directory / "schema.json"
    if not schema_path.is_file():
        raise ProfileError(f"schema not found: {schema_path}")
    return json.loads(schema_path.read_text())


def _load_profile_file(yaml_path: Path, schema: dict) -> Profile:
    data = yaml.safe_load(yaml_path.read_text())
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as exc:
        raise ProfileError(f"{yaml_path.name}: {exc.message}") from exc
    return Profile.from_dict(data)


def load_profiles(profiles_dir: Path | None = None) -> list[Profile]:
    directory = profiles_dir or _profiles_dir()
    if not directory.is_dir():
        raise ProfileError(f"profiles directory not found: {directory}")

    schema = load_schema(directory)
    return [_load_profile_file(p, schema) for p in sorted(directory.glob("*.yaml"))]


def find_profile(profile_id: str, profiles_dir: Path | None = None) -> Profile:
    directory = profiles_dir or _profiles_dir()
    yaml_path = directory / f"{profile_id}.yaml"
    if not yaml_path.is_file():
        raise ProfileError(f"no such profile: {profile_id}")
    return _load_profile_file(yaml_path, load_schema(directory))
