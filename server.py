#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import argparse, json, os
from subprocess import check_output

class Jarvis():
    def __init__(self):
        #self.path = os.path.dirname(os.path.realpath(__file__))
        self.program = [os.path.join (".", "jarvis.sh"), "-j"]
        self.mute_mode = False
    
    def _exec (self, args):
        flags = []
        if self.mute_mode:
            flags.append ("-m")
        return check_output(self.program + flags + args)
    
    def say (self, phrase):
        return self._exec (["-s", phrase])
    
    def handle_order (self, order):
        return self._exec (["-x", order])


class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('Usage: curl -d "{}" localhost:port')

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        try:
            data = json.loads(post_data)
        except ValueError, e:
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("Bad JSON format\n")
            pass
        else:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            jarvis.mute_mode = ("mute" in data) and (data ["mute"] == 'true')
            if "order" in data:
                self.wfile.write( jarvis.handle_order (data ["order"]) )
            elif "say" in data:
                self.wfile.write( jarvis.say (data ["say"]) )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Jarvis HTTP RestAPI Server')
    parser.add_argument('-p', '--port', help='Listening port (default: 8080)', type=int, default=8080)
    args = parser.parse_args()
    
    jarvis = Jarvis ()
    server_address = ('', args.port)
    http_server = HTTPServer(server_address, RESTRequestHandler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print # new line
        pass
    print 'Stopping HTTP server'
    http_server.server_close()
