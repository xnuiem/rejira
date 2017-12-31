cache_host = 'localhost'
cache_port = 6379
cache_db = 0
cache_on = True
cache_expire = 3600 # Number of seconds to 

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
jira_append_path = 'rest/api/2/'
jira_user = 'XXXX'
jira_pass = 'XXXX'

field_map = {
    "key": None,
    "creator": {
        "inside": "fields",
        "emailAddress": "email",
        "displayName": None,
        "name": None
    },
    "assignee": {
        "inside": "fields",
        "emailAddress": "email",
        "displayName": None,
        "name": None
    },
    "summary": {
        "inside": "fields",
        "sub": False
    },
    "status": {
        "inside": "fields",
        "value_field": "name",
        "sub": False
    },
    "project": {
        "inside": "fields",
        "key": None,
        "name": None
    },
    "resolution": {
        "inside": "fields",
        "sub": False
    },
    "issuetype": {
        "inside": "fields",
        "sub": False,
        "value_field": "name"
    },
    "dates": {
        "created": None,
        "lastViewed": "viewed",
        "resolutiondate": "resolved",
        "updated": None,
        "duedate": "due"
    },

}


