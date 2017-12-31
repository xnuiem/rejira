import requests


class Session:

    def __init__(self, config):
        self.s = requests.Session()
        self.s.auth = (config.jira_user, config.jira_pass)
