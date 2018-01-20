class CustomAssertions:

    @staticmethod
    def assertAttrExists(obj, attr):
        if hasattr(obj, attr):
            pass
        else:
            raise AssertionError("Object does not have attribute " + attr)

    @staticmethod
    def assertAttrNotExists(obj, attr):
        if hasattr(obj, attr):
            raise AssertionError("Object has attribute " + attr)

    @staticmethod
    def assertIsList(data):
        if isinstance(data, list):
            pass
        else:
            raise AssertionError("Not a List")

    @staticmethod
    def assertIsInList(needle, haystack):
        if needle in haystack:
            pass
        else:
            raise AssertionError(needle + " not in list " + str(haystack))

    @staticmethod
    def assertIsObject(obj):
        if isinstance(obj, type):
            pass
        else:
            raise AssertionError(str(obj) + " is not an object")
