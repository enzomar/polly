import httplib2

#config = {'ttl':ttl, 'origin':origin, 'destination':destination, 'port':port}


def call(config, method, headers, query, body=None):
    h = httplib2.Http()
    if "Host" in headers:
        del headers['Host']
    new_query = config['destination']+query
    resp, content = h.request(new_query,
                            method, body=body,
                            headers=headers )
 
    str_content = content.decode('latin-1')
    return str_content , int(resp.status)
