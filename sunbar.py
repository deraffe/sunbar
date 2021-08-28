#!/usr/bin/env python3
import argparse
import datetime
import logging
from dataclasses import dataclass

import astral
import astral.sun

log = logging.getLogger(__name__)


@dataclass
class Sun:
    dawn: datetime.datetime
    sunrise: datetime.datetime
    noon: datetime.datetime
    sunset: datetime.datetime
    dusk: datetime.datetime


def get_sun(
    latitude: float,
    longitude: float,
    elevation: float = 0.0,
    day_offset: int = 0
) -> Sun:
    observer = astral.Observer(latitude, longitude, elevation)
    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    date = datetime.date.today() + day_offset * datetime.timedelta(days=1)
    sun = astral.sun.sun(observer, date=date, tzinfo=local_tz)
    return Sun(**sun)


def get_bar(
    sunrise: datetime.datetime, now: datetime.datetime,
    sunset: datetime.datetime, length: int
) -> str:
    begin = sunrise
    bar_end = now
    point = sunset
    log.debug(f'{begin=} {bar_end=} {point=} {length=}')
    assert begin < bar_end
    assert begin < point
    day = datetime.timedelta(days=1)
    bar_end_percent = (bar_end - begin) / day
    point_percent = (point - begin) / day
    bar_end_chars = bar_end_percent * length
    bar_end_fractional_chars = bar_end_chars % 1
    bar_end_fractional_char = fractional_char(bar_end_fractional_chars)
    point_char = (point_percent * length) // 1
    bar = '█' * int(bar_end_chars)
    bar += bar_end_fractional_char
    bar += ' ' * int(length - bar_end_chars - 1)
    bar += '|'
    bar += f'\n{begin.day:02}'
    bar += ' ' * int(point_char - (1 + 2))
    bar += '^'
    bar += ' ' * int(length - point_char - 1)
    bar += '|'
    return bar


def fractional_char(fraction: float) -> str:
    chars = '▁▂▃▄▅▆▇█'
    increment = 1 / len(chars)
    for i, c in enumerate(chars):
        value = i * increment
        next_value = (i + 1) * increment
        if value < fraction < next_value:
            return c
    raise RuntimeError("Couldn't find fractional character")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--loglevel', default='WARNING', help="Loglevel", action='store'
    )
    parser.add_argument('latitude', type=float, help='Current latitude')
    parser.add_argument('longitude', type=float, help='Current longitude')
    parser.add_argument(
        '--elevation', type=float, default=0.0, help='Current elevation'
    )
    args = parser.parse_args()
    loglevel = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(loglevel, int):
        raise ValueError('Invalid log level: {}'.format(args.loglevel))
    logging.basicConfig(level=loglevel)
    sun = get_sun(args.latitude, args.longitude, args.elevation, day_offset=0)
    sun_yesterday = get_sun(
        args.latitude, args.longitude, args.elevation, day_offset=-1
    )
    local_dt = datetime.datetime.now(datetime.timezone.utc).astimezone()
    if sun.sunrise < local_dt:
        print(get_bar(sun.sunrise, local_dt, sun.sunset, 20))
    else:
        print(
            get_bar(sun_yesterday.sunrise, local_dt, sun_yesterday.sunset, 20)
        )


if __name__ == '__main__':
    main()
