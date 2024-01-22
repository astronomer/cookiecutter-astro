import pytest_cookies.plugin
from helpers.utils import bake_in_temp_dir, run_inside_dir


def test_bake(cookies: pytest_cookies.plugin.Cookies, context: dict):
    with bake_in_temp_dir(cookies, context) as result:
        assert result.exit_code == 0
        assert result.exception is None

        project_name = context["team_name"].lower().replace(" ", "_").replace("-", "_")
        assert result.project_path.name == f"astro_team_{project_name}"
        assert result.project_path.is_dir()

        toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert ".astro" in toplevel_files
        assert "dags" in toplevel_files
        assert "include" in toplevel_files
        assert "plugins" in toplevel_files
        assert "tests" in toplevel_files
        assert ".dockerignore" in toplevel_files
        assert ".gitignore" in toplevel_files
        assert "Dockerfile" in toplevel_files
        assert "packages.txt" in toplevel_files
        assert "README.md" in toplevel_files
        assert "requirements.txt" in toplevel_files


def test_bake_pytest(cookies: pytest_cookies.plugin.Cookies, context: dict):
    with bake_in_temp_dir(cookies, context) as result:
        assert result.project_path.is_dir()
        # Use Astro CLI to run generated project in a container instead of having to configure a complicated
        # environment-in-an-environment.
        assert run_inside_dir("astro dev pytest", str(result.project_path)) == 0


def test_bake_parse(cookies: pytest_cookies.plugin.Cookies, context: dict):
    with bake_in_temp_dir(cookies, context) as result:
        # Use Astro CLI to run generated project in a container instead of having to configure a complicated
        # environment-in-an-environment.
        assert run_inside_dir("astro dev parse", str(result.project_path)) == 0
