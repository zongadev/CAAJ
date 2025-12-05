-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 16, 2025 at 04:09 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.4.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `caaj`
--

-- --------------------------------------------------------

--
-- Table structure for table `apunte`
--

CREATE TABLE `apunte` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL,
  `head` varchar(100) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `tags` varchar(200) DEFAULT NULL,
  `fechahora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `apunte`
--

INSERT INTO `apunte` (`id`, `id_usuario`, `id_materia`, `head`, `content`, `tags`, `fechahora`) VALUES
(1, 1, 1, 'Límites de funciones', 'Definición de límite, ejemplos...', 'cálculo, límites, funciones', '2025-06-10 09:30:00'),
(2, 2, 2, 'Ondas y sonido', 'Ecuación de onda, velocidad...', 'física, ondas, sonido', '2025-06-11 14:45:00'),
(3, 3, 3, 'Rev. Francesa', 'Causas, etapas, consecuencias...', 'historia, revolución, francia', '2025-06-12 11:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `materia`
--

CREATE TABLE `materia` (
  `id` int(11) NOT NULL,
  `materia` varchar(100) NOT NULL,
  `UUID` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `materia`
--

INSERT INTO `materia` (`id`, `materia`, `UUID`) VALUES
(1, 'Matematicas', '101461965318127616'),
(2, 'Fisica', '101461965318127617'),
(3, 'Historia', '101461965318127618');

-- --------------------------------------------------------

--
-- Table structure for table `media`
--

CREATE TABLE `media` (
  `id` int(11) NOT NULL,
  `id_apunte` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `media`
--

INSERT INTO `media` (`id`, `id_apunte`, `nombre`, `path`) VALUES
(1, 1, 'gráfica_límites.png', '/uploads/limites.png'),
(2, 2, 'esquema_ondas.pdf', '/uploads/ondas.pdf'),
(3, 3, 'mapa_francia.jpg', '/uploads/francia.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `rol`
--

CREATE TABLE `rol` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `rol`
--

INSERT INTO `rol` (`id`, `nombre`) VALUES
(3, 'administrador'),
(1, 'alumno'),
(2, 'profesor');

-- --------------------------------------------------------

--
-- Table structure for table `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `apodo` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `dni` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `usuario`
--

INSERT INTO `usuario` (`id`, `apodo`, `email`, `pass`, `id_rol`, `nombre`, `apellido`, `dni`) VALUES
(1, 'juanp', 'juan.perez@uni.edu', 'SierraLuna12', 1, 'Juan', 'Pérez', '12345678'),
(2, 'martav', 'marta.vega@uni.edu', 'RioAmarillo', 1, 'Marta', 'Vega', '87654321'),
(3, 'profc', 'carlos@uni.edu', 'LlaveMaestra', 2, 'Carlos', 'Gómez', '11223344'),
(4, 'Gonza', 'foanfdas@gmail.com', 'a310835U', 1, 'fdsaunbfidu', 'fdbansifdb', '45613771'),
(9, 'Gonzadsa', 'foanfdsadaddas@gmail.com', 'a310835U', 1, 'fdsaunbfidudsdsaa', 'fdbansifddsabdsa', '45613221');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `apunte`
--
ALTER TABLE `apunte`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_apunte_usuario` (`id_usuario`),
  ADD KEY `fk_apunte_materia` (`id_materia`);

--
-- Indexes for table `materia`
--
ALTER TABLE `materia`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uniq_materia_nombre` (`materia`);

--
-- Indexes for table `media`
--
ALTER TABLE `media`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_media_apunte` (`id_apunte`);

--
-- Indexes for table `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uniq_rol_nombre` (`nombre`);

--
-- Indexes for table `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uniq_usuario_email` (`email`),
  ADD UNIQUE KEY `uniq_usuario_dni` (`dni`),
  ADD KEY `fk_usuario_rol` (`id_rol`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `apunte`
--
ALTER TABLE `apunte`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `materia`
--
ALTER TABLE `materia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `media`
--
ALTER TABLE `media`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `rol`
--
ALTER TABLE `rol`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `apunte`
--
ALTER TABLE `apunte`
  ADD CONSTRAINT `apunte_ibfk_materia` FOREIGN KEY (`id_materia`) REFERENCES `materia` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `apunte_ibfk_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `media`
--
ALTER TABLE `media`
  ADD CONSTRAINT `media_ibfk_apunte` FOREIGN KEY (`id_apunte`) REFERENCES `apunte` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_rol` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
