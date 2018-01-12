import config, fields
from rejira import ReJIRA
from pprint import pprint

rj = ReJIRA(config, fields.field_map)

#issue = rj.get("OM-2")
#pprint(vars(issue.custom.customfield_10006))

results = rj.search("project = OM order by lastViewed DESC")
for x in results:
    pprint(vars(x))
