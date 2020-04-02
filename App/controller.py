"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
from ADT import list as lt
from ADT import map as map
from ADT import orderedmap as tree


from DataStructures import listiterator as it
from Sorting import mergesort as sort
from time import process_time


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Funcionaes utilitarias

def printList (lst):
    iterator = it.newIterator(lst)
    while  it.hasNext(iterator):
        element = it.next(iterator)
        result = "".join(str(key) + ": " + str(value) + ",  " for key, value in element.items())
        print (result)

# Funciones para la carga de datos 

def loadAccidents (catalog, sep=','):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por 
    cada uno de ellos, se crea un arbol de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    t1_start = process_time() #tiempo inicial
    booksfile = cf.data_dir + 'us_accidents_small.csv'
    dialect = csv.excel()
    dialect.delimiter=sep
    with open(booksfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            # Se adiciona el accidente al mapa de fecha y ciudad (key=date)
            model.addDatesTree(catalog, row)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga libros:",t1_stop-t1_start," segundos")   



def initCatalog ():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

def loadData (catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadAccidents(catalog)    

# Funciones llamadas desde la vista y enviadas al modelo


def getAccidentsTree(catalog, accidentId):
    t1_start = process_time() #tiempo inicial
    #book=model.getBookInList(catalog, bookTitle)
    book=model.getBookTree(catalog, bookTitle) 
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución buscar libro:",t1_stop-t1_start," segundos")   
    if book:
        return book
    else:
        return None

def rankBookTree(catalog, bookTitle):
    t1_start = process_time() #tiempo inicial
    rank=model.rankBookTree(catalog, bookTitle)  
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución buscar libro (rank):",t1_stop-t1_start," segundos")   
    return rank

def selectBookTree(catalog, pos):
    t1_start = process_time() #tiempo inicial
    rank=model.selectBookTree(catalog, pos) 
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución buscar libro (rank):",t1_stop-t1_start," segundos")   
    return rank

def getBookByYearRating (catalog, year):
    t1_start = process_time() #tiempo inicial
    resp = model.getBookByYearRating(catalog, year)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución consultar libros por año:",t1_stop-t1_start," segundos")   
    return resp
    
def getAccidentsByYearRange (catalog, years):
    t1_start = process_time() #tiempo inicial
    counter = model.getAccidentCountByYearRange(catalog, years)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución consultar libros por rango de años:",t1_stop-t1_start," segundos")   
    return counter

def getStateByDate(catalog, date):
    t1_start = process_time() #tiempo inicial
    counter = model.getStateByDate(catalog, date)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución para consultar estado más accidentado en fecha dada:",t1_stop-t1_start," segundos")   
    return counter