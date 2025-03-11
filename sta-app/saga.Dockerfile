FROM python:3.12-slim

EXPOSE 5004/tcp

COPY requirements-saga.txt .
RUN pip install --no-cache-dir -r requirements-saga.txt

COPY . .

# Ejcutar main.py
CMD [ "python", "src/saludtech/main.py" ]