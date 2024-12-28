FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY cli/ ./cli/
COPY /build/contracts ./build/contracts

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./cli/main.py"]