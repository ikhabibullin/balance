#!/bin/bash

echo 'autoflake'
autoflake -r src
echo 'black'
black src
