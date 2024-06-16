#!/bin/sh
source scripts/initiate.sh # Initiate scripts

ruff check . --fix
black .