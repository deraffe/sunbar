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


def get_sun(latitude: float, longitude: float, elevation: float = 0.0) -> Sun:
    observer = astral.Observer(latitude, longitude, elevation)
    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    sun = astral.sun.sun(observer, tzinfo=local_tz)
    return Sun(**sun)


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
    print(get_sun(args.latitude, args.longitude, args.elevation))


if __name__ == '__main__':
    main()
