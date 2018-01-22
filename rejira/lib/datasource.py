import redis


class DataSource:
    def __init__(self, config, logger):
        self.cache_expire = config.cache_expire
        self.logger = logger
        self.count = 0
        self.last_id = 0
        self.source = redis.StrictRedis(host=config.cache_host, port=config.cache_port, db=config.cache_db)

    def insert(self, key, value):
        self.source.set(key, value)

    def exists(self, key):
        return self.source.exists(key)

    def set_expire(self, key):
        self.source.expire(key, self.cache_expire)

    def flush_all(self):
        self.source.flushall()

    def update(self, key, value):
        self.insert(key, value)

    def delete(self, key):
        self.source.delete(key)

    def get(self, key):
        return self.source.get(key)

    def search(self, term):
        return self.source.keys(term)
