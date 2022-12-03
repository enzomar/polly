import pytest
import cache
import time

# search(request)
# put(request, response, status, ttl)

def test_put():
    s = cache.put("GET uri", "\{'ciccio': 0\}", 200, 1)
    assert(s == True)

        
def test_search_hit():
    value, status = cache.search("GET uri")
    print(value)
    print(status)

    assert(value == "\{'ciccio': 0\}")
    assert(status == 200)

def test_search_miss():
    time.sleep(2)
    value, status = cache.search("GET uri")
    assert(value == None)
    assert(status == None)


