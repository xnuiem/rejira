import requests


class Session:

    def __init__(self, config, logger):
        logger.info('Created JIRA Session')
        self.s = requests.Session()
        self.s.auth = (config.jira_user, config.jira_pass)
