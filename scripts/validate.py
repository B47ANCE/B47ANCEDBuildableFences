"""Run only offline regression/version gates and preserve their output."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
header = f"Project Version: {version}\nEnvironment: Windows offline Python/Lupa; no PZ runtime\n\n"
logs = ROOT / "docs/evidence"
for filename in ("offline-tests.txt", "version-check.txt"):
    (logs / filename).write_text(header + "Validation pending\n", encoding="utf-8")
commands = [
    ("offline-tests.txt", [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"]),
    ("version-check.txt", [sys.executable, str(ROOT / "scripts/check_versions.py"), "--root", str(ROOT)]),
]
exit_code = 0
for filename, command in commands:
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    output = result.stdout + result.stderr
    record = header + "Command: " + subprocess.list2cmdline(command) + "\nExit: " + str(result.returncode) + "\n\n" + output
    (logs / filename).write_text(record, encoding="utf-8")
    print(output)
    exit_code = exit_code or result.returncode
raise SystemExit(exit_code)
