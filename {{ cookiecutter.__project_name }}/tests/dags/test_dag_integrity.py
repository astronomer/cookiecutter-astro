"""Test the validity of all DAGs. Feel free to add and remove tests."""

import logging
import os
from contextlib import contextmanager

import pytest
from airflow.models import DagBag


@contextmanager
def suppress_logging(namespace: str):
    """Utility function to suppress logging to avoid spamming the logs."""
    logger = logging.getLogger(namespace)
    old_value = logger.disabled
    logger.disabled = True
    try:
        yield
    finally:
        logger.disabled = old_value


def get_import_errors() -> list[tuple]:
    """Fetch a list of tuples (DAG filepath, import errors) in the DagBag."""
    with suppress_logging("airflow"):
        dag_bag = DagBag(include_examples=False)

        def strip_path_prefix(path):
            return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

        # Prepend (None,None) to ensure that a test object is always created even if it's a no op
        return [(None, None)] + [(strip_path_prefix(k), v.strip()) for k, v in dag_bag.import_errors.items()]


def get_dags():
    """Generate a list of tuples (DAG id, DAG object, relative DAG path) in the DagBag."""
    with suppress_logging("airflow"):
        dag_bag = DagBag(include_examples=False)

    def strip_path_prefix(path):
        return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

    return [(k, v, strip_path_prefix(v.fileloc)) for k, v in dag_bag.dags.items()]


@pytest.mark.parametrize(
    "rel_dag_filepath,import_errors",
    get_import_errors(),
    ids=[x[0] for x in get_import_errors()],
)
def test_file_imports(rel_dag_filepath, import_errors):
    """Test for import errors on a file"""

    # Collection of paths to skip (because we know they contain DAG parsing errors)
    skip_paths = {}
    if rel_dag_filepath and rel_dag_filepath not in skip_paths and import_errors:
        raise Exception(f"{rel_dag_filepath} failed to import with message:\n{import_errors}")
