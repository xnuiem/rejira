class CustomAssertions:
    def assertAttrExists(self, obj, attr):
        if hasattr(obj, attr):
            pass
        else:
            raise AssertionError("Object does not have attribute " + attr)

    def assertAttrNotExists(self, obj, attr):
        if hasattr(obj, attr):
            raise AssertionError("Object has attribute " + attr)
        pass