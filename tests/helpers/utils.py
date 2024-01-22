import logging
import os
import subprocess
from contextlib import contextmanager

import pytest_cookies.plugin
from cookiecutter.utils import rmtree


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies: pytest_cookies.plugin.Cookies, context) -> pytest_cookies.plugin.Result:
    """
    Delete the temporary directory that is created when executing the tests.

    :param cookies: Cookie to be baked and its temporary files will be removed
    :param context:
    """
    result = cookies.bake(extra_context={**context})
    try:
        yield result
    finally:
        rmtree(str(result.project_path))


def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        result = subprocess.run(command, shell=True, check=True)
        logging.info(result.stdout)
        logging.warning(result.stderr)
    return result.returncode
