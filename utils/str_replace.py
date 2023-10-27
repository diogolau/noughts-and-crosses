def replace_indexes(str, indexes, char):
    str = list(str)
    for i in indexes:
        str[i] = char
    return "".join(str)