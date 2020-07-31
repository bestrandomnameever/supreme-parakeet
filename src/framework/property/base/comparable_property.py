from abc import ABC
from ...critique.unit import DirectionalCritique

from .property_interface import PropertyInterface
# TODO maybe add abc meta

class ComparableProperty(PropertyInterface):

    def _init_valid_critiques(self):
        super()._init_valid_critiques()
        self.add_valid_critique(DirectionalCritique)

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.value < other.value
        else:
            return self.value < other

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.value > other.value
        else:
            return self.value > other