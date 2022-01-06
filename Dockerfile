FROM python:3.8

WORKDIR /app

COPY src/requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY src /app

COPY ./entrypoint.sh /entrypoint.sh

EXPOSE 5000

CMD ["python", "app.py"]
