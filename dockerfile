FROM python:3.11.4

WORKDIR /app
COPY . .

# install poetry & scikit-surprise==1.1.3
RUN pip install poetry
RUN pip install scikit-surprise==1.1.3
RUN poetry config virtualenvs.create false

COPY pyproject.toml ./
RUN poetry install --no-dev


CMD poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
