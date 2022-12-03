import pytest
import storage

def test_delete():
    s = storage.Storage()
    s.delete("key")

def test_set():
    s = storage.Storage()
    # key, value, status, ttl
    s.set("key", "value", "200", 5)

def test_get():
    s = storage.Storage()
    s.get("key")

