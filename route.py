from flask import render_template             # https://flask.palletsprojects.com/en/2.3.x/tutorial/templates/
from flask import redirect, url_for, request  # redirect: redirigir a otras rutas # url_for: generar URLs dinámicamente # request: gestiona las solicitudes http recibidas 
from werkzeug.utils import secure_filename    # Valida caracteres seguros en el nombre del un archivo
from appConfig import config                  # Archivo de configuracion de la aplicación
from uuid import uuid4                        # Crea Universally Unique IDentifier (UUID)  # https://docs.python.org/es/3/library/uuid.html#uuid.UUID
import os                                     # Gestiona acceso al sistema operativo local
from controller import *
from flask import send_from_directory

#Esto es el copypaste del prfoe hayu que ajustarlo, no me voy a poner ahora xd
def route(app):
    @app.route("/")
    @app.route("/home")
    @app.route("/index")  # Dos formas de acceder al home
    def home():
        param={}
        return index_pagina(param)

    @app.route('/login')
    def login():
        param={}
        return login_pagina(param)
    
    @app.route('/logging', methods=['POST'])
    def logging():
        param={}
        return logging_process(param,request)
    
    @app.route('/logout')
    def loggout():
        return loggout_process()
    
    @app.route('/register')
    def register():
        param={}
        return register_pagina(param)
    
    @app.route('/registrando', methods=['POST'])
    def registrando():
        param={}
        return register_process(param,request)
    
    @app.route('/profile')
    def profile():
        perfil_id= request.args.get('id_usuario') or session.get('id_usuario')
        param={}
        return profile_pagina(param,perfil_id)
    
    @app.route('/votar_apunte', methods=['POST'])
    def votar_apunte():
        data= request.get_json()
        return votar_apunte_process(data)
    
    
    @app.route('/borrar_apunte', methods = ['POST'])
    def borrar_apunte():
        return borrar_apunte_process()
        
    @app.route('/publicar_comentario', methods =['POST'])
    def publicar_cometario():
        param={}
        return publicar_comentario_process(param,request)
    
    @app.route('/borrar_comentario', methods=['POST'])
    def borrar_comentario():
        return borrar_comentario_process()
    
    @app.route('/materias')
    def materias():
        param = {}
        return materias_pagina(param)
        
    @app.route('/buscador')
    def buscador():
        materia_id = request.args.get('materia') #este request es un get, flask utiliza por defecto get si no le aclaras
        param={}
        return listaapuntes_pagina(param,materia_id)
    
    @app.route('/apunte')
    def apunte():
        apunte_id = request.args.get('apunte')
        param={}
        return apunte_pagina(param,apunte_id)
    
    @app.route('/<name>') # dinámico
    def general(name):
        res='Pagina "{}" no encontrada'.format(name)
        return res

    @app.route('/api/materias')
    def api_materias():
        param ={}
        return materiasJSON(param)
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory('uploads', filename)
    
    @app.route('/nuevoapunte')
    def editor():
        param ={}
        return nuevoapunte_pagina(param)
    
    @app.route('/publicar', methods = ['POST'])
    def publicar():
        param={}
        return publicar_process(request,param)
        
        

    # si existe el archivo devuelve True
    # os.path.exists(os.path.join('G:\\directorio\\....\\uploads',"agua.png"))

    # borrar un archivo
    # os.remove(os.path.join('G:\\directorio\\.....\\uploads',"agua.png"))

