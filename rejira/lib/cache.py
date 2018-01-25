from rejira.lib.datasource import DataSource
from rejira.lib.session import Session
from rejira.lib.issue import Issue
from rejira.lib.error import InvalidUsage
import json
import hashlib



class Cache:

    def __init__(self, config, logger, field_map):
        self.data = DataSource(config, logger)
        self.config = config
        self.logger = logger
        self.field_map = field_map
        self.jira_url = self.config.jira_options['server'] + 'rest/' + self.config.jira_options['rest_path'] + '/' + \
            self.config.jira_options['rest_api_version'] + self.config.jira_options['context_path']

    def expire_all(self):
        self.logger.warning('Flushing all Keys')
        self.data.flush_all()
        return True

    def fetch_issue(self, key):
        req = self.fetch_req(key)
        issue = Issue(self.config, self.logger).create_object(req, self.field_map)
        return issue

    def fetch_query(self, query):
        hash_key = hashlib.sha256(query.encode('utf-8')).hexdigest()
        req = self.fetch_req(hash_key, query)
        issues = self.create_issue_list(req)
        return issues

    def create_issue_list(self, req):
        issues = []
        for x in req["issues"]:
            issue = Issue(self.config, self.logger).create_object(x, self.field_map)
            issues.append(issue)
        return issues

    def fetch_req(self, key, query=""):
        if self.config.cache_on is True and self.data.exists(key) is True:
            self.logger.debug('Fetching from Cache: (%s)', key)
            req = json.loads(self.data.get(key).decode("utf-8"))
            return req

        self.logger.debug('Requesting Query (%s) from JIRA: (%s)', key, query)

        session = Session(self.config, self.logger).s
        if query is not "":
            request_url = self.jira_url + 'search'

            data = {
                "jql": query,
                "startAt": 0,
                "fields": ['*all']
            }
            req = session.post(request_url, '', data)

        else:
            request_url = self.jira_url + 'issue/' + key
            req = session.get(request_url)

        if req.status_code == 401:
            raise InvalidUsage('Authentication to JIRA failed', self.logger)
        elif req.status_code == 502:
            raise InvalidUsage('Couldn\'t find the JIRA server', self.logger)
        elif req.status_code != 200:
            raise InvalidUsage('JIRA Server returned an error: ' + str(req.status_code), self.logger)

        request_json = req.json()
        session.close()
        self.write_to_cache(key, request_json)

        return request_json

    def write_to_cache(self, key, value):
        if self.config.cache_on is True:
            self.logger.debug('Inserting record into Cache: %s', key)
            self.data.insert(key, json.dumps(value))
            self.data.set_expire(key)

    def write_req_to_file(self, req):
        if self.config.create_test_file is True:
            self.logger.debug('Writing to File')
            with open("../tests/mock-req-1.txt", 'w') as file:
                file.write(json.dumps(req))
                file.close()
