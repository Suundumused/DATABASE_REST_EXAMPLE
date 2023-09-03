FROM python:3

WORKDIR /app

COPY . /app

RUN pip install -r requeriments.txt
EXPOSE 8080

CMD ["python", "app/main.py"]