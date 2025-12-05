from _mysql_db import *
from datetime import datetime


def crearUsuario(dic):
    q = """
        INSERT INTO usuario
        (apodo, email, pass, nombre, apellido, dni, id_rol)
        VALUES (%s, %s, %s, %s, %s, %s,%s)
    """
    val = (
        dic.get('apodo'),dic.get('mail'),dic.get('contra'),dic.get('nombre'),
        dic.get('apellido'),dic.get('dni'),1
    )
    print(val)
    res_insert = insertDB(BASE, q, val)
    return res_insert

def obtenerUsuarioXEmailPass(result,email,passw):
    res=False
    sSql="""SELECT id, apodo,email,pass,id_rol,nombre,apellido,dni 
    FROM  usuario WHERE  email=%s and pass=%s;"""
    val=(email,passw)
    fila=selectDB(BASE,sSql,val)
    print(fila)
    if fila and len(fila) > 0:
        if fila!=[]:
            result['id']=fila[0][0]
            result['apodo']=fila[0][1]
            result['email']=fila[0][2]
            result['id_rol']=fila[0][4]   
            result['nombre']=fila[0][5]
            result['apellido']=fila[0][6]
            result['dni']=fila[0][7]
            res=True
    return res

def obtenerIdMateriaPorUUID(uuid):
    q = "SELECT id FROM materia WHERE uuid = %s"
    filas = selectDB(BASE, q, (uuid,))
    if filas and len(filas) > 0:
        return filas[0][0]
    return None

def obtenerApuntesxUsuario(result, id_usuario):
    q = """SELECT id, id_usuario, id_materia, head, content, tags, fechahora 
           FROM apunte WHERE id_usuario=%s;"""
    val = (id_usuario,)
    filas = selectDB(BASE, q, val)
    print(filas)
    if filas and len(filas) > 0:
        result['apuntes'] = [
            {'id': fila[0],'id_usuario': fila[1],'id_materia': fila[2],
             'titulo': fila[3],'contenido': fila[4],'tags': fila[5],'fecha': fila[6]
            } for fila in filas
        ]
    else:
        result['apuntes'] = []
    return result
    
def obtenerMateriasDB(result):
    q = """ SELECT materia,uuid,id from materia
            ORDER BY materia"""
    filas= selectDB(BASE,q)
    if filas and len(filas)>0:
        result['materia'] = [{'nombre':fila[0], 'uuid':fila[1], 'id':fila[2]} for fila in filas]
    else:
        result['materia'] =[]
    return result
def obtenerApuntesXMateriaDB(result, materia_id):
    q = """SELECT a.id, a.head, a.content, a.tags, u.apodo, m.materia
           FROM apunte AS a
           INNER JOIN usuario AS u ON a.id_usuario = u.id
           INNER JOIN materia AS m ON m.id = a.id_materia WHERE m.uuid = %s"""
    val = (materia_id,)

    filas = selectDB(BASE, q, val)
    if filas and len(filas) > 0:
        result['apuntes'] = [
            {'id': fila[0], 'titulo': fila[1], 'contenido': fila[2],
             'tags': fila[3], 'usuario': fila[4],'nombre_materia':fila[5]} for fila in filas
        ]
    else:
        result['apuntes'] = []
    return result

def crearApunte(dic,idusuario):
    q = """
        INSERT INTO apunte (ID_USUARIO,id_materia,head,content,tags,fechahora)
        VALUES (%s,%s,%s,%s,%s,%s)
    """
    val=(idusuario,obtenerIdMateriaPorUUID(dic.get('materia')),
         dic.get('titulo'),dic.get('contenido'),dic.get('tags'),datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    id = insertDB_return_id(BASE,q,val)
    return id

def obtenerApunteXidDB(result,id):
    q = """SELECT id_usuario, id_materia, head, content, tags, fechahora
            from apunte where id=(%s)"""
    filas = selectDB(BASE, q, (id,))
    if filas and len(filas) > 0:
        fila = filas[0] 
        result['apunte'] = {
            'id': id,
            'usuario': obtenerUsuarioNombreXid(fila[0]),
            'id_materia': fila[1],
            'titulo': fila[2],
            'contenido': fila[3],
            'tags': fila[4],
            'fecha': fila[5]
        }
        print(result, "IA CHIPA PIJAAAA")
        return result
    else:
        result['apunte'] = {}
        return result
    
def obtenerUsuarioNombreXid(id):
    q = """SELECT id, apodo FROM usuario WHERE id = %s"""
    filas = selectDB(BASE, q, (id,))
    if filas and len(filas) > 0:
        return {'id': filas[0][0], 'apodo': filas[0][1]}
    return None

def obtenerMediaXidDB(result, id_apunte):
    q = """SELECT nombre, path FROM media WHERE id_apunte = %s"""
    filas = selectDB(BASE, q, (id_apunte,))
    if filas and len(filas) > 0:
        result['media'] = [{'nombre': fila[0], 'path': fila[1]} for fila in filas]
    else:
        result['media'] = []
    return result

def crearMedia(id_apunte, file_name, nombre_uuid):
    q = """
        INSERT INTO media (id_apunte, nombre, path, nombre_uuid)
        VALUES (%s, %s, %s, %s)
    """
    val = (id_apunte, file_name, '/static/uploads/' + nombre_uuid, nombre_uuid)
    filas = insertDB(BASE, q, val)
    return filas

def obtenerUsuarioPorIdDB(result, id_usuario):
    q = "SELECT id, apodo, nombre, apellido, email FROM usuario WHERE id = %s"
    filas = selectDB(BASE, q, (id_usuario,))
    if filas and len(filas) > 0:
        fila = filas[0]
        result['usuario'] = {
            'id': fila[0],
            'apodo': fila[1],
            'nombre': fila[2],
            'apellido': fila[3],
            'email': fila[4]
        }
    else:
        result['usuario'] = {}
        
def obtenerComentariosDB(result, id_apunte):
    q = """
        SELECT c.id, c.id_usuario, u.apodo, c.content, c.fechahora
        FROM comentario as c
        INNER JOIN usuario u ON c.id_usuario = u.id
        WHERE c.id_apunte = %s
        ORDER BY c.fechahora ASC
    """
    filas = selectDB(BASE, q, (id_apunte,))
    if filas and len(filas) > 0:
        result['comentarios'] = [
            {
                'id': fila[0],
                'id_usuario': fila[1],
                'apodo': fila[2],
                'comentario': fila[3],
                'fecha': fila[4]
            }
            for fila in filas
        ]
    else:
        result['comentarios'] = []
    return result
    
def obtenerNombreMateriaPorId(materia_id):
    q = "SELECT materia FROM materia WHERE uuid = %s"
    filas = selectDB(BASE, q, (materia_id,))
    if filas and len(filas) > 0:
        return filas[0]
    return "Materia desconocida"

def crearComentario(id_apunte, id_usuario, comentario):
    q = """
        INSERT INTO comentario (id_apunte, id_usuario, content, fechahora)
        VALUES (%s, %s, %s, NOW())
    """
    try:
        insertDB(BASE, q, (id_apunte, id_usuario, comentario))
        return True
    except Exception as e:
        print(e)
        return False
    
def votar_apunte_db(id_apunte, id_usuario, tipo):
    # Elimina voto anterior si existe
    q_del = "DELETE FROM reaccion WHERE id_apunte=%s AND id_usuario=%s"
    deleteDB(BASE, q_del, (id_apunte, id_usuario))
    # Inserta el nuevo voto
    q_ins = "INSERT INTO reaccion (id_apunte, id_usuario, valor) VALUES (%s, %s, %s)"
    insertDB(BASE, q_ins, (id_apunte, id_usuario, tipo))
    # Cuenta likes y dislikes
    q_count = "SELECT valor, COUNT(*) FROM reaccion WHERE id_apunte=%s GROUP BY valor"
    filas = selectDB(BASE, q_count, (id_apunte,))
    likes = dislikes = 0
    for tipo_v, count in filas or []:
        if tipo_v == 'like':
            likes = count
        elif tipo_v == 'dislike':
            dislikes = count
    return True, likes, dislikes

def contar_reacciones_apunte(id_apunte):
    q = "SELECT valor, COUNT(*) FROM reaccion WHERE id_apunte=%s GROUP BY valor"
    filas = selectDB(BASE, q, (id_apunte,))
    likes = dislikes = 0
    for tipo_v, count in filas or []:
        if tipo_v == 'like':
            likes = count
        elif tipo_v == 'dislike':
            dislikes = count
    return likes, dislikes

def borrarApunteDB(id_apunte):
    try:
        q = "DELETE FROM apunte WHERE id = %s"
        deleteDB(BASE, q, (id_apunte,))
        return True
    except Exception as e:
        print(e)
        return False

def obtenerComentarioPorId(id_comentario):
    q = "SELECT id, id_usuario, id_apunte FROM comentario WHERE id = %s"
    filas = selectDB(BASE, q, (id_comentario,))
    if filas and len(filas) > 0:
        return {'id': filas[0][0], 'id_usuario': filas[0][1], 'id_apunte': filas[0][2]}
    return None

def borrarComentarioDB(id_comentario):
    try:
        q = "DELETE FROM comentario WHERE id = %s"
        deleteDB(BASE, q, (id_comentario,))
        return True
    except Exception as e:
        print(e)
        return False
