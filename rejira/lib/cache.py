from rejira.lib.datasource import DataSource
from rejira.lib.session import Session
from rejira.lib.issue import Issue
from rejira.lib.error import InvalidUsage
import json
import hashlib


class Cache:

    def __init__(self, config, field_map):
        self.data = DataSource(config)
        self.config = config
        self.session = Session(config).s
        self.field_map = field_map

    def expire_all(self):
        self.data.flush_all()
        return True

    def fetch_issue(self, key):
        if self.data.exists(key) is True and self.config.cache_on is True:
            req = json.loads(self.data.get(key).decode("utf-8"))
        else:
            request_url = self.config.jira_options['server'] + self.config.jira_append_path + 'issue/' + key
            req = self.session.get(request_url)
            if req.status_code == 401:
                raise InvalidUsage('Authentication to JIRA failed')
            elif req.status_code == 502:
                raise InvalidUsage('Couldn\'t find the JIRA server')
            elif req.status_code != 200:
                raise InvalidUsage('JIRA Server returned an error: ' + req.status_code)
            req = req.json()
            if self.config.cache_on is True:
                self.data.insert(key, json.dumps(req))
                self.data.set_expire(key)
        issue = Issue(self.config).create_object(req, self.field_map)
        return issue

    def fetch_query(self, query):
        issues = []
        hash_key = hashlib.md5(query.encode('utf-8')).hexdigest()
        if self.data.exists(hash_key) is True and self.config.cache_on is True:
            req = json.loads(self.data.get(hash_key).decode("utf-8"))
            for x in req["issues"]:
                issue = Issue(self.config).create_object(x, self.field_map)
                issues.append(issue)

        else:
            request_url = self.config.jira_options['server'] + self.config.jira_append_path + 'search'

            data = {
                "jql": query,
                "startAt": 0
            }

            req = self.session.post(request_url, '', data)
            if req.status_code == 401:
                raise InvalidUsage('Authentication to JIRA failed')
            elif req.status_code == 502:
                raise InvalidUsage('Couldn\'t find the JIRA server')
            elif req.status_code != 200:
                raise InvalidUsage('JIRA Server returned an error: ' + req.status_code)

            req = req.json()
            for x in req["issues"]:
                issue = Issue(self.config).create_object(x, self.field_map)
                issues.append(issue)
            if self.config.cache_on is True:
                self.data.insert(hash_key, json.dumps(req))
                self.data.set_expire(hash_key)
        return issues
