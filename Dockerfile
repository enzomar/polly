FROM python:3.10

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD polly /app

CMD ["python", "polly.py"]