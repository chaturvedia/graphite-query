Overview
========

```graphite-query`` <https://github.com/edin1/graphite-query>`__ is a
library created from
```graphite-web`` <https://github.com/graphite-project/graphite-web>`__
in order to make some of its functionality framework neutral, i.e. to
require as little dependencies as possible.

Installation
============

You can install ``graphite-query`` by running:

::

        pip install graphite-query

You can also download/clone the github repository, and, inside the
directory where you downloaded ``graphite-query`` run:

::

        python setup.py install

Usage
=====

This package provides the functions ``query``, ``eval_qs`` and
``get_all_leaf_nodes`` (all are part of the ``graphite.query``
subpackage).

``query``
---------

``query`` takes both positional and keyword arguments, which in turn are
taken from [graphite-web's render API]
(http://graphite.readthedocs.org/en/latest/render\_api.html) except for
the graph/format arguments, which are, of course, inapplicable to
graphite-query.

In short, its parameters (in positional order) are:

-  ``target``: required, a ``graphite-web`` compatible path (i.e.
   string), or a ``list`` of paths, see
   http://graphite.readthedocs.org/en/latest/render_api.html#target for
   additional documentation.
-  ``from`` and ``until``: two optional parameters that specify the
   relative or absolute time period to graph. see
   http://graphite.readthedocs.org/en/latest/render_api.html#from-until
-  ``tz``: optional, time zone to convert all times into. If this
   parameter is not specified, then
   ``graphite.query.settings.TIME_ZONE`` is used (if any). Finally,
   system's timezone is used if ``TIME_ZONE`` is empty. see
   http://graphite.readthedocs.org/en/latest/render_api.html#tz

A basic query might look like this:

::

        >>> from graphite.query import query
        >>> print list(query("graphite-web.compatible.path.expression")[0])

The ``query`` function *always* (even if you supply only one target
path) returns a ``list`` of instances of
``graphite.query.datalib.TimeSeries``, which in turn is a ``list``-like
object whose sub-elements are the values stored by graphite (in a
``whisper`` database) at particular points in time.

``eval_qs``
-----------

This is a helper function: it takes a URL query string as a parameter.
The query string must be compatible with the ``graphite-web``'s render
controller. ``eval_qs`` internally converts this string to a parameter
dictionary that can be passed on to ``query`` and calls ``query``.E.g.:

::

        >>> from graphite.query import query, eval_qs
        >>> print list(eval_qs("format=raw&target=*.*.*")[0])
        >>> # The above is the same as:
        >>> print list(query(**{"target": "*.*.*"}))

``get_all_leaf_nodes``
----------------------

Returns a ``list`` of all leaf nodes/targets that are found in the
``settings.STORAGE_DIR``. It doesn't have any parameters.

Configuring ``graphite-query``
==============================

The module ``graphite.settings`` can be used to set up some of the
"package-wide" parameters of ``graphite-query``. You can look into that
module to see some of the supported settings. The ``graphite.query``
subpackage directly imports this module, so one can do a
``from graphite.query import settings`` for convenience.

Perhaps the most important parameter is ``STORAGE_DIR``, the directory
that is used to look for data. By default, this directory is set to
``/opt/graphite/storage``, as this is the default directory used by
``graphite``. You could set this parameter manually, but it's better to
use the provided ``graphite.settings.setup_storage_variables`` function,
as this will set some additional dependant parameters (such as the
``whisper`` storage directory etc.). Otherwise, one would have to set
those parameters manually also.

Finally, it's possible to set the ``STORAGE_DIR`` parameter with the
environment variable ``GRAPHITE_STORAGE_DIR``, prior to
running/importing ``graphite-query``. This variable will trigger the
``setup_storage_variables`` function to set all of the default
directories relative to ``(GRAPHITE_)STORAGE_DIR``.
