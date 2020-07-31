from .base.measurable_property import MeasurableDistanceProperty

class NumericalProperty(MeasurableDistanceProperty):
    def deserialize(self, raw_value):
        return float(raw_value)