def partition(ls, size):
    """
    Returns a new list with elements
    of which is a list of certain size.

        >>> partition([1, 2, 3, 4], 3)
        [[1, 2, 3], [4]]
    """
    return [ls[i:i+size] for i in range(0, len(ls), size)]


if __name__ == '__main__':
    ls = [1, 2, 3, 4, 5]
    foo = partition(ls, 2)
    assert foo == [[1, 2], [3, 4], [5]]
