FROM python:3.12.4-slim-bullseye as builder

WORKDIR /twilio-v2v

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt --compile --no-cache-dir

COPY ./app ./app

CMD ["python", "-m", "app.main"]
