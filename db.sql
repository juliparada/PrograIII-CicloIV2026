-- phpMyAdmin SQL Dump
-- Database: `db_academica`

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `db_academica`;
USE `db_academica`;

-- --------------------------------------------------------

--
-- Table structure for table `usuarios_usss025125`
--

CREATE TABLE IF NOT EXISTS `usuarios_usss025125` (
  `idUsuario` int(10) NOT NULL AUTO_INCREMENT,
  `usuario` char(35) NOT NULL,
  `clave` char(35) NOT NULL,
  `nombre` char(85) NOT NULL,
  `direccion` char(100) DEFAULT NULL,
  `telefono` char(9) DEFAULT NULL,
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `usuarios_usss025125`
--

INSERT INTO `usuarios_usss025125` (`idUsuario`, `usuario`, `clave`, `nombre`, `direccion`, `telefono`) VALUES
(1, 'admin', '12345', 'Administrador General', 'San Salvador, El Salvador', '7890-1234');

COMMIT;
