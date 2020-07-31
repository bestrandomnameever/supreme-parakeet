# from ..item import Item

class CritiqueInterface():

    def __init__(self, critiqued_prop):
        self.critiqued_prop = critiqued_prop

    def passes_critique(self, property):
        """
        Parameters:
            item(Item): 
        """
        raise NotImplementedError("Is abstract method")

    @classmethod
    def get_description_parameters(cls):
        """
        Returns(Iterable(dict(description:string))):
            Iterable with items of format
        """
        return []
    
    def __eq__(self, value):
        return self.critiqued_prop == value.critiqued_prop

    def __hash__(self):
        return hash((self.critiqued_prop))