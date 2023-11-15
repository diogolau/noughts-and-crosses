def strdiff(str_a, str_b):
    if (len(str_a) != len(str_b)):
        return -1
    print(str_a, str_b)
    diff = []
    for i in range(len(str_a)):
        if (str_a[i] != str_b[i]):
            diff.append(i)
    return diff