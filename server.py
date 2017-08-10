#!/usr/bin/env python2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import argparse # manage program arguments
import json # read input json
import os # build path
import socket # port in use exception
import sys # exit (1)
#import ssl # https
import signal # catch kill
import urlparse # parse url parameters
from subprocess import check_output, call # run shell commands

class Jarvis():
    def __init__(self):
        #self.path = os.path.dirname(os.path.realpath(__file__))
        self.program = ["jarvis", "-j"]
        self.mute_mode = False
        self.verbose = False
    
    def _exec (self, args):
        flags = []
        if self.mute_mode:
            flags.append ("-m")
        if self.verbose:
            flags.append ("-v")
        return check_output(self.program + flags + args)
    
    def get_config (self):
        config={}
        for config_filename in os.listdir  ('config'):
            with open (os.path.join ('config', config_filename)) as config_file:
                config[config_filename]=config_file.read ().rstrip ()
        return config
    
    def set_config (self, config):
        for config_filename in os.listdir  ('config'):
            with open (os.path.join ('config', config_filename), 'w') as config_file:
                value=config[config_filename]
                if isinstance (value, bool):
                    value="true" if value else "false" # to string would give "True"
                config_file.write (value.encode('utf-8')+'\n')
    
    def say (self, phrase):
        return json.loads(self._exec (["-s", phrase]), strict=False)
    
    def handle_order (self, order):
        return json.loads(self._exec (["-x", order]), strict=False)
    
    def listen (self):
        return json.loads(self._exec (["-l"]))
    
    def get_commands (self):
        with open('jarvis-commands') as the_file:
            return { 'commands' : the_file.read() }
    
    def set_commands (sef, commands):
        commands=commands.rstrip()+'\n' # add new line end of file if missing
        with open ('jarvis-commands', 'w') as the_file:
            the_file.write (commands.encode('utf-8'))
    
    def get_events (self):
        with open('jarvis-events') as the_file:
            return { 'events' : the_file.read() }
    
    def set_events (sef, events):
        events=events.rstrip()+'\n' # add new line end of file if missing
        with open ('jarvis-events', 'w') as the_file:
            the_file.write (events.encode('utf-8'))
        call(['crontab', 'jarvis-events', '-i'])

def proper_exit (signum, frame):
    print 'Stopping HTTP server'
    http_server.server_close()
    sys.exit(0)

def handle_request (self, data):
    # check api key if defined by user
    if args.key:
        if not ("key" in data):
            raise ValueError ("Missing API Key")
        elif (data["key"] == ""):
            raise ValueError ("Empty API Key")
        elif (data["key"] != args.key):
            raise ValueError ("Invalid API Key")
    
    if "mute" in data:
        mute=data["mute"]
        jarvis.mute_mode=mute if isinstance(mute, bool) else (mute.lower() != "false")
    if "verbose" in data:
        verbose=data["verbose"]
        jarvis.verbose=verbose if isinstance(verbose, bool) else (verbose.lower() != "false")
    
    response={"status":"ok"}
    if "action" in data:
        action = data ["action"]
        if action == "listen":
            response=jarvis.listen ()
        elif action == "get_commands":
            response=jarvis.get_commands ()
        elif action == "set_commands":
            if "commands" in data:
                jarvis.set_commands (data ["commands"])
            else:
                raise ValueError ("Missing commands parameter")
        elif action == "get_events":
            response=jarvis.get_events ()
        elif action == "set_events":
            if "events" in data:
                jarvis.set_events (data ["events"])
            else:
                raise ValueError ("Missing events parameter")
        elif action == "get_config":
            response=jarvis.get_config ()
        elif action == "set_config":
            jarvis.set_config (data ["config"])
        else:
            raise ValueError ("Unsupported action: "+action)
    elif "order" in data:
        response=jarvis.handle_order (data ["order"])
    elif "say" in data:
        response=jarvis.say (data ["say"])
    else:
        raise ValueError ("Don't know what to do with: "+ json.dumps (data))
    self.send_response(200)
    self.send_header("Access-Control-Allow-Origin", "*")
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps (response))

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self._set_headers()
    
    def do_GET(self):
        url = urlparse.urlparse(self.path)
        data = dict(urlparse.parse_qsl(url.query))
        try:
            handle_request (self, data)
        except Exception as e:
            self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type", "application/json")
            self.end_headers()
            print "ERROR:", e
            self.wfile.write(json.dumps ({"error":str(e)}))
            pass
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        try:
            data = json.loads(post_data)
            handle_request (self, data)
        except Exception as e:
            self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type", "application/json")
            self.end_headers()
            print "ERROR:", e
            self.wfile.write(json.dumps ({"error":str(e)}))
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Jarvis HTTP RestAPI Server')
    parser.add_argument('-k', '--key', help='Optional secret key')
    parser.add_argument('-p', '--port', help='Listening port (default: 8080)', type=int, default=8080)
    #parser.add_argument('-s', '--ssl', help='Use SSL', action='store_true')
    args = parser.parse_args()
    
    jarvis = Jarvis ()
    try:
        http_server = HTTPServer(('', args.port), RESTRequestHandler)
        #if args.ssl:
        #    http_server.socket = ssl.wrap_socket (http_server.socket, certfile='./server.pem', server_side=True)
        for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
            signal.signal(sig, proper_exit)
        http_server.serve_forever()
    except socket.error, msg:
        print 'ERROR: ', msg
        sys.exit(1)
    except KeyboardInterrupt:
        print # new line
        pass
