#!/bin/bash

flake8 src
black --check src
autoflake --check -r src
