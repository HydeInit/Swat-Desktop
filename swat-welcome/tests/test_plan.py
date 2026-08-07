from swat_cli.profile import find_profile
from swat_welcome.plan import build_plan


def test_build_plan_empty_selection():
    assert build_plan([]) == "No profiles selected - nothing would be done."


def test_build_plan_lists_host_packages_and_profile_names():
    core = find_profile("core")
    plan = build_plan([core])
    assert "podman" in plan
    assert core.name in plan
    assert "Dry run" in plan


def test_build_plan_dedupes_shared_host_packages():
    core = find_profile("core")
    java = find_profile("java")
    plan = build_plan([core, java])
    # "podman" appears in both profiles' host_packages - should be listed
    # once in the consolidated host packages line, not duplicated.
    host_line = next(line for line in plan.splitlines() if line.startswith("Host packages"))
    assert host_line.count("podman") == 1
