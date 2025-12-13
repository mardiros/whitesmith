# Whitesmith
Test helper for blacksmith resources.

![Continuous Integration](https://github.com/mardiros/whitesmith/actions/workflows/tests.yml/badge.svg)
[![Coverage](https://codecov.io/gh/mardiros/whitesmith/graph/badge.svg?token=V1W7W6YWNN)](https://codecov.io/gh/mardiros/whitesmith)

## Motivation

While using blacksmith, resources are declared using pydantic, and, while testing,
we never do http calls.

Whitesmith is a helper that create pytest fixtures for blacksmith resources and
generate handlers for tests.

## Usage

### Generating fixtures

```bash
whitesmith generate -m my_package.resources --out-dir tests/
```

The commande above will generate a folder `tests/whitesmith` containing
handlers for all the api call with a default implementation.

> **Note**
> If you run the command again, the command does not overrite generated files.
> To generate newer version, use the `--overwrite` flag.

Those fixtures can be adapted to get the result you want,
they must be present in a whitesmith_handlers directory inside the tests suite.

### Using the fixtures

The whitesmith package provide three pytest fixtures that can be used in the testsuite.

The sync_blacksmith_client, async_blacksmith_client can be used to get
a blacksmith client instance that use the installed fixtures from the generated
directory.

Both actually consume the undelying fixtures `whitesmith_router` is a generated
fixture that contains all the routes contained in the `whitesmith_handlers` directory.
