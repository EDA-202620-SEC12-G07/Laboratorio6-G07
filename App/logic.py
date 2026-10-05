"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones
 *
 * Dario Correal
 """

import os
import csv
import time
import tracemalloc


# TODO Realice la importación del mapa linear probing
from DataStructures.Map import map_linear_probing as lp
# TODO Realice la importación de ArrayList como estructura de datos auxiliar para sus requerimientos
from DataStructures.List import array_list as al
# TODO Realice la importación del mapa separate chaining
from DataStructures.Map import map_separate_chaining as sp


data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/GoodReads/'

# Implementación de mapa (lp o sp) con la que se construye el catálogo.
# La asigna new_logic() y la usan todas las funciones que agregan y consultan datos.
map_structure = None

# Factor de carga con el que se crean los mapas del catálogo. Lo asigna new_logic().
load_factor = None


#  -------------------------------------------------------------
# Creación del catálogo
#  -------------------------------------------------------------
# Para las pruebas de rendimiento se usa UNA de las dos versiones de new_logic():
#   - LINEAR PROBING (Tabla 2): load_factor = 0.1, 0.5, 0.7 y 0.9
#   - SEPARATE CHAINING (Tabla 3): load_factor = 2.00, 4.00, 6.00 y 8.00
# Se deja descomentada la versión que se va a probar y se comenta la otra.
# La versión entregada usa LINEAR PROBING.

def new_logic():
    """
    Inicializa el catálogo de libros. Crea una lista vacía para guardar
    los libros y utiliza tablas de hash para almacenar los datos restantes con diferentes índices
    utilizando linear probing como tipo de tabla de hash
    """
    global map_structure, load_factor
    # Mapa con manejo de colisiones LINEAR PROBING
    map_structure = lp
    # Factor de carga máximo de los mapas (Tabla 2: 0.1, 0.5, 0.7, 0.9)
    load_factor = 0.7

    catalog = {"books": None,
               "books_by_id": None,
               "books_by_year_author":None,
               "books_by_authors": None,
               "tags": None,
               "book_tags": None}

    #Lista que contiene la totalidad de los libros cargados
    catalog['books'] = al.new_list()

    #Tabla de Hash que contiene los libros indexados por good_reads_book_id
    #(good_read_id -> book)
    #TODO completar la creación del mapa
    catalog['books_by_id'] = lp.new_map(1000, load_factor)

    #Tabla de Hash con la siguiente pareja llave valor: (author_name -> List(books))
    #TODO completar la creación del mapa
    catalog['books_by_authors'] = lp.new_map(1000, load_factor)

    #Tabla de Hash con la siguiente pareja llave valor: (tag_name -> tag)
    #TODO completar la creación del mapa
    catalog['tags'] = lp.new_map(1000, load_factor)

    #Tabla de Hash con la siguiente pareja llave valor: (tag_id -> book_tags)
    catalog['book_tags'] = lp.new_map(1000, load_factor)

    #Tabla de Hash principal que contiene sub-mapas dentro de los valores
    #con la siguiente representación de la pareja llave valor: (author_name -> (original_publication_year -> list(books)))
    #TODO completar la creación del mapa
    catalog['books_by_year_author'] = lp.new_map(1000, load_factor)

    return catalog


# def new_logic():
#     """
#     Inicializa el catálogo de libros. Crea una lista vacía para guardar
#     los libros y utiliza tablas de hash para almacenar los datos restantes con diferentes índices
#     utilizando separate chaining como tipo de tabla de hash
#     """
#     global map_structure, load_factor
#     # Mapa con manejo de colisiones SEPARATE CHAINING
#     map_structure = sp
#     # Factor de carga máximo de los mapas (Tabla 3: 2.00, 4.00, 6.00, 8.00)
#     load_factor = 4.0
#
#     catalog = {"books": None,
#                "books_by_id": None,
#                "books_by_year_author":None,
#                "books_by_authors": None,
#                "tags": None,
#                "book_tags": None}
#
#     #Lista que contiene la totalidad de los libros cargados
#     catalog['books'] = al.new_list()
#
#     #Tabla de Hash que contiene los libros indexados por good_reads_book_id
#     #(good_read_id -> book)
#     catalog['books_by_id'] = sp.new_map(1000, load_factor)
#
#     #Tabla de Hash con la siguiente pareja llave valor: (author_name -> List(books))
#     catalog['books_by_authors'] = sp.new_map(1000, load_factor)
#
#     #Tabla de Hash con la siguiente pareja llave valor: (tag_name -> tag)
#     catalog['tags'] = sp.new_map(1000, load_factor)
#
#     #Tabla de Hash con la siguiente pareja llave valor: (tag_id -> book_tags)
#     catalog['book_tags'] = sp.new_map(1000, load_factor)
#
#     #Tabla de Hash principal que contiene sub-mapas dentro de los valores
#     #con la siguiente representación de la pareja llave valor: (author_name -> (original_publication_year -> list(books)))
#     catalog['books_by_year_author'] = sp.new_map(1000, load_factor)
#
#     return catalog

#  -------------------------------------------------------------
# Funciones para la carga de datos
#  -------------------------------------------------------------

#TODO incorporar las funciones para toma de tiempo y memoria
def load_data(catalog, memflag):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos.

    Toma el tiempo de toda la carga y, si memflag es True, también la
    memoria utilizada. El tiempo de ejecución "real" es el que se toma con
    memflag en False, porque tracemalloc hace más lenta la ejecución.
    """
    # Se toma el tiempo inicial
    start_time = getTime()

    # Si se pide, se inicia la medición de memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    books, authors = load_books(catalog)
    tag_size = load_tags(catalog)
    book_tag_size = load_books_tags(catalog)

    # Se toma el tiempo final y se calcula el tiempo de carga
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    # Si se midió la memoria, se toma la muestra final y se detiene tracemalloc
    delta_memory = None
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(start_memory, stop_memory)

    return books, authors, tag_size, book_tag_size, delta_time, delta_memory


def load_books(catalog):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    booksfile = data_dir + "books.csv"
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for book in input_file:
        add_book(catalog, book)
    return book_size(catalog), author_size(catalog)


def load_tags(catalog):
    """
    Carga todos los tags del archivo y los agrega a la lista de tags
    """
    tagsfile = data_dir + 'tags.csv'
    input_file = csv.DictReader(open(tagsfile, encoding='utf-8'))
    for tag in input_file:
        add_tag(catalog, tag)
    return tag_size(catalog)


def load_books_tags(catalog):
    """
    Carga la información que asocia tags con libros.
    """
    bookstagsfile = data_dir +"book_tags.csv"
    input_file = csv.DictReader(open(bookstagsfile, encoding='utf-8'))
    for booktag in input_file:
        add_book_tag(catalog, booktag)
    return book_tag_size(catalog)


def new_tag(name, id):
    """
    Esta estructura almancena los tags utilizados para marcar libros.
    """
    tag = {"name": "", "tag_id": ""}
    tag['name'] = name
    tag['tag_id'] = id
    return tag


def new_book_tag(tag_id, book_id, count):
    """
    Esta estructura crea una relación entre un tag y
    los libros que han sido marcados con dicho tag.
    """
    book_tag = {'tag_id': tag_id, 'book_id': book_id,'count':count}
    return book_tag

#  -----------------------------------------------
#  Funciones para agregar informacion al catalogo
#  -----------------------------------------------

def add_book(catalog, book):
    """
    Adiciona un libro al mapa de libros.
    Además, guarda la información de los autores en las tablas de hash correspondientes
    """
    # Se adiciona el libro a la lista general de libros
    al.add_last(catalog['books'], book)
    # Se adiciona el libro a la tabla de hash indexada por goodreads_book_id
    map_structure.put(catalog['books_by_id'],book['goodreads_book_id'], book)
    # Se obtienen los autores del libro
    authors = book['authors'].split(",")
    # Para cada autor, se agrega en la tabla de hash indexada por autores y
    # en las tablas de hash indexadas por autor y por año de publicación
    for author in authors:
        add_book_author(catalog, author.strip(), book)
        add_book_author_and_year(catalog,author.strip(), book)
    return catalog


def add_book_author(catalog, author_name, book):
    """
    Adiciona un autor al mapa de autores, la cual guarda referencias
    a los libros de dicho autor
    """
    authors = catalog['books_by_authors']
    author_value = map_structure.get(authors,author_name)
    if author_value:
        #Si el autor ya se había agregado al mapa, se obtiene la lista que contiene sus libros y se agrega el nuevo elemento.
        al.add_last(author_value,book)
    else:
        #Si es un autor nuevo, se agrega al mapa teniendo como llave el nombre del autor
        # y como valor una lista que contiene los libros asociados al autor.
        authors_books = al.new_list()
        al.add_last(authors_books,book)
        map_structure.put(authors,author_name,authors_books)
    return catalog


def add_book_author_and_year(catalog, author_name, book):
    """
    Adiciona un autor a los mapas indexados por autor y por año de publicación.
    Si el autor ya se había agregado:
        - Si el año de publicación también se había agregado, se obtiene la lista en el tercer nivel y se agrega el libro.
        - Si el año de publicación no se había agregado, se agrega un nuevo mapa dentro del indice del autor y dentro de
        este mapa se agrega una lista con el libro asociado.
    Si el autor no se había agregado:
        - Se crea el indice del nuevo autor, se crea dentro del valor el mapa asociado al nuevo año de publicación y
        en el tercer nivel se agrega una lista como valor de este ultimo mapa con el libro asociado
    """
    books_by_year_author = catalog['books_by_year_author']
    pub_year = book['original_publication_year']
    #Si el año de publicación está vacío se reemplaza por un valor simbolico
    #TODO Completar manejo de los escenarios donde el año de publicación es vacío.
    pub_year = format_pub_year(pub_year)
    author_value = map_structure.get(books_by_year_author,author_name)
    if author_value:
        pub_year_value = map_structure.get(author_value,pub_year)
        if pub_year_value:
            al.add_last(pub_year_value,book)
        else:
            # El año es nuevo para este autor: se agrega al mapa del autor
            # una lista con el libro asociado
            books = al.new_list()
            al.add_last(books, book)
            map_structure.put(author_value,pub_year,books)
    else:
        # TODO Completar escenario donde no se había agregado el autor al mapa principal
        # Se crea la lista del tercer nivel con el libro asociado
        books = al.new_list()
        al.add_last(books, book)
        # Se crea el mapa del segundo nivel (año de publicación -> lista de libros).
        # Un autor tiene pocos años de publicación distintos (en books.csv son 2 en
        # promedio y 41 como máximo), por eso se crea para 10 elementos: si el autor
        # tiene más años, el rehash agranda el mapa. Crear uno de 1000 por cada uno
        # de los 5841 autores llena la memoria del computador.
        pub_year_map = map_structure.new_map(10, load_factor)
        map_structure.put(pub_year_map, pub_year, books)
        # Se agrega el autor al mapa principal (autor -> mapa de años)
        map_structure.put(books_by_year_author, author_name, pub_year_map)
    return catalog


def format_pub_year(pub_year):
    """
    Retorna el año de publicación con el formato con el que se guarda como llave
    en el mapa de años:
        - Si el año está vacío se reemplaza por el valor simbólico "Desconocido".
        - Si el año viene como "2008.0" (así está en el archivo), se deja como "2008".
    Se usa al cargar los datos y al consultar, para que ambas llaves coincidan.
    """
    pub_year = pub_year.strip()
    if pub_year == "":
        return "Desconocido"
    if pub_year.endswith(".0"):
        return pub_year[:-2]
    return pub_year


def add_tag(catalog, tag):
    """
    Adiciona un tag al mapa de tags indexado por nombre del tag
    """
    t = new_tag(tag['tag_name'], tag['tag_id'])
    map_structure.put(catalog['tags'],tag['tag_name'],t)
    return catalog


def add_book_tag(catalog, book_tag):
    """
    Adiciona un tag a la lista de tags.
    Si el book_tag ya había sido agregado:
        - Se obtiene la lista asociada al valor del indice y se agrega el book_yag
    Si el book_tag no había sido agregado:
        - Se crea el nuevo indice en el mapa y como valor se agrega una nueva lista con el book_tag asociado.
    """
    t = new_book_tag(book_tag['tag_id'], book_tag['goodreads_book_id'], book_tag['count'])
    book_tag_value = map_structure.contains(catalog['book_tags'],t['tag_id'])
    if book_tag_value:
        book_tag_list = map_structure.get(catalog['book_tags'],t['tag_id'])
        al.add_last(book_tag_list,book_tag)
    else:
        #TODO Completar escenario donde el book_tag no se había agregado al mapa
        # Se crea la lista de book_tags del tag y se agrega al mapa con llave tag_id
        book_tag_list = al.new_list()
        al.add_last(book_tag_list, book_tag)
        map_structure.put(catalog['book_tags'], t['tag_id'], book_tag_list)
    return catalog

#  -------------------------------------------------------------
# Funciones de consulta
#  -------------------------------------------------------------

def get_book_info_by_book_id(catalog, good_reads_book_id):
    """
    Retorna toda la informacion que se tenga almacenada de un libro según su good_reads_id.
    """
    #TODO Completar función de consulta
    # El mapa books_by_id tiene como llave el goodreads_book_id: get retorna el libro o None
    return map_structure.get(catalog['books_by_id'], good_reads_book_id)


def get_books_by_author(catalog, author_name):
    """
    Retorna los libros asociado al autor ingresado por párametro
    """
    #TODO Completar función de consulta
    # El mapa books_by_authors retorna la lista de libros del autor (o None si no existe).
    # Se retorna también el nombre del autor porque la vista lo imprime.
    books = map_structure.get(catalog['books_by_authors'], author_name)
    return author_name, books


def get_books_by_tag(catalog, tag_name):
    """
    Retorna el número de libros que fueron etiquetados con el tag_name especificado.
    - Se obtiene el tag asociado al tag_name dado.
    - Teniendo la información del tag, se obtiene el tag_id para relacionarlo con la estructura que contiene el
    set de datos de book_tags y obtener más información.
    - Teniendo el tag_id, se puede obtener el goodreads_book_id de la estructura que contiene los datos
    de book_tags y finalmente relacionarlo con los datos completos del libro.

    """
    #TODO Completar función de consulta
    # 1. Se obtiene el tag a partir de su nombre. Si no existe, no hay libros (None)
    tag = map_structure.get(catalog['tags'], tag_name)
    if tag is None:
        return None

    # 2. Con el tag_id se obtiene la lista de book_tags asociados al tag
    book_tag_list = map_structure.get(catalog['book_tags'], tag['tag_id'])
    if book_tag_list is None:
        return None

    # 3. Por cada book_tag se busca el libro completo con su goodreads_book_id
    books = al.new_list()
    for pos in range(0, al.size(book_tag_list)):
        book_tag = al.get_element(book_tag_list, pos)
        book = map_structure.get(catalog['books_by_id'], book_tag['goodreads_book_id'])
        if book is not None:
            al.add_last(books, book)
    return books


def get_books_by_author_pub_year(catalog, author_name, pub_year):
    """
    - Se obtiene el mapa asociado al author_name dado
    - Si el author existe, se obtiene el mapa asociado al año de publicación
    Retorna los libros asociados a un autor y un año de publicación específicos
    """
    # Iniciar medición de tiempo
    start_time = getTime()

    # Iniciar medición de memoria
    tracemalloc.start()
    start_memory = getMemory()

    # TODO Completar la función de consulta
    resultado = None
    # Se obtiene el mapa de años del autor (author_name -> mapa de años)
    pub_year_map = map_structure.get(catalog['books_by_year_author'], author_name)
    if pub_year_map is not None:
        # El año se busca con el mismo formato con el que se guardó la llave
        resultado = map_structure.get(pub_year_map, format_pub_year(pub_year))

    # Detener medición de memoria
    stop_memory = getMemory()
    tracemalloc.stop()

    # Calcular medición de tiempo y memoria
    end_time = getTime()
    tiempo_transcurrido = deltaTime(end_time, start_time)
    memoria_usada = deltaMemory(start_memory, stop_memory)

    return resultado, tiempo_transcurrido, memoria_usada


#  -------------------------------------------------------------
# Funciones utilizadas para obtener el tamaño de los mapas
#  -------------------------------------------------------------

def book_size(catalog):
    return map_structure.size(catalog['books_by_id'])


def author_size(catalog):
    return map_structure.size(catalog['books_by_authors'])


def tag_size(catalog):
    return map_structure.size(catalog['tags'])


def book_tag_size(catalog):
    return map_structure.size(catalog['book_tags'])

#  -------------------------------------------------------------
# Funciones utilizadas para obtener memoria y tiempo
#  -------------------------------------------------------------

def getTime():
    """
    Devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter() * 1000)

def getMemory():
    """
    Toma una muestra de la memoria alocada en un instante de tiempo
    """
    return tracemalloc.take_snapshot()

def deltaTime(end, start):
    """
    Devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    return float(end - start)

def deltaMemory(start_memory, stop_memory):
    """
    Calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en kBytes
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = sum(stat.size_diff for stat in memory_diff) / 1024.0
    return delta_memory
