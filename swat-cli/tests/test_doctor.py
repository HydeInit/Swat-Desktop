from swat_cli.doctor import CheckResult, run_all


def test_run_all_returns_results_with_valid_status():
    results = run_all()
    assert results
    for result in results:
        assert isinstance(result, CheckResult)
        assert result.status in ("ok", "warn", "error")
        assert result.name
        assert result.message
