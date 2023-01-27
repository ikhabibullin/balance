#!/bin/bash

echo 'flake8'
flake8 src
echo 'black'
black --check src
echo 'autoflake'
autoflake --check -r src
