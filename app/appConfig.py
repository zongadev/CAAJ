from os import path 

config = {}

# Directorio del proyecto
# Obtiene el directorio del archivo actual y lo asigna a 'project_folder'
# para cualquier sistema operativo
config['project_folder'] = path.dirname(path.realpath(__file__))

# Directorio para subir archivos (con el path completo)
# Crea una ruta completa para la carpeta 'uploads' dentro del directorio del proyecto
#config['upload_folder'] = path.join(config['project_folder'], 'uploads')
config['upload_folder'] = path.join(config['project_folder'], 'static/uploads')

