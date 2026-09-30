import random
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al


def new_map(num_elements, load_factor, prime=109345121):
    """
    Crea un mapa que resuelve colisiones usando separate chaining.
    Cada posición del vector contiene una lista de entradas (key, value).
    """
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
    bucket = my_map["table"][hash_value]

    if bucket is None:
        bucket = al.new_list()

    for pos in range(al.size(bucket)):
        entry = al.get_element(bucket, pos)
        if me.get_key(entry) == key:
            me.set_value(entry, value)
            my_map["table"][hash_value] = bucket
            return my_map

    al.add_last(bucket, me.new_map_entry(key, value))
    my_map["table"][hash_value] = bucket
    my_map["size"] += 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    if my_map["current_factor"] > my_map["limit_factor"]:
        rehash(my_map)

    return my_map


def contains(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    bucket = my_map["table"][hash_value]
    if bucket is None:
        return False

    for pos in range(al.size(bucket)):
        entry = al.get_element(bucket, pos)
        if me.get_key(entry) == key:
            return True
    return False


def get(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    bucket = my_map["table"][hash_value]
    if bucket is None:
        return None

    for pos in range(al.size(bucket)):
        entry = al.get_element(bucket, pos)
        if me.get_key(entry) == key:
            return me.get_value(entry)
    return None


def remove(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    bucket = my_map["table"][hash_value]
    if bucket is None:
        return my_map

    for pos in range(al.size(bucket)):
        entry = al.get_element(bucket, pos)
        if me.get_key(entry) == key:
            al.delete_element(bucket, pos)
            my_map["size"] -= 1
            my_map["current_factor"] = my_map["size"] / my_map["capacity"]
            if al.is_empty(bucket):
                my_map["table"][hash_value] = None
            else:
                my_map["table"][hash_value] = bucket
            break

    return my_map


def size(my_map):
    return my_map["size"]


def is_empty(my_map):
    return my_map["size"] == 0


def key_set(my_map):
    keys = al.new_list()
    for bucket in my_map["table"]:
        if bucket is not None:
            for pos in range(al.size(bucket)):
                entry = al.get_element(bucket, pos)
                al.add_last(keys, me.get_key(entry))
    return keys


def value_set(my_map):
    values = al.new_list()
    for bucket in my_map["table"]:
        if bucket is not None:
            for pos in range(al.size(bucket)):
                entry = al.get_element(bucket, pos)
                al.add_last(values, me.get_value(entry))
    return values


def find_slot(my_map, key, hash_value):
    bucket = my_map["table"][hash_value]
    if bucket is None:
        return False, hash_value

    for pos in range(al.size(bucket)):
        entry = al.get_element(bucket, pos)
        if me.get_key(entry) == key:
            return True, pos
    return False, hash_value


def is_available(table, position):
    return table[position] is None


def rehash(my_map):
    old_table = my_map["table"]
    new_capacity = mf.next_prime(my_map["capacity"] * 2)
    my_map["capacity"] = new_capacity
    my_map["table"] = [None] * new_capacity
    my_map["size"] = 0
    my_map["current_factor"] = 0

    for bucket in old_table:
        if bucket is not None:
            for pos in range(al.size(bucket)):
                entry = al.get_element(bucket, pos)
                put(my_map, me.get_key(entry), me.get_value(entry))

    return my_map
