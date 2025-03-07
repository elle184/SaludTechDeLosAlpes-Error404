FROM python:3.10.9

EXPOSE 5002/tcp

COPY requirements-anonimizador.txt ./
RUN pip install --no-cache-dir -r requirements-anonimizador.txt

COPY . .

CMD [ "flask", "--app", "./api", "run", "--host=0.0.0.0", "--port=5002"]