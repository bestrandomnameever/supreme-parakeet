from abc import ABC as _ABC, abstractmethod

class CritiquingRecommenderInterface(_ABC):
    def __init__(self, items):
        self.critique_history = []
        self.items = items
        self._anchor = None
        
    def get_anchor(self):
        return self._anchor

    def set_anchor(self, new_anchor):
        """
        Set new anchor
        """
        self._anchor = new_anchor

    @abstractmethod
    def get_critiques_for_anchor(self):
        pass

    @abstractmethod
    def recommend_items(self):
        pass

    def select_critique(self, critique):
        """
        Apply a critique
        """
        # Add to history
        self.critique_history.append(critique)

    def finish(self, succes=True):
        """
        Used for logging purposes and historical data generation
        """
        