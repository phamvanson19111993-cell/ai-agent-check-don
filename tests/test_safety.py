from pathlib import Path

import pytest

from cleaner_agent.safety import Guard, is_within


@pytest.fixture
def home(tmp_path, monkeypatch):
    h = tmp_path / "home"
    (h / "Documents").mkdir(parents=True)
    (h / ".cache").mkdir()
    (h / ".ssh").mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: h))
    return h


def test_blocks_documents(home):
    g = Guard()
    f = home / "Documents" / "hop-dong.pdf"
    f.write_text("x")
    assert not g.check(f).allowed


def test_blocks_ssh_keys(home):
    g = Guard()
    f = home / ".ssh" / "id_rsa"
    f.write_text("x")
    assert not g.check(f).allowed


def test_blocks_home_itself(home):
    assert not Guard().check(home).allowed


def test_blocks_system_roots(home):
    g = Guard()
    assert not g.check(Path("/etc/passwd")).allowed
    assert not g.check(Path("/")).allowed


def test_allows_cache_file(home):
    g = Guard()
    f = home / ".cache" / "thumb.png"
    f.write_text("x")
    assert g.check(f).allowed


def test_blocks_sensitive_suffix_even_in_cache(home):
    g = Guard()
    f = home / ".cache" / "server.pem"
    f.write_text("x")
    assert not g.check(f).allowed


def test_blocks_git_worktree(home):
    g = Guard()
    d = home / ".cache" / "proj" / ".git" / "objects"
    d.mkdir(parents=True)
    f = d / "abc123"
    f.write_text("x")
    assert not g.check(f).allowed


def test_unprotect_opens_one_personal_dir(home):
    target = home / "Documents" / "Zalo Received Files"
    target.mkdir()
    f = target / "anh-cu.jpg"
    f.write_text("x")

    assert not Guard().check(f).allowed
    assert Guard(unprotect=[target]).check(f).allowed


def test_unprotect_cannot_open_sensitive_dirs(home):
    f = home / ".ssh" / "id_rsa"
    f.write_text("x")
    assert not Guard(unprotect=[home / ".ssh"]).check(f).allowed


def test_unprotect_cannot_open_home_or_system(home):
    assert not Guard(unprotect=[home]).check(home / "Documents" / "a.txt").allowed
    assert not Guard(unprotect=[Path("/etc")]).check(Path("/etc/passwd")).allowed


def test_is_within():
    assert is_within(Path("/a/b/c"), Path("/a"))
    assert is_within(Path("/a"), Path("/a"))
    assert not is_within(Path("/a"), Path("/a/b"))
