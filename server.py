import SocketServer
# coding: utf-8
import os
# Copyright 2013 Eric Lam, Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        inputData = self.data.split('\n')
        path = os.path.abspath(os.path.dirname(__file__))
        getRequest = "/www/"
        getRequest += inputData[0].split(" ")[1]
        
        # Check if directory or not if it is, then file html file
        path += getRequest
        if os.path.isdir(path) and path.endswith("/"):
            path += "index.html"

        # Check if directory and if it doesn't have a trailing slash, to deal with '/deep'
        if os.path.isdir(path) and not path.endswith("/"):
            path += "/index.html"

        # Cheap fix to deal with the css when faced with '/deep'
        # Issue is '/www//deep.css'
        if path.endswith("//deep.css"):
            replace = path.split("//")
            path = replace[0]
            replace[1] = "/deep/deep.css"
            path += replace[1]
            
        dataToSend = ''
        
        # For CSS files
        if(path.endswith(".css")):
            try:
                responseCSS = open(path, "r")
                dataToSend += 'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n'

                dataToSend += responseCSS.read()
                self.request.sendall(dataToSend)
            except IOError:
                self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n")
        # For HTML files
        elif(path.endswith(".html")):
            try:
                response = open(path, "r")
                dataToSend = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
                dataToSend += response.read()
                self.request.sendall(dataToSend)
            except IOError:
                self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n")
        # Otherwise just 404
        else:
            self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
