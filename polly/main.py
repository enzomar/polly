#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import argparse
import json
from functools import partial
import cache
import forwarder


class Handler(BaseHTTPRequestHandler):
	def __init__(self, config, *args, **kwargs):
		self.config = config
		super().__init__(*args, **kwargs)

	def process(self, method, headers, query, body=None):

		reply, status =  cache.search(query)
		if not reply:
			reply, status = forwarder.call(self.config, method, headers, query, body=None)
			cache.put(query, reply, status, ttl)
		return reply.encode('utf-8'), status
		

	def do_GET(self):
		query = self.path
		
		reply, status = self.process(method="GET", headers=self.headers,query=query)

		self.send_response(status)
		self.end_headers()
		self.wfile.write(reply)
		return



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def parse_arg():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', '--local_ip', default="127.0.0.1") 
	parser.add_argument('-p', '--local_port', default=5500) 
	parser.add_argument('-t', '--ttl', default="-1")  #seconds
	parser.add_argument('-d', '--destination', required=True) 
	parser.add_argument('-o', '--port', default="80") 
	parser.add_argument('-f', '--flush', default=False, action='store_true') 
	parser.add_argument('-v', '--verbose', default=False, action='store_true')

	args = parser.parse_args()

	return args.local_ip, int(args.local_port), int(args.ttl), args.destination, args.port, args.flush, args.verbose


def run(local_ip, local_port, ttl, destination, port, flush, verbose):

	if flush:
		cache.flush()
	config = {'ttl':ttl, 'destination':destination, 'port':port}
	handler = partial(Handler, config)
	server = ThreadedHTTPServer((local_ip, local_port), handler)
	print ('Starting server, use <Ctrl-C> to stop')
	server.serve_forever()
	

if __name__ == '__main__':
	local_ip, local_port, ttl, destination, port, flush, verbose = parse_arg()
	run(local_ip, local_port, ttl, destination, port, flush, verbose)


