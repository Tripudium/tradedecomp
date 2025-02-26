from typing import Union
import calendar
from datetime import datetime, timedelta
import pytz
import re

def nanoseconds(input: Union[str, datetime]) -> int:
    """
    Convert datetime or string input to return nanosecond UNIX timestamp (int).

    The input can by one of the following:
        - YYMMDD.HHMM
        - dt.datetime (with or without timezone)
        
        Example:
            >>> nanoseconds(dt.datetime(2018, 3, 20, 18, 30, tzinfo=pytz.timezone('America/Chicago')))
        1521588600000000000 
    """
    assert isinstance(input, datetime) or isinstance(input, str)
    if isinstance(input, str):
        try:
            input = datetime.strptime(input, "%y%m%d.%H%M")
        except ValueError:
            print("Input string not in correct format")
    # Deal with some timezone issues
    used_tz = input.tzinfo if input.tzinfo is not None else pytz.utc
    input = used_tz.localize(input.replace(tzinfo=None))
    time_tuple = input.utctimetuple()
    timestamp = 1000 * (calendar.timegm(time_tuple) * 1000 * 1000 + input.microsecond)
    return timestamp

def str_to_timedelta(s: str) -> timedelta:
    """
    Convert a string like '30s' to a timedelta.
    """
    match = re.fullmatch(r"(\d+)(ns|us|ms|s|m|h)", s)
    if not match:
        raise ValueError(f"Input string '{s}' is not in the expected format, e.g., '30s', '1m', or '2h'.")
    number, unit = match.groups()
    number = int(number)
    
    if unit == 'ms':
        return timedelta(milliseconds=number)
    elif unit == 'us':
        return timedelta(microseconds=number)
    elif unit == 'ns':  # nanoseconds
        return timedelta(nanoseconds=number)
    elif unit == 's':  # seconds
        return timedelta(seconds=number)
    elif unit == 'm':  # minutes
        return timedelta(minutes=number)
    elif unit == 'h':  # hours
        return timedelta(hours=number)
    else:
        raise ValueError(f"Unrecognized unit '{unit}' in input string '{s}'.")
    
def timedelta_to_str(td: timedelta) -> str:
    """
    Convert a timedelta to a string.
    """
    total_seconds = td.total_seconds()
    
    # Check hours first
    if total_seconds >= 3600 and total_seconds % 3600 == 0:
        return f"{int(total_seconds // 3600)}h"
    # Then minutes
    elif total_seconds >= 60 and total_seconds % 60 == 0:
        return f"{int(total_seconds // 60)}m"
    # Then seconds
    elif total_seconds.is_integer():
        return f"{int(total_seconds)}s"
    # Then milliseconds
    elif total_seconds * 1000 % 1 == 0:
        return f"{int(total_seconds * 1000)}ms"
    # Then microseconds
    elif total_seconds * 1_000_000 % 1 == 0:
        return f"{int(total_seconds * 1_000_000)}us"
    # Finally nanoseconds
    else:
        return f"{int(total_seconds * 1_000_000_000)}ns"
