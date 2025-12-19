from pathlib import Path

from whitesmith.entrypoints.cli import main


def test_generate_fixtures(tmp_path: Path):
    main(["whitesmith", "generate", "-o", str(tmp_path), "-m", "tests.resources"])
    files = {f.name: f.read_text() for f in tmp_path.glob("whitesmith_handlers/*.py")}
    assert files.keys() == {"__init__.py", "address.py", "notif.py", "organization.py"}


def test_generate_openapi(tmp_path: Path):
    main(
        ["whitesmith", "generate-openapi", "-o", str(tmp_path), "-m", "tests.resources"]
    )
    files = {f.name: f.read_text() for f in tmp_path.glob("*")}
    assert files.keys() == {
        "index.html",
        "address.json",
        "notif.json",
        "organization.json",
    }
