FROM python:3.10.16-bookworm

COPY ../.. /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

EXPOSE 8000

CMD ["-m", "flask", "--app", "src/sta/api", "run", "--host=0.0.0.0", "--port=8000"]