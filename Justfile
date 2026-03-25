default_test_suite := 'tests/unittests'
functional_test_suite := 'tests/functests'
package := 'whitesmith'

install:
    uv sync --group dev

upgrade: && update
    uv lock --upgrade

update:
    #!/bin/bash
    uv sync --all-groups

lint:
    uv run ruff check .

typecheck:
    uv run mypy src/ tests/

unittests test_suite=default_test_suite:
    uv run pytest -sxv {{test_suite}}

functest functests=functional_test_suite:
    rm -rf tests/whitesmith_handlers/*
    PYTHONPATH=. uv run whitesmith generate -m tests.resources -o tests
    uv run ruff check --fix tests/whitesmith_handlers/
    uv run pytest -sxv {{functests}}

test: lint typecheck unittests functest

genopenapi:
    PYTHONPATH=. uv run whitesmith generate-openapi -m tests.resources -o tests/openapis --overwrite
    cd tests/openapis/ && python -m http.server 8000

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
    uv version --bump {{major_minor_patch}}

changelog:
    uv run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md


publish:
    git commit -am "Release $(uv version --short --color=never)"
    git tag "v$(uv version --short --color=never)"
    git push
    git push origin "v$(uv version --short --color=never)"
