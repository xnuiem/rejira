import datetime
from rejira.lib.error import InvalidUsage

from pprint import pprint


class Issue:

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    @staticmethod
    def find_sub_value(json, fields, obj):
        for key, value in fields["fields"].items():
            if value is None:
                setattr(obj, key, json[key])
            else:
                setattr(obj, value, json[key])
        return obj

    def create_raw_object(self, json):
        self.logger.debug('Raw Object Create')

        from pprint import pprint
        for key, value in json.items():
            if isinstance(value, str):
                setattr(self, key, value)
            elif isinstance(value, list):
                setattr(self, key, self.handle_raw_list(value))
            elif isinstance(value, dict):
                setattr(self, key, self.handle_raw_dict(value))

        self.close()
        return self

    def handle_raw_list(self, value):
        ret_list = []

        return ret_list

    def handle_raw_dict(self, json):

        obj = type("values", (), {})
        for key, value in json.items():
            if isinstance(value, str):
                setattr(obj, key, value)
            elif isinstance(value, list):
                setattr(obj, key, self.handle_raw_list(value))
            elif isinstance(value, dict):
                setattr(obj, key, self.handle_raw_dict(value))

        return obj




    def create_object(self, json, fields):

        for key, value in fields.items():
            field_name = key
            sub_json = json
            self.logger.debug("Key/Field Name: %s", field_name)
            self.logger.debug("JSON: %s", sub_json)
            self.logger.debug("Value: %s", value)

            if value is not None and value is not True and "name" in value.keys() and value["name"] is not None:
                field_name = value["name"]
            if key not in json:
                sub_json = json["fields"]

            self.logger.debug('Field: %s', field_name)
            self.logger.debug('Map: %s', sub_json)

            if key is "dates":
                setattr(self, "dates", self.handle_dates(json, value))
            elif key is "comments":
                setattr(self, "comments", self.handle_comments(json, value))
            elif key is "attachments":
                setattr(self, "attachments", self.handle_attachments(json, value))
            elif key is "sprint" and value is True:
                setattr(self, "sprint", self.handle_sprint(json["fields"]))
            elif key is "custom":
                setattr(self, "custom", self.handle_custom(json, value))
            elif value is not None:
                if isinstance(sub_json[key], str):
                    pass
                elif isinstance(sub_json[key], list):
                    setattr(self, field_name, self.handle_list(sub_json[key], value))
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

    def handle_attachments(self, json, fields):
        self.logger.info('Handle Attachments')
        self.logger.debug('fields: %s, json: %s', fields, json)
        attachments = []

        for attachment in json["fields"]["attachment"]:
            self.logger.debug('Attachment: %s', attachment)
            attachment_obj = type("attachment", (), {})
            for field_key, field_value in fields["fields"].items():
                name = field_key
                self.logger.debug("Field Key: %s", name)
                if isinstance(field_value, dict):
                    if attachment[field_key] is not None:
                        sub_obj = self.find_sub_value(attachment[field_key], field_value, type(name, (), {}))
                        setattr(attachment_obj, name, sub_obj)
                else:
                    if field_value is not None:
                        name = field_value
                    setattr(attachment_obj, name, attachment[field_key])

            attachments.append(attachment_obj)
            del attachment_obj
        return attachments

    def handle_sprint(self, json):
        self.logger.info('Handle Sprint')
        for x in json:

            if isinstance(json[x], list) \
                    and len(json[x]) > 0 \
                    and 'com.atlassian.greenhopper.service.sprint.Sprint' in json[x][0]:

                sprint_obj = type("sprint", (), {})
                sprint_field = json[x][0].split('[')[1].split(']')[0].split(',')
                for s in sprint_field:
                    a = s.split("=")
                    setattr(sprint_obj, a[0], a[1])

                return sprint_obj

        return None

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
                    elif isinstance(value, dict): # not sure if this ever happens
                        sub_custom_obj = type("custom", (), {})
                        for key1, value1 in value.items():
                            setattr(sub_custom_obj, key1, value1)
                        setattr(custom_obj, field_name, sub_custom_obj)
                    else:
                        setattr(custom_obj, field_name, value)

        return custom_obj

    def handle_dict(self, json):
        self.logger.info('Handle Dict: %s', json)
        obj = type("custom_dict", (), {})
        for key1, value1 in json.items():
            setattr(obj, key1, value1)
        return obj

    def handle_list(self, json, fields):
        self.logger.info('Handle List: %s', fields )

        ret_list = []

        self.logger.debug('JSON: %s, Fields: %s', json, fields)
        for x in json:
            if isinstance(x, dict):  # list of dicts
                if len(fields["fields"]) > 1:
                    sub_obj = type("list", (), {})
                    for y in fields["fields"]:
                        if y in x:
                            setattr(sub_obj, y, x[y])
                        elif y in fields["fields"]:
                            if fields["fields"][y] is None:
                                setattr(sub_obj, y, x["fields"][y])
                            elif isinstance(fields["fields"][y], dict):
                                sub_sub_obj = type("list", (), {})
                                for j in fields["fields"][y]:
                                    setattr(sub_sub_obj, j, x["fields"][y][j])
                                setattr(sub_obj, y, sub_sub_obj)
                            elif fields["fields"][y] in x["fields"][y]:
                                setattr(sub_obj, y, x["fields"][y][fields["fields"][y]])
                    ret_list.append(sub_obj)
                else:
                    for y in fields["fields"]:
                        ret_list.append(x[y])
        return ret_list

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
        return comments

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
        return obj

    def close(self):
        self.logger.debug('Closing')
        del self.config
        del self.logger

    def raise_exception(self):
        raise InvalidUsage('Error', self.logger)
