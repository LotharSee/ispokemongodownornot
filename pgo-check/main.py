import os
import time
import logging

from datadog import initialize, api as dog
from datadog.api.constants import CheckStatus

# Has to run inside the `pogo` directory
from pogo import api


AUTH = os.environ.get('PGO_AUTH')
EMAIL = os.environ.get('PGO_EMAIL')
PASSWORD = os.environ.get('PGO_PASSWORD')
LOCATION = os.environ.get('PGO_LOCATION')

DD_OPTIONS = {
    'api_key': os.environ.get('DATADOG_API_KEY'),
    'app_key': os.environ.get('DATADOG_APP_KEY'),
}
DATADOG_HOSTNAME = os.environ.get('DATADOG_HOSTNAME')


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
    if not (AUTH and EMAIL and PASSWORD and LOCATION):
        return

    setupLogger()
    initialize(**DD_OPTIONS)

    start = time.time()

    # Login to the server
    logging.info("Attempt to login with %s", AUTH)
    session = None
    try:
        if AUTH == 'ptc':
            session = api.createPTCSession(EMAIL, PASSWORD, LOCATION)
        elif AUTH == 'google':
            session = api.createGoogleSession(EMAIL, PASSWORD, LOCATION)
    except Exception:
        logging.error("Failed to get session")

    # If it succeed, get the profile
    if session:
        profile = session.getProfile()
        logging.info("Properly logged as %s", profile.local_player.username)
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

    logging.info("metrics properly reported")

if __name__ == "__main__":
    main()
