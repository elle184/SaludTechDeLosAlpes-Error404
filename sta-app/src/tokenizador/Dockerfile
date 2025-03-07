FROM python:3.10.9

EXPOSE 5001/tcp

COPY requirements-tokenizacion.txt ./
RUN pip install --no-cache-dir -r requirements-tokenizacion.txt

COPY . .

CMD [ "flask", "--app", "./api", "run", "--host=0.0.0.0", "--port=5001"]