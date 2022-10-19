FROM python:3.8

LABEL maintainer="Rashmi"

COPY . /app

WORKDIR /app/project/techtrends/

RUN /bin/sh -c pip3 install -r requirements.txt

RUN /bin/sh -c python init_db.py

CMD ["python", "app.py"]
 
EXPOSE 3111
