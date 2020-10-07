#! /usr/bin/env python3
from flask import Flask, request
import requests
import socket
import json


app = Flask(__name__)


def dns_query(hostname, type='A', server_ip="127.0.0.1", server_port=53533, client_ip="0.0.0.0", client_port=53535):
    #Create a socket for DNS
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
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
    

@app.route('/fibonacci')
def fibonacci():
    #Parse url parameters and ensure none are empty
    hostname =  request.args.get('hostname')
    fs_port  =  request.args.get('fs_port')
    number   =  request.args.get('number')
    as_ip    =  request.args.get('as_ip')
    as_port  =  request.args.get('as_port')
    params = [hostname, fs_port, number, as_ip, as_port]
    if None in params:
        return '', 400
    #Cast parameters to correct type
    hostname =  str(hostname)
    fs_port  =  int(fs_port)
    number   =  int(number)
    as_ip    =  str(as_ip)
    as_port  =  int(as_port)

    #Lookup fibonnaci server ip address from authoritative server
    fs_ip = dns_query(hostname, server_ip=as_ip, server_port=as_port)
    #Craft url to query fibonnaci server
    url = "http://{}:{}/fibonacci".format(fs_ip,fs_port)
    num = {'number': number}
    #Make request
    r = requests.get(url, params=num)
    #Return response from fibonnaci server
    return r.text, 200


if __name__ == '__main__':
    #Start flask server
    app.run(host='0.0.0.0', port=8080, debug=True)
