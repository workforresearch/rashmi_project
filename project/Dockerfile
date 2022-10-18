FROM python:3.8

LABEL maintainer="Rashmi"

COPY . /app

WORKDIR /app/techtrends/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
 
EXPOSE 3111
