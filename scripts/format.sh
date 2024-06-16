#!/bin/sh

set -e # ensure no error appears
source ./venv/Scripts/activate # Activate virtual env

ruff check . --fix
black .