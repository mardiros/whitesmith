default_test_suite := 'tests'
package := 'whitesmith'

install:
    uv sync --group dev

lint:
    uv run ruff check .

typecheck:
    uv run mypy src/ tests/

functest:
    rm -rf tests/whitesmith/conftest.py
    rm -rf tests/whitesmith/fixtures.py
    rm -rf tests/whitesmith/handlers/*
    PYTHONPATH=. uv run whitesmith generate -m tests
    uv run ruff check --fix tests/whitesmith/
    uv run pytest -sxv tests/whitesmith/

test: lint typecheck functest

lf:
    uv run pytest -sxvvv --lf

cov test_suite=default_test_suite:
    rm -f .coverage
    rm -rf htmlcov
    uv run pytest --cov-report=html --cov={{package}} {{test_suite}}
    xdg-open htmlcov/index.html

fmt:
    uv run ruff check --fix .
    uv run ruff format src tests

release major_minor_patch: && changelog
    #! /bin/bash
    # Try to bump the version first
    if ! uvx pdm bump {{major_minor_patch}}; then
        # If it fails, check if pdm-bump is installed
        if ! uvx pdm self list | grep -q pdm-bump; then
            # If not installed, add pdm-bump
            uvx pdm self add pdm-bump
        fi
        # Attempt to bump the version again
        uvx pdm bump {{major_minor_patch}}
    fi
    uv sync

changelog:
    uv run python scripts/write_changelog.py
    cat CHANGELOG.rst >> CHANGELOG.rst.new
    rm CHANGELOG.rst
    mv CHANGELOG.rst.new CHANGELOG.rst
    $EDITOR CHANGELOG.rst


publish:
    git commit -am "Release $(uv run scripts/get_version.py)"
    git tag "v$(uv run scripts/get_version.py)"
    git push
    git push origin "v$(uv run scripts/get_version.py)"
