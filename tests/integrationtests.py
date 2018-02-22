import unittest
import logging
import sys
import inspect
import os
import xmlrunner
import hashlib
from ddt import ddt, data
from customassertions import CustomAssertions
from mockFields import field_map
import mockconfig
import time

cmd_folder = os.path.abspath(os.path.join(os.path.split(inspect.getfile(
    inspect.currentframe()))[0], ".."))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from rejira.lib.cache import Cache
from rejira.lib.error import InvalidUsage


def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError


@ddt
class ReJIRAIntegrationTest(unittest.TestCase, CustomAssertions):

    def setUp(self):
        self.config = self.setup_config()
        self.logging = self.setup_logging()

    def tearDown(self):
        del self.config
        del self.logging

    @staticmethod
    def setup_config():
        config = mockconfig
        config.cache_host = os.getenv('REJIRA_CACHE_HOST', 'localhost')
        config.cache_port = os.getenv('REJIRA_CACHE_PORT', 6379)
        config.cache_db = os.getenv('REJIRA_CACHE_DB', 0)
        config.cache_on = str_to_bool(os.getenv('REJIRA_CACHE_ON', True))
        config.cache_expire = os.getenv('REJIRA_CACHE_EXPIRE', 3600)
        config.jira_user = os.getenv('REJIRA_JIRA_USER', '')
        config.jira_pass = os.getenv('REJIRA_JIRA_PASS', '')
        config.jira_options["server"] = os.getenv('REJIRA_JIRA_SERVER', '')
        config.logging_level = os.getenv('REJIRA_LOGGING_LEVEL', 'ERROR')
        config.logging_file = os.getenv('REJIRA_LOGGING_FILE', '')
        http_proxy = os.getenv('REJIRA_HTTP_PROXY', None)
        https_proxy = os.getenv('REJIRA_HTTPS_PROXY', None)

        if http_proxy is not None:
            config.proxies.append(http_proxy)

        if https_proxy is not None:
            config.proxies.append(https_proxy)

        return config

    def setup_logging(self):
        logging.basicConfig(level=self.config.logging_level)
        logger = logging.getLogger(__name__)

        if self.config.logging_file:
            handler = logging.FileHandler(self.config.logging_file)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                "%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @data("RJTEST-1")
    def test_jira_fetch_issue(self, issue_key):
        self.config.cache_on = False
        issue = Cache(self.config, self.logging, field_map).fetch_issue(
            issue_key)
        self.assertEqual(issue.key, issue_key)
        self.setup_config()

    def test_jira_fetch_query_count(self):
        self.config.cache_on = False
        issues = Cache(self.config, self.logging, field_map).fetch_query(
            "project = 'RJTEST'")
        self.assertEqual(len(issues), 8)
        self.setup_config()

    def test_jira_fetch_query_issue_value(self):
        self.config.cache_on = False
        issues = Cache(self.config, self.logging, field_map).fetch_query(
            "project = 'RJTEST'")
        self.assertEqual(issues[2].key, "RJTEST-6")
        self.setup_config()

    @data("RJTEST-1")
    def test_redis_write_read_values(self, issue_key):
        self.config.cache_on = True
        cache = Cache(self.config, self.logging, field_map)
        issue = cache.fetch_issue(issue_key)
        issue_cached = cache.fetch_issue(issue_key)
        self.assertEqual(issue.key, issue_cached.key)
        cache.expire_all()
        self.setup_config()

    @data("RJTEST-1")
    def test_redis_get_by_key(self, issue_key):
        self.config.cache_on = True
        cache = Cache(self.config, self.logging, field_map)
        cache.fetch_issue(issue_key)
        self.assertTrue(cache.data.exists(issue_key))
        cache.expire_all()
        self.setup_config()

    @data("RJTEST-1")
    def test_redis_get_expire_by_key(self, issue_key):
        self.config.cache_on = True
        cache = Cache(self.config, self.logging, field_map)
        cache.fetch_issue(issue_key)
        self.assertTrue(cache.data.exists(issue_key))
        cache.data.delete(issue_key)
        self.assertFalse(cache.data.exists(issue_key))
        cache.expire_all()
        self.setup_config()

    @staticmethod
    def create_hash_key(query):
        hash_key = hashlib.sha256(query.encode('utf-8')).hexdigest()
        return hash_key

    @data("project = 'RJTEST'")
    def test_redis_write_read_query(self, query):
        self.config.cache_on = True
        cache = Cache(self.config, self.logging, field_map)
        issues = cache.fetch_query(query)
        issues_cached = cache.fetch_query(query)
        self.assertEqual(issues[2].key, issues_cached[2].key)
        cache.expire_all()
        self.setup_config()

    @data("project = 'RJTEST'")
    def test_redis_hash(self, query):
        self.config.cache_on = True
        cache = Cache(self.config, self.logging, field_map)
        cache.fetch_query(query)
        self.assertTrue(cache.data.exists(self.create_hash_key(query)))
        cache.expire_all()
        self.setup_config()

    @data("RJTEST-1")
    def test_redis_time_expire(self, issue_key):
        self.config.cache_on = True
        self.config.cache_expire = 10
        cache = Cache(self.config, self.logging, field_map)
        cache.fetch_issue(issue_key)
        self.assertTrue(cache.data.exists(issue_key))
        time.sleep(12)
        self.assertFalse(cache.data.exists(issue_key))
        cache.expire_all()
        self.setup_config()

    @data({'RJTEST-1','RJTEST-2','RJTEST-3'})
    def test_redis_expire_all(self, issues):
        self.config.cache_on = True
        cache = Cache(self.config, self.logging, field_map)
        for issue_key in issues:
            cache.fetch_issue(issue_key)

        self.assertEqual(len(cache.data.search("RJTEST")), 3)
        cache.expire_all()
        self.assertEqual(len(cache.data.search("RJTEST")), 0)
        self.setup_config()

    @data("RJTEST-44454")
    def test_jira_no_issue(self, issue_key):
        self.config.cache_on = True
        cache = Cache(self.config, self.logging, field_map)
        with self.assertRaises(InvalidUsage):
            cache.fetch_issue(issue_key)
        cache.expire_all()
        self.setup_config()


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='reports'))
