import os
import time
import logging

from datadog import initialize, api as dog
from datadog.api.constants import CheckStatus

# Has to run inside the `pogo` directory
from pogo.api import createPTCSession, createGoogleSession
from pogo.location import Location

AUTH = os.environ.get('PGO_AUTH')
USERNAME = os.environ.get('PGO_USERNAME')
PASSWORD = os.environ.get('PGO_PASSWORD')


# GPS location
LATITUDE = float(os.environ.get('PGO_LATITUDE', 0))
LONGITUDE = float(os.environ.get('PGO_LONGITUDE', 0))
ALTITUDE = float(os.environ.get('PGO_ALTITUDE', 0))
# Or searched location
LOCATION = os.environ.get('PGO_LOCATION')


DD_OPTIONS = {
    'api_key': os.environ.get('DATADOG_API_KEY'),
    'app_key': os.environ.get('DATADOG_APP_KEY'),
}
DATADOG_HOSTNAME = os.environ.get('DATADOG_HOSTNAME')

# Define the entire lifetime of the container.
# Combined with docker `--restart=always`, allows to run the check periodically
CONTAINER_LIFETIME = int(os.environ.get('CONTAINER_LIFETIME', 0))


def setupLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] [%(process)d] [%(filename)s:%(lineno)d] - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def main():
    """Report to datadog the state of the Pokemon GO authentication with Google Auth"""

    # Set the location, either a string we will search, or directly the exact coordinates
    location = LOCATION
    if (LATITUDE or LONGITUDE or ALTITUDE):
        location = Location(LATITUDE, LONGITUDE, ALTITUDE)

    setupLogger()
    initialize(**DD_OPTIONS)

    start = time.time()

    # Login to the server
    logging.info("Attempt to login with %s", AUTH)
    session = None
    try:
        if AUTH == 'ptc':
            session = createPTCSession(USERNAME, PASSWORD, location)
        elif AUTH == 'google':
            session = createGoogleSession(USERNAME, PASSWORD, location)
    except Exception as e:
        logging.error("Failed to get session")
        logging.exception(e)

    profile = None
    # If it succeed, get the profile
    if session:
        try:
            profile = session.getProfile()
            logging.info("Properly logged as %s", profile.local_player.username)
        except Exception:
            logging.error("Failed to get the profile")

    if profile and getattr(profile, 'username', None):
        elapsed = time.time() - start

        dog.ServiceCheck.check(
            check="pgo.login.up",
            host_name=DATADOG_HOSTNAME,
            status=CheckStatus.OK,
            tags=["auth:%s" % AUTH],
        )
        dog.Metric.send(metric="pgo.login.uptime", points=1, host=DATADOG_HOSTNAME, tags=["auth:%s" % AUTH])
        dog.Metric.send(metric="pgo.login.lag", points=elapsed, host=DATADOG_HOSTNAME, tags=["auth:%s" % AUTH])

    else:
        dog.ServiceCheck.check(
            check="pgo.login.up",
            host_name=DATADOG_HOSTNAME,
            status=CheckStatus.CRITICAL,
            tags=["auth:%s" % AUTH],
        )
        dog.Metric.send(metric="pgo.login.uptime", points=0, host=DATADOG_HOSTNAME, tags=["auth:%s" % AUTH])

    logging.info("Metrics properly reported")

    if CONTAINER_LIFETIME:
        extra_sleep = CONTAINER_LIFETIME - (time.time() - start)
        if extra_sleep > 0:
            logging.info("Sleeping an extra %.1f seconds" % extra_sleep)
            time.sleep(extra_sleep)

    logging.info("Exiting")

if __name__ == "__main__":
    main()
