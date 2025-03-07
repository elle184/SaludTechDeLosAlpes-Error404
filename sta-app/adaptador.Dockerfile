FROM python:3.10.9

EXPOSE 50051/tcp

COPY requirements-sidecar.txt ./
RUN pip install --no-cache-dir -r requirements-sidecar.txt

COPY . .

CMD [ "python", "./src/sidecar/main.py" ]