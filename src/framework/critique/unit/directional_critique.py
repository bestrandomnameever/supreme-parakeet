from enum import Enum

from .critique_interface import CritiqueInterface
# from ..item import Item

# from ..helper.docstring_inherit import doc_inherit

class DirectionalCritiqueDirections(Enum):
    SMALLER = 0
    GREATER = 1

class DirectionalCritique(CritiqueInterface):
    # def __init__(self, prop_name, critiqued_prop, direction: DirectionalCritiqueDirections):
    #     # TODO way to integrate a "minimum" distance
    #     super().__init__(prop_name, critiqued_prop)
    #     self.direction = direction

    # def passes_critique(self, item: 'Item'):
    #     if self.direction == DirectionalCritiqueDirections.SMALLER:
    #         return item[self.prop_name] < self.critiqued_prop
    #     elif self.direction == DirectionalCritiqueDirections.GREATER:
    #         return item[self.prop_name] > self.critiqued_prop
    #     return False

    # def get_description_parameters():
    #     return [
    #         {
    #             "name": "direction",
    #             "type": DirectionalCritiqueDirections
    #         }
    #     ]
    
    # def __str__(self):
    #     return "<DirectionalCritique> {} (for {} at {})".format(self.direction, self.prop_name, self.critiqued_prop)
    def __init__(self, critiqued_prop, direction: DirectionalCritiqueDirections):
        # TODO way to integrate a "minimum" distance
        super().__init__(critiqued_prop)
        self.direction = direction

    def passes_critique(self, property):
        if self.direction == DirectionalCritiqueDirections.SMALLER:
            return property < self.critiqued_prop
        elif self.direction == DirectionalCritiqueDirections.GREATER:
            return property > self.critiqued_prop
        return False

    @classmethod
    def get_description_parameters(cls):
        return [
            {
                "name": "direction",
                "type": DirectionalCritiqueDirections
            }
        ]
    
    def __str__(self):
        return "<DirectionalCritique> {} (for {})".format(self.direction, self.critiqued_prop)