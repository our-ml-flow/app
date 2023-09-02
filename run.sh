#!/bin/bash
export AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID"

export AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY"

export MLFLOW_S3_ENDPOINT_URL=http://localhost:9000

export MLFLOW_TRACKING_URI=http://localhost:5000

prefect cloud login --key "$PREFECT_API" --workspace "$WORK_SPACE"

uvicorn app.main:app --reload
