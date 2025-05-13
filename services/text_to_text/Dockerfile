FROM python:3.11-slim

WORKDIR /app

COPY services/text_to_text/requirements.txt .
COPY core /app/core
COPY pyproject.toml /app/

RUN pip install -e .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./services/text_to_text/app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]