import sqlite3
import threading
import datetime as dt
import base64
import logging


class Storage(object):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            # another thread could have created the instance
            # before we acquired the lock. So check that the
            # instance is still nonexistent.
            if not cls._instance:
                cls._instance = super(Storage, cls).__new__(cls)
                cls._instance._initialized = False

            return cls._instance


    def _conn(self):
        logging.debug("Fetch DB connection")
        conn = sqlite3.connect("cache.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS messages (key PRIMARY KEY, \
                value TEXT NOT NULL, status TEXT NOT NULL, expire_at DATETIME NOT NULL)")
        return conn

    def _encode(self, message: str):
        message_bytes = message.encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        return base64_bytes.decode('utf-8')

    def _decode(self, base64_message: str):
        base64_bytes = base64_message.encode('utf-8')
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('utf-8')

    def delete(self, key):
        with self._conn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM messages WHERE key == ?", (key,))
        
    def flush(self):
        with self._conn() as conn:
        ## ttl is in seconds
            cursor = conn.cursor()
            cursor.execute("DELETE from messages;")
            conn.commit()
            return True
        return False

    def set(self, key: str, value: str, status: int, ttl: int):
        with self._conn() as conn:
            ## ttl is in seconds
            created_at = dt.datetime.now()
            expire_at = created_at+dt.timedelta(seconds=ttl)
            cursor = conn.cursor()
            value64 = self._encode(value)
            cursor.execute("INSERT INTO messages VALUES (?, ?, ?, ?)", (str(key), str(value64), int(status), expire_at.replace(microsecond=0)))
            conn.commit()
            return True
        return False


    def get(self, key):
        with self._conn() as conn:
            cursor = conn.cursor()
            row = cursor.execute("SELECT value, status, expire_at FROM messages WHERE key == ?",(key,)).fetchone()
            if not row:
                return None, None
            value, status, expire_at_str = row
            expire_at = dt.datetime.strptime(expire_at_str, '%Y-%m-%d %H:%M:%S')
            if expire_at < dt.datetime.now():
                self.delete(key)
                return None, None
            return self._decode(value), int(status)
        