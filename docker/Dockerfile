FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY scripts/ ./scripts/
COPY /build/contracts ./build/contracts

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./scripts/interact.py"]