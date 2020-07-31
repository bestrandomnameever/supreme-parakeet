from abc import ABC

from .comparable_property import ComparableProperty

# TODO maybe add abc meta
class MeasurableDistanceProperty(ComparableProperty):
    def  __sub__(self, other):
        return self.value-other.value