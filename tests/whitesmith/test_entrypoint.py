from pathlib import Path

from whitesmith.entrypoint import main


def test_main(tmp_path: Path):
    main(["whitesmith", "generate", "-o", str(tmp_path), "-m", "tests.resources"])
    files = {f.name: f.read_text() for f in tmp_path.glob("whitesmith/*.py")}
    assert files.keys() == {"__init__.py", "conftest.py", "fixtures.py"}
    files = {f.name: f.read_text() for f in tmp_path.glob("whitesmith/handlers/*.py")}
    assert files.keys() == {"__init__.py", "address.py", "notif.py", "organization.py"}
