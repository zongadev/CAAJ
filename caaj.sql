-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-05-2025 a las 14:41:21
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `caaj`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumno`
--

CREATE TABLE `alumno` (
  `ALU_ID` int(11) NOT NULL,
  `ALU_NOM` varchar(50) NOT NULL,
  `ALU_APE` varchar(50) NOT NULL,
  `ALU_DNI` int(8) NOT NULL,
  `ALU_LEGAJO` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alumno`
--

INSERT INTO `alumno` (`ALU_ID`, `ALU_NOM`, `ALU_APE`, `ALU_DNI`, `ALU_LEGAJO`) VALUES
(1, 'Zonga', 'asasa', 231312, 3213);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `apunte`
--

CREATE TABLE `apunte` (
  `APUN_ID` int(11) NOT NULL,
  `APUN_USU_ID` int(11) NOT NULL,
  `APUN_HEAD` varchar(125) NOT NULL,
  `APUN_BODY` text DEFAULT NULL,
  `APUN_TAGS` varchar(125) DEFAULT NULL,
  `APUN_FECHA_CREACION` date NOT NULL,
  `APUN_MATERIA_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `USU_ID` int(11) NOT NULL,
  `USU_ALU_ID` int(11) NOT NULL,
  `USU_APODO` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`USU_ID`, `USU_ALU_ID`, `USU_APODO`) VALUES
(1, 1, 'Gonza');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alumno`
--
ALTER TABLE `alumno`
  ADD PRIMARY KEY (`ALU_ID`);

--
-- Indices de la tabla `apunte`
--
ALTER TABLE `apunte`
  ADD PRIMARY KEY (`APUN_ID`),
  ADD KEY `APUN_ID` (`APUN_ID`,`APUN_USU_ID`),
  ADD KEY `MATERIA_ID` (`APUN_MATERIA_ID`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`USU_ID`),
  ADD KEY `ALU_ID` (`USU_ALU_ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alumno`
--
ALTER TABLE `alumno`
  MODIFY `ALU_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `apunte`
--
ALTER TABLE `apunte`
  MODIFY `APUN_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `USU_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`USU_ALU_ID`) REFERENCES `alumno` (`ALU_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
