from .critique_interface import CritiqueInterface

class NotCritique(CritiqueInterface):

    def __init__(self, critiqued_prop):
        super().__init__(critiqued_prop)

    def passes_critique(self, property):
        # TODO allow system to signal whioch item could not be compared because their respective property is missing (is None) instead of just ignoring it
        if property == None:
            return False
        return property != self.critiqued_prop

    def __str__(self):
        return "<NotCritique> (for {})".format(self.critiqued_prop)