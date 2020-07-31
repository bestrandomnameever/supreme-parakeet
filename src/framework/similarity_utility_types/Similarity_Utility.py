# from abc import ABC, abstractmethod
from ..item import Item
from ..property.property import NumericalProperty
from ..similarity.similarity import DistanceSimilarity,EqualitySimilarity

# ATM uses lineair sum of property similarities (not really sure if there is a use-case for a more complex total similarity calc)
def calc_items_similarity(item1, item2, weights=None, override_sim_funcs={}):
    """
    Parameters:
        weights(list(int)): weights of each properties similarity in total similarity sum (default is equal weights)
        override_sim_funcs(dict(string, Similarity)): Dictionary mapping overriding the used similarity method property identified by the key instead of the default method
    """
    # Check if items are of same structure
    # TODO atm only support items that have identical structure (item with missing props will be denied)
    if len(Item.calc_items_prop_difference(item1, item2)) > 0:
        # Set equal weights if weights were not provided
        weights = weights if weights else {prop_name: 1 for prop_name, _ in item1.iter_props()}

        sim_sum = 0
        for prop_name, _ in item1.iter_props():
            custom_sim_calc = override_sim_funcs[prop_name] if prop_name in override_sim_funcs else None 
            sim = calc_property_similarity(item1.get_prop(prop_name), item2.get_prop(prop_name), custom_sim_calc=custom_sim_calc)
            sim_sum += sim * weights[prop_name]
        return sim_sum
    else:
        # Maybe too agrresive
        raise Exception("2 provided items are of different structure")


def calc_property_similarity(prop1, prop2, *, custom_sim_calc=None): # Add default_prop_sim override?
    # At the moment only support similarity calc between 2 properties of identical type (duplicate operation in calc_items_similarity)
    if type(prop1) is type(prop2):
        if custom_sim_calc:
            sim_func = custom_sim_calc
        else:
            sim_func = __get_default_sim_calc_for_prop(prop1).get_similarity
        
        return sim_func(prop1, prop2)
    else:
        raise Exception("Different property types")
    
def __get_default_sim_calc_for_prop(prop):
    mapping = {
        NumericalProperty: DistanceSimilarity
    }

    for prop_type in mapping:
        if (issubclass(type(prop), prop_type)):
            return mapping[prop_type]
            # Default return equality similarity
    return EqualitySimilarity



def equalityAttrSim(val1, val2):
    return 1 if val1 == val2 else 0