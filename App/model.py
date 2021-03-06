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
    Crea una nueva estructura para almacenar los accidentes por fecha
    """
    accident = {"id": row['ID'], "city":row['City'], "date":row['Start_Time'], 'state':row["State"]}
    return accident

def newDate (date, row):
    """
    Crea una nueva estructura para almacenar los accidentes por fecha 
    """
    dateNode = {"date":date, "severityMap":None, "cityMap":None, "total":1, "stateMap":None,"stateMost":None}
    dateNode['severityMap']=map.newMap(11,maptype='CHAINING')
    dateNode ['cityMap'] = map.newMap(300,maptype='CHAINING')
    dateNode["stateMap"]=map.newMap(300,maptype='CHAINING')
    severity = int(row['Severity'])
    city = row['City']
    state = row["State"]
    dateNode['stateMost']=row["State"]
    map.put(dateNode['severityMap'], severity, 1, compareByKey)
    map.put(dateNode['cityMap'],city, 1, compareByKey)
    map.put(dateNode['stateMap'],state, 1, compareByKey)
    return dateNode

def addDatesTree (catalog, row):
    """
    Adiciona el accidente al arbol por día key=Start_Time
    """
    dateText= row['Start_Time']
    if row['Start_Time']:
        dateText=row['Start_Time'][0:row['Start_Time'].index(' ')]     
    date = strToDate(dateText,'%Y-%m-%d')
    dateNode = tree.get(catalog['datesTree'], date, greater)
    if dateNode:
        dateNode['total']+=1
        severity = int(row['Severity'])
        severityCount = map.get(dateNode['severityMap'], severity, compareByKey)
        city = row['City']
        cityCount = map.get(dateNode['cityMap'], city, compareByKey)
        state=row["State"]
        stateCount=map.get(dateNode['stateMap'], state, compareByKey)
        Most=dateNode['stateMost']
        Mostval=map.get(dateNode['stateMap'], Most, compareByKey)
        if  severityCount:
            severityCount+=1
            map.put(dateNode['severityMap'], severity, severityCount, compareByKey)
        else:
            map.put(dateNode['severityMap'], severity, 1, compareByKey)
        if stateCount:
            stateCount+=1
            map.put(dateNode['stateMap'], state, stateCount, compareByKey)
            if stateCount>Mostval:
                    dateNode['stateMost']=state
        else:
            map.put(dateNode['stateMap'], state, 1, compareByKey)
            
        if  cityCount:
            cityCount+=1
            map.put(dateNode['cityMap'], city, cityCount, compareByKey)
        else:
            map.put(dateNode['cityMap'], city, 1, compareByKey)
    else:
        dateNode = newDate(date,row)
        catalog['datesTree']  = tree.put(catalog['datesTree'] , date, dateNode, greater)
# Funciones de consulta

def rankDateMap (catalog, date):
    """
    Retorna la cantidad de llaves menores (titulos) dentro del arbol
    """
    dateFormat=strToDate(date,'%Y-%m-%d')
    return tree.rank(catalog['datesTree'], dateFormat, greater)

def getAccidentByDateSeverity (catalog, date):
    """
    Retorna la cantidad de libros para un año y con un rating dado
    """
    dateElement=tree.get(catalog['datesTree'], strToDate(date,'%Y-%m-%d'), greater)
    response=''
    if dateElement:
        severityList = map.keySet(dateElement['severityMap'])
        iteraSev=it.newIterator(severityList)
        while it.hasNext(iteraSev):
            severityKey = it.next(iteraSev)
            response += 'Severity '+str(severityKey) + ':' + str(map.get(dateElement['severityMap'],severityKey,compareByKey)) + '\n'
        return response
    return None

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


def getStateByDate(catalog, date):
    date = strToDate(date,'%Y-%m-%d')
    dateNode = tree.get(catalog['datesTree'], date, greater)
    if dateNode:
        return dateNode['stateMost']
    else:
        return None

def getPrevious (catalog, dateText):
    arbol= catalog['datesTree']
    accidentes=0
    date= strToDate(dateText, '%Y-%m-%d')
    #nodeRank= tree.rank(arbol, date, greater)
    dateList= tree.keySet(arbol)
    #dateRank=dateList[0:nodeRank]
    iteraDate=it.newIterator(dateList)
    while it.hasNext(iteraDate):
        dateElement = it.next(iteraDate)
        if dateElement<date:
            dia=tree.get(arbol, dateElement, greater)
            accidentes+=dia['total']
    return accidentes
        


def getAccidentCountByYearRange (catalog, years):
    """
    Retorna la cantidad de libros por rating para un rango de años
    """
    #Retorna la cantidad total de accidentes en esos años
    startYear = strToDate(years.split(" ")[0],'%Y-%m-%d')
    endYear = strToDate(years.split(" ")[1],'%Y-%m-%d')
    dateList = tree.valueRange(catalog['datesTree'], startYear, endYear, greater)
    counter = 0
    response=''
    cities=map.newMap(capacity=51, prime=109345121, maptype='CHAINING')
    if dateList:
        iteraDate=it.newIterator(dateList)
        while it.hasNext(iteraDate):
            dateElement = it.next(iteraDate)
            counter += dateElement['total']
            if dateElement['cityMap']:#Si el nodo tiene dicho map
                    if map.isEmpty(cities):#Si cities está vacío, se le asigna el map de accidentes por ciudad del primer nodo
                        cities=dateElement['cityMap']
                    else: #De lo contrario, se compara cada ciudad del map de cada nodo con el map cities
                        ciudadesNodo=map.keySet(dateElement['cityMap'])#Lista de las ciudades que tuvieron accidentes en esa fecha(nodo)
                        ciudadesCities=map.keySet(cities)
                        iteraCiudades=it.newIterator(ciudadesNodo)
                        while it.hasNext(iteraCiudades):
                            ciudadElement=it.next(iteraCiudades)#Nombre de la ciudad que está en el cityMap de cada nodo
                            if ciudadElement:
                                if lt.isPresent(ciudadesCities, ciudadElement, compareByStr): #Se verifica si la ciudad está en los valores del map cities
                                    num=map.get(cities, ciudadElement, compareByKey)
                                    num+=map.get(dateElement['cityMap'], ciudadElement, compareByKey)
                                    map.put(cities, ciudadElement, num, compareByKey)
                                else:
                                    num=map.get(dateElement['cityMap'],ciudadElement,compareByKey)
                                    map.put(cities, ciudadElement, num, compareByKey)

    if not map.isEmpty(cities):
        cityList= map.keySet(cities)
        iteracity=it.newIterator(cityList)
        while it.hasNext(iteracity):
            cityKey = it.next(iteracity)
            response += str(cityKey) + ':' + str(map.get(cities,cityKey,compareByKey)) + " "
        return counter, response
    return None
    #Retorna los accidentes por ciudad en esos años
    
# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )  

def compareByTitle(bookTitle, element):
    return  (bookTitle == element['title'] )

def compareByStr (cityName, element):
    return (str(cityName)==str(element))

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