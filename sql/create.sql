-- --------------------------------------------------------
-- Tabla rol
-- --------------------------------------------------------
DROP TABLE IF EXISTS `rol`;
CREATE TABLE `rol` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_rol_nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla materia
-- --------------------------------------------------------
DROP TABLE IF EXISTS `materia`;
CREATE TABLE `materia` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `materia` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_materia_nombre` (`materia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla usuario
-- --------------------------------------------------------
DROP TABLE IF EXISTS `usuario`;
CREATE TABLE `usuario` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `apodo` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `pass` VARCHAR(255) NOT NULL,
  `id_rol` INT(11) NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `apellido` VARCHAR(50) NOT NULL,
  `dni` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_usuario_email` (`email`),
  UNIQUE KEY `uniq_usuario_dni` (`dni`),
  KEY `fk_usuario_rol` (`id_rol`),
  CONSTRAINT `usuario_ibfk_rol`
    FOREIGN KEY (`id_rol`)
    REFERENCES `rol` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla apunte
-- --------------------------------------------------------
DROP TABLE IF EXISTS `apunte`;
CREATE TABLE `apunte` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` INT(11) NOT NULL,
  `id_materia` INT(11) NOT NULL,
  `head` VARCHAR(100) DEFAULT NULL,
  `content` TEXT DEFAULT NULL,
  `tags` VARCHAR(200) DEFAULT NULL,
  `fechahora` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_apunte_usuario` (`id_usuario`),
  KEY `fk_apunte_materia` (`id_materia`),
  CONSTRAINT `apunte_ibfk_usuario`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `apunte_ibfk_materia`
    FOREIGN KEY (`id_materia`)
    REFERENCES `materia` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla media
-- --------------------------------------------------------
DROP TABLE IF EXISTS `media`;
CREATE TABLE `media` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `id_apunte` INT(11) NOT NULL,
  `nombre` VARCHAR(100) DEFAULT NULL,
  `path` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_media_apunte` (`id_apunte`),
  CONSTRAINT `media_ibfk_apunte`
    FOREIGN KEY (`id_apunte`)
    REFERENCES `apunte` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla comentario
-- --------------------------------------------------------
DROP TABLE IF EXISTS `comentario`;
CREATE TABLE `comentario` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` INT(11) NOT NULL,
  `id_apunte` INT(11) NOT NULL,
  `content` TEXT NOT NULL,
  `fechahora` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comentario_usuario` (`id_usuario`),
  KEY `fk_comentario_apunte` (`id_apunte`),
  CONSTRAINT `comentario_ibfk_usuario`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `comentario_ibfk_apunte`
    FOREIGN KEY (`id_apunte`)
    REFERENCES `apunte` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla reaccion
-- --------------------------------------------------------
DROP TABLE IF EXISTS `reaccion`;
CREATE TABLE `reaccion` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` INT(11) NOT NULL,
  `id_apunte` INT(11) NOT NULL,
  `valor` ENUM('like','dislike') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_reaccion_usuario_apunte` (`id_usuario`,`id_apunte`),
  KEY `fk_reaccion_usuario` (`id_usuario`),
  KEY `fk_reaccion_apunte` (`id_apunte`),
  CONSTRAINT `reaccion_ibfk_usuario`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `reaccion_ibfk_apunte`
    FOREIGN KEY (`id_apunte`)
    REFERENCES `apunte` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
