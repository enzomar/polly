import httplib2

#config = {'ttl':ttl, 'origin':origin, 'destination':destination, 'port':port}


def call(config, method, headers, query, body=None):
    h = httplib2.Http()
    del headers['Host']
    new_query = config['destination']+query
    (resp, content) = h.request(new_query,
                            method, body=body,
                            headers=headers )
    print(content)
    return content.decode("latin-1") , int(resp.status)
