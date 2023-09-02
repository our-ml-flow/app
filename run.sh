#!/bin/bash
prefect cloud login --key "$PREFECT_API" --workspace "$WORK_SPACE"

uvicorn app.main:app --reload
