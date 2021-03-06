FROM python:3.7-alpine
WORKDIR /api
ENV FLASK_APP api.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache git tk-dev gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
