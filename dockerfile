FROM python:3.12.1-slim

WORKDIR /code
COPY . /code
ENV DATA_FOLDER=/code/data
RUN pip install --no-cache-dir .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]