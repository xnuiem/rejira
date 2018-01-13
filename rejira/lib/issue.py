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
        return obj

    def create_object(self, json, fields):

        for key, value in fields.items():
            field_name = key
            sub_json = json
            self.logger.debug("Key/Field Name: %s", field_name)
            self.logger.debug("JSON: %s", sub_json)
            self.logger.debug("Value: %s", value)
            if value is not None and "name" in value.keys() and value["name"] is not None:
                field_name = value["name"]
            if key not in json:
                sub_json = json["fields"]

            self.logger.debug('Field: %s', field_name)
            self.logger.debug('Map: %s', sub_json)

            if key is "dates":
                self.handle_dates(json, value)
            elif key is "comments":
                self.handle_comments(json, value)
            elif key is "sprint" and value is True:
                self.handle_sprint(json)
            elif key is "custom":
                self.handle_custom(json, value)
            elif value is not None:
                if isinstance(sub_json[key], str):
                    pass
                elif isinstance(sub_json[key], list):
                    self.handle_list(sub_json[key], value, field_name)
                elif isinstance(sub_json[key], dict):
                    obj = type(field_name, (), {})
                    if len(value["fields"]) > 1:
                        if sub_json[key] is not None:
                            self.find_sub_value(sub_json[key], value, obj)
                        else:
                            setattr(obj, key, None)

                    else:
                        for x in value["fields"]:
                            obj = sub_json[key][x]

                    setattr(self, field_name, obj)
                else:
                    setattr(self, field_name, sub_json[key])
            else:
                setattr(self, key, sub_json[key])
        self.close()
        return self

    def handle_sprint(self, json):
        self.logger.info('Handle Sprint')
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
        custom_obj = type("custom", (), {})
        self.logger.info('Handle Custom Fields')
        self.logger.debug('Fields: %s', fields)
        all_custom = False

        if "all" in fields.keys() and fields["all"] is True:
            all_custom = True

        for key in json["fields"]:
            set_custom = False
            if all_custom is True:
                set_custom = True

            value = json["fields"][key]
            if "customfield_" in key:
                id_of_custom = key[12:]
                self.logger.debug('CustomID: %s', id_of_custom)
                self.logger.debug('Custom Value: %s', value)
                field_name = key
                if id_of_custom in fields["fields"].keys():
                    set_custom = True
                    if fields["fields"][id_of_custom] is not None:
                        field_name = fields["fields"][id_of_custom]

                if set_custom is True:
                    if isinstance(value, list):
                        sub_list = []
                        for x in value:
                            if isinstance(x, dict):
                                sub_list.append(self.handle_dict(x))
                            else:
                                sub_list = value
                        setattr(custom_obj, field_name, sub_list)
                    elif isinstance(value, dict):
                        sub_custom_obj = type("custom", (), {})
                        for key1, value1 in value.items():
                            setattr(sub_custom_obj, key1, value1)
                        setattr(custom_obj, field_name, sub_custom_obj)
                    else:
                        setattr(custom_obj, field_name, value)

        setattr(self, "custom", custom_obj)

    def handle_dict(self, json):
        self.logger.info('Handle Dict: %s', json)
        obj = type("custom_dict", (), {})
        # if not in mapping, map everything you find
        for key1, value1 in json.items():
            setattr(obj, key1, value1)

        return obj

    def handle_list(self, json, fields, field_name):
        self.logger.info('Handle List: %s', field_name)

        ret_list = []

        self.logger.debug('JSON: %s, Fields: %s', json, fields)
        for x in json:
            if isinstance(x, dict):  # list of dicts
                if len(fields["fields"]) > 1:
                    sub_obj = type(field_name, (), {})
                    for y in fields["fields"]:
                        setattr(sub_obj, y, x[y])
                    ret_list.append(sub_obj)
                else:
                    for y in fields["fields"]:
                        ret_list.append(x[y])
            elif isinstance(x, list):  # list of lists
                pass
            elif isinstance(x, str):  # list of strings
                pass
        setattr(self, field_name, ret_list)

    def handle_comments(self, json, fields):
        self.logger.info('Handle Comments')
        self.logger.debug('fields: %s, json: %s', fields, json)
        comments = []

        for comment in json["fields"]["comment"]["comments"]:
            self.logger.debug('Comment: %s', comment)
            comment_obj = type("comment", (), {})
            for field_key, field_value in fields["fields"].items():
                name = field_key
                self.logger.debug("Field Key: %s", name)
                if isinstance(field_value, dict):
                    if comment[field_key] is not None:
                        sub_obj = self.find_sub_value(comment[field_key], field_value, type(name, (), {}))
                        setattr(comment_obj, name, sub_obj)
                else:
                    if field_value is not None:
                        name = field_value
                    setattr(comment_obj, name, comment[field_key])

            comments.append(comment_obj)
            del comment_obj
        setattr(self, "comments", comments)

    def handle_dates(self, json, fields):
        self.logger.info('Handle Dates')
        obj = type("dates", (), {})
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
        setattr(self, "dates", obj)

    def close(self):
        self.logger.debug('Closing')
        del self.config
        del self.logger
