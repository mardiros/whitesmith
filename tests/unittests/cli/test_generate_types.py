from pathlib import Path
from typing import Any

import pytest

from whitesmith.bin.generate_types import handler, safe_open, snake_to_pascal


def test_snake_to_pascal():
    return snake_to_pascal("foo_bar") == "FooBar"


def test_creates_file_and_parent_directories(tmp_path: Path):
    output = tmp_path / "nested" / "dir" / "dummy.py"

    with safe_open(str(output), overwrite=False) as f:
        f.write("hello")

    assert output.exists()
    assert output.read_text() == "hello"


def test_raises_if_file_exists_and_overwrite_is_false(tmp_path: Path):
    output = tmp_path / "dummy.py"
    output.write_text("existing")

    with pytest.raises(FileExistsError, match="already exists"):
        safe_open(str(output), overwrite=False)

    assert output.read_text() == "existing"


def test_overwrites_existing_file(tmp_path: Path):
    output = tmp_path / "dummy.py"
    output.write_text("existing")

    with safe_open(str(output), overwrite=True) as f:
        f.write("new content")

    assert output.read_text() == "new content"


def test_raises_permission_error_if_parent_not_writable(
    tmp_path: Path, monkeypatch: Any
):
    output = tmp_path / "dummy.py"

    monkeypatch.setattr(
        "whitesmith.bin.generate_types.os.access", lambda path, mode: False
    )

    with pytest.raises(PermissionError, match="not writable"):
        safe_open(str(output), overwrite=False)


def test_raises_not_a_directory_if_parent_component_is_a_file(tmp_path: Path):
    parent = tmp_path / "not_a_directory"
    parent.write_text("I am a file")

    output = parent / "dummy.py"

    with pytest.raises(NotADirectoryError):
        safe_open(str(output), overwrite=False)


def test_handler(tmp_path: Path):
    handler(["tests.resources"], output=str(tmp_path / "dummy.py"))

    content = (tmp_path / "dummy.py").read_text()
    assert "class AsyncAppClientFactory" in content
    assert "class SyncAppClientFactory" in content


def test_handler_stdout(capsys: pytest.CaptureFixture[str]):
    handler(["tests.resources"])
    captured = capsys.readouterr()
    assert "class AsyncAppClientFactory" in captured.out
    assert "class SyncAppClientFactory" in captured.out


def test_handler_sync(tmp_path: Path):
    handler(["tests.resources"], sync=True, output=str(tmp_path / "dummy.py"))

    content = (tmp_path / "dummy.py").read_text()
    assert "class AsyncAppClientFactory" not in content
    assert "class SyncAppClientFactory" in content


def test_handler_async(tmp_path: Path):
    handler(["tests.resources"], async_=True, output=str(tmp_path / "dummy.py"))

    content = (tmp_path / "dummy.py").read_text()
    assert "class AsyncAppClientFactory" in content
    assert "class SyncAppClientFactory" not in content
