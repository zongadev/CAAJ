-- --------------------------------------------------------
-- 1. Tabla rol
-- --------------------------------------------------------
INSERT INTO `rol` (`nombre`)
VALUES
  ('alumno'),
  ('profesor'),
  ('administrador');
-- Al omitir `id`, AUTO_INCREMENT asigna 1, 2 y 3 respectivamente.

-- --------------------------------------------------------
-- 2. Tabla materia
-- --------------------------------------------------------
INSERT INTO `materia` (`materia`)
VALUES
  ('Matemáticas'),
  ('Física'),
  ('Historia');
-- `materia` es UNIQUE, así evitamos duplicados.

-- --------------------------------------------------------
-- 3. Tabla usuario
-- --------------------------------------------------------
INSERT INTO `usuario`
  (`apodo`,  `email`,              `pass`,           `id_rol`, `nombre`, `apellido`, `dni`)
VALUES
  ('juanp',  'juan.perez@uni.edu', 'SierraLuna',     1,        'Juan',   'Pérez',   '12345678'),
  ('martav', 'marta.vega@uni.edu', 'RioAmarillo',    1,        'Marta',  'Vega',    '87654321'),
  ('profc',  'carlos@uni.edu',     'LlaveMaestra',   2,        'Carlos', 'Gómez',   '11223344');
/*
 - `pass` en claro para pruebas: palabras compuestas fáciles de recordar.
 - El motor autoasigna `id` al ser AUTO_INCREMENT.
 - `email` y `dni` quedan garantizados como únicos.
*/

-- --------------------------------------------------------
-- 4. Tabla apunte
-- --------------------------------------------------------
INSERT INTO `apunte`
  (`id_usuario`, `id_materia`, `head`,                   `content`,                        `tags`,                         `fechahora`)
VALUES
  (1,             1,            'Límites de funciones', 'Definición de límite, ejemplos...', 'cálculo, límites, funciones',  '2025-06-10 09:30:00'),
  (2,             2,            'Ondas y sonido',      'Ecuación de onda, velocidad...',      'física, ondas, sonido',        '2025-06-11 14:45:00'),
  (3,             3,            'Rev. Francesa',       'Causas, etapas, consecuencias...',     'historia, revolución, francia','2025-06-12 11:00:00');
/* 
 - `tags` separado por comas para búsquedas con LIKE.
 - `fechahora` en DATETIME para orden cronológico.
*/

-- --------------------------------------------------------
-- 5. Tabla media
-- --------------------------------------------------------
INSERT INTO `media`
  (`id_apunte`, `nombre`,               `path`)
VALUES
  (1,            'gráfica_límites.png', '/uploads/limites.png'),
  (2,            'esquema_ondas.pdf',   '/uploads/ondas.pdf'),
  (3,            'mapa_francia.jpg',    '/uploads/francia.jpg');

-- --------------------------------------------------------
-- 6. Tabla comentario
-- --------------------------------------------------------
INSERT INTO `comentario`
  (`id_usuario`, `id_apunte`, `content`,                                `fechahora`)
VALUES
  (2,             1,            'Muy útil la explicación de los límites.',      '2025-06-10 12:00:00'),
  (1,             2,            '¿Podrías añadir más ejemplos de resonancia?', '2025-06-11 16:20:00'),
  (1,             3,            'Excelente resumen de la Revolución.',         '2025-06-12 12:15:00');

-- --------------------------------------------------------
-- 7. Tabla reaccion
-- --------------------------------------------------------
INSERT INTO `reaccion`
  (`id_usuario`, `id_apunte`, `valor`)
VALUES
  (1,             1,           ' like'),   -- like
  (2,             1,            'dislike'),   -- like
  (1,             2,           'like'),   -- dislike
  (3,             3,            'dislike');   -- like
/*
 - Asegura cálculos directos de puntaje con SUM(valor).
 - La columna `valor` debe estar definida como TINYINT o SMALLINT.
*/
