FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y python3.8 python3-pip \
	&& mkdir -p /var/www/authoritative_server

WORKDIR /var/www/authoritative_server

COPY requirements.txt dict.json authoritativeServer.py ./

RUN pip3 install -r requirements.txt

CMD ["python3","authoritativeServer.py"]