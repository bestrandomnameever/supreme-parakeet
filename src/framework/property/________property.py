# TODO delete if no problems pop up
# from abc import ABC

# from ..critique.unit import NotCritique, DirectionalCritique

# class PropertyInterface(ABC):
#     def __init__(self, raw_value, custom_deserialize=None):
#         self.valid_critiques = list()
#         self._init_valid_critiques()

#         if custom_deserialize:
#             self.value = custom_deserialize(raw_value)
#         else:
#             self.value = self.deserialize(raw_value)

#     def deserialize(self, raw_value):
#         return raw_value

#     def add_valid_critique(self, crit_type):
#         self.valid_critiques.insert(0,crit_type)

#     def get_valid_critiques(self):
#         """
#         Returns a list of each type of possible critique
#         """
#         # If value of property is missing (aka is None) than it can not be critiqued
#         if self.value is None:
#             return []
#         return self.valid_critiques

#     def _init_valid_critiques(self):
#         """
#         Needs to overrided in each child class that appends additional possible critiques besides those already in the superclasses
#         (always call super()._init_valid_critiques())
#         """
#         self.add_valid_critique(NotCritique)

#     def __str__(self):
#         return "{}".format(self.value)
#     def __eq__(self, other):
#         if other is self:
#             return True
#         if isinstance(other, self.__class__):
#             return self.value == other.value
#         # Allows for comparison with primitive types eg. Property.value = 3 and other = 3 ==> True
#         return self.value == other
    
#     def __hash__(self):
#         return hash((self.value))
        
#     def __add__(self, other):
#         raise NotImplementedError("Property doesnt allow this operation, use property type that does")
#     def  __sub__(self, other):
#         raise NotImplementedError("Property doesnt allow this operation, use property type that does")
#     def __lt__(self, other):
#         raise NotImplementedError("Property doesnt allow this operation, use property type that does")
#     def __gt__(self, other):
#         raise NotImplementedError("Property doesnt allow this operation, use property type that does")

# class ComparableProperty(PropertyInterface):

#     def _init_valid_critiques(self):
#         super()._init_valid_critiques()
#         self.add_valid_critique(DirectionalCritique)

#     def __lt__(self, other):
#         if isinstance(other, self.__class__):
#             return self.value < other.value
#         else:
#             return self.value < other

#     def __gt__(self, other):
#         if isinstance(other, self.__class__):
#             return self.value > other.value
#         else:
#             return self.value > other

# class MeasurableDistanceProperty(ComparableProperty):
#     def  __sub__(self, other):
#         return self.value-other.value

# class NumericalProperty(MeasurableDistanceProperty):
#     def deserialize(self, raw_value):
#         return float(raw_value)

# class CategoricalProperty(PropertyInterface):
#     def deserialize(self, raw_value):
#         return raw_value

# class BooleanProperty(PropertyInterface):
#     def deserialize(self, raw_value):
#         if raw_value:
#             return True
#         return False

# TODO need a way to handle properties that are collections like genres (or could just use seperate prop for each but that doesnt mesh with some parts like it would the named mapping) 