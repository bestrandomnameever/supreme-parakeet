def binary_search(list, query):
    """Given an sorted list, return index of query if found, else -1"""
    l = 0
    r = len(list) - 1
    while r >= l:
        m = l + ((r-l) // 2)
        
        if list[m] == query:
            return m
        elif list[m] > query:
            r = m - 1
        else:
            l = m + 1
    # Loop has exited without finding the query
    return -1 