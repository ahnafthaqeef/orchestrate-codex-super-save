"""Validate the portable Super Save bundle without network access."""
from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "super-save-scout": ("gpt-5.6-luna", "medium"),
    "super-save-researcher": ("gpt-5.6-luna", "xhigh"),
    "super-save-coder": ("gpt-5.6-luna", "max"),
}


def main() -> None:
    config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
    assert config["features"]["multi_agent"] is True
    assert config["agents"]["max_threads"] == 2
    found = {}
    for path in sorted((ROOT / ".codex" / "agents").glob("*.toml")):
        role = tomllib.loads(path.read_text(encoding="utf-8"))
        assert role["name"] == path.stem
        assert role.get("developer_instructions", "").strip()
        found[role["name"]] = role
    assert set(found) == set(EXPECTED) | {"super-save-architect"}
    for name, pair in EXPECTED.items():
        assert (found[name]["model"], found[name]["model_reasoning_effort"]) == pair
    architect = found["super-save-architect"]
    assert "model" not in architect and "model_reasoning_effort" not in architect
    skill = (ROOT / ".agents" / "skills" / "orchestrate-super-save" / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\nname: orchestrate-super-save\n")
    normalized_skill = " ".join(skill.lower().split())
    for phrase in ("at most two", "explicit user approval", "gpt-5.6-luna / max"):
        assert phrase in normalized_skill
    assert (ROOT / "LICENSE").is_file()
    print("PASS: skill, four unique roles, two-worker cap, model routing, and MIT license")


if __name__ == "__main__":
    main()
