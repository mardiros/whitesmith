default_test_suite := 'tests/unittests'
package := 'whitesmith'

install:
    uv sync --group dev

lint:
    uv run ruff check .

typecheck:
    uv run mypy src/ tests/

functest:
    rm -rf tests/unittests/conftest.py
    rm -rf tests/unittests/fixtures.py
    rm -rf tests/unittests/handlers/*
    PYTHONPATH=. uv run whitesmith generate -m tests
    uv run ruff check --fix tests/unittests/
    uv run pytest -sxv tests/unittests/

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
    uvx --with=pdm,pdm-bump --python-preference system pdm bump {{major_minor_patch}}
    uv sync --frozen --group dev

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
