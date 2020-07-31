from .base.property_interface import PropertyInterface

class BooleanProperty(PropertyInterface):
    def deserialize(self, raw_value):
        if raw_value:
            return True
        return False