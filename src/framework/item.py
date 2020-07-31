import logging as log
# from pandas import Series

from .parser import pandas_parser
# from .property.base import PropertyInterface

class Item:
    def __init__(self, id, properties_dict):
        self.id = id
        self.properties = properties_dict

    def get_prop(self, prop_name):
        return self.properties[prop_name]

    def iter_props(self):
        return self.properties.items()

    def __str__(self):
        return "<id:{}, properties:{}>".format(self.id, {k: str(v) for k,v in self.properties.items()})

    def __hash__(self):
        return hash(id)

    def __eq__(self, other):
        # Simple check if it references same object in memory
        if other is self:
            return True

        if isinstance(other, self.__class__):
            # Check if same amount of props and if they all match
            if self.id == other.id:
                if len(self.properties) == len(other.properties) and len(list(1 for k,v in self.properties.items() if self.properties[k] == other.properties[k])) == len(self.properties):
                    return True
                else:
                    log.warn("duplicate ids: 2 items were compared with the same id but different properties")
                    log.debug("duplicate ids for items: {} {}".format(str(self), str(other)))
        return False

    def __getitem__(self, arg):
        return self.get_prop(arg)

    # TODO linkedto other TODO, may allow later for 'compatible' properties ie. common property superclass
    @classmethod
    def calc_items_prop_difference(cls, item1, item2, include_type_dif = True):
        """
        Given 2 items, returns which props of each item do not occur in the other

        Parameters:
            include_type_dif(bool): Add properties that do occur in both by name but are of different type
        """
        item1_prop_names = set(item1.properties.keys())
        item2_prop_names = set(item1.properties.keys())
        
        dif = item1_prop_names.symmetric_difference(item2_prop_names)
        if include_type_dif:
            for prop_name in item1_prop_names.intersection(item2_prop_names):
                # Check if they are of the same type
                if type(item1[prop_name]) is type(item2[prop_name]):
                    dif.add(prop_name)
        return dif

    def as_series(self):
        return pandas_parser.item_as_series(self)

    @classmethod
    def item_collection_as_dataframe(cls, items):
        return pandas_parser.items_as_dataframe(items)


def create_item_from_raw_values(id, raw_properties_dict, raw_to_prop_type_map={}, custom_deserialize_map={}, *, missing_raw_as_none=True):
    """
    Given a dictionary of raw property values, create an item with the given id and properties mapped from the raw values according to the supplied mapping

    Parameters:
        id: Id of the item, needs to be unique among all items
        raw_properties_dict: dict mapping property names to their raw values.
        raw_to_prop_type_map: dict mapping property names (same as raw_properties_dict) to the correct property type they need to be mapped to. Only raw properties that have been supplied a mapping will be added as properties to the item

        missing_raw_as_none: if true and a mapping was provided but no raw value, still add property but with None value. If false, throw error
        custom_deserialize_map: dict mapping property name to custom deserialization for property mapping
    Returns:
        Item: Item that has id an properties of the supplied types
    """
    # Select which raw values have been supplied a mapping 
    item_props_dict = dict()
    for prop_name in raw_to_prop_type_map:
        
        if prop_name in raw_properties_dict:
            raw_val = raw_properties_dict[prop_name]
        elif missing_raw_as_none:
            raw_val = None
        else:
            raise Exception("No '{}' property present and missing_raw_as_none is set as False so no property needs to be present".format(prop_name))
        
        prop_type = raw_to_prop_type_map[prop_name]
        custom_des = custom_deserialize_map[prop_name] if prop_name in custom_deserialize_map else None

        item_props_dict[prop_name] = prop_type(raw_val, custom_des)
        # if raw_val:
        #     item_props_dict[prop_name] = prop_type(raw_val, custom_des)
        # else:
        #     item_props_dict[prop_name] = None
    
    return Item(id, item_props_dict)
