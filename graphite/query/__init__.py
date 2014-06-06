""" This is a modified version of package render from graphite-web """
import pytz
from graphite import settings
from graphite.settings import setup_storage_variables
from graphite.query.evaluator import evaluateTarget
from graphite.query.attime import parseATTime
import tzlocal

def query(*args, **kwargs):
    """ Returns a list of graphite.query.datalib.TimeSeries instances

        kwargs is a dictionary whose both keys and values are strings,
        except target, which is a list of strings.

        The params are taken from:
        http://graphite.readthedocs.org/en/latest/render_api.html
        except for the graph/format parameters

        tz: see http://graphite.readthedocs.org/en/latest/render_api.html#tz
        until/from: see http://graphite.readthedocs.org/en/latest/render_api.html#from-until
        target: see http://graphite.readthedocs.org/en/latest/render_api.html#target
    """
    params = {}

    try:
        params['target'] = args[0]
    except IndexError:
        pass

    try:
        params['from'] = args[1]
    except IndexError:
        pass

    try:
        params['until'] = args[2]
    except IndexError:
        pass

    try:
        params['tz'] = args[3]
    except IndexError:
        pass

    params.update(kwargs)

    if kwargs.has_key('from_'):
        params['from'] = kwargs['from_']

    if kwargs.has_key('from_time'):
        params['from'] = kwargs['from_time']

    try:
        tzinfo = pytz.timezone(settings.TIME_ZONE)
    except AttributeError:
        tzinfo = tzlocal.get_localzone()
    if 'tz' in params:
        try:
            tzinfo = pytz.timezone(params['tz'])
        except pytz.UnknownTimeZoneError:
            pass
    params['tzinfo'] = tzinfo

    if 'until' in params:
        untilTime = parseATTime(params['until'], tzinfo)
    else:
        untilTime = parseATTime('now', tzinfo)
    if 'from' in params:
        fromTime = parseATTime(params['from'], tzinfo)
    else:
        fromTime = parseATTime('-1d', tzinfo)
    startTime = min(fromTime, untilTime)
    endTime = max(fromTime, untilTime)
    assert startTime < endTime, "Invalid empty time range"

    params['startTime'] = startTime
    params['endTime'] = endTime

    data = []
    if isinstance(params['target'], basestring):
        data.extend(evaluateTarget(params, params['target']))
    elif isinstance(params['target'], list):
        for target in params['target']:
            data.extend(evaluateTarget(params, target))
    else:
        raise TypeError("The target parameter must be a string or a list")

    return data

def eval_qs(query_string):
    from urlparse import parse_qs

    params = parse_qs(query_string)

    # In parse_qs every value is a list, so we convert
    # them to strings
    for key, value in params.items():
        if key != "target":
            params[key] = value[0]
    return query(params)
