"""Test isolated, idempotent installation and conflict refusal."""
from pathlib import Path
import shutil
import subprocess
import sys
import uuid


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.py"


def run(home: Path, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(INSTALLER), "--home", str(home), "--codex-home", str(home / ".codex")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == expected, result.stdout + result.stderr
    return result


def main() -> None:
    home = ROOT / f".test-home-{uuid.uuid4().hex}"
    home.mkdir()
    try:
        run(home)
        skill = home / ".agents" / "skills" / "orchestrate-super-save" / "SKILL.md"
        assert skill.is_file()
        assert not (home / ".agents" / "skills" / "orchestrate" / "SKILL.md").exists()
        for role in ("scout", "researcher", "coder", "architect"):
            assert (home / ".codex" / "agents" / f"super-save-{role}.toml").is_file()
        before = skill.read_bytes()
        run(home)
        assert skill.read_bytes() == before
        target = home / ".codex" / "agents" / "super-save-scout.toml"
        target.write_text("conflict", encoding="utf-8")
        result = run(home, expected=2)
        assert "conflict" in (result.stdout + result.stderr).lower()
    finally:
        shutil.rmtree(home)
    print("PASS: isolated install, original untouched, idempotence, and conflict refusal")


if __name__ == "__main__":
    main()
