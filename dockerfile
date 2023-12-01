FROM python:3.12

# Copy dependencies and install
COPY /pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy the source code
COPY . .

# Run the server
CMD ["uvicorn", "stemsim.main:app", "--host", "0.0.0.0", "--port", "80"]