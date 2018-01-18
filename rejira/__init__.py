import logging
import os

from rejira.lib.cache import Cache

class ReJIRA:

    def __init__(self, config, field_map):
        self.config = config
        self.setup_config()

        logging.basicConfig(level=self.config.logging_level)
        logger = logging.getLogger(__name__)

        if config.logging_file:
            handler = logging.FileHandler(self.config.logging_file)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        self.logger = logger
        self.logger.info('Starting')
        self.logger.debug('===========================')
        self.logger.debug('Configuration')
        self.logger.debug('LOGGING level:%s, file:%s', self.config.logging_level, self.config.logging_file)
        self.logger.debug('CACHE host:%s, port:%s, db:%s, expire:%s, toggle:%s', self.config.cache_host, self.config.cache_port,
                          self.config.cache_db, self.config.cache_expire, self.config.cache_on)

        self.logger.debug('MAPPING fields:%s, raw:%s', self.config.map_fields, self.config.map_raw)
        self.logger.debug('JIRA lib:%s, options:%s', self.config.jira_lib, self.config.jira_options)
        self.logger.debug('===========================')
        self.cache = Cache(self.config, self.logger, field_map)

    def setup_config(self):
        self.config.cache_host = os.getenv('REJIRA_CACHE_HOST', 'localhost')
        self.config.cache_port = os.getenv('REJIRA_CACHE_PORT', 6379)
        self.config.cache_db = os.getenv('REJIRA_CACHE_DB', 0)
        self.config.cache_on = os.getenv('REJIRA_CACHE_ON', True)
        self.config.cache_expire = os.getenv('REJIRA_CACHE_EXPIRE', 3600)
        self.config.jira_user = os.getenv('REJIRA_JIRA_USER', '')
        self.config.jira_pass = os.getenv('REJIRA_JIRA_PASS', '')
        self.config.jira_options["server"] = os.getenv('REJIRA_JIRA_SERVER', '')
        self.config.logging_level = os.getenv('REJIRA_LOGGING_LEVEL', 'WARN')
        self.config.logging_file = os.getenv('REJIRA_LOGGING_FILE', '')


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
