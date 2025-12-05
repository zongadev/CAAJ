from _mysql_db import *
from datetime import datetime


# crea un usuario nuevo en la BD
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

# busca un usuario por email y contraseña (para el login)
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

# ahora recibe un ID directamente, no un UUID
# devuelve el ID tal cual si es valido
def obtenerIdMateriaPorUUID(materia_id):
    try:
        return int(materia_id)
    except (ValueError, TypeError):
        return None

# trae todos los apuntes de un usuario con info de la materia
def obtenerApuntesxUsuario(result, id_usuario):
    q = """SELECT a.id, a.id_usuario, a.id_materia, a.head, a.content, a.tags, a.fechahora, m.materia
           FROM apunte a
           LEFT JOIN materia m ON a.id_materia = m.id
           WHERE a.id_usuario=%s
           ORDER BY a.fechahora DESC;"""
    val = (id_usuario,)
    filas = selectDB(BASE, q, val)
    print(filas)
    if filas and len(filas) > 0:
        result['apuntes'] = [
            {'id': fila[0],'id_usuario': fila[1],'id_materia': fila[2],
             'titulo': fila[3],'contenido': fila[4],'tags': fila[5],'fecha': fila[6],
             'nombre_materia': fila[7]
            } for fila in filas
        ]
    else:
        result['apuntes'] = []
    return result
    
# trae todas las materias disponibles ordenadas alfabeticamente
def obtenerMateriasDB(result):
    q = """ SELECT materia, id from materia
            ORDER BY materia"""
    filas= selectDB(BASE,q)
    if filas and len(filas)>0:
        result['materia'] = [{'nombre':fila[0], 'id':fila[1]} for fila in filas]
    else:
        result['materia'] =[]
    return result

# busca en toda la BD (materias y apuntes) con normalizacion de tildes
def buscarGlobal(result, query):
    print(f"🔍 buscarGlobal llamado con query: '{query}'")
    if not query or len(query.strip()) == 0:
        result['resultados'] = []
        return result
    
    # normalizamos el query quitando tildes y pasando a minusculas para buscar mejor
    # buscamos tanto en materias como en apuntes
    q = """
        SELECT 'materia' as tipo, m.id, m.materia as titulo, NULL as contenido, m.id as materia_id
        FROM materia m
        WHERE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(m.materia, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u')) 
        LIKE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u'))
        UNION
        SELECT 'apunte' as tipo, a.id, a.head as titulo, a.content as contenido, a.id_materia as materia_id
        FROM apunte a
        WHERE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(a.head, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u')) 
        LIKE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u'))
        OR LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(a.tags, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u')) 
        LIKE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u'))
        LIMIT 10
    """
    search_term = f'%{query}%'
    print(f"🔍 Ejecutando query con term: '{search_term}'")
    filas = selectDB(BASE, q, (search_term, search_term, search_term))
    print(f"🔍 Resultados obtenidos: {len(filas) if filas else 0}")
    
    if filas and len(filas) > 0:
        result['resultados'] = [
            {
                'tipo': fila[0],
                'id': fila[1],
                'titulo': fila[2],
                'contenido': fila[3][:100] if fila[3] else None,
                'materia_id': fila[4]
            } for fila in filas
        ]
    else:
        result['resultados'] = []
    return result
def obtenerApuntesXMateriaDB(result, materia_id, query=''):
    if query:
        # busqueda con normalizacion de tildes para que funcione mejor
        q = """SELECT a.id, a.head, a.content, a.tags, u.apodo, m.materia
               FROM apunte AS a
               INNER JOIN usuario AS u ON a.id_usuario = u.id
               INNER JOIN materia AS m ON m.id = a.id_materia 
               WHERE m.id = %s
               AND (
                   LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(a.head, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u')) 
                   LIKE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u'))
                   OR LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(a.tags, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u')) 
                   LIKE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u'))
                   OR LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(u.apodo, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u')) 
                   LIKE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u'))
               )"""
        search_term = f'%{query}%'
        val = (materia_id, search_term, search_term, search_term)
    else:
        # sin busqueda, traemos todos los apuntes de la materia
        q = """SELECT a.id, a.head, a.content, a.tags, u.apodo, m.materia
               FROM apunte AS a
               INNER JOIN usuario AS u ON a.id_usuario = u.id
               INNER JOIN materia AS m ON m.id = a.id_materia WHERE m.id = %s"""
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

# crea un nuevo apunte y devuelve su id
def crearApunte(dic,idusuario):
    q = """
        INSERT INTO apunte (ID_USUARIO,id_materia,head,content,tags,fechahora)
        VALUES (%s,%s,%s,%s,%s,%s)
    """
    val=(idusuario,obtenerIdMateriaPorUUID(dic.get('materia')),
         dic.get('titulo'),dic.get('contenido'),dic.get('tags'),datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    id = insertDB_return_id(BASE,q,val)
    return id

# actualiza un apunte existente con nueva info
def actualizarApunte(id_apunte, dic):
    q = """
        UPDATE apunte 
        SET id_materia=%s, head=%s, content=%s, tags=%s
        WHERE id=%s
    """
    materia_id = obtenerIdMateriaPorUUID(dic.get('materia'))
    print(f"DEBUG actualizarApunte - materia raw: {dic.get('materia')}, convertido: {materia_id}")
    print(f"DEBUG actualizarApunte - titulo: {dic.get('titulo')}, contenido: {dic.get('contenido')}, tags: {dic.get('tags')}")
    
    if materia_id is None:
        print(f"ERROR: materia_id es None para valor: {dic.get('materia')}")
        return False
        
    val=(materia_id, dic.get('titulo'), dic.get('contenido'), dic.get('tags'), id_apunte)
    try:
        updateDB(BASE, q, val)
        print(f"Apunte {id_apunte} actualizado exitosamente")
        return True
    except Exception as e:
        print(f"Error actualizando apunte: {e}")
        import traceback
        traceback.print_exc()
        return False

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
        INSERT INTO media (id_apunte, nombre, path)
        VALUES (%s, %s, %s)
    """
    val = (id_apunte, file_name, '/static/uploads/' + nombre_uuid)
    filas = insertDB(BASE, q, val)
    return filas

# elimina un archivo de un apunte (tanto de la BD como del disco)
def eliminarArchivoApunte(id_apunte, nombre_archivo):
    # primero buscamos el path para poder borrar el archivo fisico
    q = "SELECT path FROM media WHERE id_apunte = %s AND nombre = %s"
    filas = selectDB(BASE, q, (id_apunte, nombre_archivo))
    
    if not filas or len(filas) == 0:
        return False
    
    path = filas[0][0]
    
    # borramos el registro de la BD
    q_delete = "DELETE FROM media WHERE id_apunte = %s AND nombre = %s"
    deleteDB(BASE, q_delete, (id_apunte, nombre_archivo))
    
    # ahora borramos el archivo del servidor
    try:
        import os
        # el path es tipo '/static/uploads/archivo.pdf', extraemos el nombre
        if path.startswith('/static/uploads/'):
            nombre_uuid = path.replace('/static/uploads/', '')
            file_path = os.path.join('static', 'uploads', nombre_uuid)
            if os.path.exists(file_path):
                os.remove(file_path)
        return True
    except Exception as e:
        print(f"Error al eliminar archivo físico: {e}")
        return False

# trae el voto del usuario para un apunte (like, dislike o nada)
def obtenerVotoUsuario(result, id_apunte, id_usuario):
    if not id_usuario:
        result['voto_usuario'] = None
        return
    
    q = "SELECT valor FROM reaccion WHERE id_apunte = %s AND id_usuario = %s"
    filas = selectDB(BASE, q, (id_apunte, id_usuario))
    
    if filas and len(filas) > 0:
        result['voto_usuario'] = filas[0][0]  # puede ser 'like' o 'dislike'
    else:
        result['voto_usuario'] = None

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
    q = "SELECT materia FROM materia WHERE id = %s"
    filas = selectDB(BASE, q, (materia_id,))
    if filas and len(filas) > 0:
        return filas[0][0]
    return "Materia desconocida"

def crearComentario(id_apunte, id_usuario, comentario):
    q = """
        INSERT INTO comentario (id_apunte, id_usuario, content, fechahora)
        VALUES (%s, %s, %s, NOW())
    """
    try:
        from _mysql_db import insertDB_return_id
        id_comentario = insertDB_return_id(BASE, q, (id_apunte, id_usuario, comentario))
        return id_comentario
    except Exception as e:
        print(e)
        return None

def actualizarComentario(id_comentario, contenido):
    q = """
        UPDATE comentario 
        SET content=%s
        WHERE id=%s
    """
    try:
        updateDB(BASE, q, (contenido, id_comentario))
        return True
    except Exception as e:
        print(f"Error actualizando comentario: {e}")
        return False
    
# maneja los votos de un apunte (agregar, quitar, cambiar)
def votar_apunte_db(id_apunte, id_usuario, tipo):
    # chequeamos si el usuario ya voto antes
    q_check = "SELECT valor FROM reaccion WHERE id_apunte=%s AND id_usuario=%s"
    filas = selectDB(BASE, q_check, (id_apunte, id_usuario))
    
    voto_existente = filas[0][0] if filas and len(filas) > 0 else None
    voto_actual = None
    
    # si vota lo mismo que ya tenia, se lo quitamos (toggle)
    if voto_existente == tipo:
        q_del = "DELETE FROM reaccion WHERE id_apunte=%s AND id_usuario=%s"
        deleteDB(BASE, q_del, (id_apunte, id_usuario))
        voto_actual = None  # voto removido
    else:
        # borramos el voto anterior si habia uno
        if voto_existente:
            q_del = "DELETE FROM reaccion WHERE id_apunte=%s AND id_usuario=%s"
            deleteDB(BASE, q_del, (id_apunte, id_usuario))
        # metemos el voto nuevo
        q_ins = "INSERT INTO reaccion (id_apunte, id_usuario, valor) VALUES (%s, %s, %s)"
        insertDB(BASE, q_ins, (id_apunte, id_usuario, tipo))
        voto_actual = tipo  # voto nuevo activo
    
    # contamos cuantos likes y dislikes tiene ahora
    q_count = "SELECT valor, COUNT(*) FROM reaccion WHERE id_apunte=%s GROUP BY valor"
    filas = selectDB(BASE, q_count, (id_apunte,))
    likes = dislikes = 0
    for tipo_v, count in filas or []:
        if tipo_v == 'like':
            likes = count
        elif tipo_v == 'dislike':
            dislikes = count
    return True, likes, dislikes, voto_actual

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
