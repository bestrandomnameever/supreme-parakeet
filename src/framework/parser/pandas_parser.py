import numpy as np
import pandas as pd
from ..item import Item, create_item_from_raw_values

def parse_dataframe_as_items(dataframe, property_maps, id_col=None, *, custom_deserialize_map={}):
    """
    Parse a pandas Dataframe into a collection of items
    
    Parameters:
        dataframe(Dataframe): A pandas Dataframe
        property_maps(dict|list): Either a dict or list  mapping the column values to their appropriate Property-type. A dict maps a column-name key to a property type value. A list maps a property type to the column with the same index (missing maps by excluding them in the dict or padding the list with Nones for columns will ignore those columns)
        id_col(string): Set which column column will be used as values for the items ids
    
    Returns:
        list of items parsed from the dataframe 
    """

    if id_col:
        if id_col in dataframe.columns:
            dataframe = dataframe.set_index(id_col)
        else:
            raise Exception("No {} column in dataframe to be used as item id values".format(id_col))
    
    if type(property_maps) is list:
        temp = {}
        for i in range(len(property_maps)):
            prop_type = property_maps[i]
            if prop_type:
                temp[dataframe.columns[i]] = prop_type
        property_maps = temp
    elif type(property_maps) is not dict:
        raise Exception("Not a valid property map")

    items = []
    for id, unparsed_props_series in dataframe.iterrows():
        # item = Item(id, unparsed_props_series.to_dict(), property_maps)
        # item = create_item_from_raw_values(id, unparsed_props_series.to_dict(), property_maps, custom_deserialize_map)
        item = parse_series_as_item(unparsed_props_series, property_maps, id, custom_deserialize_map=custom_deserialize_map)
        items.append(item)
    return items

def parse_series_as_item(series, property_maps, id=None, *, id_col=None, custom_deserialize_map={}):
    if id is None:
        if id_col is not None:
            id = series.pop(id_col)
        else:
            id = series.name

    # Convert NaN's to None to make item logic agnostic from pandas
    series_dict = series.to_dict()
    for k, v in series_dict.items():
        if v is np.nan:
            series_dict[k] = None

    return create_item_from_raw_values(id, series_dict, property_maps, custom_deserialize_map)

def item_as_series(item):
    prop_names = list()
    props = list()
    for prop_name, prop in item.iter_props():
        prop_names.append(prop_name)
        props.append(str(prop))
    return pd.Series(props, prop_names, name=item.id)

def items_as_dataframe(items):
    series_reprs = list(item_as_series(item) for item in items)
    return pd.concat(series_reprs, axis=1).transpose()