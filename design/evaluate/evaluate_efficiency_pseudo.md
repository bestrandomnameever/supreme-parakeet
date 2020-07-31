## Evaluate flow

A critiquing recommender is evaluated by **how many user-systems interactions** are needed before the desired/statisfactory item is reached (Efficiency of Task Support).

### Pseudocode
For each **item** in **test-dataset**
* Take an other item as starting point (anchor)
    * Random item
    * Select (random) properties of target item to create constraint. Search for items matching constraint and select a result (*recommended*)
* Get all possible critiques for each property of the **anchor** item
    * (compound and dynamic critiques interacting with multiple properties are also generated)
* Use method to "rank" the quality of the critiques
* Filter the critiques to those that satisfy the target item (aka what a user would select while searching for the target item)
    * TODO later incorperate user error (user sometimes selects a critique that doesnt match target item (find paper which mentions technique))
* Select a critique
    * First (simple)
    * Select random from top N
    * Probability based on distance from top of list
* Return items matching the selected critique
* From these items, recommend a top K
    * Traditional recommendation approach can be used here
* From the recommended items and current anchor, select the new anchor as
    * Pick at random (pure random, probability based distance top of list, ...)(TODO might make more complex)
* The new anchor matches the target?
    * YES ==> Stop
    * NO ==> Start again from generating valid critiques for each property of new anchor

