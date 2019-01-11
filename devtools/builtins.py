import builtins
from collections import UserList, UserDict


class List(UserList):
    def partition(self, size):
        """
        Returns a new list with elements
        of which is a list of certain size.

            >>> partition([1, 2, 3, 4], 3)
            [[1, 2, 3], [4]]
        """
        return [self[i:i+size] for i in range(0, len(self), size)]

    def split(self, sep=None, maxsplit=-1):
        """
        Split a list by sep

            >>> split([1, None, None, 2, 3, None, 4])
            [[1], [], [2, 3], [4]]
        """
        res = []
        tmplist = []
        for elem in self:
            if elem == sep and maxsplit != 0:
                res.append(tmplist)
                tmplist = []
                maxsplit -= 1
            else:
                tmplist.append(elem)
        else:
            res.append(tmplist)
        return res


class Dict(UserDict):
    def inverse(self):
        """
        Returns a new dictionary with keys and values swapped.

            >>> inverse({1: 2, 3: 4})
            {2: 1, 4: 3}
        """
        return {value: key for key, value in self.items()}

    def find(dictionary, element):
        """
        Returns a key whose value in `dictionary` is `element`
        or, if none exists, None.

            >>> d = {1:2, 3:4}
            >>> find(d, 4)
            3
            >>> find(d, 5)
        """
        for key, value in dictionary.items():
            if element is value:
                return key


builtins.list = List
builtins.dict = Dict


if __name__ == '__main__':
    print(list)
    print(list(['a', 'b', 'c']).partition(2))
    print([].__class__)
    print(dict({1: 2, 3: 4}).inverse())
    print(dict({1: 2, 3: 4}).find(4))
