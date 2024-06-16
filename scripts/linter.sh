#!/bin/sh
source scripts/initiate.sh # Initiate scripts

ruff check .
black . --check
mypy
