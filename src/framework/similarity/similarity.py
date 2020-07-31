# from ..property.property import NumericalProperty

class Similarity():
    def get_similarity(item1, item2):
        """
        Returns the similarity between 2 properties as a number
        """
        raise NotImplementedError("Needs to be implemented by child classes")

class EqualitySimilarity(Similarity):
    def get_similarity(item1, item2):
        return 1 if item1 == item2 else 0

class DistanceSimilarity(Similarity):
    def get_similarity(item1, item2):
        return abs(item1 - item2)

class CustomSimilarity(Similarity):
    """
    Calculates similarity between 2 properties based on custom function

    Parameters:
        custom_sim_method(def): Custom function that takes two properties as parameters and returns the similarity
    """
    def __init__(self, custom_sim_method):
        self.custom_sim_method = custom_sim_method
    
    def get_similarity(item1, item2):
        return custom_sim_method(item1, item2)
