# Whitesmith

Test helper for blacksmith resources.

![Continuous Integration](https://github.com/mardiros/whitesmith/actions/workflows/tests.yml/badge.svg)
[![Coverage](https://codecov.io/gh/mardiros/whitesmith/graph/badge.svg?token=V1W7W6YWNN)](https://codecov.io/gh/mardiros/whitesmith)

## Motivation

Whitesmith is the swissknife for developping and testing code base that use
[[https://](https://github.com/mardiros/blacksmith](blacksmith).

While using blacksmith, resources are declared using pydantic, and, while testing,
we never do http calls.

Whitesmith is a helper that create pytest fixtures with handlers for tests,
client types and generate documentation for blacksmith resources and .

## Usage

### Generating typed client

The command bellow will create a file `blacksmith_client.py` in the codebase
that override the blacksmith client factory to get a fully typed client.

```bash
whitesmith generate-types -m my_package.resources -o my_package/resources/blacksmith_client.py
```

Use `--overwrite` if the file exists and you want to regenerate it.

Now, you can import the `AsyncAppClientFactory` or `SyncAppClientFactory`
to get a fully typed client and not import blacksmith module anywhere from the codebase.

### Generating fixtures

The command below will generate a folder `tests/whitesmith` containing
handlers for all the api call with a default implementation.

```bash
whitesmith generate-handlers -m my_package.resources --out-dir tests/
```

> **Note**
> If you run the command again, the command does not overwrite generated files.
> To generate a newer version, use the `--overwrite` flag.

Those fixtures can be adapted to get the result you want,
they must be present in a whitesmith_handlers directory inside the tests suite.

### Using the fixtures

The whitesmith package provide three pytest fixtures that can be used in the testsuite.

The fixtures `sync_blacksmith_client`, `async_blacksmith_client` can be used to get
a blacksmith client instance that use the installed fixtures from the generated
directory.

Both actually consume the undelying fixtures `whitesmith_router` is a generated
fixture that contains all the routes contained inside a `whitesmith_handlers` directory.
This directory is the one created by the commande above `whitesmith generate-handlers`.

You can have multiple `whitesmith_handlers` by creating tests submodules
to handle mulptiple behavior when its needed.


### Building a client contract (open api format)

This feature is a bit experimental but was the main motivation of blacksmith,
provide a tool for consumer-driven contract (CDC) so generated document
of client contract is nice to have.
A tool to ensure server and client contract compatibility could be used to
enforce maintainability.


```bash
uv run whitesmith generate-openapi -m my_package.resources -o docs/resources/openapis --overwrite
cd docs/resources/openapis
python -m http.server 8000
```
