"""Install Orchestrate Codex Super Save without changing default routing."""
from __future__ import annotations

import argparse
import filecmp
import os
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]


def same_tree(source: Path, destination: Path) -> bool:
    left = {p.relative_to(source): p.is_dir() for p in source.rglob("*")}
    right = {p.relative_to(destination): p.is_dir() for p in destination.rglob("*")}
    return left == right and all(
        is_dir or filecmp.cmp(source / rel, destination / rel, shallow=False)
        for rel, is_dir in left.items()
    )


def same_path(source: Path, destination: Path) -> bool:
    if source.is_dir() and destination.is_dir():
        return same_tree(source, destination)
    return source.is_file() and destination.is_file() and filecmp.cmp(source, destination, shallow=False)


def install(home: Path, codex_home: Path) -> None:
    source_skill = ROOT / ".agents" / "skills" / "orchestrate-super-save"
    target_skill = home / ".agents" / "skills" / "orchestrate-super-save"
    source_agents = sorted((ROOT / ".codex" / "agents").glob("super-save-*.toml"))
    target_agents = codex_home / "agents"
    planned = [(source_skill, target_skill)] + [(p, target_agents / p.name) for p in source_agents]
    conflicts = [str(dst) for src, dst in planned if dst.exists() and not same_path(src, dst)]
    if conflicts:
        raise FileExistsError("Conflicting local files:\n- " + "\n- ".join(conflicts))
    if not target_skill.exists():
        target_skill.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_skill, target_skill)
    target_agents.mkdir(parents=True, exist_ok=True)
    for source in source_agents:
        target = target_agents / source.name
        if not target.exists():
            shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--codex-home", type=Path)
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    codex_home = (args.codex_home or Path(os.environ.get("CODEX_HOME", home / ".codex"))).expanduser().resolve()
    try:
        install(home, codex_home)
    except FileExistsError as exc:
        print(f"Installation conflict: {exc}", file=sys.stderr)
        return 2
    print("Orchestrate Super Save installed. Restart Codex, then invoke $orchestrate-super-save.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

