def new_list():
    return {"elements": [], "size": 0}


def get_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    return my_list["elements"][pos]


def is_present(my_list, element, cmp_function):
    for position in range(my_list["size"]):
        if cmp_function(element, my_list["elements"][position]) == 0:
            return position
    return -1


def add_first(my_list, element):
    my_list["elements"].insert(0, element)
    my_list["size"] += 1
    return my_list


def add_last(my_list, element):
    my_list["elements"].append(element)
    my_list["size"] += 1
    return my_list


def size(my_list):
    return my_list["size"]


def first_element(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    return my_list["elements"][0]


def is_empty(my_list):
    return my_list["size"] == 0


def last_element(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    return my_list["elements"][my_list["size"] - 1]


def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    my_list["elements"].pop(pos)
    my_list["size"] -= 1
    return my_list


def remove_first(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    removed = my_list["elements"].pop(0)
    my_list["size"] -= 1
    return removed


def remove_last(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    removed = my_list["elements"].pop(my_list["size"] - 1)
    my_list["size"] -= 1
    return removed


def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list["size"]:
        raise IndexError("list index out of range")
    my_list["elements"].insert(pos, element)
    my_list["size"] += 1
    return my_list


def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    my_list["elements"][pos] = new_info
    return my_list


def exchange(my_list, pos_1, pos_2):
    if (pos_1 < 0 or pos_1 >= my_list["size"] or
            pos_2 < 0 or pos_2 >= my_list["size"]):
        raise IndexError("list index out of range")
    my_list["elements"][pos_1], my_list["elements"][pos_2] = (
        my_list["elements"][pos_2], my_list["elements"][pos_1]
    )
    return my_list


def sub_list(my_list, pos_i, num_elements):
    if pos_i < 0 or pos_i >= my_list["size"]:
        raise IndexError("list index out of range")
    sub = new_list()
    for element in my_list["elements"][pos_i:pos_i + num_elements]:
        add_last(sub, element)
    return sub


def default_sort_criteria(element_1, element_2):
    return element_1 < element_2


def selection_sort(my_list, sort_crit):
    for position in range(my_list["size"] - 1):
        selected_position = position
        for current_position in range(position + 1, my_list["size"]):
            if sort_crit(my_list["elements"][current_position],
                         my_list["elements"][selected_position]):
                selected_position = current_position
        exchange(my_list, position, selected_position)
    return my_list


def insertion_sort(my_list, sort_crit):
    for position in range(1, my_list["size"]):
        current_position = position
        while (current_position > 0 and
               sort_crit(my_list["elements"][current_position],
                         my_list["elements"][current_position - 1])):
            exchange(my_list, current_position, current_position - 1)
            current_position -= 1
    return my_list


def shell_sort(my_list, sort_crit):
    gap = my_list["size"] // 2
    while gap > 0:
        for position in range(gap, my_list["size"]):
            current_position = position
            while (current_position >= gap and
                   sort_crit(my_list["elements"][current_position],
                             my_list["elements"][current_position - gap])):
                exchange(my_list, current_position, current_position - gap)
                current_position -= gap
        gap //= 2
    return my_list


def merge_sort(my_list, sort_crit):
    if my_list["size"] > 1:
        mid = my_list["size"] // 2
        left_list = sub_list(my_list, 0, mid)
        right_list = sub_list(my_list, mid, my_list["size"] - mid)
        merge_sort(left_list, sort_crit)
        merge_sort(right_list, sort_crit)

        left_index = right_index = current_index = 0
        while (left_index < left_list["size"] and
               right_index < right_list["size"]):
            left_element = get_element(left_list, left_index)
            right_element = get_element(right_list, right_index)
            if sort_crit(left_element, right_element):
                change_info(my_list, current_index, left_element)
                left_index += 1
            else:
                change_info(my_list, current_index, right_element)
                right_index += 1
            current_index += 1

        while left_index < left_list["size"]:
            change_info(my_list, current_index,
                        get_element(left_list, left_index))
            left_index += 1
            current_index += 1

        while right_index < right_list["size"]:
            change_info(my_list, current_index,
                        get_element(right_list, right_index))
            right_index += 1
            current_index += 1
    return my_list


def quick_sort(my_list, sort_crit):
    quick_sort_recursive(my_list, 0, size(my_list) - 1, sort_crit)
    return my_list


def quick_sort_recursive(my_list, lo, hi, sort_crit):
    if lo < hi:
        pivot = partition(my_list, lo, hi, sort_crit)
        quick_sort_recursive(my_list, lo, pivot - 1, sort_crit)
        quick_sort_recursive(my_list, pivot + 1, hi, sort_crit)
    return my_list


def partition(my_list, lo, hi, sort_crit):
    pivot = my_list["elements"][hi]
    follower = lo
    for leader in range(lo, hi):
        if sort_crit(my_list["elements"][leader], pivot):
            exchange(my_list, follower, leader)
            follower += 1
    exchange(my_list, follower, hi)
    return follower