FROM python:3.10.9

COPY requirements-notificacion.txt ./
RUN pip install --no-cache-dir -r requirements-notificacion.txt

COPY . .

CMD [ "python", "./src/notificaciones/main.py" ]