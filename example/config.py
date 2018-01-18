jira_options = {"async": False,
                "rest_api_version": "2",
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
jira_lib = False  # Use the JIRA Library (https://github.com/pycontribs/jira)

map_fields = False
map_raw = False

create_test_file = False

