from rejira.lib.error import InvalidUsage
import datetime
from pprint import pprint


class Issue:

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def find_sub_value(self, json, fields, obj):
        for key, value in fields["fields"].items():
            if value is None:
                setattr(obj, key, json[key])
            else:
                setattr(obj, value, json[key])

    def create_object(self, json, fields):
        for key, value in fields.items():
            if key is "dates":
                self.handle_dates(json, value)
            elif key is "comments":
                self.handle_comments(json, value)
            elif key is "sprint" and value is True:
                self.handle_sprint(json)
            elif key is "custom":
                self.handle_custom(json, value)
            elif value is not None:
                if "obj_list" in value:
                    self.handle_list(json[key], value, key)
                elif "is_list" in value:
                    self.handle_list(json[key], value, key, True)
                elif isinstance(value, dict):
                    # I dont use this anymore.  Need to check for just one value.  Value field is gone now too
                    if "sub" in value and value["sub"] is False:
                        if "value_field" in value:
                            v = json[key][value["value_field"]]
                        else:
                            v = json[key]
                        setattr(self, key, v)
                    else:
                        field_name = key
                        sub_json = json
                        if "name" in value.keys() and value["name"] is not None:
                            field_name = value["name"]
                        if key not in json:
                            sub_json = json["fields"]

                        if len(value["fields"]) > 1:
                            obj = type(field_name, (), {})
                            if sub_json[key] is not None:
                                self.find_sub_value(sub_json[key], value, obj)
                            else:
                                setattr(obj, key, None)

                        else:
                            for x in value["fields"]:
                                obj = sub_json[key][x]

                        setattr(self, field_name, obj)
                else:
                    setattr(self, value, json[key])
            else:
                if key not in json:
                    sub_json = json["fields"]
                else:
                    sub_json = json
                setattr(self, key, sub_json[key])
        self.close()
        return self

    def handle_sprint(self, json):
        self.logger.info('Adding Sprint to Issue')
        found_sprint = False
        for x in json:

            if isinstance(json[x], list) \
                    and len(json[x]) > 0 \
                    and 'com.atlassian.greenhopper.service.sprint.Sprint' in json[x][0]:
                found_sprint = True
                sprint_obj = type("sprint", (), {})
                sprint_field = json[x][0].split('[')[1].split(']')[0].split(',')
                for s in sprint_field:
                    a = s.split("=")
                    setattr(sprint_obj, a[0], a[1])

                setattr(self, "sprint", sprint_obj)
        if found_sprint is False:
            raise InvalidUsage("No Sprint Object Found.  Is this a Kanban Project?", self.logger)


    def handle_custom(self, json, fields):
        custom_obj = lambda: None
        if fields["all"] is True:
            for key in json[fields["inside"]]:
                value = json[fields["inside"]][key]
                if "customfield_" in key:
                    if isinstance(value, list):
                        setattr(custom_obj, key, value)
                    elif isinstance(value, dict):
                        for key1, value1 in value:
                            setattr(custom_obj, key1, value1)
                    else:
                        setattr(custom_obj, key, value)

        else:
            for key, value in fields["mapping"].items():
                check = "customfield_" + key
                if check in json[fields["inside"]]:
                    name = value
                    if value is None:
                        name = key

                    if isinstance(json[fields["inside"]][check], list):
                        setattr(custom_obj, name, json[fields["inside"]][check])
                    elif isinstance(json[fields["inside"]][check], dict):
                        for key1, value1 in json[fields["inside"]][check]:
                            setattr(custom_obj, key1, value1)
                    else:
                        setattr(custom_obj, name, json[fields["inside"]][check])

        setattr(self, "custom", custom_obj)

    def handle_dict(self, json, fields={}):
        pass

    def handle_list(self, json, fields, obj_name, pure_list=False):
        ret_list = []
        for x in json:
            if pure_list is True:
                ret_list.append(x)
            elif isinstance(x, dict):
                for key, value in fields.items():
                    if key in x:
                        ret_list.append(x[key])

        setattr(self, obj_name, ret_list)

    def handle_comments(self, json, fields):
        comments = []

        for comment in json["fields"]["comment"]["comments"]:
            comment_obj = lambda: None
            for field_key, field_value in fields.items():
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
        for key, value in fields.items():
            name = key
            if value is not None:
                name = value

            v = json["fields"][key]
            if v is None:
                setattr(obj, name, v)
            else:
                date_obj = datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f%z")
                setattr(obj, name, date_obj)

    def close(self):
        del self.config
        del self.logger
