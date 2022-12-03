import storage
import key

def put(request: str, response: str, status, ttl):
    k = key.build(request)
    s = storage.Storage()
    return s.set(k, response, status, ttl)

def search(request):
    k = key.build(request)
    s = storage.Storage()
    return s.get(k)

def flush(request):
    s = storage.Storage()
    return s.delete_all(k)

    
