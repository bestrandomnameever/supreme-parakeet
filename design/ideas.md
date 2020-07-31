## Ideas
* Metric for quality of critique ordering (perhaps linked to position in ranked list akin to nDCG)
    * TODO needs further working out for a way to calculate the gain by eg. the support of the critique
* When presenting a limited amount of critiques, the cummulative coverage of all the critiques should cover all items
    * When using permanent pruning, already pruned items are not included in this requirement
* Can't prepare a structure for items compatability with a critique since critiques are dynamicly based on an item. It is however possible to create structures comparing properties of items based in the type of property which would immediatly answer critique support query with the critique based on the items property.
* Convert lists of items to sets of items to improve performance