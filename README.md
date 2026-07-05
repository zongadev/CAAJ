# CAAJ

Proyecto realizado para la asignatura **Programación Web** de la UCA (Universidad Centroamericana). Grupo **CAAJ**.

Es una aplicación web construida con **Flask** que muestra el uso de plantillas **Jinja2**, formularios, subida de imágenes y conexión a una base de datos **MySQL**.

## Tecnologías

- **Python 3** con **Flask** — servidor web y rutas
- **Jinja2** — plantillas HTML (`templates/`)
- **MySQL** (`mysql-connector-python`) — base de datos
- **HTML / CSS** — recursos estáticos (`static/`)

## Estructura del proyecto

| Archivo / carpeta | Descripción |
| --- | --- |
| `run.py` | Punto de entrada: crea la app Flask y la ejecuta |
| `route.py` | Definición de las rutas (`/home`, `/login`, `/form`, `/menu`, ...) |
| `appConfig.py` | Configuración de la app (rutas de proyecto y de subida de archivos) |
| `model.py` | Lógica de acceso a datos (p. ej. crear usuario) |
| `_mysql_db.py` | Funciones de conexión y consultas a MySQL |
| `templates/` | Plantillas HTML (Jinja2) |
| `static/` | Archivos estáticos (CSS, imágenes, `uploads/`) |
| `sql/` | Scripts SQL de la base de datos |
| `docs/` | Documentación del proyecto |

## Requisitos previos

- Python 3.8 o superior
- Un servidor MySQL en funcionamiento

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/zongadev/CAAJ.git
   cd CAAJ
   ```

2. (Recomendado) crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux / macOS
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install flask mysql-connector-python
   ```

4. Crea la base de datos importando el script de la carpeta `sql/`:

   ```bash
   mysql -u root -p < sql/caaj.sql
   ```

## Ejecución

```bash
python run.py
```

La aplicación quedará disponible en http://localhost:5000 (por ejemplo, http://localhost:5000/home).

## Rutas principales

| Ruta | Descripción |
| --- | --- |
| `/home` | Página de inicio |
| `/login` | Formulario de inicio de sesión |
| `/form` | Formulario de pruebas |
| `/menu` | Menú de navegación |
| `/tabla` | Tabla de datos de ejemplo |

## Grupo CAAJ

Proyecto académico desarrollado por el grupo CAAJ para la asignatura Programación Web de la UCA.
