from array import array

from cy_array import DArray


class Array:
    def __init__(self, type_code: str, initial: object) -> object:
        self.type_code = type_code
        self.dar = DArray(type_code, len(initial))

        for item in initial:
            self.dar.append(item)

    def __getitem__(self, index: int) -> object:
        if index < 0:
            if -index <= self.dar.used:
                index = self.dar.used + index
            else:
                raise IndexError()
        return self.dar[index]

    def __setitem__(self, index: int, value: object):
        if index < 0:
            if index <= self.dar.used:
                index = self.dar.used + index
            else:
                raise IndexError()
        self.dar[index] = value

    def append(self, value: object):
        self.dar.append(value)

    def insert(self, index: int, value: object):
        if index < 0:
            if -index <= self.dar.used:
                index = self.dar.used + index
            else:
                index = 0
        self.dar.insert(index, value)

    def remove(self, value: object):
        self.dar.remove(value)

    def pop(self, index: int) -> object:
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
        return_string = ''
        for x in self.dar:
            return_string.join(str(x))
            return_string.join(', ')
        return return_string

    def __repr__(self):
        return self.__str__()
