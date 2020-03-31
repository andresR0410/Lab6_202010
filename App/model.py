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
from ADT import list as lt
from ADT import orderedmap as tree
from ADT import map as map
from ADT import list as lt
from DataStructures import listiterator as it
from datetime import datetime

"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores 
y otra para géneros
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo y retorna el catalogo inicializado.
    """
    catalog = {'datesTree':None}
    #implementación de Black-Red Tree (brt) por default
    catalog['datesTree'] = tree.newMap ()
    return catalog


def newAccident (row):
    """
    Crea una nueva estructura para almacenar un libro 
    """
    accident = {"id": row['ID'], "ciudad":row['City'], "date":row['Start_Time']}
    return accident

def newDate (date, row):
    """
    Crea una nueva estructura para almacenar los accidentes por fecha 
    """
    dateNode = {"date":date, "cityMap":None, "total":1}
    dateNode ['cityMap'] = map.newMap(11,maptype='CHAINING')
    city = (row['City'])
    map.put(dateNode['cityMap'],city, 1, compareByKey)
    return dateNode

def addDatesTree (catalog, row):
    """
    Adiciona el libro al arbol por fecha key=date
    """
    dateText= row['Start_Time']
    if row['Start_Time']:
        dateText=row['Start_Time'][0:row['Start_Time'].index(' ')]     
    date = strToDate(dateText,'%Y-%m-%d')
    dateNode = tree.get(catalog['datesTree'], date, greater)
    if dateNode:
        dateNode['total']+=1
        city = row['City']
        cityCount = map.get(dateNode['cityMap'], city, compareByKey)
        if  cityCount:
            cityCount+=1
            map.put(dateNode['cityMap'], city, cityCount, compareByKey)
        else:
            map.put(dateNode['cityMap'], cityCount, 1, compareByKey)
    else:
        dateNode = newDate(date,row)
        catalog['datesTree']  = tree.put(catalog['datesTree'] , date, dateNode, greater)

# Funciones de consulta


def getBookTree (catalog, bookTitle):
    """
    Retorna el libro desde el mapa a partir del titulo (key)
    """
    return tree.get(catalog['booksTitleTree'], bookTitle, greater)

def rankBookTree (catalog, bookTitle):
    """
    Retorna la cantidad de llaves menores (titulos) dentro del arbol
    """
    return tree.rank(catalog['booksTitleTree'], bookTitle, greater)

def selectBookTree (catalog, pos):
    """
    Retorna la operación select (titulos) dentro del arbol
    """
    return tree.select(catalog['booksTitleTree'], pos) 

def getAccidentByYearRating (catalog, year):
    """
    Retorna la cantidad de libros por rating para un año
    """
    yearElement=tree.get(catalog['yearsTree'], strToDate(year,'%Y'), greater)
    response=''
    if yearElement:
        ratingList = map.keySet(yearElement['ratingMap'])
        iteraRating=it.newIterator(ratingList)
        while it.hasNext(iteraRating):
            ratingKey = it.next(iteraRating)
            response += 'Rating '+str(ratingKey) + ':' + str(map.get(yearElement['ratingMap'],ratingKey,compareByKey)) + '\n'
        return response
    return None


def getAccidentCountByYearRange (catalog, years):
    """
    Retorna la cantidad de libros por rating para un rango de años
    """
    #Retorna la cantidad total de accidentes en esos años
    startYear = strToDate(years.split(" ")[0],'%Y-%m-%d')
    endYear = strToDate(years.split(" ")[1],'%Y-%m-%d')
    dateList = tree.valueRange(catalog['datesTree'], startYear, endYear, greater)
    counter = 0
    if dateList:
        iteraDate=it.newIterator(dateList)
        while it.hasNext(iteraDate):
            dateElement = it.next(iteraDate)
            #print(yearElement['year'],yearElement['count'])
            counter += dateElement['total']
        return counter
    #Retorna los accidentes por ciudad en esos años






    return None



# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )  

def compareByTitle(bookTitle, element):
    return  (bookTitle == element['title'] )

def greater (key1, key2):
    if ( key1 == key2):
        return 0
    elif (key1 < key2):
        return -1
    else:
        return 1

def strToDate(date_string, format):
    
    try:
        # date_string = '2016/05/18 13:55:26' -> format = '%Y/%m/%d %H:%M:%S')
        return datetime.strptime(date_string,format)
    except:
        return datetime.strptime('1900', '%Y')

