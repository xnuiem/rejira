# reJIRA
A very quick and easy to way to query a JIRA instance and cache the results for fast queries and searches.  JIRA's API 
can be very slow, especially in large hosted projects.  This module attempts to solve for that by caching the results
of queries in redis. 

## Installation
The easy way to install is 
```text
pip install rejira
```
# Usage
## Quick Start
```python
import config, fields
from rejira import ReJIRA
 
rj = ReJIRA(config, fields.field_map)
 
issue = rj.get("OM-1")
print(issue.key) # "OM-1"
print(issue.sprint.name) # "Sprint 66"
```

Or you can use search() to run JQL and return the results as a list of objects
```python
...
issues = rj.search('project = OM and fixVersion in ("1.1.1", "1.1.0")')
for issue in issues:
    print(issue.project.name) # "Project Old Main"  
```

## Fields
The structure of the issue objects is set by the field configuration.  This is basically a large dictionary that lets 
reJIRA know how to structure your issue objects.



## Configuration Options
ReJIRA uses environment variables for most of its configuration.  But there are some to be found in the configuration 
file as well.

### Environment Variables
Defaults are (<strong>bold</strong>)

#### REJIRA_CACHE_HOST
The host for Redis. (<strong>localhost</strong>)

#### REJIRA_CACHE_PORT
The host for Redis. (<strong>6379</strong>)

#### REJIRA_CACHE_DB
Redis Database (<strong>0</strong>)

#### REJIRA_CACHE_ON
Use the Redis Cache. (<strong>True</strong>)

#### REJIRA_CACHE_EXPIRE
Number of seconds to expire a cached result. (<strong>3600</strong>)

#### REJIRA_JIRA_USER
Your JIRA Username.

#### REJIRA_JIRA_PASS
Your JIRA Password

#### REJIRA_JIRA_SERVER
Your JIRA host URL.  Make sure it is https and has a trailing slash. (e.g. https://jira.atlassian.net)

#### REJIRA_LOGGING_LEVEL
Logging Level (<strong>WARN</strong>)

#### REJIRA_LOGGING_FILE
The file to write logs to.  Defaults to STDOUT.  If this is not blank, it will write the logs to this file. (<strong>blank</strong>)

#### REJIRA_HTTP_PROXY
HTTP Proxy. Can be domain or host. (<strong>None</strong>)(e.g. http://username:password@proxy.host.com:8888)

#### REJIRA_HTTPS_PROXY
HTTPS Proxy. Can be domain or host. (<strong>None</strong>)(e.g. http://username:password@proxy.host.com:8888)

### Config Parameters
For an example of these, look in /example/config.py

#### jira_options
Uses the same options as the jira library for python.   
```python
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
```
#### jira_lib
Not currently used 

#### map_fields
Not currently used
 
#### map_raw
Not currently used 

#### create_test_file
Not currently used 

#### proxies = {}
If you are behind a proxy server, put the strings for them here.  Include basic auth in the proxy.  
Example:
```python
proxies = { 'https://user:password@proxy.somewhere.com:8888', \
'http://user:password@proxy.somewhere.com:8888' }
```
For proxies, you can also use environment variables as well.


## Methods
### get
Parameters
### search
### expire








# Credits
Xnuiem - Ryan C Meinzer - https://thescrum.ninja

# License
Copyright 2018 XM Tek LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
