from rejira.lib.cache import Cache
import logging


class ReJIRA:

    def __init__(self, config, field_map):
        self.config = config
        logging.basicConfig(level=config.logging_level)
        logger = logging.getLogger(__name__)

        if config.logging_file:
            handler = logging.FileHandler(config.logging_file)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        self.logger = logger
        self.logger.info('Starting')
        self.logger.debug('===========================')
        self.logger.debug('Configuration')
        self.logger.debug('LOGGING level:%s, file:%s', config.logging_level, config.logging_file)
        self.logger.debug('CACHE host:%s, port:%s, db:%s, expire:%s, toggle:%s', config.cache_host, config.cache_port,
                          config.cache_db, config.cache_expire, config.cache_on)

        self.logger.debug('MAPPING fields:%s, raw:%s', config.map_fields, config.map_raw)
        self.logger.debug('JIRA lib:%s, options:%s', config.jira_lib, config.jira_options)
        self.logger.debug('===========================')
        self.cache = Cache(config, self.logger, field_map)

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
                self.logger.info('Flushing All Keys')
                source.flush_all()
            else:
                self.logger.info('Deleting: %s', scope)
                source.delete(scope)
            return True
        else:
            return False
