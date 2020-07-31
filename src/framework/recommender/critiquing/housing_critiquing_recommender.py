# Example implementation of a critiquing recommender

import random as rng

from .critiquing_recommender_interface import CritiquingRecommenderInterface

from ...critique.critique_recommender import get_support_for_critique
from ...critique.unit_critique_generator import generate_valid_critiques
from ...critique.compound.dynamic_critique_generator import apriori

class ImplementedCritiquingRecommender(CritiquingRecommenderInterface):
    def __init__(self, items, method="passing"):
        super().__init__(items)
        self.method = method

    def recommend_items(self):
        # TEMP return random items
        return rng.sample(self.items, k=20) if len(self.items) > 20 else list(self.items)

    def get_critiques_for_anchor(self):
        unit_crits = generate_valid_critiques(self.get_anchor())
        apriori_compound_crits = apriori(unit_crits, self.items, 0.2, method=self.method)
        apriori_compound_crits = sort_by_support(apriori_compound_crits, self.items)
        return apriori_compound_crits + unit_crits

    def select_critique(self, critique):
        super().select_critique(critique)
        # Remove all items that don't match
        self.items = set(item for item in self.items if critique.passes_critique(item))
        self.critique_history.append(critique)


def sort_by_support(critiques, items):
    crit_supp_pairs = [(crit, get_support_for_critique(crit, items)) for crit in critiques]
    crit_supp_pairs = sorted(crit_supp_pairs, key=lambda x: x[1])
    return [crit for crit, supp in crit_supp_pairs]