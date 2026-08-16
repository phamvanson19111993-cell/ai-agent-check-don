import time
from pathlib import Path

import pytest

from cleaner_agent.cleaner import run_once
from cleaner_agent.config import (
    AIConfig, Config, GeneralConfig, QuarantineConfig, SafetyConfig,
)
from cleaner_agent.quarantine import Quarantine
from cleaner_agent.rules import Rule
from cleaner_agent.safety import Guard
from cleaner_agent.scanner import scan

OLD = time.time() - 40 * 86400


def _age(path: Path, when: float = OLD) -> None:
    import os

    os.utime(path, (when, when))


@pytest.fixture
def home(tmp_path, monkeypatch):
    h = tmp_path / "home"
    (h / ".cache").mkdir(parents=True)
    (h / "Documents").mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: h))
    return h


def _rule(root: Path) -> Rule:
    return Rule(id="test", description="test", roots=[str(root)], min_age_days=7)


def test_scan_finds_old_files_only(home):
    cache = home / ".cache"
    old, new = cache / "old.tmp", cache / "new.tmp"
    old.write_text("aaaa")
    new.write_text("bbbb")
    _age(old)

    result = scan([_rule(cache)], Guard())
    paths = {c.path for c in result.candidates}
    assert old in paths
    assert new not in paths


def test_scan_never_leaves_the_rule_root_into_protected(home):
    cache = home / ".cache"
    (cache / "sub").mkdir()
    f = cache / "sub" / "junk.tmp"
    f.write_text("x")
    _age(f)

    result = scan([_rule(cache)], Guard())
    assert f in {c.path for c in result.candidates}

    doc = home / "Documents" / "junk.tmp"
    doc.write_text("x")
    _age(doc)
    result = scan([_rule(home / "Documents")], Guard())
    assert result.candidates == []


def _config(home: Path, **general) -> Config:
    return Config(
        general=GeneralConfig(**general),
        quarantine=QuarantineConfig(dir=home / "quarantine", retention_days=7),
        safety=SafetyConfig(),
        ai=AIConfig(enabled=False, review_roots=[]),
        state_dir=home / "state",
    )


def test_dry_run_touches_nothing(home, monkeypatch):
    f = home / ".cache" / "old.tmp"
    f.write_text("x" * 100)
    _age(f)

    monkeypatch.setattr(
        "cleaner_agent.cleaner.active_rules", lambda cfg: [_rule(home / ".cache")]
    )
    rep = run_once(_config(home, dry_run=True))

    assert rep.found == 1
    assert rep.cleaned == 0
    assert f.exists()


def test_apply_moves_to_quarantine_and_restores(home, monkeypatch):
    f = home / ".cache" / "old.tmp"
    f.write_text("x" * 100)
    _age(f)

    monkeypatch.setattr(
        "cleaner_agent.cleaner.active_rules", lambda cfg: [_rule(home / ".cache")]
    )
    cfg = _config(home, dry_run=False)
    rep = run_once(cfg, apply=True)

    assert rep.cleaned == 1
    assert not f.exists()

    q = Quarantine(cfg.quarantine.dir, cfg.quarantine.retention_days)
    entries = q.entries()
    assert len(entries) == 1

    restored = q.restore(entries[0].id)
    assert restored == f
    assert f.exists()
    assert f.read_text() == "x" * 100


def test_limits_are_respected(home, monkeypatch):
    for i in range(10):
        f = home / ".cache" / f"f{i}.tmp"
        f.write_text("x" * 1000)
        _age(f)

    monkeypatch.setattr(
        "cleaner_agent.cleaner.active_rules", lambda cfg: [_rule(home / ".cache")]
    )
    rep = run_once(_config(home, dry_run=True, max_delete_per_run=3))

    assert rep.found == 10
    assert len(rep.items) == 3
    assert "trần" in rep.note


def test_quarantine_purge_respects_retention(home):
    q = Quarantine(home / "quarantine", retention_days=7)
    f = home / ".cache" / "a.tmp"
    f.write_text("x")
    entry = q.store(f, "test", 1)

    assert q.purge(now=time.time())[0] == 0
    assert q.purge(now=time.time() + 8 * 86400)[0] == 1
    assert not Path(entry.stored_path).exists()
