def new_list():
    return {"first": None, "last": None, "size": 0}


def get_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    node = my_list["first"]
    for _ in range(pos):
        node = node["next"]
    return node["info"]


def is_present(my_list, element, cmp_function):
    node = my_list["first"]
    position = 0
    while node is not None:
        if cmp_function(element, node["info"]) == 0:
            return position
        node = node["next"]
        position += 1
    return -1


def add_first(my_list, element):
    node = {"info": element, "next": my_list["first"]}
    my_list["first"] = node
    if my_list["size"] == 0:
        my_list["last"] = node
    my_list["size"] += 1
    return my_list


def add_last(my_list, element):
    node = {"info": element, "next": None}
    if my_list["size"] == 0:
        my_list["first"] = node
    else:
        my_list["last"]["next"] = node
    my_list["last"] = node
    my_list["size"] += 1
    return my_list


def size(my_list):
    return my_list["size"]


def first_element(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    return my_list["first"]["info"]


def is_empty(my_list):
    return my_list["size"] == 0


def last_element(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    return my_list["last"]["info"]


def remove_first(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    removed = my_list["first"]["info"]
    my_list["first"] = my_list["first"]["next"]
    my_list["size"] -= 1
    if my_list["size"] == 0:
        my_list["last"] = None
    return removed


def remove_last(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    removed = my_list["last"]["info"]
    if my_list["size"] == 1:
        my_list["first"] = None
        my_list["last"] = None
    else:
        node = my_list["first"]
        while node["next"] is not my_list["last"]:
            node = node["next"]
        node["next"] = None
        my_list["last"] = node
    my_list["size"] -= 1
    return removed


def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list["size"]:
        raise IndexError("list index out of range")
    if pos == 0:
        return add_first(my_list, element)
    if pos == my_list["size"]:
        return add_last(my_list, element)
    previous = my_list["first"]
    for _ in range(pos - 1):
        previous = previous["next"]
    previous["next"] = {"info": element, "next": previous["next"]}
    my_list["size"] += 1
    return my_list


def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    if pos == 0:
        remove_first(my_list)
        return my_list
    previous = my_list["first"]
    for _ in range(pos - 1):
        previous = previous["next"]
    deleted = previous["next"]
    previous["next"] = deleted["next"]
    if pos == my_list["size"] - 1:
        my_list["last"] = previous
    my_list["size"] -= 1
    return my_list


def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    node = my_list["first"]
    for _ in range(pos):
        node = node["next"]
    node["info"] = new_info
    return my_list


def exchange(my_list, pos_1, pos_2):
    if (pos_1 < 0 or pos_1 >= my_list["size"] or
            pos_2 < 0 or pos_2 >= my_list["size"]):
        raise IndexError("list index out of range")
    if pos_1 == pos_2:
        return my_list
    node_1 = my_list["first"]
    node_2 = my_list["first"]
    for _ in range(pos_1):
        node_1 = node_1["next"]
    for _ in range(pos_2):
        node_2 = node_2["next"]
    node_1["info"], node_2["info"] = node_2["info"], node_1["info"]
    return my_list


def sub_list(my_list, pos, num_elements):
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    node = my_list["first"]
    for _ in range(pos):
        node = node["next"]
    sub = new_list()
    for _ in range(num_elements):
        if node is None:
            break
        add_last(sub, node["info"])
        node = node["next"]
    return sub


def default_sort_criteria(element_1, element_2):
    return element_1 < element_2


def selection_sort(my_list, sort_crit):
    current = my_list["first"]
    while current is not None:
        selected = current
        candidate = current["next"]
        while candidate is not None:
            if sort_crit(candidate["info"], selected["info"]):
                selected = candidate
            candidate = candidate["next"]
        current["info"], selected["info"] = selected["info"], current["info"]
        current = current["next"]
    return my_list


def insertion_sort(my_list, sort_crit):
    if my_list["size"] > 1:
        current = my_list["first"]["next"]
        while current is not None:
            element = current["info"]
            node = my_list["first"]
            while node is not current and not sort_crit(element, node["info"]):
                node = node["next"]
            while node is not current:
                node["info"], element = element, node["info"]
                node = node["next"]
            current["info"] = element
            current = current["next"]
    return my_list


def shell_sort(my_list, sort_crit):
    gap = my_list["size"] // 2
    while gap > 0:
        for position in range(gap, my_list["size"]):
            current_position = position
            while (current_position >= gap and sort_crit(
                    get_element(my_list, current_position),
                    get_element(my_list, current_position - gap))):
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
            left = get_element(left_list, left_index)
            right = get_element(right_list, right_index)
            if sort_crit(right, left):
                change_info(my_list, current_index, right)
                right_index += 1
            else:
                change_info(my_list, current_index, left)
                left_index += 1
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
    pivot = get_element(my_list, hi)
    follower = lo
    for leader in range(lo, hi):
        if sort_crit(get_element(my_list, leader), pivot):
            exchange(my_list, follower, leader)
            follower += 1
    exchange(my_list, follower, hi)
    return follower