'''
    Modulo para la conexion a la base de datos MySQL.
    Este modulo contiene las funciones necesarias para conectarse a una base de datos MySQL, realizar consultas y manejar errores.
'''
    
import mysql.connector
import os

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
                charset='utf8mb4',
                use_unicode=True
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

def consultaDB(mydb, sQuery="", param=None, title=False,dictionary=False):
    """
    Ejecuta una consulta SQL en la base de datos.
    
    :param mydb: Objeto de conexion a la base de datos.
    :param consulta: Consulta SQL a ejecutar.
    :param params: Parametros para la consulta, si es necesario. Para evitar sql injection.
    :param title: booleana, si true, agrega a la lista los titulos de las columnas
    :return: Resultado de la consulta.
    """
    resultado = None
    cursor= None
    if mydb is not None:
        
        try:
            cursor = mydb.cursor()
            if param is not None:
                cursor.execute(sQuery, param)
            else:
                cursor.execute(sQuery)
            resultado = cursor.fetchall()
            if title and resultado is not None:
                resultado.insert(0,cursor.column_names)
            if dictionary and resultado is not None:
                keys=cursor.column_names
                # devuelve una lista de diccionarios en vez de tuplas
                resultado = [dict(zip(keys, row)) for row in resultado]
        except mysql.connector.Error as e:
            print(f"Error al consultar: {e}")
        finally:
            if cursor is not None:
                cursor.close()
    return resultado


def ejecutarDB(mydb, query="", param=None):
    resultado = None
    try:
        cursor = mydb.cursor()
        if param is not None:
            cursor.execute(query, param)
        else:
            cursor.execute(query)
        mydb.commit()
        resultado = cursor.rowcount
        print("resultado", resultado)
    except mysql.connector.Error as e:
        mydb.rollback()
        print(f"Error al intentar ejecutar una accion: {e} ")
    return resultado

## Funciones secundarias. Estas son las que se llaman desde model
## para conectar, consultar/ejecutar y cerrar la conexion a la BD en una sola funcion

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

def insertDB(configDB=None,sql="",param={}):
    ''' ########## INSERT
        :param 'configDB': un 'dict' con los parámetros de conexion
        :param 'sql': una cadena con la consulta sql
        :param 'param': valores separados anti sql injection
    '''
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,query=sql,param=param)
        cerrarBD(mydb)
    return res

def insertDB_return_id(configDB=None, sql="", param=None):
    '''
    INSERT que retorna el id del registro insertado.
    '''
    id = None
    if configDB is not None:
        mydb = conectarBD(configDB)
        try:
            cursor = mydb.cursor()
            if param is not None:
                cursor.execute(sql, param)
            else:
                cursor.execute(sql)
            mydb.commit()
            id = cursor.lastrowid
        except Exception as e:
            mydb.rollback()
            print(f"Error al insertar y obtener id: {e}")
        finally:
            cursor.close()
            cerrarBD(mydb)
    return id

def updateDB(configDB=None,sql="",param=None):
    ''' ########## UPDATE
        :param 'configDB': un 'dict' con los parámetros de conexion
        :param 'sql': una cadena con la consulta sql
        :param 'param': valores separados anti sql injection
    '''
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,query=sql,param=param)
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
        res=ejecutarDB(mydb,query=sql,param=param)
        cerrarBD(mydb)
    return res

BASE={ "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "pass": os.getenv("DB_PASSWORD", ""),
        "dbname": os.getenv("DB_NAME", "caaj")}