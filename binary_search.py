"""Binary Search"""


def in_search(array: object, item: object) -> int:
    """
    Index searching
    :param array: array
    :param item: element
    :return: element index
    """
    start = 0
    mid = 0
    end = len(array) - 1
    while start <= end:
        mid = (start + end) // 2
        mid_value = array[mid]
        if item == mid_value:
            return mid

        if mid_value < item:
            start = mid + 1
        elif mid_value > item:
            end = mid - 1
        else:
            return mid
    return None


def search(array: object, item: object) -> int:
    """
    Index searching, checking first match
    :param array: array
    :param item: element
    :return: element index
    """
    index = in_search(array, item)

    if index and index > 0:
        if array[index - 1] == array[index]:
            index -= 1
    return index
