import unittest
import json
import logging
import sys
import inspect
import os
import xmlrunner
from ddt import ddt, data
from customassertions import CustomAssertions
from mockFields import field_map
import mockconfig

cmd_folder = os.path.abspath(os.path.join(os.path.split(inspect.getfile(
    inspect.currentframe()))[0], ".."))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from rejira.lib.issue import Issue
from rejira.lib.session import Session
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
class ReJIRAUnitTest(unittest.TestCase, CustomAssertions):

    def setUp(self):
        self.config = self.setup_config()
        self.logging = self.setup_logging()

    def tearDown(self):
        del self.config
        del self.logging

    @staticmethod
    def get_req(file_name):
        with open(file_name, 'r') as file:
            req = file.read()
            file.close()
        return json.loads(req)

    def create_issue(self):
        return Issue(self.config, self.logging)

    @staticmethod
    def setup_config():
        config = mockconfig
        config.cache_host = os.getenv('REJIRA_CACHE_HOST', 'localhost')
        config.cache_port = os.getenv('REJIRA_CACHE_PORT', 6379)
        config.cache_db = os.getenv('REJIRA_CACHE_DB', 0)
        config.cache_on = str_to_bool(os.getenv('REJIRA_CACHE_ON', 'True'))
        config.cache_expire = os.getenv('REJIRA_CACHE_EXPIRE', 3600)
        config.jira_user = os.getenv('REJIRA_JIRA_USER', '')
        config.jira_pass = os.getenv('REJIRA_JIRA_PASS', '')
        config.jira_options["server"] = os.getenv('REJIRA_JIRA_SERVER', '')
        config.logging_level = os.getenv('REJIRA_LOGGING_LEVEL', 'ERROR')
        config.logging_file = os.getenv('REJIRA_LOGGING_FILE', '')
        config.verify_host = str_to_bool(os.getenv('REJIRA_VERIFY_HOST', 'True'))
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

    def test_issue_close_logger(self):
        """Issue Close Logger"""
        issue = self.create_issue().close()
        self.assertAttrNotExists(issue, "logger")

    def test_issue_close_config(self):
        """Issue Close Config"""
        issue = self.create_issue().close()
        self.assertAttrNotExists(issue, "config")

    @data('mock-req-1.txt', 'mock-req-1.txt')
    def test_issue_handle_sprint_name(self, file_name):
        req = self.get_req(file_name)
        sprint_obj = self.create_issue().handle_sprint(req["fields"])
        self.assertEqual(sprint_obj.name, 'RT Sprint 1')

    @data('mock-req-3.txt')
    def test_issue_handle_sprint_none(self, file_name):
        req = self.get_req(file_name)
        sprint_obj = self.create_issue().handle_sprint(req["fields"])
        self.assertIsNone(sprint_obj)

    @data('mock-req-1.txt', 'mock-req-2.txt')
    def test_issue_handle_sprint_complete_date(self, file_name):
        req = self.get_req(file_name)
        sprint_obj = self.create_issue().handle_sprint(req["fields"])
        self.assertEqual(sprint_obj.completeDate, '2018-02-22T10:03:20.400Z')

    @data('mock-req-1.txt')
    def test_issue_handle_simple_list(self, file_name):
        req = self.get_req(file_name)
        ret_list = self.create_issue().handle_list(req["fields"]["components"],
                                                   {'fields': {'name': None}})
        self.assertIsInList('comp1', ret_list)

    @data('mock-req-1.txt')
    def test_issue_handle_complex_list_is_list(self, file_name):
        req = self.get_req(file_name)
        ret_list = self.create_issue().handle_list(req["fields"]["components"],
                                                   {'fields': {'name': None,
                                                               'id': None}})
        self.assertIsList(ret_list)

    @data('mock-req-2.txt')
    def test_issue_handle_complex_list_is_list_of_objects(self, file_name):
        req = self.get_req(file_name)
        ret_list = self.create_issue().handle_list(req["fields"]["components"],
                                                   {'fields': {'name': None,
                                                               'id': None}})
        self.assertIsObject(ret_list[0])

    @data('mock-req-1.txt')
    def test_issue_handle_complex_list_attr(self, file_name):
        req = self.get_req(file_name)
        ret_list = self.create_issue().handle_list(req["fields"]["components"],
                                                   {'fields': {'name': None,
                                                               'id': None}})
        self.assertAttrExists(ret_list[0], 'name')

    @data('mock-req-1.txt')
    def test_issue_handle_complex_list_attr_value(self, file_name):
        req = self.get_req(file_name)
        ret_list = self.create_issue().handle_list(req["fields"]["components"],
                                                   {'fields': {'name': None,
                                                               'id': None}})
        self.assertEqual(ret_list[0].name, 'comp1')



    @data('mock-req-1.txt')
    def test_issue_handle_dict_display_name(self, file_name):
        req = self.get_req(file_name)
        obj = self.create_issue().handle_dict(req["fields"]["creator"])
        self.assertEqual(obj.displayName, 'Ryan Meinzer')

    @data('mock-req-1.txt')
    def test_issue_handle_custom_object(self, file_name):
        req = self.get_req(file_name)
        obj = self.create_issue().handle_custom(req, field_map["custom"])
        self.assertIsObject(obj)

    @data('mock-req-1.txt')
    def test_issue_handle_custom_epic(self, file_name):
        req = self.get_req(file_name)
        obj = self.create_issue().handle_custom(req, field_map["custom"])
        self.assertEqual(obj.epic, 'RJTEST-1')

    @data('mock-req-1.txt')
    def test_issue_handle_custom_none(self, file_name):
        req = self.get_req(file_name)
        obj = self.create_issue().handle_custom(req, field_map["custom"])
        self.assertIsNone(obj.customfield_10024)

    @data('mock-req-4.txt')
    def test_issue_handle_custom_string(self, file_name):
        req = self.get_req(file_name)
        obj = self.create_issue().handle_custom(req, field_map["custom"])
        self.assertEqual(obj.customfield_10026, 'Some String')

    @data('mock-req-1.txt')
    def test_issue_handle_custom_checkbox(self, file_name):
        req = self.get_req(file_name)
        obj = self.create_issue().handle_custom(req, field_map["custom"])
        self.assertIsNone(obj.checkbox)

    @data('mock-req-4.txt')
    def test_issue_handle_custom_list(self, file_name):
        req = self.get_req(file_name)
        obj = self.create_issue().handle_custom(req, field_map["custom"])
        self.assertIsList(obj.customfield_10027)

    @data('mock-req-4.txt')
    def test_issue_handle_custom_list_object_value(self, file_name):
        req = self.get_req(file_name)
        obj = self.create_issue().handle_custom(req, field_map["custom"])
        self.assertEqual(obj.customfield_10027[0].name, 'admin')

    @data('mock-req-1.txt')
    def test_issue_handle_dates_due_is_none(self, file_name):
        req = self.get_req(file_name)
        obj = self.create_issue().handle_dates(req, field_map["dates"])
        self.assertIsNone(obj.due)

    @data('mock-req-1.txt')
    def test_issue_handle_dates_create_year_is_2017(self, file_name):
        req = self.get_req(file_name)
        obj = self.create_issue().handle_dates(req, field_map["dates"])
        self.assertEqual(obj.created.year, 2018)

    @data('mock-req-2.txt')
    def test_issue_handle_comments_number_of_comments(self, file_name):
        req = self.get_req(file_name)
        comments = self.create_issue().handle_comments(req,
                                                       field_map["comments"])
        self.assertEqual(len(comments), 2)

    @data('mock-req-2.txt')
    def test_issue_handle_comments_body_content(self, file_name):
        req = self.get_req(file_name)
        comments = self.create_issue().handle_comments(req,
                                                       field_map["comments"])
        self.assertEqual(comments[0].body, 'Adding a comment')

    @data('mock-req-2.txt')
    def test_issue_handle_comments_updated_not_exists(self, file_name):
        req = self.get_req(file_name)
        comments = self.create_issue().handle_comments(req,
                                                       field_map["comments"])
        self.assertAttrNotExists(comments[0], 'updated')

    @data('mock-req-2.txt')
    def test_issue_handle_comments_author_display_name(self, file_name):
        req = self.get_req(file_name)
        comments = self.create_issue().handle_comments(req,
                                                       field_map["comments"])
        self.assertEqual(comments[0].author.displayName, 'Ryan Meinzer')

    @data('mock-req-1.txt', 'mock-req-2.txt', 'mock-req-3.txt')
    def test_issue_create_object(self, file_name):
        req = self.get_req(file_name)
        issue = self.create_issue().create_object(req, field_map)
        self.assertAttrExists(issue, 'key')

    def test_session_headers(self):
        session = Session(self.config, self.logging)
        self.assertAttrExists(session.s, 'headers')

    def test_session_auth(self):
        session = Session(self.config, self.logging)
        self.assertAttrExists(session.s, 'auth')

    @data('mock-query-1.txt')
    def test_cache_create_issue_list_returns_3(self, file_name):
        req = self.get_req(file_name)
        issues = Cache(self.config, self.logging, field_map).create_issue_list(
            req)
        self.assertEqual(len(issues), 8)

    @data('mock-query-1.txt')
    def test_cache_create_issue_list_3rd_issue_no_sprint(self, file_name):
        req = self.get_req(file_name)
        issues = Cache(self.config, self.logging, field_map).create_issue_list(
            req)
        self.assertIsNone(issues[2].sprint)

    @data('mock-query-1.txt')
    def test_cache_create_issue_list_2nd_issue_sprint(self, file_name):
        req = self.get_req(file_name)
        issues = Cache(self.config, self.logging, field_map).create_issue_list(
            req)
        self.assertEqual(issues[1].sprint.name, 'RT Sprint 1')

    @data('mock-query-1.txt')
    def test_cache_create_issue_list_1st_issue_sprint(self, file_name):
        req = self.get_req(file_name)
        issues = Cache(self.config, self.logging, field_map).create_issue_list(
            req)
        self.assertEqual(issues[0].sprint.name, 'RT Sprint 2')

    @data('mock-query-1.txt')
    def test_cache_create_issue_list_comment_author_display_name(self,
                                                                 file_name):
        req = self.get_req(file_name)
        issues = Cache(self.config, self.logging, field_map).create_issue_list(
            req)
        self.assertEqual(issues[1].comments[1].author.displayName,
                         'Ryan Meinzer')

    def test_error_invalid_usage(self):
        with self.assertRaises(InvalidUsage):
            Issue(self.config, self.logging).raise_exception()


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='reports'))
