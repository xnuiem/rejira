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
