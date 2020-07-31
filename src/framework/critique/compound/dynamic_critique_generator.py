from .. import CompoundPropCritique as CompCrit
from ..critique_recommender import get_passing_items_for_critique, get_passing_items_for_critiques

def map_item_as_set_of_passing_critiques(prop_critiques, item):
    """
    Given a set of prop critiques, maps each item to a collection of which of those critiques they pass
    """
    return list(prop_crit for prop_crit in prop_critiques if prop_crit.passes_critique(item))


# TODO Kan waarschijnlijk geen kwaad om eens wat testen voor te schrijven
def apriori(anchor_crits, items, support_threshold, confidence_threshold = 0, max_compound_length=None, method="passing"):
    # Convert to compound critiques (for hashing recoverability in later passes and to allow combination)
    anchor_crits_as_comp = [CompCrit([crit]) for crit in anchor_crits]
    supporting_items_for_current_pass = {crit: passing_items for crit, passing_items in get_passing_items_for_critiques(anchor_crits_as_comp, items).items()}
    current_pass_support = {crit: len(passing_items)/len(items) for crit, passing_items in supporting_items_for_current_pass.items()}    

    # Filter by support only  
    current_pass = set(crit for crit, support in current_pass_support.items() if support >= support_threshold)
    
    # Start iterative loop
    current_pass_comp_length = 1
    dynamic_comp_crits = list()
    last_pass = list(current_pass)
    supporting_items_for_last_pass = supporting_items_for_current_pass
    last_pass_support = current_pass_support
    max_length_reached = True if max_compound_length == 1 else False
    # While last_pass created at least two critiques so that one larger one could be created
    while(len(last_pass) >= 2 and not max_length_reached):
        current_pass_comp_length += 1
        current_pass = set()
        supporting_items_for_current_pass = dict()
        current_pass_support = dict()
        
        # Go over all combinations of critiques in the last pass (order of crits doesnt matter)      
        for i, crit_a in enumerate(last_pass):
            for crit_b in last_pass[:i]:
                # Check if the required amount of common critiques are present in the compound critiques, which is length of critiques in previous previous pass - 1 
                if len(CompCrit.get_common_prop_critiques_of_compounds(crit_a, crit_b)) == current_pass_comp_length - 2:
                    # Make sure that to be combined critiques (not common) don't cover the same property 
                    # TODO voelt correct maar niet zeker van
                    uncommon_crits = CompCrit.get_prop_critiques_sym_difference_of_compounds(crit_a, crit_b)
                    if not _have_overlapping_props_for_crits(uncommon_crits):
                        # Create new compound critique of size k+1 from 2 critiques of size k with k - 1 common prop critiques                       
                        new_comp_crit = CompCrit.combine_compound_crits(crit_a, crit_b)
                        # Check if a permutation of this critique has already been added                        
                        if new_comp_crit not in current_pass:
                            # Find supporting items for both critiques of the previous pass
                            common_supporting_items = _get_common_supporting_items(supporting_items_for_last_pass[crit_a], crit_a, supporting_items_for_last_pass[crit_b], crit_b, method=method)
                            supporting_items_for_current_pass[new_comp_crit] = common_supporting_items
                            # Calculate support new compound critique
                            support = len(common_supporting_items) / len(items)
                            current_pass_support[new_comp_crit] = support
                            # Calculate confidence with support and supports of parts
                            confidence = support / (last_pass_support[crit_a] * last_pass_support[crit_b])
                            
                            # Filter based on support and confidence
                            # TODO confidence/lift toevoegen
                            if support >= support_threshold:
                                current_pass.add(new_comp_crit)


        # Add all satisfactory new compound critiques of the pass to the total list of all passes
        dynamic_comp_crits = dynamic_comp_crits + list(current_pass)
        # Make data of current pass available for next pass        
        last_pass = list(current_pass)
        supporting_items_for_last_pass = supporting_items_for_current_pass
        last_pass_support = current_pass_support
        
        # Check if max compound length has been set, and if so, if it has been reached
        if max_compound_length and current_pass_comp_length == max_compound_length:
            max_length_reached = True
    return dynamic_comp_crits

def _have_overlapping_props_for_crits(crits):
    return len(set(crit.prop_name for crit in crits)) < len(crits)

def _get_common_supporting_items(supp_items_crit_1, crit_1, supp_items_crit_2, crit_2, method="intersection"):
    if method == "intersection":
        return supp_items_crit_1.intersection(supp_items_crit_2)
    elif method  == "in":
        shortest, longest = (supp_items_crit_1, supp_items_crit_2) if len(supp_items_crit_1) < len(supp_items_crit_2) else (supp_items_crit_1, supp_items_crit_2)
        return set(supp_item for supp_item in shortest if supp_item in longest)
    elif method == "passing":
        crit_for_shortest, shortest = (crit_1, supp_items_crit_1) if len(supp_items_crit_1) < len(supp_items_crit_2) else (crit_2, supp_items_crit_2)
        other_crit  = crit_1 if crit_for_shortest is crit_2 else crit_2
        new_unit_crit = CompCrit.get_prop_critiques_difference_of_compounds(other_crit, crit_for_shortest)
        if len(new_unit_crit) != 1:
            raise Exception("Should only have a difference of one")
        new_unit_crit_as_comp = CompCrit(new_unit_crit)
        return set(item for item in shortest if new_unit_crit_as_comp.passes_critique(item))
    else:
        raise Exception("Invalid option")

def generate_dynamic_critiques(unit_critiques_by_prop,items):
    # Map each item to the critiques from unit_critiques_by_prop for which its properties are valid in passing the critiques
    items_as_critiques = list(map_item_as_set_of_passing_critiques(unit_critiques_by_prop, item) for item in items if item)

    return items_as_critiques