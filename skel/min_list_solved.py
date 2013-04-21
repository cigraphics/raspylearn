
def min_list(li):
    m = 255

    for elem in li:
        if elem < m:
            m = elem

    return m
