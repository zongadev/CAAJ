from flask import request, session,redirect,render_template
from flask import jsonify
from datetime import datetime
from model import *
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from appConfig import config

# aca armamos el menu del header dependiendo si esta logueado o no
def obtenerMenuHead(param):
    if 'id_usuario' in session:
        param["menuHead"]= {
                "mnub01":{"href":"/materias","content":"Materias","class":"nav-button "},
                "mnub02":{"href":"/logout","content":"Cerrar sesión","class":"nav-button"},
                "mnub03":{"href":"/profile","content":"Perfil","class":"nav-button"},
                "mnub04":{"href":"/nuevoapunte","content":"Nuevo apunte","class":"nav-button"}
            }
    else:
        param["menuHead"]= {
                "mnub01":{"href":"/materias","content":"Materias","class":"nav-button"},
                "mnub02":{"href":"/login","content":"Iniciar sesión","class":"login-btn"},
            }

# traemos la info del usuario para mostrarla en el perfil
def obtenerUsuInfo(param,id_usuario):
    result = {}
    obtenerUsuarioPorIdDB(result, id_usuario)
    param['usuario'] = result.get('usuario', {})

# aca traemos todos los apuntes que hizo un usuario        
def obtenerApuntesUsu(param,id_usuario):
    result={}
    obtenerApuntesxUsuario(result, id_usuario)
    param['apuntes'] = result.get('apuntes', []) # si no encuentra nada devuelve lista vacia

# busca los apuntes de una materia especifica, con opcion de busqueda
def obtenerApuntesXMateria(param, materia_id, query=''):
    result={}
    obtenerApuntesXMateriaDB(result, materia_id, query)
    param['apuntes'] = result.get('apuntes', [])

# trae los archivos adjuntos de un apunte
def obtenerMediaXid(param, apunteid):
    result={}
    obtenerMediaXidDB(result,apunteid)
    param['media']=result.get('media',[])

# trae todas las materias disponibles    
def obtenerMaterias(param):
    result={}
    obtenerMateriasDB(result)
    param['materias'] = result.get('materia',[])
    print("Param materias en controller:", param['materias'])

# busca un apunte por su id y le calcula los likes/dislikes
def obtenerApunteXid(param,apunteid):
    result={}
    obtenerApunteXidDB(result,apunteid)
    apunte = result.get('apunte', [])
    if isinstance(apunte, list) and apunte:
        apunte = apunte[0]
    elif not isinstance(apunte, dict):
        apunte = {}
    likes, dislikes = contar_reacciones_apunte(apunteid)
    apunte['likes'] = likes
    apunte['dislikes'] = dislikes
    param['apunte'] = apunte

    
# borra un apunte, chequea que seas el dueño o admin
def borrar_apunte_process():
    rol = session.get('rol')
    id_apunte = request.form.get('id_apunte')
    id_usuario = session.get('id_usuario')
    param = {}
    obtenerApunteXid(param, id_apunte)
    apunte = param.get('apunte', {})
    if not id_usuario or not id_apunte:
        return "No autorizado 22"
    if rol == 3 or (apunte.get('usuario', {}).get('id') == id_usuario):
        exito = borrarApunteDB(id_apunte)
        if exito:
            return redirect('/index')  # manda al index si sale todo bien
        else:
            return "Error al borrar"
    return "No autorizado"

# muestra la pagina para editar un apunte existente
def editar_apunte_pagina(param, id_apunte):
    id_usuario = session.get('id_usuario')
    rol = session.get('rol')
    
    if not id_usuario or not id_apunte:
        return redirect('/index')
    
    obtenerApunteXid(param, id_apunte)
    apunte = param.get('apunte', {})
    
    # chequeamos que seas el dueño o admin para poder editar
    if rol != 3 and apunte.get('usuario', {}).get('id') != id_usuario:
        return "No autorizado"
    
    obtenerMenuHead(param)
    obtenerMaterias(param)
    obtenerMediaXid(param, id_apunte)
    param['editando'] = True
    param['id_apunte'] = id_apunte
    return render_template('nuevoapunte.html', param=param)

# procesa la actualizacion de un apunte existente
def actualizar_apunte_process(request, param):
    id_apunte = request.form.get('id_apunte')
    id_usuario = session.get('id_usuario')
    rol = session.get('rol')
    
    if not id_usuario or not id_apunte:
        return redirect('/index')
    
    # chequeamos permisos antes de hacer nada
    obtenerApunteXid(param, id_apunte)
    apunte = param.get('apunte', {})
    
    if rol != 3 and apunte.get('usuario', {}).get('id') != id_usuario:
        return "No autorizado"
    
    mirequest = {}
    getRequest(mirequest)
    
    exito = actualizarApunte(id_apunte, mirequest)
    
    if exito:
        # si hay archivos nuevos los subimos
        if 'archivo[]' in request.files and any(f.filename for f in request.files.getlist('archivo[]')):
            print(f"DEBUG: Procesando archivos para apunte {id_apunte}")
            file_result = {}
            upload_file(file_result)
            print(f"DEBUG: file_result = {file_result}")
            for archivo_info in file_result.get('archivos', []):
                if archivo_info and not archivo_info.get('file_error'):
                    print(f"DEBUG: Creando media - id_apunte={id_apunte}, nombre={archivo_info['file_name']}, uuid={archivo_info['file_name_new']}")
                    result = crearMedia(id_apunte, archivo_info['file_name'], archivo_info['file_name_new'])
                    print(f"DEBUG: crearMedia resultado = {result}")
        
        return redirect(f'/apunte?apunte={id_apunte}')
    else:
        param['error_msg'] = "Error al actualizar el apunte"
        obtenerMenuHead(param)
        obtenerMaterias(param)
        obtenerMediaXid(param, id_apunte)
        param['editando'] = True
        param['id_apunte'] = id_apunte
        return render_template('nuevoapunte.html', param=param)

# elimina un archivo de un apunte (chequea permisos)
def eliminar_archivo_process(request, param):
    data = request.get_json()
    nombre_archivo = data.get('nombre_archivo')
    id_apunte = data.get('id_apunte')
    id_usuario = session.get('id_usuario')
    rol = session.get('rol')
    
    if not id_usuario or not nombre_archivo or not id_apunte:
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400
    
    # verificamos que puedas borrar archivos de este apunte
    obtenerApunteXid(param, id_apunte)
    apunte = param.get('apunte', {})
    
    if rol != 3 and apunte.get('usuario', {}).get('id') != id_usuario:
        return jsonify({'success': False, 'message': 'No autorizado'}), 403
    
    # borramos el archivo del servidor y la BD
    exito = eliminarArchivoApunte(id_apunte, nombre_archivo)
    
    if exito:
        return jsonify({'success': True, 'message': 'Archivo eliminado'})
    else:
        return jsonify({'success': False, 'message': 'Error al eliminar archivo'}), 500

# trae todos los comentarios de un apunte
def obtenerComentarios(param,apunteid):
    result = {}
    obtenerComentariosDB(result, apunteid)
    param['comentarios'] = result.get('comentarios', [])

    
# crea un nuevo comentario y devuelve el HTML para agregarlo sin recargar
def publicar_comentario_process(param, request):
    id_apunte = request.form.get('id_apunte')
    comentario = request.form.get('comentario', '').strip()
    id_usuario = session.get('id_usuario')
    apodo = session.get('username', 'Anónimo')

    if not id_usuario or not comentario or not id_apunte:
        return '<span class="error-msg">Datos incompletos</span>'

    id_comentario = crearComentario(id_apunte, id_usuario, comentario)
    if id_comentario:
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M')
        # armamos el HTML del comentario con botones de editar/borrar si corresponde
        edit_delete_btns = f'''
            <button class="edit-comment-btn" onclick="editarComentario({id_comentario})" title="Editar comentario">
              ✏️
            </button>
            <form method="post" action="/borrar_comentario" class="inline-form">
              <input type="hidden" name="id_comentario" value="{id_comentario}" />
              <button type="submit" class="delete-btn delete-comment-btn" onclick="return confirm('¿Eliminar este comentario?');">
                🗑️
              </button>
            </form>
        ''' if session.get('id_usuario') == id_usuario or session.get('rol') == 3 else ''
        
        return f'''
        <div class="comment" data-comment-id="{id_comentario}">
          <div class="author">
            <a href="/profile?id_usuario={id_usuario}">
              <strong>{apodo}</strong>
            </a>
            <span class="comment-date">{fecha}</span>
            {edit_delete_btns}
          </div>
          <div class="comment-text" id="comment-text-{id_comentario}">
            {comentario}
          </div>
          <div class="comment-edit" id="comment-edit-{id_comentario}">
            <textarea id="comment-textarea-{id_comentario}" rows="3">{comentario}</textarea>
            <div class="edit-actions">
              <button class="save-comment-btn" onclick="guardarComentario({id_comentario})">Guardar</button>
              <button class="cancel-comment-btn" onclick="cancelarEdicion({id_comentario})">Cancelar</button>
            </div>
          </div>
        </div>
        '''
    else:
        return '<span class="error-msg">Error al guardar el comentario</span>'
    
# procesa un voto (like o dislike) en un apunte    
def votar_apunte_process(data):
    id_apunte = data.get('id_apunte')
    tipo = data.get('tipo')  # puede ser 'like' o 'dislike'
    id_usuario = session.get('id_usuario')
    if not id_usuario or not id_apunte or tipo not in ['like', 'dislike']:
        return jsonify({'success': False, 'msg': 'Datos inválidos'}), 400
    exito, likes, dislikes, voto_actual = votar_apunte_db(id_apunte, id_usuario, tipo)
    return jsonify({'success': exito, 'likes': likes, 'dislikes': dislikes, 'voto_actual': voto_actual})


def index_pagina(param):
    obtenerMenuHead(param)
    obtenerMaterias(param)
    return render_template('index.html',param=param)

# devuelve todas las materias en formato JSON para el buscador
def materiasJSON(param):
    obtenerMaterias(param)
    return jsonify(param['materias'])

# busca en toda la BD (materias y apuntes) y devuelve JSON
def buscarJSON(param, query):
    result = {}
    buscarGlobal(result, query)
    return jsonify(result.get('resultados', []))

# muestra la pagina de login
def login_pagina(param):
    msg = request.args.get('msg')
    if msg:
        param['success_msg'] = msg
    return render_template('login.html',param=param)

# procesa el login del usuario
def logging_process(param,request):
    return ingresoUsuarioValidacion(param,request)

# hace logout y limpia la sesion
def loggout_process():
    try:    
        session.clear()
    except:
        pass
    return login_pagina({})

# muestra la pagina de registro
def register_pagina(param):
    return render_template('register.html',param=param)

# procesa el registro de un nuevo usuario
def register_process(param,request):
    res = ''
    if registrarValidacion():
        res= redirect('/login?msg=El registro fue exitoso')
    else:
        mirequest={}
        getRequest(mirequest)
        param['error_msg_regis']="Error: Hubo un error al registrarse, intentelo de vuelta"
        param['form_data'] = mirequest
        res = register_pagina(param)
    return res  

def materias_pagina(param):
    obtenerMenuHead(param)
    obtenerMaterias(param)
    return render_template("materias.html",param=param)

def profile_pagina(param,id_usuario):
    obtenerMenuHead(param)
    obtenerUsuInfo(param,id_usuario)
    obtenerApuntesUsu(param,id_usuario)
    return render_template('profile.html',param=param)

# publica un nuevo apunte y maneja la subida de archivos
def publicar_process(request, param):
    id_apunte = cargarApunte(request)
    if id_apunte:
        # si sale todo bien manda al apunte recien creado
        return redirect(f'/apunte?apunte={id_apunte}')
    else:
        param['error_msg'] = "Error al crear el apunte"
        obtenerMenuHead(param)
        obtenerMaterias(param)
        return render_template('nuevoapunte.html', param=param)

# crea un apunte nuevo y sube los archivos adjuntos
def cargarApunte(request):
    mirequest = {}
    
    getRequest(mirequest)
    id_apunte = crearApunte(mirequest, session['id_usuario'])
    if id_apunte is not None:
        if 'archivo[]' in request.files and any(f.filename for f in request.files.getlist('archivo[]')): # chequea si realmente hay archivos
            file_result = {}
            upload_file(file_result)
            for archivo_info in file_result.get('archivos', []):
                if archivo_info and not archivo_info.get('file_error'):
                    crearMedia(id_apunte, archivo_info['file_name'], archivo_info['file_name_new'])

    return id_apunte
        
    
# muestra todos los apuntes de una materia (con opcion de busqueda)
def listaapuntes_pagina(param, materia_id, query=''):
    obtenerApuntesXMateria(param, materia_id, query)
    obtenerMenuHead(param)
    if param['apuntes']:
        param['nombre_materia'] = param['apuntes'][0]['nombre_materia']
    else:
        # si no hay apuntes buscamos el nombre de la materia igual
        param['nombre_materia'] = obtenerNombreMateriaPorId(materia_id)
    return render_template('buscador.html',param=param)


def nuevoapunte_pagina(param):
    obtenerMenuHead(param)
    obtenerMaterias(param)
    return render_template('nuevoapunte.html',param=param)


def ingresoUsuarioValidacion(param, request):
    '''
    Valida el usuario y el pass contra la BD.
    recibe 'param' dict de parámetros
    recibe 'request' una solicitud http con los datos usuario y pass
    retorna: 
        Si es valido el usuario y pass => crea una session y retorna 
        la pagina home.
        Si NO es valido el usuario y pass => retorna la pagina login
        y agrega en el diccionario de parámetros una clave con un mensaje 
        de error para ser mostrada en la pagina login.
    '''

    if crearSesion():
        res=redirect('home') # redirige a home para que no quede /logging en la URL
    else:
        param['error_msg_login']="Error: Usuario y/o password inválidos"
        res= login_pagina(param)       
    return res  

def crearSesion():
    '''
    Crea una sesion. Consulta si los datos recibidos son validos.
    Si son validos carga una sesion con los datos del usuario
    no recibe request pq getRequest usa el global y no el del parametro
    retorna True si se logra un session, False caso contrario
    '''
    sesionValida=False
    mirequest={}
    try: 
        # carga los datos del formulario en mirequest          
        getRequest(mirequest)
        # consulta a la BD si el usuario y pass son correctos
        dicUsuario={}
        if obtenerUsuarioXEmailPass(dicUsuario,mirequest.get("mail"),mirequest.get("password")):
            # si esta todo ok carga la sesion
            cargarSesion(dicUsuario)
            sesionValida = True
    except ValueError:                              
        pass
    return sesionValida

def cargarSesion(dicUsuario):
    '''
    Realiza la carga de datos del usuario
    en la variable global dict 'session'.
    recibe 'dicUsuario' que es un diccionario con datos
    de un usuario.
    Comentario: Usted puede agregar en 'session' las claves que necesite
    '''
    print(dicUsuario,"dictUsuario")
    session['id_usuario'] = dicUsuario['id']
    session['username']     = dicUsuario['apodo']
    session['email']   = dicUsuario['email']
    session['rol']   = dicUsuario['id_rol']
    session['nombre']     = dicUsuario['nombre'] 
    session['apellido']        = dicUsuario['apellido'] 
    session['dni']       =  dicUsuario['dni'] 
    session["time"]       = datetime.now()  

# valida y crea un usuario nuevo
def registrarValidacion():
    # getRequest maneja request de forma global
    mirequest={}
    registroValido=False
    try:
        getRequest(mirequest)
        if(crearUsuario(mirequest)==1):
            registroValido=True
    except:
        pass
    finally:
        return registroValido

# muestra la pagina de un apunte con todos sus detalles
def apunte_pagina(param,apunteid):
    obtenerMenuHead(param)
    obtenerApunteXid(param,apunteid)
    obtenerMediaXid(param,apunteid)
    obtenerComentarios(param,apunteid)
    
    # si esta logueado traemos su voto para mostrar cual boton esta activo
    id_usuario = session.get('id_usuario')
    if id_usuario:
        obtenerVotoUsuario(param, apunteid, id_usuario)
    
    return render_template('apunte.html',param=param)
    
    

# extrae los datos de un request (POST o GET) y los mete en un diccionario
def getRequest(diResult):
    if request.method == 'POST':
        for name in request.form.to_dict().keys():
            li = request.form.getlist(name)
            if len(li) > 1:
                diResult[name] = request.form.getlist(name)
            elif len(li) == 1:
                diResult[name] = li[0]
            else:
                diResult[name] = ""
    elif request.method == 'GET':
        for name in request.args.to_dict().keys():
            li = request.args.getlist(name)
            if len(li) > 1:
                diResult[name] = request.args.getlist(name)
            elif len(li) == 1:
                diResult[name] = li[0]
            else:
                diResult[name] = ""     
                
# maneja la subida de archivos, valida extensiones y tamaño
def upload_file(diResult):
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.jpeg', '.pdf', '.doc', '.docx']
    MAX_CONTENT_LENGTH = 1024 * 1024 * 5  # maximo 5MB por archivo
    if request.method == 'POST':
        print(request.files.getlist('archivo[]'),"dsadadas")
        files = request.files.getlist('archivo[]')
        diResult['archivos'] = []
        for f in files:
            file_info = {}
            file_info['file_error'] = False
            if f and f.filename != "":
                file_extension = str(os.path.splitext(f.filename)[1]).lower()
                filename_unique = str(uuid4()) + file_extension
                path_filename = os.path.join(config['upload_folder'], filename_unique)
                if file_extension not in UPLOAD_EXTENSIONS:
                    file_info['file_error'] = True
                    file_info['file_msg'] = 'Error: No se admite subir archivos con extensión ' + file_extension
                elif os.path.exists(path_filename):
                    file_info['file_error'] = True
                    file_info['file_msg'] = 'Error: el archivo ya existe.'
                    file_info['file_name'] = f.filename
                else:
                    try:
                        f.save(path_filename)
                        file_info['file_error'] = False
                        file_info['file_name_new'] = filename_unique
                        file_info['file_name'] = f.filename
                        file_info['file_msg'] = 'OK. Archivo cargado exitosamente'
                    except Exception as e:
                        file_info['file_error'] = True
                        file_info['file_msg'] = f'Se ha producido un error: {e}'
            diResult['archivos'].append(file_info)

# borra un comentario (solo si sos el dueño o admin)
def borrar_comentario_process():
    id_comentario = request.form.get('id_comentario')
    id_usuario = session.get('id_usuario')
    rol = session.get('rol')
    # traemos el comentario para verificar quien es el dueño
    comentario = obtenerComentarioPorId(id_comentario)
    if not id_usuario or not id_comentario:
        return "No autorizado"
    if rol == 3 or (comentario and comentario['id_usuario'] == id_usuario):
        exito = borrarComentarioDB(id_comentario)
        if exito:
            return redirect(request.referrer or '/apunte?apunte=' + str(comentario['id_apunte']))
        else:
            return "Error al borrar"
    return "No autorizado"

# actualiza el contenido de un comentario existente
def actualizar_comentario_process():
    data = request.get_json()
    id_comentario = data.get('id_comentario')
    contenido = data.get('contenido', '').strip()
    id_usuario = session.get('id_usuario')
    rol = session.get('rol')
    
    if not id_usuario or not id_comentario or not contenido:
        return jsonify({'success': False, 'msg': 'Datos incompletos'})
    
    # verificamos que puedas editar este comentario
    comentario = obtenerComentarioPorId(id_comentario)
    if not comentario:
        return jsonify({'success': False, 'msg': 'Comentario no encontrado'})
    
    if rol != 3 and comentario['id_usuario'] != id_usuario:
        return jsonify({'success': False, 'msg': 'No autorizado'})
    
    exito = actualizarComentario(id_comentario, contenido)
    
    if exito:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'msg': 'Error al actualizar el comentario'})