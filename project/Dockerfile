FROM python:3.8

LABEL maintainer="Rashmi"

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN /bin/sh -c pip install -r requirements.txt

RUN /bin/sh -c python init_db.py

COPY . .

CMD ["python", "app.py"]
 
EXPOSE 3111
