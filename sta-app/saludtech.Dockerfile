FROM python:3.10.9

EXPOSE 5000/tcp

COPY requirements-saludtech.txt ./
RUN pip install --no-cache-dir -r requirements-saludtech.txt

COPY . .

CMD [ "flask", "--app", "./src/saludtech/api", "run", "--host=0.0.0.0", "--port=5000"]