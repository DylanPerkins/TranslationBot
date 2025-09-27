import time


from typing import Union
from datetime import datetime, timezone


def date(
    target: Union[datetime, float, int],
    clock: bool = True,
    ago: bool = False,
    only_ago: bool = False
) -> str:
    """ Converts a timestamp to a Discord timestamp format """
    if isinstance(target, int) or isinstance(target, float):
        target = datetime.now(timezone.utc) if target == 0 else datetime.fromtimestamp(
            target, tz=timezone.utc)

    unix = int(time.mktime(target.timetuple()))
    timestamp = f"<t:{unix}:{'f' if clock else 'D'}>"
    if ago:
        timestamp += f" (<t:{unix}:R>)"
    if only_ago:
        timestamp = f"<t:{unix}:R>"
    return timestamp
