-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 03, 2025 at 01:39 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

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
-- Table structure for table `alumno`
--

CREATE TABLE `alumno` (
  `ALU_ID` int(11) NOT NULL,
  `USU_ID` int(11) NOT NULL,
  `ALU_NOMBRE` varchar(50) NOT NULL,
  `ALU_APELLIDO` varchar(50) NOT NULL,
  `ALU_DNI` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `apunte`
--

CREATE TABLE `apunte` (
  `APU_ID` int(11) NOT NULL,
  `USU_ID` int(11) NOT NULL,
  `MAT_ID` int(11) NOT NULL,
  `APU_HEAD` varchar(100) DEFAULT NULL,
  `APU_CONT` text DEFAULT NULL,
  `APU_TAGS` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `comentario`
--

CREATE TABLE `comentario` (
  `COM_ID` int(11) NOT NULL,
  `USU_ID` int(11) NOT NULL,
  `APU_ID` int(11) NOT NULL,
  `COM_CONTENIDO` text NOT NULL,
  `COM_FECHA` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `materia`
--

CREATE TABLE `materia` (
  `MAT_ID` int(11) NOT NULL,
  `MAT_NOM` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `media`
--

CREATE TABLE `media` (
  `MED_ID` int(11) NOT NULL,
  `APU_ID` int(11) NOT NULL,
  `MED_NOM` varchar(100) DEFAULT NULL,
  `MED_FILE` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reaccion`
--

CREATE TABLE `reaccion` (
  `REA_ID` int(11) NOT NULL,
  `USU_ID` int(11) NOT NULL,
  `APU_ID` int(11) NOT NULL,
  `REA_TYPE` varchar(10) NOT NULL CHECK (`REA_TYPE` in ('like','dislike')),
  `REA_FECHA` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `rol`
--

CREATE TABLE `rol` (
  `ROL_ID` int(11) NOT NULL,
  `ROL_NOM` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `usuario`
--

CREATE TABLE `usuario` (
  `USU_ID` int(11) NOT NULL,
  `ROL_ID` int(11) NOT NULL,
  `USU_APODO` varchar(50) NOT NULL,
  `USU_EMAIL` varchar(100) NOT NULL,
  `USU_CONTRASENA` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alumno`
--
ALTER TABLE `alumno`
  ADD PRIMARY KEY (`ALU_ID`),
  ADD UNIQUE KEY `USU_ID` (`USU_ID`),
  ADD UNIQUE KEY `ALU_DNI` (`ALU_DNI`);

--
-- Indexes for table `apunte`
--
ALTER TABLE `apunte`
  ADD PRIMARY KEY (`APU_ID`),
  ADD KEY `USU_ID` (`USU_ID`),
  ADD KEY `MAT_ID` (`MAT_ID`);

--
-- Indexes for table `comentario`
--
ALTER TABLE `comentario`
  ADD PRIMARY KEY (`COM_ID`),
  ADD KEY `USU_ID` (`USU_ID`),
  ADD KEY `APU_ID` (`APU_ID`);

--
-- Indexes for table `materia`
--
ALTER TABLE `materia`
  ADD PRIMARY KEY (`MAT_ID`);

--
-- Indexes for table `media`
--
ALTER TABLE `media`
  ADD PRIMARY KEY (`MED_ID`),
  ADD KEY `APU_ID` (`APU_ID`);

--
-- Indexes for table `reaccion`
--
ALTER TABLE `reaccion`
  ADD PRIMARY KEY (`REA_ID`),
  ADD UNIQUE KEY `USU_ID` (`USU_ID`,`APU_ID`),
  ADD KEY `APU_ID` (`APU_ID`);

--
-- Indexes for table `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`ROL_ID`),
  ADD UNIQUE KEY `ROL_NOM` (`ROL_NOM`);

--
-- Indexes for table `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`USU_ID`),
  ADD UNIQUE KEY `USU_EMAIL` (`USU_EMAIL`),
  ADD KEY `ROL_ID` (`ROL_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comentario`
--
ALTER TABLE `comentario`
  MODIFY `COM_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `alumno`
--
ALTER TABLE `alumno`
  ADD CONSTRAINT `alumno_ibfk_1` FOREIGN KEY (`USU_ID`) REFERENCES `usuario` (`USU_ID`);

--
-- Constraints for table `apunte`
--
ALTER TABLE `apunte`
  ADD CONSTRAINT `apunte_ibfk_1` FOREIGN KEY (`USU_ID`) REFERENCES `usuario` (`USU_ID`),
  ADD CONSTRAINT `apunte_ibfk_2` FOREIGN KEY (`MAT_ID`) REFERENCES `materia` (`MAT_ID`);

--
-- Constraints for table `comentario`
--
ALTER TABLE `comentario`
  ADD CONSTRAINT `comentario_ibfk_1` FOREIGN KEY (`USU_ID`) REFERENCES `usuario` (`USU_ID`),
  ADD CONSTRAINT `comentario_ibfk_2` FOREIGN KEY (`APU_ID`) REFERENCES `apunte` (`APU_ID`);

--
-- Constraints for table `media`
--
ALTER TABLE `media`
  ADD CONSTRAINT `media_ibfk_1` FOREIGN KEY (`APU_ID`) REFERENCES `apunte` (`APU_ID`);

--
-- Constraints for table `reaccion`
--
ALTER TABLE `reaccion`
  ADD CONSTRAINT `reaccion_ibfk_1` FOREIGN KEY (`USU_ID`) REFERENCES `usuario` (`USU_ID`),
  ADD CONSTRAINT `reaccion_ibfk_2` FOREIGN KEY (`APU_ID`) REFERENCES `apunte` (`APU_ID`);

--
-- Constraints for table `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`ROL_ID`) REFERENCES `rol` (`ROL_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
