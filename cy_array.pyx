from cpython.long cimport PyLong_AsLong
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from cpython.float cimport PyFloat_AsDouble
from array import array


cdef struct array_descriptor:
    char* type_code
    int item_size
    object (*getitem)(DArray, size_t)
    int (*setitem)(DArray, size_t, object)


cdef object long_getitem(DArray ar, size_t index):
    return (<long *> ar.data)[index]


cdef object double_getitem(DArray ar, size_t index):
    return (<double *> ar.data)[index]


cdef int long_setitem(DArray ar, size_t index, object item):
    if not isinstance(item, int) and not isinstance(item, float):
        return -1

    cdef long value = PyLong_AsLong(item)
    if index >= 0:
        (<long *> ar.data)[index] = value
    return 0


cdef int double_setitem(DArray ar, size_t index, object item):
    if not isinstance(item, int) and not isinstance(item, float):
        return -1

    cdef double value = PyFloat_AsDouble(item)
    if index >= 0:
        (<double *> ar.data)[index] = value
    return 0


cdef array_descriptor[2] descriptors = [
    array_descriptor('i', sizeof(long), long_getitem, long_setitem),
    array_descriptor('d', sizeof(double), double_getitem, double_setitem),
]


cdef enum TypeCode:
    LONG = 0
    DOUBLE = 1

cdef int type_code_to_type(str type_code):
    if type_code == 'i':
        return TypeCode.LONG
    elif type_code == 'd':
        return TypeCode.DOUBLE
    return -1

cdef class DArray:
    cdef readonly size_t used
    cdef size_t size
    cdef char *data
    cdef int iteration
    cdef array_descriptor* dsc

    def __cinit__(self, str type_code, object initial, size_t length):
            self.used = 0
            self.iteration = 0
            if length > 0:
                self.size = length
            else:
                self.size = 4 # default length
            self.dsc = &descriptors[type_code_to_type(type_code)]

            self.data = <char *> PyMem_Malloc(length * self.dsc.item_size)
            for item in initial:
                self.append(item)
            if not self.data:
                raise MemoryError()

    def __dealloc__(self):
        PyMem_Free(self.data)

    def __getitem__(self, size_t index):
        if 0 <= index < self.used:
            return self.dsc.getitem(self, index)
        raise IndexError()

    def __setitem__(self, int index, object value):
        if 0 <= index < self.used:
            self.dsc.setitem(self, index, value)
        else:
            raise IndexError()

    def expand(self):
        if self.size == self.used:
            self.data = <char *> PyMem_Realloc(
                self.data, 2 * self.size *  self.dsc.item_size
            )
            if not self.data:
                raise MemoryError()
    def optimize(self):
        if self.used and self.size / self.used >= 4:
            self.data = <char *> PyMem_Realloc(
                self.data, self.size * self.dsc.item_size / 2
            )
            self.size /= 2

    def append(self, object value):
        self.expand()
        self.dsc.setitem(self, self.used, value)
        self.used += 1

    def insert(self, size_t index, object value):
        cdef int i, idx = <int> index
        if index >= self.used:
            self.append(value)
        else:
            self.expand()
            for i in range(self.used - 1, idx - 1, -1):
                self.dsc.setitem(
                    self, i + 1, self.dsc.getitem(self, i)
                )
            self.dsc.setitem(self, index, value)
            self.used += 1

    def remove(self, object item):
        cdef int i, j
        for i in range(self.used):
            if item == self.dsc.getitem(self, i):
                for j in range(i + 1, self.used):
                    self.dsc.setitem(
                        self, j - 1, self.dsc.getitem(self, j)
                    )
                self.used -= 1
                self.optimize()
                break

    def pop(self, size_t index):
        if 0 <= index <= self.used:
            value = self.dsc.getitem(self, index)
            self.remove(value)
            if value:
                self.optimize()
            return value
        raise IndexError()

    def __iter__(self):
        self.iteration = 0
        return self

    def __next__(self):
        if self.iteration < self.used:
            self.iteration += 1
            return self.dsc.getitem(self, self.iteration - 1)
        else:
            raise StopIteration

    def __len__(self):
        return self.used

    def __sizeof__(self):
        return self.dsc.item_size * self.used

    def __eq__(self, other):
        cdef int i
        if isinstance(other, (DArray, list, array)) and \
            len(other) == len(self):
            for i in range(self.used):
                if self[i] != other[i]:
                    return False
            return True
        return False
