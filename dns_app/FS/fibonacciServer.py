#! /usr/bin/env python3
from flask import Flask, request
import socket
import json
import random

app = Flask(__name__)


def dns_query(hostname, type='A', server_ip="127.0.0.1", server_port=53533, client_ip="0.0.0.0", client_port=53535):
    #Create a socket for DNS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    #Format query
    query = 'TYPE={}\nNAME={}'.format(type,hostname).encode()
    #Listen on authoritative client port
    sock.bind((client_ip, client_port))
    #Send lookup to authoritative server
    sock.sendto(query, (server_ip, server_port))
    #Get response from authoritative server
    data, addr = sock.recvfrom(1024)
    #Close socket
    sock.close()
    #Handle response
    data = json.loads(data.decode().replace("\'", "\""))

    # Return hostnames ip address
    return data.get('VALUE')

    
def dns_register(hostname, record_type='A', ip_addr=None, ttl=10, server_ip="127.0.0.1", server_port=53533, client_ip="0.0.0.0", client_port=53535):
    #Create a socket for DNS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    #Format query
    query = 'TYPE={}\nNAME={}\nVALUE={}\nTTL={}'.format(record_type,hostname,ip_addr,ttl).encode()
    #Listen on authoritative client port
    sock.bind((client_ip, client_port))
    #Send registration to authoritative server
    sock.sendto(query, (server_ip, server_port))
    #Get response from authoritative server
    data, addr = sock.recvfrom(1024)
    #Close socket
    sock.close()
    return data.decode()


@app.route('/register', methods=["PUT"])
def register():
    content  =  request.json
    hostname =  content['hostname']
    ip_addr  =  content['ip']
    as_ip    =  content['as_ip']
    as_port  =  int(content['as_port'])
    print(hostname, ip_addr, as_ip, as_port)
    success = dns_register(hostname, ip_addr=ip_addr, server_ip=as_ip, server_port=as_port) # check for success or failure
    if success == 1:
        return "", 400
    return "", 201

def calculateFibonacci(n):
    if n ==1:
        return 0
    elif n==2:
        return 1
    else:
        return calculateFibonacci(n-1) + calculateFibonacci(n-2)

    
@app.route('/fibonacci')
def fibonacci():
    number = int(request.args.get('number'))
    if not isinstance(number, int):
        return "", 400
    
    return str(calculateFibonacci(number))


if __name__ == '__main__':
    #Start flask server
    app.run(host="0.0.0.0", port=9090, debug=True)
