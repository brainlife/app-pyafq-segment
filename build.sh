#!/bin/bash

set -x
set -e

docker build -t brainlife/pyafq .
docker tag brainlife/pyafq brainlife/pyafq:1.0
docker push brainlife/pyafq:1.0
