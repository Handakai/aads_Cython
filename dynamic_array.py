"""DynamicArray wrapper"""
from array import array

from cy_array import DArray


class Array:
    """DynamicArray wrapper class"""
    def __init__(self, type_code: str, initial: object) -> object:
        """
        Array class constructor
        :param type_code: array type
        :param initial: array initializer
        """
        self.type_code = type_code
        self.dar = DArray(type_code, initial)


    def __getitem__(self, index: int) -> object:
        """
        Getting element from array
        :param index: element index
        :return: value
        """
        if index < 0:
            if -index <= self.dar.used:
                index = self.dar.used + index
            else:
                raise IndexError()
        return self.dar[index]

    def __setitem__(self, index: int, value: object):
        """
        Adding element in array
        :param index: element index
        :param value: element value
        :return:
        """
        if index < 0:
            if -index <= self.dar.used:
                index = self.dar.used + index
            else:
                raise IndexError()
        self.dar[index] = value

    def append(self, value: object):
        """
        Appending element
        :param value: element
        :return:
        """
        self.dar.append(value)

    def insert(self, index: int, value: object):
        """
        Inserting element by index
        :param index: index
        :param value: element
        :return:
        """
        if index < 0:
            if -index <= self.dar.used:
                index = self.dar.used + index
            else:
                index = 0
        self.dar.insert(index, value)

    def remove(self, value: object):
        """
        Removing first occurrence of element in array
        :param value: element
        :return:
        """
        self.dar.remove(value)

    def pop(self, index: int) -> object:
        """
        Removing element from array by index and returning element
        :param index: element index
        :return: element value
        """
        if index < 0:
            if -index <= self.dar.used:
                index = self.dar.used + index
            else:
                raise IndexError()
        return self.dar.pop(index)

    def __next__(self):
        return self.dar.__next__()

    def __len__(self):
        return self.dar.__len__()

    def __sizeof__(self):
        return self.dar.__sizeof__()

    def __eq__(self, other):
        if isinstance(other, Array):
            return self.dar.__eq__(other.dar)
        if isinstance(other, (list, array)):
            return self.dar.__eq__(other)
        return False

    def __str__(self):
        return f'[{", ".join([str(e) for e in self.dar])}]'

    def __repr__(self):
        return self.__str__()
