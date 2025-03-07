FROM python:3.10.9

EXPOSE 5678/tcp

COPY requirements-ui.txt ./
RUN pip install --no-cache-dir -r requirements-ui.txt

COPY . .

CMD [ "python", "./src/ui/main.py" ]