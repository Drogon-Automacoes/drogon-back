#!/bin/bash
set -e

echo "Running Black (Formatter)..."
black app tests

echo "Running Ruff (Linter & Import Sorter)..."
ruff check app tests --fix

echo "Linting Completo!"
