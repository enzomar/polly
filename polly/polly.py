#!/usr/bin/env python3

from fastapi import FastAPI, Request
import argparse
import json
from fastapi.responses import HTMLResponse
from . import cache
from . import forwarder
import logging
import uvicorn


app = FastAPI()
logging.getLogger().setLevel(logging.INFO)
_config = {}


def process(method, headers, query, body=None):
	logging.debug("New request info")
	logging.debug("method: {0}".format(method))
	logging.debug("headers: {0}".format(headers))
	logging.debug("query: {0}".format(query))
	logging.debug("body: {0}".format(body))

	reply, status =  cache.search(query)
	if not reply:
		logging.debug("Nothing found in the case, forward ... ")
		reply, status = forwarder.call(_config, method, headers, query, body=None)
		logging.debug("Reply received, storing in the cache ... ")
		cache.put(query, reply, status, _config['ttl'])
	
	logging.debug("Reply status: {0}".format(status))	
	return reply, status


@app.get("/{full_path:path}", response_class=HTMLResponse)
async def proxy_get(request: Request, full_path: str):
	local_headers = request.headers.mutablecopy()

	reply, status = process(method="GET", headers=local_headers,query=full_path)
	HTMLResponse(content=reply, status_code=status)
	return reply


def parse_arg():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', '--local_ip', default="0.0.0.0") 
	parser.add_argument('-p', '--local_port', default=5500) 
	parser.add_argument('-t', '--ttl', default="-1")  #seconds
	parser.add_argument('-d', '--destination', required=True) 
	parser.add_argument('-o', '--port', default="80") 
	parser.add_argument('-f', '--flush', default=False, action='store_true') 
	parser.add_argument('-v', '--verbose', default=False, action='store_true')

	args = parser.parse_args()

	return args.local_ip, int(args.local_port), int(args.ttl), args.destination, args.port, args.flush, args.verbose


def run(local_ip, local_port, ttl, destination = "", port = 80, flush = False, verbose = False):
	global _config
	if verbose:
		logging.getLogger().setLevel(logging.DEBUG)

	if flush:
		cache.flush()
	_config = {'ttl':ttl, 'destination':destination, 'port':port}
	logging.info('Starting server, use <Ctrl-C> to stop')
	uvicorn.run(app, host=local_ip, port=local_port)


if __name__ == '__main__':
	local_ip, local_port, ttl, destination, port, flush, verbose = parse_arg()
	run(local_ip, local_port, ttl, destination, port, flush, verbose)


