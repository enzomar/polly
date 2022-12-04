FROM python:3.10

ENV LOCAL_IP "127.0.0.1"
ENV LOCAL_PORT "5500" 
ENV TTL -1
ENV DESTINATION 0
ENV PORT "80" 
ENV FLUSH 0

EXPOSE 5000

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD polly /app

CMD python main.py -l $LOCAL_IP -p $LOCAL_PORT -t $TTL -d $DESTINATION -o $PORT