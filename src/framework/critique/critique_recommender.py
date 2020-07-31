from random import shuffle

def recommend_critiques(item_critiques, items_without_anchor):
    # TODO TEMP use ordering logic later
    crits = item_critiques.copy()
    shuffle(crits)
    return crits

def get_support_for_critique(critique, items):
    return len(get_passing_items_for_critique(critique, items)) / len(items)

def get_passing_items_for_critiques(critiques, items):
    """
    Returns a dictionary with for each critique the list of items that pass the critique
    """
    return {critique: get_passing_items_for_critique(critique, items) for critique in critiques}

def get_passing_items_for_critique(critique, items):
    """
    Get all items that pass the critique
    """
    # return [item for item in items if critique.passes_critique(item)]
    return set(item for item in items if critique.passes_critique(item))

# def calc_anchor_crits_support_structure(item, items_without_anchor):
#     """
#     Calculate which items support each valid critique
#     """
#     supporting = dict()
#     for prop_name in anchor_prop_crits_dict:
#         supporting[prop_name] = dict()
#         for crit in anchor_prop_crits_dict[prop_name]:
#             supporting[prop_name][crit] = _calc_supporting_items(crit, prop_name, items_without_anchor)
#     return supporting
     