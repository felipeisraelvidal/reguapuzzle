def insert_substr(source_str, insert_str, pos):
    return source_str[:pos] + insert_str + source_str[pos:]

def replacer(variable, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(variable)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + variable
    if index > len(variable):  # add it to the end
        return variable + newstring

    # insert the new string between "slices" of the original
    return variable[:index] + newstring + variable[index + 1:]

find = lambda fun, lst: next((x for x in lst if fun(x)), None)