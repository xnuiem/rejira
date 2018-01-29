# reJIRA
A very quick and easy to way to query a JIRA instance and cache the results for fast queries and searches.   


## Installation
The easy way to install is 

pip install rejira


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

issues = rj.search('project = OM and fixVersion in ("1.1.1", "1.1.0")')
for issue in issues:
    print(issue.project.name) # "Project Old Main"  
```

## Fields
The structure of the issue objects is set by the field configuration.



## Configuration Options
ReJIRA uses environment variables for most of its configuration.  But there are some to be found in the configuration 
file as well.

### Environment Variables

#### REJIRA_CACHE_HOST
Default: localhost

#### REJIRA_CACHE_PORT
Default: 6379


#### REJIRA_CACHE_DB
Default: 0


#### REJIRA_CACHE_ON
Default: True


#### REJIRA_CACHE_EXPIRE
Default: 3600


#### REJIRA_JIRA_USER


#### REJIRA_JIRA_PASS

#### REJIRA_JIRA_SERVER

#### REJIRA_LOGGING_LEVEL
Default: WARN

#### REJIRA_LOGGING_FILE


#### REJIREA_HTTP_PROXY
Default: None


#### REJIRA_HTTPS_PROXY
Default: None



### Config Parameters
For an example of these, look in /example/config.py

#### jira_options
Uses the same options as the jira library for python.   

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
proxies = { 'https://user:password@proxy.somewhere.com:8888', 'http://user:password@proxy.somewhere.com:8888' }
```
For proxies only, you can also use environment variables as well.


## Methods
### get
### search
### expire






# Credits
Xnuiem - Ryan C Meinzer - https://thescrum.ninja