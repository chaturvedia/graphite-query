## Overview

graphite-query is a library created from graphite-web in order to make
some of its functionality framework neutral, i.e. to require as little
dependencies as possible.

## Usage
This package provides the function `query`
(part of the `graphite.query` subpackage).
`query` takes both positional and keyword arguments, which in turn are taken
from `graphite-web's render API <http://graphite.readthedocs.org/en/latest/render_api.html>`_
except for the graph/format arguments (which are, of course,
inapplicable to graphite-query) 

In short, its parameters (in positional order) are:

* `target`: a graphite-web compatible path (string), or a list of paths,
 see <http://graphite.readthedocs.org/en/latest/render_api.html#target>
* `from`: see <http://graphite.readthedocs.org/en/latest/render_api.html#from-until>
* `until`: see <http://graphite.readthedocs.org/en/latest/render_api.html#from-until>
* `tz`: see <http://graphite.readthedocs.org/en/latest/render_api.html#tz>

    >>> from graphite.query import query
    >>> print list(query({"target": "graphite-web.compatible.path.expression"})[0])

The `query` function returns a list of instances of
`graphite.query.datalib.TimeSeries`, which in turn is a list-like object whose
sub-elements are the values stored by graphite in a whisper database
at particular points in time


## Configuring graphite-query