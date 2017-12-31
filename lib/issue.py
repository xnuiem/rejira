from lib.map import field_map
from lib.error import InvalidUsage

class Issue:

    def __init__(self, config):
        self.config = config

    def find_sub_value(self, json, fields, obj):
        for key, value in fields.items():
            if key != "inside":
                if value is None:
                    setattr(obj, key, json[key])
                else:
                    setattr(obj, value, json[key])

    def create_object(self, json, fields=field_map):
        for key, value in fields.items():
            if key is "dates":
                self.handle_dates(json, fields)
            elif value is not None:
                if isinstance(value, dict):
                    if "sub" in value and value["sub"] is False:
                        if "value_field" in value:
                            v = json[value["inside"]][key][value["value_field"]]
                        else:
                            v = json[value["inside"]][key]
                        setattr(self, key, v)
                        pass
                    else:
                        setattr(self, key, lambda: None)
                        obj = getattr(self, key)
                        if json[value["inside"]][key] is not None:
                            self.find_sub_value(json[value["inside"]][key], value, obj)
                        else:
                            setattr(obj, key, None)
                else:
                    setattr(self, value, json[key])
            else:
                setattr(self, key, json[key])
        return self

    def handle_dates(self, json, fields):
        setattr(self, "dates", lambda: None)
        obj = getattr(self, "dates")
        for key, value in fields["dates"].items():
            v = json["fields"][key]
            if value is None:
                setattr(obj, key, v)
            else:
                setattr(obj, value, v)

    def close(self):
        del self.config

