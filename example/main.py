import config
from rejira import ReJIRA
from pprint import pprint

rj = ReJIRA(config)

issue = rj.get("OM-1")
pprint(vars(issue))

results = rj.search("project = OM order by lastViewed DESC")
for x in results:
    pprint(vars(x))



