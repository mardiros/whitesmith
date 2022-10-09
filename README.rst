Whitesmith
==========

Test helper for blacksmith resources.


Motivation
----------

While using blacksmith, resources are declared using pydantic, and, while testing,
we never do http calls.

Whitesmith is a helper that create pytest fixtures for blacksmith resources and
generate handlers for tests.


Usage
-----

::

  whitesmith generate -m my_package.resources --out-dir tests/


The commande above will generate a folder ``tests/whitesmith`` containing
handlers for all the api call with a default implementation.


.. note::
    | If you run the command again, the command does not overrite generated files.
    | To generate newer version, use the ``--overwrite`` flag.


The command will generate also a `conftest.py` file containing two fixtures,

for sync and async version.


Tests that require those fixture are suppose to be created inside the whitesmith folder.

To create the test elsewhere, you have to copy create your own fixtures by copy,
pasting and adapting import path.
