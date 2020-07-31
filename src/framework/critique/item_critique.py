from abc import ABC, abstractmethod

class ItemCritiqueInterface(ABC):
    @abstractmethod
    def passes_critique(self, item):
        pass

class PropCritique(ItemCritiqueInterface):
    def __init__(self, prop_name, critique):
        self.prop_name = prop_name
        self.critique = critique

    def passes_critique(self, item):
        return self.critique.passes_critique(item[self.prop_name])

    def __str__(self):
        return "<Prop: '{}' Critique: {}>".format(self.prop_name, self.critique)
    
    def __eq__(self, other):
        if other is self:
            return True
        elif isinstance(other, self.__class__):
            return self.prop_name == other.prop_name and self.critique == other.critique
        return False
    
    def __hash__(self):
        return hash((self.prop_name, self.critique))

class CompoundPropCritique(ItemCritiqueInterface):
    def __init__(self, prop_critiques=None):
        # self.prop_critiques = prop_critiques if prop_critiques else list()
        self.prop_critiques = set(prop_critiques) if prop_critiques else set()

    @classmethod
    def create_from_critiques_by_prop_dict(cls, crits_by_prop_dict):
        cmpCrt = cls()
        for prop in crits_by_prop_dict:
            for crit in crits_by_prop_dict[prop]:
                cmpCrt.prop_critiques.append(PropCritique(prop, crit))
        return cmpCrt

    def add_critique(self, prop_name, critique):
        # self.unit_critiques.append()
        self.prop_critiques.add(critique)

    # def add_unit_critique(self, unit_critique):
    #     self.unit_critiques.append(unit_critique)

    def passes_critique(self, item):
        return all(prop_crit.passes_critique(item) for prop_crit in self.prop_critiques)

    def __str__(self):
        return "[{}]".format(",".join([str(crit) for crit in self.prop_critiques]))
    
    def __eq__(self, value):
        if len(self.prop_critiques) == len(value.prop_critiques):
            return len(set(self.prop_critiques).intersection(set(value.prop_critiques))) == len(self.prop_critiques)
        else:
            return False

    def __hash__(self):
        # return hash([crit for crit in self.prop_critiques])
        return 0

    @classmethod
    def get_common_prop_critiques_of_compounds(cls, com_crit_a, com_crit_b):
        return com_crit_a.prop_critiques.intersection(com_crit_b.prop_critiques)
    
    @classmethod
    def get_prop_critiques_difference_of_compounds(cls, com_crit_a, com_crit_b):
        return com_crit_a.prop_critiques.difference(com_crit_b.prop_critiques)

    @classmethod
    def get_prop_critiques_sym_difference_of_compounds(cls, com_crit_a, com_crit_b):
        return com_crit_a.prop_critiques.symmetric_difference(com_crit_b.prop_critiques)
    
    @classmethod
    def combine_compound_crits(cls, com_crit_a, com_crit_b):
        return CompoundPropCritique(com_crit_a.prop_critiques.union(com_crit_b.prop_critiques))