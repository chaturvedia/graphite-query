## Overview

graphite-query is a library created from graphite-web in order to make
some of its functionality framework neutral.

## Usage
    >>> from graphite.query import query
    >>> print list(query({"target": "graphite-web.compatible.path.expression"})[0])
The `query` function returns a list of instances of
`graphite.query.datalib.TimeSeries`, which in turn is a list-like object whose
sub-elements are the values stored by graphite at particular points in time


## Configuring graphite-query