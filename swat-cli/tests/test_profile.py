from swat_cli.profile import Profile, find_profile, load_profiles


def test_load_profiles_returns_valid_profiles():
    profiles = load_profiles()
    assert profiles
    ids = {p.id for p in profiles}
    assert {"core", "java", "python", "minecraft-neoforge"} <= ids
    for p in profiles:
        assert isinstance(p, Profile)
        assert p.name
        assert p.description
        assert p.version >= 1


def test_find_profile_returns_matching_profile():
    core = find_profile("core")
    assert core.id == "core"
    assert "podman" in core.host_packages
