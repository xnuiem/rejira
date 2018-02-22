# this dictionary represents what the resulting issue objects look like.
field_map = {
    "key": None, # Nothing changes.  The key field is placed into issue.key  this is the default behaviour
    "self": None,
    "id": None,
    "summary": None,
    "description": None,
    "resolution": None,
    "sprint": True,
    "assignee": { # this creates a sub-object.  issue.assignee
        "fields": { # this tells it, that in the assignee json, which has lots of fields, to only use these fields
            "emailAddress": "email", # this changes the name of the field to "email".  If this were None, it would come
            # back as assignee.emailAddress, but like this, it will come back assignee.email
            "displayName": None,
            "name": None
        }
    },
    "creator": {
        "fields": {
            "emailAddress": "email", # issue.creator.email
            "displayName": None,     # issue.creator.displayName
            "name": None             # issue.creator.name
        }
    },
    "reporter": {
        "fields": {
            "emailAddress": "email",
            "displayName": None,
            "name": None
        }
    },
    "status": {
        "fields": { # again this is to ignore all fields in the response not listed here.  Since there is only a single
            # field listed, the response is a little different.  It will come back as issue.status instead of
            # issue.status.name .  If there were more than one field, it would come back as the sub objects, but in
            # this case, with only a single field listed in "fields", it just maps the value up to the parent.
            "name": None # this would be issue.status so print(issue.status) = "Pending" (NOT issue.status.name)
        }
    },
    "project": {
        "fields": {
            "key": None, # issue.project.key
            "name": None
        }
    },
    "issuetype": {
        "fields": {
            "name": None #issue.issuetype
        }
    },
    "priority": {
        "fields": {
            "name": None #issue.priority
        }
    },
    "votes": {
        "fields": {
            "votes": None
        }
    },
    "dates": { #creates an object of date objects.  These are python date objects so things like
        # issue.dates.created.hour work
        "created": None,  # issue.dates.created
        "lastViewed": "viewed",
        "resolutiondate": "resolved",
        "updated": None,
        "duedate": "due"
    },
    "labels": None, # since this value in the response is a list, it will come back as a list
    # issue.labels = ['support','sales','customers']
    "components": {
        "fields": {
            "name": None
        }
    },
    "fixVersions": { # a list, because that is the type of field we get back from JIRA
        "fields": {
            "name": None
        }
    },
    "custom": { # this one is a bit interesting
        "fields": {
            "10008": "epic", # renames customfield_10008 to epic.  issue.custom.epic
            "10025": "checkbox"
        },
        "all": True # return all custom fields, regardless if they are listed in "fields".  they will return as
        # customfield_<ID>.  So, issue.custom.10001 = 'Pending'
    },
    "comments": { # comments is a list of objects with more objects in it
        "fields": {
            "body": None, #issue.comments[0].body
            "created": "date", #issue.comments[0].date (if this were None, it would be issue.comments[0].created
            "author": { #the author sub object.  issue.comments[0].author
                "fields": {
                    "displayName": None, #issue.comments[0].author.displayName
                    "emailAddress": "email", #issue.comments[0].author.email
                    "name": None
                }
            }
        }
    },
    "attachments": {
        "fields": {
            "content": None,
            "author": {
                "fields": {
                    "displayName": None,
                    "emailAddress": "email",
                    "name": None
                }
            }
        }
    },
    "subtasks": {
        "fields": {
            "key": None,
            "priority": "name",
            "status": {
                "name": None,
                "self": None
            },
            "summary": None
        }
    }
}
