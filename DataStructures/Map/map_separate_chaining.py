"""
Implementación del TAD Map (tabla de símbolos) con manejo de colisiones
por SEPARATE CHAINING (encadenamiento separado).

La tabla es un array_list de tamaño ``capacity`` donde cada posición
(bucket) es una single_linked_list de map_entry. Todas las llaves cuyo hash
cae en la misma posición se guardan en la lista de esa posición, por lo que
el factor de carga puede ser mayor a 1.
"""

import random

from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sl
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements, load_factor, prime=109345121):
    """
    Crea una nueva tabla de símbolos (map) sin elementos.

    :param num_elements: Número de elementos que se espera almacenar en la tabla.
    :type num_elements: int
    :param load_factor: Factor de carga límite de la tabla antes de hacer un rehash.
    :type load_factor: float
    :param prime: Número primo usado para calcular el hash. Por defecto es 109345121.
    :type prime: int

    :return: Tabla recién creada.
    :rtype: map_separate_chaining
    """
    # La capacidad es el siguiente primo mayor a num_elements / load_factor
    capacity = mf.next_prime(int(num_elements / load_factor))

    # La tabla es un array_list con una single_linked_list vacía en cada posición
    table = lt.new_list()
    for _ in range(capacity):
        lt.add_last(table, sl.new_list())

    my_map = {
        "prime": prime,
        "capacity": capacity,
        # scale y shift son los valores aleatorios a y b del método MAD
        "scale": random.randint(1, prime - 1),
        "shift": random.randint(0, prime - 1),
        "table": table,
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0,
    }
    return my_map


def put(my_map, key, value):
    """
    Agrega una nueva entrada llave-valor a la tabla. Si la llave ya existe en
    la tabla, se actualiza el value de la entrada.

    :param my_map: Tabla de símbolos a la cual se desea agregar un nuevo elemento.
    :type my_map: map_separate_chaining
    :param key: Llave del nuevo elemento.
    :type key: any
    :param value: Valor del nuevo elemento.
    :type value: any

    :return: Tabla de símbolos con el nuevo elemento agregado.
    :rtype: map_separate_chaining
    """
    # 1. Se calcula el hash de la llave
    hash_value = mf.hash_value(my_map, key)
    # 2. Se busca la lista (bucket) en la posición del hash
    bucket = lt.get_element(my_map["table"], hash_value)
    pos = sl.is_present(bucket, key, default_compare)

    if pos > -1:
        # 3. La llave ya existe en la lista: se actualiza el valor
        entry = sl.get_element(bucket, pos)
        me.set_value(entry, value)
    else:
        # 4. La llave no existe: se agrega una nueva entrada al final de la lista
        sl.add_last(bucket, me.new_map_entry(key, value))
        # 5. Se actualiza el tamaño y el factor de carga actual
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        # 6. Si se supera el factor de carga límite, se hace rehash
        if my_map["current_factor"] > my_map["limit_factor"]:
            my_map = rehash(my_map)
    return my_map


def default_compare(key, entry):
    """
    Función de comparación por defecto. Compara la llave key con la llave de
    una entry dada.

    :param key: Llave con la que se desea comparar.
    :type key: any
    :param entry: Entrada de la tabla de símbolos con la que se desea comparar.
    :type entry: map_entry

    :return: 0 si son iguales, 1 si key > la llave del entry, -1 si key < la llave del entry.
    :rtype: int
    """
    if key == me.get_key(entry):
        return 0
    elif key > me.get_key(entry):
        return 1
    return -1


def contains(my_map, key):
    """
    Verifica si una llave se encuentra en la tabla de símbolos.

    :param my_map: Tabla de símbolos en la cual se desea verificar la llave.
    :type my_map: map_separate_chaining
    :param key: Llave que se desea verificar.
    :type key: any

    :return: True si la llave se encuentra en la tabla, False en caso contrario.
    :rtype: bool
    """
    hash_value = mf.hash_value(my_map, key)
    bucket = lt.get_element(my_map["table"], hash_value)
    pos = sl.is_present(bucket, key, default_compare)
    return pos > -1


def remove(my_map, key):
    """
    Elimina una entrada de la tabla de símbolos asociada a una llave dada.

    :param my_map: Tabla de símbolos de la cual se desea eliminar una entrada.
    :type my_map: map_separate_chaining
    :param key: Llave de la entrada que se desea eliminar.
    :type key: any

    :return: Tabla de símbolos con la entrada eliminada.
    :rtype: map_separate_chaining
    """
    hash_value = mf.hash_value(my_map, key)
    bucket = lt.get_element(my_map["table"], hash_value)
    pos = sl.is_present(bucket, key, default_compare)
    if pos > -1:
        # Se elimina la entrada de la lista y se actualizan los contadores
        sl.delete_element(bucket, pos)
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    return my_map


def get(my_map, key):
    """
    Obtiene el valor asociado a una llave en la tabla de símbolos.

    :param my_map: Tabla de símbolos de la cual se desea obtener el valor.
    :type my_map: map_separate_chaining
    :param key: Llave de la cual se desea obtener el valor asociado.
    :type key: any

    :return: Valor asociado a la llave. Si la llave no está, retorna None.
    :rtype: any
    """
    hash_value = mf.hash_value(my_map, key)
    bucket = lt.get_element(my_map["table"], hash_value)
    pos = sl.is_present(bucket, key, default_compare)
    if pos > -1:
        entry = sl.get_element(bucket, pos)
        return me.get_value(entry)
    return None


def size(my_map):
    """
    Obtiene la cantidad de elementos en la tabla de símbolos.

    :param my_map: Tabla de símbolos.
    :type my_map: map_separate_chaining

    :return: Cantidad de elementos en la tabla.
    :rtype: int
    """
    return my_map["size"]


def is_empty(my_map):
    """
    Verifica si la tabla de símbolos se encuentra vacía.

    :param my_map: Tabla de símbolos.
    :type my_map: map_separate_chaining

    :return: True si la tabla está vacía, False en caso contrario.
    :rtype: bool
    """
    return my_map["size"] == 0


def key_set(my_map):
    """
    Obtiene la lista de llaves de la tabla de símbolos.

    :param my_map: Tabla de símbolos de la cual se desea obtener las llaves.
    :type my_map: map_separate_chaining

    :return: Lista de llaves de la tabla de símbolos.
    :rtype: array_list
    """
    keys = lt.new_list()
    # Se recorre cada bucket de la tabla y cada entrada de su lista
    for pos in range(lt.size(my_map["table"])):
        bucket = lt.get_element(my_map["table"], pos)
        for i in range(sl.size(bucket)):
            entry = sl.get_element(bucket, i)
            lt.add_last(keys, me.get_key(entry))
    return keys


def value_set(my_map):
    """
    Obtiene la lista de valores de la tabla de símbolos.

    :param my_map: Tabla de símbolos de la cual se desea obtener los valores.
    :type my_map: map_separate_chaining

    :return: Lista de valores de la tabla de símbolos.
    :rtype: array_list
    """
    values = lt.new_list()
    # Se recorre cada bucket de la tabla y cada entrada de su lista
    for pos in range(lt.size(my_map["table"])):
        bucket = lt.get_element(my_map["table"], pos)
        for i in range(sl.size(bucket)):
            entry = sl.get_element(bucket, i)
            lt.add_last(values, me.get_value(entry))
    return values


def rehash(my_map):
    """
    Realiza un rehashing de la tabla de símbolos.

    1. Crea una nueva tabla map_separate_chaining con capacity igual al
       siguiente primo al doble del capacity actual.
    2. Recorre la tabla actual y reinserta cada elemento en la nueva tabla.
    3. Asigna la nueva tabla como la tabla actual.
    4. Retorna la tabla nueva.

    :param my_map: Tabla de símbolos a la cual se le desea realizar un rehashing.
    :type my_map: map_separate_chaining

    :return: Tabla de símbolos con un nuevo tamaño.
    :rtype: map_separate_chaining
    """
    old_table = my_map["table"]

    # Nueva tabla con capacity = siguiente primo al doble del actual,
    # con una single_linked_list vacía en cada posición
    new_capacity = mf.next_prime(2 * my_map["capacity"])
    new_table = lt.new_list()
    for _ in range(new_capacity):
        lt.add_last(new_table, sl.new_list())

    # Se asigna la nueva tabla y se reinician los contadores (put los vuelve a sumar)
    my_map["table"] = new_table
    my_map["capacity"] = new_capacity
    my_map["size"] = 0
    my_map["current_factor"] = 0

    # Se recorre cada bucket de la tabla anterior y se reinserta cada entrada
    for pos in range(lt.size(old_table)):
        bucket = lt.get_element(old_table, pos)
        for i in range(sl.size(bucket)):
            entry = sl.get_element(bucket, i)
            put(my_map, me.get_key(entry), me.get_value(entry))

    return my_map
