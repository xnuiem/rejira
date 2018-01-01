import redis
from rejira.lib.error import InvalidUsage


class DataSource:
    def __init__(self, config):
        self.cache_expire = config.cache_expire
        self.count = 0
        self.last_id = 0
        self.source = redis.StrictRedis(host=config.cache_host, port=config.cache_port, db=config.cache_db)

    def insert(self, key, value):
        try:
            self.source.set(key, value)
        except:
            raise InvalidUsage('Error Connecting to Redis Server in Insert')

    def exists(self, key):
        try:
            ret = self.source.exists(key)
        except:
            raise InvalidUsage('Error Connecting to Redis Server in Exists')

        return ret

    def set_expire(self, key):
        try:
            self.source.expire(key, self.cache_expire)
        except:
            raise InvalidUsage('Error Connecting to Redis Server in Set_Expire')

    def flush_all(self):
        try:
            self.source.flushall()
        except:
            raise InvalidUsage('Error Connecting to Redis Server in Flush_All')

    def update(self, key, value):
        self.insert(key, value)

    def delete(self, key):
        try:
            self.source.delete(key)
        except:
            raise InvalidUsage('Error Connecting to Redis Server in Delete')

    def get(self, key):
        try:
            r = self.source.get(key)
            return r
        except:
            raise InvalidUsage('Error Connecting to Redis Server in Get')

    def search(self, term):
        try:
            r = self.source.keys(term)
            return r
        except:
            raise InvalidUsage('Error Connecting to Redis Server in Search')
