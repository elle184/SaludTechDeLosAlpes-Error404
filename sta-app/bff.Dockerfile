FROM python:3.10.9

EXPOSE 5050/tcp

COPY requirements-bff.txt ./
RUN pip install --no-cache-dir -r requirements-bff.txt

COPY . .

CMD [ "flask", "--app", "./src/bff/api", "run", "--host=0.0.0.0", "--port=5050"]