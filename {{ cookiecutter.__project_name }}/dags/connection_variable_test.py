"""
The purpose of this DAG is to verify Airflow connections and variables.
Trigger the DAG and provide connection and variable ids to validate.
"""

import datetime

from airflow.decorators import dag, task
from airflow.exceptions import (
    AirflowException,
    AirflowNotFoundException,
    AirflowSkipException,
)
from airflow.hooks.base import BaseHook
from airflow.models import Param, Variable


@dag(
    start_date=datetime.datetime(2023, 1, 1),
    schedule=None,
    params={
        "connection_ids": Param(
            default=[],
            title="Connection ids",
            description_html=(
                "List of connection ids to test. For example:"
                "<pre><code>myconn1</br>myconn2</br>myconn3</pre></code>"
            ),
            type=["array", "null"],
        ),
        "variable_ids": Param(
            default=[],
            title="Variable ids",
            description_html=(
                "List of variable ids to check for existence. For example:"
                "<pre><code>myvar1</br>myvar2</br>myvar3</pre></code>"
            ),
            type=["array", "null"],
        ),
    },
    description=__doc__,
)
def connection_variable_test():
    @task
    def verify_connections(params=None):
        """For every given connection id, run the test_connection() method to verify connectivity."""

        if not params["connection_ids"]:
            raise AirflowSkipException("⏭️ No connection ids provided. Nothing to do.")

        found_and_verified_connections = set()
        found_not_verified_connections = {}  # type: dict[str, str]
        not_found_connections = set()

        conn_ids = params["connection_ids"]
        for conn_id in conn_ids:
            try:
                conn = BaseHook.get_connection(conn_id=conn_id)
                test_success, message = conn.test_connection()
                if test_success:
                    found_and_verified_connections.add(conn_id)
                else:
                    found_not_verified_connections[conn_id] = message
            except AirflowNotFoundException:
                not_found_connections.add(conn_id)
            except Exception as e:
                found_not_verified_connections[conn_id] = str(e)

        if found_and_verified_connections:
            print(
                "Successfully read and connected to "
                f"{len(found_and_verified_connections)}/{len(conn_ids)} connections:"
            )
            for conn_id in found_and_verified_connections:
                print(f"✅ {conn_id}")

        if found_not_verified_connections:
            print(
                "Successfully read but failed to test "
                f"{len(found_not_verified_connections)}/{len(conn_ids)} connections:"
            )
            for conn_id, message in found_not_verified_connections.items():
                print(f"❌ {conn_id}: {message}")

        if not_found_connections:
            print(f"Unable to read {len(not_found_connections)}/{len(conn_ids)} connections:")
            for conn_id in not_found_connections:
                print(f"❓ {conn_id}")

        if found_not_verified_connections or not_found_connections:
            raise AirflowException("Not all connections were verified successfully.")

    @task
    def check_variable_existence(params=None):
        """
        Variables can take any structure. Therefore, we can only check if they exist, but not verify if the
        content is correct.
        """
        variable_ids = params["variable_ids"]
        if not variable_ids:
            raise AirflowSkipException("⏭️ No variable ids provided. Nothing to do.")

        found_variables = set()
        not_found_variables = set()
        for variable_id in variable_ids:
            try:
                Variable.get(key=variable_id)
                found_variables.add(variable_id)
            except KeyError:
                not_found_variables.add(variable_id)

        if found_variables:
            print(f"Found {len(found_variables)}/{len(variable_ids)} variables:")
            for variable_id in found_variables:
                print(f"✅ {variable_id}")

        if not_found_variables:
            print(f"Could NOT find {len(not_found_variables)}/{len(variable_ids)} variables:")
            for variable_id in not_found_variables:
                print(f"❌ {variable_id}")

            raise AirflowException("At least 1 variable not found.")

    verify_connections()
    check_variable_existence()


connection_variable_test()
