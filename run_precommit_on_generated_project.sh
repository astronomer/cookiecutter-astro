#!/usr/bin/env bash

set -ex

cookiecutter_dir="$(realpath "$(dirname "$0")")"
temporary_dir=$(mktemp -d)
trap 'rm -rf -- "${temporary_dir}"' EXIT

# Generate a project from the cookiecutter template
cd "${temporary_dir}"
cookiecutter --no-input "${cookiecutter_dir}"

# Navigate to the generated project
cd *

# Run pre-commit
git init
git add .
pre-commit run --color=always --all-files
