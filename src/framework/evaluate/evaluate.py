import random as rng
from ..critique.unit_critique_generator import generate_valid_critiques

from ..recommender.critiquing.critiquing_recommender_interface import CritiquingRecommenderInterface

def simple_evaluation(critiquing_recommender: CritiquingRecommenderInterface):
    # Pick random starting item to critique and a goal for the recommendations session
    random_anchor = rng.choice(critiquing_recommender.items)
    # items.remove(random_anchor)
    goal = rng.choice(critiquing_recommender.items)
    # items.remove(goal)

    print("Goal is in items: {}".format(goal in critiquing_recommender.items))

    print("Staring item: {}".format(str(random_anchor)))
    print("Goal: {}".format(str(goal)))
    print("")

    iteractions = 0

    # Initialize recommender on starting item
    critiquing_recommender.set_anchor(random_anchor)
    while critiquing_recommender.get_anchor() != goal:
        iteractions += 1
        crits = critiquing_recommender.get_critiques_for_anchor()

        # Select first of the critiques that matches the goal item
        i = 0
        while not crits[i].passes_critique(goal):
            i += 1
        print("--------------------------------------------------")
        critiquing_recommender.select_critique(crits[i])
        print("Selected critique: {}".format(crits[i]))
        print("Goal is still in items: {}".format(goal in critiquing_recommender.items))
        recommended_items = critiquing_recommender.recommend_items()

        # TEMP pick a random item
        # TODO use probabilities
        critiquing_recommender.set_anchor(rng.choice(recommended_items))
        print("New anchor: {}".format(str(critiquing_recommender.get_anchor())))
        print("--------------------------------------------------")
    print("Amount of interactions: {}".format(iteractions))