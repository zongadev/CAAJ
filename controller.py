from flask import request, session,redirect,render_template
from flask import jsonify
from datetime import datetime
from model import *
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from appConfig import config

def obtenerMenuHead(param):
    if 'id_usuario' in session:
        param["menuHead"]= {
                "mnub01":{"href":"/materias","content":"Materais","class":"nav-button "},
                "mnub02":{"href":"/logout","content":"Log Out","class":"nav-button"},
                "mnub03":{"href":"/profile","content":"Perfil","class":"nav-button"},
                "mnub04":{"href":"/nuevoapunte","content":"Nuevo apunte","class":"nav-button"}
            }
    else:
        param["menuHead"]= {
                "mnub01":{"href":"/login","content":"Iniciar sesion","class":"login-btn"},
            }

def obtenerUsuInfo(param,id_usuario):
    result = {}
    obtenerUsuarioPorIdDB(result, id_usuario)
    param['usuario'] = result.get('usuario', {})
        
def obtenerApuntesUsu(param,id_usuario):
    result={}
    obtenerApuntesxUsuario(result, id_usuario)
    param['apuntes'] = result.get('apuntes', []) #si no encuentra la key apuntes devuelve []

def obtenerApuntesXMateria(param, materia_id):
    result={}
    obtenerApuntesXMateriaDB(result,materia_id)
    param['apuntes'] = result.get('apuntes', [])

def obtenerMediaXid(param, apunteid):
    result={}
    obtenerMediaXidDB(result,apunteid)
    param['media']=result.get('media',[])
    
def obtenerMaterias(param):
    result={}
    obtenerMateriasDB(result)
    param['materias'] = result.get('materia',[])

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
            return redirect('/index')  # O donde quieras redirigir
        else:
            return "Error al borrar"
    return "No autorizado"

def obtenerComentarios(param,apunteid):
    result = {}
    obtenerComentariosDB(result, apunteid)
    param['comentarios'] = result.get('comentarios', [])

    
def publicar_comentario_process(param, request):
    id_apunte = request.form.get('id_apunte')
    comentario = request.form.get('comentario', '').strip()
    id_usuario = session.get('id_usuario')
    apodo = session.get('username', 'Anónimo')

    if not id_usuario or not comentario or not id_apunte:
        return '<span class="error-msg">Datos incompletos</span>'

    exito = crearComentario(id_apunte, id_usuario, comentario)
    if exito:
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M')
        # Devuelve el HTML del nuevo comentario
        return f'''
        <div class="comment">
          <div class="author">
            <a href="/profile?id_usuario={id_usuario}">
              <strong>{apodo}</strong>
            </a>
            <span class="comment-date">{fecha}</span>
          </div>
          <div class="comment-text">
            {comentario}
          </div>
        </div>
        '''
    else:
        return '<span class="error-msg">Error al guardar el comentario</span>'
    
def votar_apunte_process(data):
    id_apunte = data.get('id_apunte')
    tipo = data.get('tipo')  # 'like' o 'dislike'
    id_usuario = session.get('id_usuario')
    if not id_usuario or not id_apunte or tipo not in ['like', 'dislike']:
        return jsonify({'success': False, 'msg': 'Datos inválidos'}), 400
    exito, likes, dislikes = votar_apunte_db(id_apunte, id_usuario, tipo)
    return jsonify({'success': exito, 'likes': likes, 'dislikes': dislikes})


def index_pagina(param):
    obtenerMenuHead(param)
    return render_template('index.html',param=param)

def materiasJSON(param):
    obtenerMaterias(param)
    return jsonify(param['materias']) #devuelve un json con todfas las materias

def login_pagina(param):
    msg = request.args.get('msg')
    if msg:
        param['success_msg'] = msg
    return render_template('login.html',param=param)


def logging_process(param,request):
    return ingresoUsuarioValidacion(param,request)

def loggout_process():
    try:    
        session.clear()
    except:
        pass
    return login_pagina({})

def register_pagina(param):
    return render_template('register.html',param=param)

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

def publicar_process(request, param):
    exito = cargarApunte(request)
    if exito:
        param['success_msg'] = "¡El apunte se cargó con éxito!"
    obtenerMenuHead(param)
    obtenerMaterias(param)
    return render_template('nuevoapunte.html', param=param)

def cargarApunte(request):
    mirequest = {}
    carga = False
    
    getRequest(mirequest)
    id_apunte = crearApunte(mirequest, session['id_usuario'])
    carga=True
    if id_apunte is not None:
        if 'archivo[]' in request.files and any(f.filename for f in request.files.getlist('archivo[]')): #hay que chequear lo del nombre pq no viene vacio si no hay nada adjunto
            file_result = {}
            upload_file(file_result)
            for archivo_info in file_result.get('archivos', []):
                if archivo_info and not archivo_info.get('file_error'):
                    crearMedia(id_apunte, archivo_info['file_name'], archivo_info['file_name_new'])

    return carga
        
    
def listaapuntes_pagina(param,materia_id):
    obtenerApuntesXMateria(param,materia_id)
    obtenerMenuHead(param)
    if param['apuntes']:
        param['nombre_materia'] = param['apuntes'][0]['nombre_materia']
    else:
        # Buscar el nombre de la materia por id (debes tener esta función)
        param['nombre_materia'] = obtenerNombreMateriaPorId(materia_id)
    return render_template('buscador.html',param=param)


def nuevoapunte_pagina(param):
    obtenerMenuHead(param)
    obtenerMaterias(param)
    return render_template('nuevoapunte.html',param=param)


def ingresoUsuarioValidacion(param, request):
    '''info:
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
        res=redirect('home') #para que no te quede el url en logging
    else:
        param['error_msg_login']="Error: Usuario y/o password inválidos"
        res= login_pagina(param)       
    return res  

def crearSesion():
    '''info:
        Crea una sesion. Consulta si los datos recibidos son validos.
        Si son validos carga una sesion con los datos del usuario
        no recibe request pq getRequest usa el global y no el del parametro
        retorna True si se logra un session, False caso contrario
    '''
    sesionValida=False
    mirequest={}
    try: 
        #Carga los datos recibidos del form cliente en el dict 'mirequest'.          
        getRequest(mirequest)
        # CONSULTA A LA BASE DE DATOS. Si usuario es valido => crea session
        dicUsuario={}
        if obtenerUsuarioXEmailPass(dicUsuario,mirequest.get("mail"),mirequest.get("password")):
            # Carga sesion (Usuario validado)
            cargarSesion(dicUsuario)
            sesionValida = True
    except ValueError:                              
        pass
    return sesionValida

def cargarSesion(dicUsuario):
    '''info:
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

def registrarValidacion():
    #request lo maneja de forma global
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

def apunte_pagina(param,apunteid):
    obtenerMenuHead(param)
    obtenerApunteXid(param,apunteid)
    obtenerMediaXid(param,apunteid)
    obtenerComentarios(param,apunteid)
    return render_template('apunte.html',param=param)
    
    

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
                
def upload_file(diResult):
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.jpeg', '.pdf', '.doc', '.docx']
    MAX_CONTENT_LENGTH = 1024 * 1024 * 5  # 5MB
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

def borrar_comentario_process():
    id_comentario = request.form.get('id_comentario')
    id_usuario = session.get('id_usuario')
    rol = session.get('rol')
    # Obtener el comentario para verificar el dueño
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