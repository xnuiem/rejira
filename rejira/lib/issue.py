from rejira.lib.error import InvalidUsage
from pprint import pprint


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

    def create_object(self, json, fields):
        for key, value in fields.items():
            if key is "dates":
                self.handle_dates(json, fields)
            elif key is "comments":
                self.handle_comments(json, fields)
            elif value is not None:
                if isinstance(value, dict):
                    if "sub" in value and value["sub"] is False:
                        if "value_field" in value:
                            v = json[value["inside"]][key][value["value_field"]]
                        else:
                            v = json[value["inside"]][key]
                        setattr(self, key, v)
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
        self.close()
        return self

    def handle_comments(self, json, fields):
        comments = []

        for comment in json["fields"]["comment"]["comments"]:
            comment_obj = lambda: None
            for field_key, field_value in fields["comments"].items():
                name = field_key
                if isinstance(field_value, dict):
                    setattr(comment_obj, field_key, lambda: None)
                    sub_obj = getattr(comment_obj, field_key)
                    if comment[field_key] is not None:
                        self.find_sub_value(comment[field_key], field_value, sub_obj)
                else:
                    if field_value is not None:
                        name = field_value
                    setattr(comment_obj, name, comment[field_key])
            comments.append(comment_obj)
            del comment_obj
        setattr(self, "comments", comments)

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
