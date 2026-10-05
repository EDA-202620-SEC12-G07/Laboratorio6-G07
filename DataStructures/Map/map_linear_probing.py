"""
Implementación del TAD Map (tabla de símbolos) con manejo de colisiones
por LINEAR PROBING (sondeo lineal / open addressing).

La tabla es un array_list de tamaño ``capacity`` donde cada posición guarda
una map_entry. Una posición puede estar en tres estados:

* key = None        -> la posición nunca se ha usado.
* key = "__EMPTY__" -> la posición se usó, pero su entrada fue eliminada.
* key = otra llave  -> la posición está ocupada por una pareja llave-valor.

Cuando dos llaves caen en la misma posición (colisión), se busca la
siguiente posición libre de forma circular: (pos + 1) % capacity.
"""

import random

from DataStructures.List import array_list as lt
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements, load_factor, prime=109345121):
    """
    Crea una nueva tabla de hash (map) donde sus entradas llave-valor se
    inicializan con valores None-None.

    :param num_elements: Número de elementos que se desean almacenar en la tabla.
    :type num_elements: int
    :param load_factor: Factor de carga límite de la tabla antes de hacer un rehash.
    :type load_factor: float
    :param prime: Número primo utilizado para el cálculo del hash. Por defecto es 109345121.
    :type prime: int

    :return: Tabla recién creada.
    :rtype: map_linear_probing
    """
    # La capacidad es el siguiente primo mayor a num_elements / load_factor
    capacity = mf.next_prime(int(num_elements / load_factor))

    # La tabla es un array_list con 'capacity' entradas vacías (None, None)
    table = lt.new_list()
    for _ in range(capacity):
        lt.add_last(table, me.new_map_entry(None, None))

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
    Agrega una nueva entrada llave-valor a la tabla de hash. Si la llave ya
    existe en la tabla, se actualiza el value de la entrada.

    :param my_map: Tabla de símbolos a la cual se desea agregar el elemento.
    :type my_map: map_linear_probing
    :param key: Llave del elemento a agregar.
    :type key: any
    :param value: Valor del elemento a agregar.
    :type value: any

    :return: Tabla de símbolos con el nuevo elemento agregado.
    :rtype: map_linear_probing
    """
    # 1. Se calcula el hash de la llave
    hash_value = mf.hash_value(my_map, key)
    # 2. Se busca la posición de la llave (o la primera posición disponible)
    ocupied, pos = find_slot(my_map, key, hash_value)

    if ocupied:
        # La llave ya existía: solo se actualiza su valor
        entry = lt.get_element(my_map["table"], pos)
        me.set_value(entry, value)
    else:
        # 3. La llave es nueva: se inserta la entrada en la posición disponible
        lt.change_info(my_map["table"], pos, me.new_map_entry(key, value))
        # 4. Se actualiza el tamaño y el factor de carga actual
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        # 5. Si se supera el factor de carga límite, se hace rehash
        if my_map["current_factor"] > my_map["limit_factor"]:
            my_map = rehash(my_map)
    return my_map


def find_slot(my_map, key, hash_value):
    """
    Busca la posición en la tabla donde se debe insertar/encontrar una
    entrada con una llave dada.

    Parte de la posición hash_value. Si en esa posición está la key, se
    informa esa posición. Si la posición nunca ha sido ocupada, la key puede
    ir ahí. Si otra pareja ocupa la posición, se sigue con la siguiente.

    :param my_map: Tabla de símbolos en la que se desea buscar la posición.
    :type my_map: map_linear_probing
    :param key: Llave de la entrada que se desea buscar.
    :type key: any
    :param hash_value: Valor del hash de la llave.
    :type hash_value: int

    :return: (True, posición donde está la key) si la key se encontró;
             (False, primera posición disponible para la key) si no.
    :rtype: bool, int
    """
    first_avail = None
    found = False
    ocupied = False
    while not found:
        if is_available(my_map["table"], hash_value):
            # Posición libre (None o "__EMPTY__"): se guarda la primera encontrada
            if first_avail is None:
                first_avail = hash_value
            entry = lt.get_element(my_map["table"], hash_value)
            # Si la posición nunca se usó, la key no puede estar más adelante
            if me.get_key(entry) is None:
                found = True
        elif default_compare(key, lt.get_element(my_map["table"], hash_value)) == 0:
            # La key está en esta posición
            first_avail = hash_value
            found = True
            ocupied = True
        # Se avanza a la siguiente posición de forma circular
        hash_value = (hash_value + 1) % my_map["capacity"]
    return ocupied, first_avail


def is_available(table, pos):
    """
    Verifica si la posición pos en la tabla de símbolos está disponible.

    Una posición está disponible si su llave es None (nunca se ha usado) o
    "__EMPTY__" (la entrada fue eliminada).

    :param table: Tabla de símbolos en la que se desea verificar la disponibilidad.
    :type table: array_list
    :param pos: Posición en la tabla que se desea verificar.
    :type pos: int

    :return: True si la posición está disponible, False en caso contrario.
    :rtype: bool
    """
    entry = lt.get_element(table, pos)
    if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
        return True
    return False


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
    Valida si una llave dada se encuentra en la tabla de símbolos.

    :param my_map: Tabla de símbolos en la que se desea buscar la llave.
    :type my_map: map_linear_probing
    :param key: Llave que se desea buscar en la tabla.
    :type key: any

    :return: True si la llave se encuentra en la tabla, False en caso contrario.
    :rtype: bool
    """
    hash_value = mf.hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, hash_value)
    return ocupied


def remove(my_map, key):
    """
    Elimina una entrada llave-valor de la tabla de símbolos asociada a una
    llave dada. La entrada eliminada se reemplaza por la entrada
    "__EMPTY__", "__EMPTY__" para no cortar la secuencia de sondeo de las
    llaves que colisionaron con ella.

    :param my_map: Tabla de símbolos de la cual se desea eliminar la entrada.
    :type my_map: map_linear_probing
    :param key: Llave de la entrada que se desea eliminar.
    :type key: any

    :return: Tabla de símbolos sin la entrada asociada a la llave dada.
    :rtype: map_linear_probing
    """
    hash_value = mf.hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, hash_value)
    if ocupied:
        # Se marca la posición como liberada y se actualizan los contadores
        lt.change_info(my_map["table"], pos, me.new_map_entry("__EMPTY__", "__EMPTY__"))
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    return my_map


def get(my_map, key):
    """
    Obtiene el valor asociado a una llave dada en la tabla de símbolos.

    :param my_map: Tabla de símbolos en la que se desea buscar el valor.
    :type my_map: map_linear_probing
    :param key: Llave de la cual se desea obtener el valor.
    :type key: any

    :return: Valor asociado a la llave dada. Si la llave no está, retorna None.
    :rtype: any
    """
    hash_value = mf.hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, hash_value)
    if ocupied:
        entry = lt.get_element(my_map["table"], pos)
        return me.get_value(entry)
    return None


def size(my_map):
    """
    Obtiene la cantidad de elementos (parejas llave-valor) en la tabla.

    :param my_map: Tabla de símbolos.
    :type my_map: map_linear_probing

    :return: Cantidad de elementos en la tabla.
    :rtype: int
    """
    return my_map["size"]


def is_empty(my_map):
    """
    Verifica si la tabla de símbolos se encuentra vacía.

    :param my_map: Tabla de símbolos.
    :type my_map: map_linear_probing

    :return: True si la tabla está vacía, False en caso contrario.
    :rtype: bool
    """
    return my_map["size"] == 0


def key_set(my_map):
    """
    Obtiene la lista de llaves de la tabla de símbolos.

    :param my_map: Tabla de símbolos de la cual se desea obtener las llaves.
    :type my_map: map_linear_probing

    :return: Lista de llaves de la tabla de símbolos.
    :rtype: array_list
    """
    keys = lt.new_list()
    for pos in range(lt.size(my_map["table"])):
        # Solo se agregan las posiciones ocupadas (no None ni "__EMPTY__")
        if not is_available(my_map["table"], pos):
            entry = lt.get_element(my_map["table"], pos)
            lt.add_last(keys, me.get_key(entry))
    return keys


def value_set(my_map):
    """
    Obtiene la lista de valores de la tabla de símbolos.

    :param my_map: Tabla de símbolos de la cual se desea obtener los valores.
    :type my_map: map_linear_probing

    :return: Lista de valores de la tabla de símbolos.
    :rtype: array_list
    """
    values = lt.new_list()
    for pos in range(lt.size(my_map["table"])):
        # Solo se agregan las posiciones ocupadas (no None ni "__EMPTY__")
        if not is_available(my_map["table"], pos):
            entry = lt.get_element(my_map["table"], pos)
            lt.add_last(values, me.get_value(entry))
    return values


def rehash(my_map):
    """
    Realiza un rehash de la tabla de símbolos.

    1. Crea una nueva tabla map_linear_probing con capacity igual al
       siguiente primo al doble del capacity actual.
    2. Inserta los elementos de la tabla actual en la nueva tabla uno por uno.
    3. Asigna la nueva tabla a la tabla actual.
    4. Retorna la tabla nueva.

    :param my_map: Tabla de símbolos de la cual se desea realizar el rehash.
    :type my_map: map_linear_probing

    :return: Tabla de símbolos con el rehash realizado.
    :rtype: map_linear_probing
    """
    old_table = my_map["table"]

    # Nueva tabla vacía con capacity = siguiente primo al doble del actual
    new_capacity = mf.next_prime(2 * my_map["capacity"])
    new_table = lt.new_list()
    for _ in range(new_capacity):
        lt.add_last(new_table, me.new_map_entry(None, None))

    # Se asigna la nueva tabla y se reinician los contadores (put los vuelve a sumar)
    my_map["table"] = new_table
    my_map["capacity"] = new_capacity
    my_map["size"] = 0
    my_map["current_factor"] = 0

    # Se reinsertan con put las entradas ocupadas de la tabla anterior
    #    (las posiciones None y "__EMPTY__" no se copian)
    for pos in range(lt.size(old_table)):
        if not is_available(old_table, pos):
            entry = lt.get_element(old_table, pos)
            put(my_map, me.get_key(entry), me.get_value(entry))

    return my_map
