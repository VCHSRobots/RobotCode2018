
def parentKeys(dict, parent):
    keys = []
    invdict = {val: key for key, val in dict.items()}
    keys.append(invdict[parent])
    keys.append(parent)
    while parent in dict.keys():
        parent = dict[parent]
        keys.append(parent)
    return keys
