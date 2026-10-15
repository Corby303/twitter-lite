import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("duration, expected_status", [(0.1, 0), (2.0, 1), (3.0, 1)])
def test_benchmark_cli_exit_status_matches_target(duration, expected_status):
    script = Path(__file__).resolve().parents[1] / "scripts" / "measure_feed.py"
    # Exercise the CLI without sleeping or depending on the machine's speed.
    probe = """
import runpy
import sys
from unittest.mock import patch

duration = float(sys.argv[1])
ticks = iter(value for i in range(20) for value in (i * 10.0, i * 10.0 + duration))
with patch("time.perf_counter", side_effect=lambda: next(ticks)):
    runpy.run_path(sys.argv[2], run_name="__main__")
"""
    result = subprocess.run(
        [sys.executable, "-c", probe, str(duration), str(script)],
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == expected_status, result.stdout + result.stderr
    expected_result = "PASS" if expected_status == 0 else "FAIL"
    assert f"Target p95 < 2s: {expected_result}" in result.stdout
