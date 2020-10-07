FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y python3.8 python3-pip \
	&& mkdir -p /var/www/fibonacci_server

WORKDIR /var/www/fibonacci_server

COPY requirements.txt fibonacciServer.py ./

RUN pip3 install -r requirements.txt

CMD ["python3","fibonacciServer.py"]
