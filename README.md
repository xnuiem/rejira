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
print(issue.key) # OM-1
```
## Fields



## Configuration Options






# Credits
Xnuiem - Ryan C Meinzer - https://thescrum.ninja