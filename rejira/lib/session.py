import requests


class Session:

    def __init__(self, config, logger):
        logger.info('Created JIRA Session')
        self.s = requests.Session()
        self.s.auth = (config.jira_user, config.jira_pass)
        self.s.headers.update(config.jira_options["headers"])
        if len(config.proxies) != 0:
            self.s.proxies.update(config.proxies)
