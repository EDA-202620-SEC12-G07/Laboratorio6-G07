import random

from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements, load_factor, prime=109345121):
    capacity = mf.next_prime(int(num_elements / load_factor))
    return {
        "prime": prime,
        "capacity": capacity,
        "scale": random.randint(1, prime - 1),
        "shift": random.randint(0, prime - 1),
        "table": [None] * capacity,
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0,
    }


def put(my_map, key, value):
    hash_value = mf.hash_value(my_map, key)
    occupied, position = find_slot(my_map, key, hash_value)

    if occupied:
        me.set_value(my_map["table"][position], value)
    else:
        my_map["table"][position] = me.new_map_entry(key, value)
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

        if my_map["current_factor"] > my_map["limit_factor"]:
            rehash(my_map)

    return my_map


def contains(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    occupied, _ = find_slot(my_map, key, hash_value)
    return occupied


def get(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    occupied, position = find_slot(my_map, key, hash_value)
    if occupied:
        return me.get_value(my_map["table"][position])
    return None


def remove(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    occupied, position = find_slot(my_map, key, hash_value)
    if occupied:
        me.set_key(my_map["table"][position], None)
        me.set_value(my_map["table"][position], None)
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    return my_map


def size(my_map):
    return my_map["size"]


def find_slot(my_map, key, hash_value):
    first_available = -1
    position = hash_value

    for _ in range(my_map["capacity"]):
        entry = my_map["table"][position]
        if entry is None:
            if first_available == -1:
                first_available = position
            break
        if me.get_key(entry) is None:
            if first_available == -1:
                first_available = position
        elif mf.default_compare(me.get_key(entry), key) == 0:
            return True, position
        position = (position + 1) % my_map["capacity"]

    return False, first_available


def is_available(table, position):
    return table[position] is None or me.get_key(table[position]) is None


def rehash(my_map):
    old_table = my_map["table"]
    new_capacity = mf.next_prime(my_map["capacity"] * 2)
    my_map["capacity"] = new_capacity
    my_map["table"] = [None] * new_capacity
    my_map["size"] = 0
    my_map["current_factor"] = 0

    for entry in old_table:
        if entry is not None and me.get_key(entry) is not None:
            put(my_map, me.get_key(entry), me.get_value(entry))

    return my_map