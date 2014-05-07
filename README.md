## Overview

A library created from graphite-web in order to make
some of its functionality framework neutral.

Usage:

    from graphite.query import query
    print list(query({"target": "graphite-web.compatible.path.expression"})[0])
