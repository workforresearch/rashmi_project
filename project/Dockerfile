FROM python:3.8

LABEL maintainer="Rashmi"

COPY . /app

WORKDIR /app/project/techtrends/

RUN pip install -r requirements.txt

RUN python init_db.py

CMD ["python", "app.py"]
 
EXPOSE 3111
