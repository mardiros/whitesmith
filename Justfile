default_test_suite := 'tests/unittests'

install:
    poetry install --with dev

doc:
    cd docs && poetry run make html
    xdg-open docs/build/html/index.html

cleandoc:
    cd docs && poetry run make clean

lint:
    poetry run flake8 && echo "$(tput setaf 10)Success: no lint issue$(tput setaf 7)"

mypy:
    poetry run mypy src/

functest:
    rm -rf tests/whitesmith/conftest.py
    rm -rf tests/whitesmith/fixtures.py
    rm -rf tests/whitesmith/handlers/*
    poetry run whitesmith generate -m tests
    poetry run black tests/whitesmith/
    poetry run pytest -sxv tests/whitesmith/

test: lint mypy functest

black:
    poetry run isort .
    poetry run black .

rtd:
    poetry export --dev -f requirements.txt -o docs/requirements.txt --without-hashes

release major_minor_patch: && changelog
    poetry version {{major_minor_patch}}
    poetry install

changelog:
    poetry run python scripts/write_changelog.py
    cat CHANGELOG.rst >> CHANGELOG.rst.new
    rm CHANGELOG.rst
    mv CHANGELOG.rst.new CHANGELOG.rst
    $EDITOR CHANGELOG.rst

publish:
    git commit -am "Release $(poetry run python scripts/show_release.py)"
    poetry build
    poetry publish
    git push
    git tag "$(poetry run python scripts/show_release.py)"
    git push origin "$(poetry run python scripts/show_release.py)"
