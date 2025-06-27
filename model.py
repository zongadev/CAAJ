from _mysql_db import *

def crearUsuario(dict):
    q="""
        INSERT INTO usuario
        (apodo, email, pass, nombre, apellido, dni,id_rol)
        VALUES
        %s,%s,%s,%s,%s,%s,%i)
    """
    val=(dict.get('apodo'),dict.get('email'),dict.get('pass'),dict.get('nombre'),dict.get('apellido'),dict.get('dni'),1)
    res_insert= insertDB(BASE,q,val)
    return res_insert==1
