import logging
import subprocess

import pytest


@pytest.fixture(scope="session", autouse=True)
def context():
    return {"team_name": "test_team"}


@pytest.fixture(scope="session", autouse=True)
def astro_cli():
    """Ensure Astro CLI and Docker/Podman are available for testing DAGs."""
    try:
        subprocess.check_call("astro version", shell=True)
    except Exception:
        logging.error(
            """
            Install the Astro CLI and try again.
            https://docs.astronomer.io/astro/cli/install-cli
            """
        )

    try:
        subprocess.check_call("docker run hello-world", shell=True)
    except Exception:
        logging.error("Could not run Docker.")
        raise
    try:
        subprocess.check_call("podman run hello-world", shell=True)
    except Exception:
        logging.error("Could not run Podman, trying Docker...")
