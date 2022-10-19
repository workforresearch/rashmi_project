FROM python:3.8

LABEL maintainer="Rashmi"

COPY . /app

WORKDIR /app/techtrends/

RUN /bin/sh -c pip install -r requirements.txt

RUN /bin/sh -c python init_db.py

CMD ["python", "app.py"]
 
EXPOSE 3111
