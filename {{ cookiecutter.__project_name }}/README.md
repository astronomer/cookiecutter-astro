# Astro project for team {{ cookiecutter.team_name }}

This project contains Airflow code for team {{ cookiecutter.team_name }}.

## Project Contents

This project contains the following files/folders:

```text
├── .github                         # Folder containing scripts for CI/CD on GitHub Actions
├── Dockerfile                      # Astro Runtime Dockerfile. This defines the environment that your workflows run in.
├── README.md                       # You're looking at it
├── dags                            # Folder for your Airflow DAGs
│   ├── connection_variable_test.py # Utility DAG for validating Airflow connections and variables
│   └── hello_world.py              # Bare-minimum Airflow DAG to validate the Deployment
├── include                         # A folder for any additional files that you want to include with the project
├── packages.txt                    # OS-level packages
├── plugins                         # A folder for Airflow plugins
├── pyproject.toml                  # Configuration file for various tools used in this project
├── requirements.txt                # Python requirements
└── tests                           # Folder for tests
    └── dags
        └── test_dag_integrity.py   # Test checking if Python can parse DAG files
```

## Deploy Your Project Locally

1. Start Airflow on your local machine by running `astro dev start`.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering asynchronous tasks

1. Verify that all 4 Docker containers are running `astro dev ps`.

Note: Running `astro dev start` will start your project with the Airflow Webserver exposed on port 8080 and Postgres exposed on port 5432. If you already have those ports allocated, you can either [stop your existing Docker containers or change the port](https://docs.astronomer.io/astro/test-and-troubleshoot-locally#ports-are-not-available).

1. Access the Airflow UI for your local Airflow project. To do so, go to <http://localhost:8080/> and log in with `admin` for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5432/postgres'.

## Deploy Your Project to Astronomer

TODO explain development setup...
