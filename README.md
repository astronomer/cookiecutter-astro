# cookiecutter-astro

This project contains a Cookiecutter template for Astro projects.

## Create a New Repo From This Template

First install the latest Cookiecutter version if you haven't installed it yet:

```shell
pip install -Y cookiecutter
```

Next, generate a new Astro project from this Cookiecutter project:

```shell
# If you have GitHub SSH configured:
cookiecutter git@github.com:astronomer/cookiecutter-astro.git

# If you have GitHub HTTPS configured:
cookiecutter https://github.com/astronomer/cookiecutter-astro.git
```

Provide a team name. For example:

```shell
  [1/1] team_name (X): business intelligence
```

This will generate an Astro project from the template using the provided values:

```bash
astro_team_business_intelligence/
├── .astro
│   ├── config.yaml                      # Astronomer config file
│   └── test_dag_integrity_default.py    # Astronomer test for validating DAG structure
├── .dockerignore                        # List of files and directories to exclude from Docker build context
├── .github
│   └── workflows
│       ├── astro_deploy.yaml            # GitHub Actions workflow for deploying to a dev and prod deployment
│       └── template-project-update.yaml # GitHub Actions workflow polling this repository for updates
├── .gitignore                           # List of files and directories to exclude when making a commit
├── .pre-commit-config.yaml              # Pre-commit configuration for checks before creating a commit
├── .yamllint.yaml                       # Yamllint configuration
├── Dockerfile                           # Docker image definition in which Astro will run
├── README.md                            # Project readme
├── dags
│   ├── .airflowignore                   # List of pattern to exclude from Airflow
│   ├── connection_variable_test.py      # DAG for validating connections and variables
│   └── hello_world.py                   # Example DAG
├── include                              # Folder for user-defined data, code, etc.
├── packages.txt                         # OS-dependencies to install
├── plugins                              # Folder for Airflow plugins
├── pyproject.toml                       # Configuration for various code checking tools
├── requirements.txt                     # Python-dependencies to install
└── tests
    └── dags
        └── test_dag_integrity.py        # Test for validating DAG structure
```

## Contributing

To contribute to this Cookiecutter template project:

### Install Dependencies

Contributing to this project requires several Python dependencies and the Astro CLI to be installed:

- Install Python dependencies in (virtual) environment with: `pip install -r requirements`
- Install Astro CLI with these instructions: https://docs.astronomer.io/astro/cli/install-cli

After setting up your environment, you can run the tests with:

```shell
pytest tests
```

And static code checks using pre-commit with:

```shell
pre-commit install # (optional)
pre-commit run --all-files
```

Because this project is essentially a project-in-a-project, managing dependencies, tests, code checks, etc. can be a bit tricky. To avoid conflicts, the `.pre-commit-config.yaml` on the root level excludes the complete `{{ cookiecutter.__project_name }}` folder. To validate all the pre-commit checks within a generated project, run the script `run_precommit_on_generated_project.sh`. This generates a new project in a temporary folder and runs all pre-commit checks from there. This keeps dependencies/static code checks/etc. between the two projects seperated while the code is stored in the same repository.

```shell
./run_precommit_on_generated_project.sh
```

The same script is also run in the GitHub Actions CI/CD pipeline.
