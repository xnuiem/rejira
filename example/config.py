cache_host = 'localhost'
cache_port = 6379
cache_db = 0
cache_on = False
cache_expire = 3600  # Number of seconds until expire

jira_options = {'async': False,
                'rest_api_version': '2',
                'verify': False,
                'agile_rest_path': 'greenhopper',
                'server': 'https://jira.atlassian.net/',
                'rest_path': 'api',
                'check_update': False,
                'agile_rest_api_version': '1.0',
                'client_cert': None,
                'context_path': '/',
                'headers': {
                    'X-Atlassian-Token': 'no-check',
                    'Cache-Control': 'no-cache',
                    'Content-Type': 'application/json'
                },
                'resilient': True
                }
jira_user = 'XXXX'
jira_pass = 'XXXX'
