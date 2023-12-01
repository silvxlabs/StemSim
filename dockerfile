FROM python:3.12

RUN pip install poetry

COPY . .

RUN poetry install

CMD exec uvicorn ttsim.main:app --host 127.0.0.1 --port 8000