cache_host = "localhost"
cache_port = 6379
cache_db = 0
cache_on = True
cache_expire = 3600  # Number of seconds until expire

jira_options = {"async": False,
                "rest_api_version": "2",
                "server": "https://jira.atlassian.net/",
                "rest_path": "api",
                "client_cert": None,
                "context_path": "/",
                "headers": {
                    "X-Atlassian-Token": "no-check",
                    "Cache-Control": "no-cache",
                    "Content-Type": "application/json"
                },
                "resilient": True
                }
jira_user = ""
jira_pass = ""
jira_lib = False  # Use the JIRA Library (https://github.com/pycontribs/jira)

logging_level = "DEBUG"
logging_file = ""

map_fields = False
map_raw = False

