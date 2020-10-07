#! /usr/bin/env python3
import socket
import json


class AuthoritativeServer:

    
    def __init__(self):
        #Load current DNS mappings (ensure that this file is at least an empty dict)
        with open("dict.json", "r") as f:
            self.entries = json.load(f)

         
    def write(self, data):
        #Parse values out of request
        try:
            self.TYPE  = data[0].split("=")[1]
            self.NAME  = data[1].split("=")[1]
            self.VALUE = data[2].split("=")[1]
            self.TTL   = data[3].split("=")[1]
            #Add values to DNS map
            self.entries[self.NAME] = { "TYPE":  self.TYPE,
                                        "NAME":  self.NAME,
                                        "VALUE": self.VALUE,
                                        "TTL":   self.TTL}
            #Save DNS map to file
            with open("dict.json", "w") as f:
                data = json.dumps(self.entries)
                f.write(data)
            return 0
        except:
            return 1


    def lookup(self, data):
        #Parse values out of request
        self.NAME  = data[1].split("=")[1]
        #Return lookup
        return self.entries.get(self.NAME)


def listen(server_ip="0.0.0.0", server_port=53533,client_port=53535): # Change client port depending on if you're talking to user or fibonnaci
    #Create a socket for DNS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Listen on authoritative server port
    sock.bind((server_ip, server_port))
    #Listen forever
    while True:
        data, addr = sock.recvfrom(1024)
        data = data.decode().splitlines()
        #If request is 4 lines it is to register
        if len(data) == 4:
            success = AuthoritativeServer().write(data)
            sock.sendto(str(success).encode(), addr)
        #If 2 request is 2 lines it is to lookup
        elif len(data) == 2:
            entry = AuthoritativeServer().lookup(data)
            #Send lookup response back to client
            sock.sendto(str(entry).encode(), addr)


if __name__=="__main__":
    #Run authoritative server
    listen()
            
        
    

   



        
