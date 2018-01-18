from rejira.lib.datasource import DataSource
from rejira.lib.session import Session
from rejira.lib.issue import Issue
from rejira.lib.error import InvalidUsage
import json
import hashlib
from pprint import pprint


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
        if self.config.cache_on is True and self.data.exists(key) is True:
            self.logger.debug('Fetching Issue (%s) from Cache', key)
            req = json.loads(self.data.get(key).decode("utf-8"))
        else:
            self.logger.debug('Requesting Issue (%s) from JIRA', key)
            request_url = self.jira_url + 'issue/' + key
            session = Session(self.config, self.logger).s
            req = session.get(request_url)
            if req.status_code == 401:
                raise InvalidUsage('Authentication to JIRA failed', self.logger)
            elif req.status_code == 502:
                raise InvalidUsage('Couldn\'t find the JIRA server', self.logger)
            elif req.status_code != 200:
                raise InvalidUsage('JIRA Server returned an error: ' + str(req.status_code), self.logger)
            req = req.json()

            self.write_req_to_file(req)

            if self.config.cache_on is True:
                self.logger.debug('Inserting record to cache: %s', key)
                self.data.insert(key, json.dumps(req))
                self.data.set_expire(key)


        issue = Issue(self.config, self.logger).create_object(req, self.field_map)
        return issue

    def fetch_query(self, query):
        issues = []
        hash_key = hashlib.md5(query.encode('utf-8')).hexdigest()
        if self.config.cache_on is True and self.data.exists(hash_key) is True:
            self.logger.debug('Fetching Query (%s) from Cache: (%s)', hash_key, query)
            req = json.loads(self.data.get(hash_key).decode("utf-8"))
            for x in req["issues"]:
                issue = Issue(self.config, self.logger).create_object(x, self.field_map)
                issues.append(issue)

        else:
            self.logger.debug('Requesting Query (%s) from JIRA: (%s)', hash_key, query)
            request_url = self.jira_url + 'search'

            data = {
                "jql": query,
                "startAt": 0,
                "fields": ['*all']
            }
            session = Session(self.config, self.logger).s
            req = session.post(request_url, '', data)
            if req.status_code == 401:
                raise InvalidUsage('Authentication to JIRA failed', self.logger)
            elif req.status_code == 502:
                raise InvalidUsage('Couldn\'t find the JIRA server', self.logger)
            elif req.status_code != 200:
                raise InvalidUsage('JIRA Server returned an error: ' + str(req.status_code), self.logger)

            req = req.json()
            self.write_req_to_file(req)
            for x in req["issues"]:
                issue = Issue(self.config, self.logger).create_object(x, self.field_map)
                issues.append(issue)
            if self.config.cache_on is True:
                self.logger.debug('Inserting record into Cache: %s', hash_key)
                self.data.insert(hash_key, json.dumps(req))
                self.data.set_expire(hash_key)
        return issues

    def write_req_to_file(self, req):
        if self.config.create_test_file is True:
            self.logger.debug('Writing to File')
            with open("../tests/mock-req-1.txt", 'w') as file:
                file.write(json.dumps(req))
                file.close()
