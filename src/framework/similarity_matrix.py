import numpy as np
import pandas as pd

from pandas import DataFrame, Series

from .item import Item
from .helper.search import binary_search
from .similarity_utility_types.Similarity_Utility import calc_items_similarity, calc_property_similarity

class similarity_matrix():
    def __init__(self, ids, objects, *, dynamic=False):
        """
        Data structure to calculate and hold similarity information given the data and methods to calculate similarity between items. To reduce duplication, similarities are kept in nested structure indexed by smallest then largest id
        Any change for either the items or the sim_calculator requires a recalculation for the similarity matrix

        Parameters:
        items: Pandas Dataframe at least containing an 'id' column or set id_col_name to indentify the items
        sim_calculator: A Similarity_Utility implementation that is compatible with the provided items to calculate their similarity

        dynamic: If true, similarity calculations are only done when they initialy queried (Default=False)
        id_col_name: Alternative id column name if not 'id'
        """
        self.ids = ids
        self.objects = objects
        self.dynamic = dynamic

        # Abstracted array of similarities
        self.similarities = dict()

        if (not dynamic):
            self.__calc_all()

    def get_sim(self, id1, id2):
        """Query similarity value in matrix by id's of items"""
        major, minor = self.__get_major_and_minor_id(id1, id2)
        # Calculate first if it has not been calculated before
        if (self.dynamic and not (major in self.similarities and minor in self.similarities[major])):
            # Query the 2 items
            obj1 = self.__get_obj_with_id(id1)
            obj2 = self.__get_obj_with_id(id2)

            sim = self._calc_sim_between(obj1, obj2)
            self.__add_val_to_matrix(major, minor, sim)

        # Query from precalculated similarities
        return self.__get_val_from_matrix(major, minor)

    def get_sims_compared_to(self, id):
        """Return dict with similarity between item with item_id and every other item. Keyed with ids of other items"""
        sim_dict = dict()

        other_ids = set(self.ids)
        other_ids.remove(id)
        for other_id in other_ids:
            sim_dict[other_id] = self.get_sim(id, other_id)
        return sim_dict


    def as_dataframe(self, *, calc_unknowns=True):
        ids = self.ids
        # Neccesary because binary search is used
        ids.sort()

        inner_numpy = np.full((len(ids), len(ids)), np.nan)

        # Create a structure of dictionary of lists for each major minor pair that needs to be added to the list
        # Initialize with all already calculated similarities
        pairs = { major: self.similarities[major] for major in self.similarities }   
        # Add all missing pairs if calc_unknowns is True
        if self.dynamic and calc_unknowns:
            missing = self.__get_missing_sim_major_minors()
            for major in missing:
                pairs[major] = pairs[major] + missing[major]

        for major in self.similarities:
            for minor in self.similarities[major]:
                val = self.get_sim(major,minor)

                major_idx = binary_search(ids, major)
                minor_idx = binary_search(ids, minor)

                inner_numpy[major_idx][minor_idx] = val
                # Mirror around bisection
                inner_numpy[minor_idx][major_idx] = val
        return pd.DataFrame(data=inner_numpy, index=ids, columns=ids)

    def _calc_sim_between(self, obj1, obj2):
        raise NotImplementedError("Must be implemented in child classes")

    def __get_val_from_matrix(self, major, minor):
        if (major in self.similarities and minor in self.similarities[major]):
            return self.similarities[major][minor]
        else:
            return None

    def __add_val_to_matrix(self, major, minor, similarity_val):
        if (major not in self.similarities):
            self.similarities[major] = dict()
        self.similarities[major][minor] = similarity_val

    def __calc_all(self):
        """Used if dynamic is False in constructor"""
        # TODO maybe add multithreading
        count = len(self.ids)
        for i in range(0,count):
            ref_id = self.ids[i]
            ref_obj = self.objects[i]
            for j in range(0,i):
                comp_id = self.ids[j]
                comp_obj = self.objects[j]

                sim = self._calc_sim_between(ref_obj, comp_obj)
                major, minor = self.__get_major_and_minor_id(ref_id, comp_id)
                self.__add_val_to_matrix(major, minor, sim)
 
    def __get_missing_sim_major_minors(self):
        """Returns missing similarity "coordinates" for full matrix as a dictionary of arrays, dic keys containing the majors, the arrays containing the minors"""
        missing = dict()

        for i in range(0, len(self.ids)):
            major = self.ids[i]

            expected_minors = set(self.ids[j] for j in list(range(0, i)))
            if major not in self.similarities:
                missing_for_major = expected_minors
            else:
                currently_calculated_minors = set(self.similarities[major].keys())
                missing_for_major = expected_minors.difference(currently_calculated_minors)

            missing[major] = missing_for_major
        return missing

    def __get_major_and_minor_id(self, item_id_1, item_id_2):
        """Since matrix is abstracted behind structure that indexes by smallest, then largest id, calculate the order of access"""
        return [item_id_1, item_id_2] if item_id_1 < item_id_2 else [item_id_2, item_id_1]

# TODO find way to handle similarities if one of the properties has a None value

class item_similarity_matrix(similarity_matrix):
    def __init__(self, items, weights=None, override_sim_funcs={}, *, dynamic=False):
        self.weights = weights
        self.override_sim_funcs = override_sim_funcs
        super().__init__(list(item.id for item in items), items, dynamic=dynamic)

    def _calc_sim_between(self, item1, item2):
        return calc_items_similarity(item1, item2, self.weights, self.override_sim_funcs)

class property_similarity_matrix(similarity_matrix):
    def __init__(self, item_ids, prop_for_each_item, sim_function=None, *, dynamic=False):
        self.sim_function = sim_function
        super().__init__(item_ids, prop_for_each_item, dynamic=dynamic)
    
    def _calc_sim_between(self, prop1, prop2):
        return calc_property_similarity(prop1, prop2, custom_sim_calc=self.sim_function)