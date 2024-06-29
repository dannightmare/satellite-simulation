from sgp4.api import jday
from sgp4.api import Satrec
from godot import Vector3
from io import StringIO


def extractxyz(inputstring, time) -> list():
    buffer = StringIO(inputstring)
    xyzlist = []
    now = time

    while True:
        name = buffer.readline()
        tle_line1 = buffer.readline()
        tle_line2 = buffer.readline()

        if tle_line2 == "":
            break

        # Initialize the satellite object from TLE data
        satellite = Satrec.twoline2rv(tle_line1, tle_line2)

        # Use a specific date for which you want the position
        jd, fr = jday(now.year, now.month, now.day, now.hour,
                      now.minute, now.second + now.microsecond * 1e-6)

        # Get the position and velocity of the satellite
        e, position, velocity = satellite.sgp4(jd, fr)

        # Extract x, y, z coordinates from the position
        z, x, y = position
        x /= 100
        y /= 100
        z /= 100
        xyzlist.append((name, Vector3(x, y, z)))

    return xyzlist
