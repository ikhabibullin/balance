#!/bin/bash

poetry install
cp .env.example .env
docker-compose up -d --build
poetry shell