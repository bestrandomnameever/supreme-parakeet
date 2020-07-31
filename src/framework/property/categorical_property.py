from .base.property_interface import PropertyInterface

class CategoricalProperty(PropertyInterface):
    def deserialize(self, raw_value):
        return raw_value