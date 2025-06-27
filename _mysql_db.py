'''
    Modulo para la conexion a la base de datos MySQL.
    Este modulo contiene las funciones necesarias para conectarse a una base de datos MySQL, realizar consultas y manejar errores.
'''
    
import mysql.connector

def conectarBD(configDB=None):
    """
    Conecta a la base de datos MySQL utilizando la configuracion proporcionada.
    
    :param configDB: Diccionario con la configuracion de la base de datos.
    :return: Objeto de conexion a la base de datos.
    """
    mydb=None
    if configDB is not None:
        try:
            mydb =mysql.connector.connect(
                host=configDB.get('host'),
                user=configDB.get('user'),
                password=configDB.get('pass'),
                database=configDB.get('dbname'),
            )
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
    return mydb

def cerrarBD(mydb):
    """
    Cierra la conexion a la base de datos MySQL.
    
    :param mydb: Objeto de conexion a la base de datos.
    """
    if mydb is not None:
        try:
            mydb.close()
        except mysql.connector.Error as e:
            print(f"Error al cerrar la base de datos: {e}")

def consultaDB(mydb, query="", params=None, title=False,dictionary=False):
    """
    Ejecuta una consulta SQL en la base de datos.
    
    :param mydb: Objeto de conexion a la base de datos.
    :param consulta: Consulta SQL a ejecutar.
    :param params: Parametros para la consulta, si es necesario. Para evitar sql injection.
    :param title: booleana, si true, agrega a la lista los titulos de las columnas
    :return: Resultado de la consulta.
    """
    resultado = None
    if mydb is not None:
        try:
            cursor = mydb.cursor()
            cursor.execute(query, params)
            resultado = cursor.fetchall()
            if title:
                resultado.insert(0,cursor.column_names)
            if dictionary:
                keys=cursor.column_names
                # Para obtener una respuesta de lista de diccionarios
                resultado = [dict(zip(keys, row)) for row in resultado]
        except mysql.connector.Error as e:
            print(f"Error al consultar: {e}")
        finally:
            cursor.close()
    return resultado


def ejecutarDB(mydb,query="",params=None):
    ''' 
    Realiza las consultas 'INSERT' 'UPDATE' 'DELETE'
    :param recibe: 'mydb' una conexion a una base de datos
    :param recibe:'sQuery' la cadena con la consulta (query) sql.
    :param recibe:'params' valores separados anti sql injection
    :return: la cantidad de filas afectadas con la query.
    '''
    resultado=None
    try:
        cursor = mydb.cursor()    
        cursor.execute(query)
        mydb.commit()
        resultado = cursor.rowcount
    except mysql.connector.Error as e:
        mydb.rollback()
        print(f"Error al intentar ejecutar una accion: {e} ")
        
## Fuciones secundarias. Estas funciones son las que seran llamadas
## por el model, permitiendo iniciar la conexion, consultar/ejecutar y cerrar la conexion a traves de una funcion

def selectDB(configDB=None,sql="",param=None,dictionary=False,title=False):
    ''' ########## SELECT
        :param 'configDB': un 'dict' con los parámetros de conexion
        :param 'sql': una cadena con la consulta sql
        :param 'param': valores separados anti sql injection
        :param 'title': booleana
        :return: 'list' con el resultado de la consulta
            cada fila de la 'list' es una 'tuple'
            Si 'title' es True, entonces agrega a la lista los títulos de las columnas.
    '''
    resQuery=None
    if configDB is not None:
        mydb=conectarBD(configDB)
        resQuery=consultaDB(mydb,sQuery=sql,param=param,title=title,dictionary=dictionary)
        cerrarBD(mydb)
    return resQuery

def insertDB(configDB=None,sql="",param=None):
    ''' ########## INSERT
        :param 'configDB': un 'dict' con los parámetros de conexion
        :param 'sql': una cadena con la consulta sql
        :param 'param': valores separados anti sql injection
    '''
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,sQuery=sql,param=param)
        cerrarBD(mydb)
    return res

def updateDB(configDB=None,sql="",param=None):
    ''' ########## UPDATE
        :param 'configDB': un 'dict' con los parámetros de conexion
        :param 'sql': una cadena con la consulta sql
        :param 'param': valores separados anti sql injection
    '''
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,sQuery=sql,param=param)
        cerrarBD(mydb)
    return res

def deleteDB(configDB=None,sql="",param=None):
    ''' ########## DELETE
        :param 'configDB': un 'dict' con los parámetros de conexion
        :param 'sql': una cadena con la consulta sql
        :param 'param': valores separados anti sql injection
    '''
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,sQuery=sql,param=param)
        cerrarBD(mydb)
    return res