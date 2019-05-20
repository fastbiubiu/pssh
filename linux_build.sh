#!/bin/bash

docker run --rm -v $(pwd):/app -w /app  python:latest sh build.sh