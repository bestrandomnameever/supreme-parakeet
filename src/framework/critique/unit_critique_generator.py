from itertools import product
from . import PropCritique

def generate_valid_critiques(item):
    """
    Returns a list of every possible automatically generated propertycritique for an item given its properties
    
    Parameters:
        item(Item): reference item to get all property types from
    """
    crits = list()
    for prop_name, prop in item.iter_props():
        for crit in get_critiques_for_prop(prop):
            crits.append(PropCritique(prop_name, crit))
    return crits

def get_critiques_for_prop(prop):
    critiques = []
    for crit_type in prop.get_valid_critiques():
        # If the critique has parameters
        crit_params_desc = crit_type.get_description_parameters()
        if crit_params_desc:
            permuts_crit_params = _create_parameter_args_permutations(crit_params_desc)
            for permu in permuts_crit_params:
                critiques.append(crit_type(prop, **permu))
        else:
            critiques.append(crit_type(prop))
    return critiques

def _create_parameter_args_permutations(parameters_description):
    # Each parameter type should be an enum
    param_count = len(parameters_description)
    param_names = list(entry["name"] for entry in parameters_description)
    param_enum_options = list(entry["type"] for entry in parameters_description)

    # Make cartesian product
    cartesian = product(*param_enum_options)

    return list({param_names[j]: permutation[j] for j in range(param_count)} for permutation in cartesian)
