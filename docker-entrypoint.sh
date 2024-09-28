#!/bin/bash

echo "starting the consumer"
uvicorn main:app --host 0.0.0.0 --port 7000
