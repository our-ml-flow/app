prefect cloud login --key "$PREFECT_API" --workspace "$WORK_SPACE"

uvicorn main:app --reload