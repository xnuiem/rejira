from rejira.lib.cache import Cache


class ReJIRA:

    def __init__(self, config, field_map):
        self.config = config
        self.cache = Cache(config, field_map)

    def get(self, key):
        """Fetches a single issue, returning it as a dict.
        key should be the key, not ID, of the issue to return
        """
        issue = self.cache.fetch_issue(key)
        return issue

    def search(self, query):
        """Fetches results of a JQL query
        query should be properly formatted JQL
        """
        results = self.cache.fetch_query(query)
        return results

    def expire(self, scope="all"):
        """Expires the Cache
        Scope can either be a single key or hash_key (for search results)
        or scope can be "all" to flush entire cache.
        "all" is default
        """
        if self.config.cache_on is True:
            from rejira.lib.datasource import DataSource
            source = DataSource(self.config)
            if scope == "all":
                source.flush_all()
            else:
                source.delete(scope)
            return True
        else:
            return False
