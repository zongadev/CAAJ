from flask import render_template             # https://flask.palletsprojects.com/en/2.3.x/tutorial/templates/
from flask import redirect, url_for, request  # redirect: redirigir a otras rutas # url_for: generar URLs dinámicamente # request: gestiona las solicitudes http recibidas 
from werkzeug.utils import secure_filename    # Valida caracteres seguros en el nombre del un archivo
from appConfig import config                  # Archivo de configuracion de la aplicación
from uuid import uuid4                        # Crea Universally Unique IDentifier (UUID)  # https://docs.python.org/es/3/library/uuid.html#uuid.UUID
import os                                     # Gestiona acceso al sistema operativo local


#Esto es el copypaste del prfoe hayu que ajustarlo, no me voy a poner ahora xd
def route(app):

    @app.route("/home")  # Dos formas de acceder al home
    def home():
        cab="Bienvenido al Sistema ABC"
        colMed="Esto es una prueba de JINJA 2"
        pie="ABC"
        return render_template('layout_flex.html', header=cab,colMiddle=colMed,footer=pie)

    @app.route('/login')
    def login():
        return render_template('sigin.html',mensaje="Ingrese su Nombre de usuario: ")

    @app.route('/form') # PROBAR FORMULARIO PARA VER INTERACCION CON EL SERVIDOR
    def form():
        return render_template('form_pruebas.html')  
     
    @app.route('/recibir_datos',methods = ['POST', 'GET']) # post y get ver diferencias
    def formrecibe():
        diRequest={}            # Inicializa un diccionario vacío para almacenar los datos de la solicitud
        getRequest(diRequest)    # Llena el diccionario con datos de la solicitud (ya sea POST o GET)
        upload_file(diRequest)  # Maneja la carga de archivos y actualiza el diccionario con la información de la carga de archivos
        return diRequest        # Devuelve el diccionario que contiene todos los datos de la solicitud y la información de la carga de archivos
    @app.route('/verimagen')
    def verimagen():
        return render_template('verimagen.html')

    @app.route('/menu')
    def menu():
        param={}
        obtenerDatosMenu(param)
        return render_template('menu.html',param=param)
    
    @app.route('/<name>') # dinámico
    def general(name):
        if name=="tabla":
            param={}
            obtenerDatosTabla(param)
            res= render_template('tabla.html', param=param)
        else:
            res='Pagina "{}" no encontrada'.format(name)
        return res

def getRequest(diResult):  # Función para obtener los datos de la solicitud y almacenarlos en un diccionario
    if request.method=='POST':                    # Si el método de la solicitud es POST
        for name in request.form.to_dict().keys():  # Itera sobre las claves del formulario
            li=request.form.getlist(name)           # Obtiene la lista de valores para cada clave
            if len(li)>1:                           # Si hay más de un valor
                diResult[name]=request.form.getlist(name)  # Almacena la lista de valores en el diccionario
            elif len(li)==1:                        # Si hay un solo valor
                diResult[name]=li[0]                # Almacena el valor en el diccionario
            else:                                   # Si no hay valores
                diResult[name]=""                   # Almacena una cadena vacía en el diccionario
    elif request.method=='GET':                   # Si el método de la solicitud es GET
        for name in request.args.to_dict().keys():  # Itera sobre las claves de los argumentos
            li=request.args.getlist(name)           # Obtiene la lista de valores para cada clave
            if len(li)>1:                           # Si hay más de un valor
                diResult[name]=request.args.getlist(name)  # Almacena la lista de valores en el diccionario
            elif len(li)==1:                        # Si hay un solo valor
                diResult[name]=li[0]                # Almacena el valor en el diccionario
            else:                                   # Si no hay valores
                diResult[name]=""                   # Almacena una cadena vacía en el diccionario

 
def upload_file (diResult) :
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
    MAX_CONTENT_LENGTH = 1024 * 1024     
    if request.method == 'POST' :         
        for key in request.files.keys():  
            diResult[key]={} 
            diResult[key]['file_error']=False            
            
            f = request.files[key] 
            if f.filename!="":     
                #filename_secure = secure_filename(f.filename)
                file_extension=str(os.path.splitext(f.filename)[1])
                filename_unique = uuid4().__str__() + file_extension
                path_filename=os.path.join( config['upload_folder'] , filename_unique)
                # Validaciones
                if file_extension not in UPLOAD_EXTENSIONS:
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: No se admite subir archivos con extension '+file_extension
                if os.path.exists(path_filename):
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: el archivo ya existe.'
                    diResult[key]['file_name']=f.filename
                try:
                    if not diResult[key]['file_error']:
                        diResult[key]['file_error']=True
                        diResult[key]['file_msg']='Se ha producido un error.'

                        f.save(path_filename)   
                        diResult[key]['file_error']=False
                        diResult[key]['file_name_new']=filename_unique
                        diResult[key]['file_name']=f.filename
                        diResult[key]['file_msg']='OK. Archivo cargado exitosamente'
 
                except:
                        pass
            else:
                diResult[key]={} # viene vacio el input del file upload

    # si existe el archivo devuelve True
    # os.path.exists(os.path.join('G:\\directorio\\....\\uploads',"agua.png"))

    # borrar un archivo
    # os.remove(os.path.join('G:\\directorio\\.....\\uploads',"agua.png"))


def obtenerDatosMenu(param):
    param["menu"]= [{"href":"/home","contenido":"Home"},
                    {"href":"/login","contenido":"Log In"},
                    {"href":"/logout","contenido":"Log Out"},
                    {"href":"/About","contenido":"About"}
                    #{"href":"#","contenido":'&#128587'}#1F64B  # &#128587; #u'\u2630'
                   ]
   

def obtenerDatosTabla(param):
    param['titulo']="El titulo principal tabla"
    param['parrafo_01']="Esto es una prueba con una tabla"
    param['tabla']={"titulos":["NOMBRE","APELLIDO","DNI","EDAD"],
                      "datos":[["Juan","Perez",1234,23],
                              ["Laura","Lopez",9632,55],
                              ["Lucia","Marano",8775,28],
                              ["Pablo","Cuti",7744,63]
                        ]
                    }

    