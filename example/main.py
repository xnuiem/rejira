import config, fields
import os, inspect, sys
from pprint import pprint

cmd_folder = os.path.abspath(os.path.join(os.path.split(inspect.getfile(
    inspect.currentframe()))[0], ".."))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from rejira import ReJIRA


rj = ReJIRA(config, fields.field_map)

#issue = rj.get("RJTEST-8")
#pprint(vars(issue))

results = rj.search("project = RJTEST order by lastViewed DESC")
#for x in results:
#    pprint(vars(x))
