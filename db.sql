-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 21, 2026 at 08:43 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `db_sistema_impuestos`
--

-- --------------------------------------------------------

--
-- Table structure for table `clientes`
--

CREATE TABLE `clientes` (
  `idCliente` int(10) NOT NULL,
  `codigo` char(10) NOT NULL,
  `nombre` char(100) NOT NULL,
  `direccion` char(150) NOT NULL,
  `telefono` char(10) NOT NULL,
  `email` char(150) NOT NULL,
  `tipo` char(10) NOT NULL DEFAULT 'particular'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`idCliente`, `codigo`, `nombre`, `direccion`, `telefono`, `email`, `tipo`) VALUES
(1, '001', 'Luis Hernandez', 'Usulutan', '4545-3256', 'luishernandez@ugb.edu.sv', 'particular');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_tarifaria`
--

CREATE TABLE `tabla_tarifaria` (
  `idTarifa` int(10) NOT NULL,
  `desde` decimal(12,2) NOT NULL,
  `hasta` decimal(12,2) NOT NULL,
  `precio_base` decimal(10,2) NOT NULL,
  `adicional` decimal(10,2) NOT NULL,
  `porcentaje` decimal(5,2) NOT NULL DEFAULT 0.00
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tabla_tarifaria`
--

INSERT INTO `tabla_tarifaria` (`idTarifa`, `desde`, `hasta`, `precio_base`, `adicional`, `porcentaje`) VALUES
(1, 0.01, 500.00, 1.50, 0.00, 0.00),
(2, 500.01, 1000.00, 1.50, 3.00, 0.00),
(3, 1000.01, 2000.00, 3.00, 3.00, 0.00),
(4, 2000.01, 3000.00, 6.00, 3.00, 0.00),
(5, 3000.01, 6000.00, 9.00, 2.00, 0.00),
(6, 8000.01, 18000.00, 15.00, 2.00, 0.00),
(7, 18000.01, 30000.00, 39.00, 2.00, 0.00),
(8, 30000.01, 60000.00, 63.00, 1.00, 0.00),
(9, 60000.01, 100000.00, 93.00, 0.80, 0.00),
(10, 100000.01, 200000.00, 125.00, 0.70, 0.00),
(11, 200000.01, 300000.00, 195.00, 0.60, 0.00),
(12, 300000.01, 400000.00, 255.00, 0.45, 0.00),
(13, 400000.01, 500000.00, 300.00, 0.40, 0.00),
(14, 500000.01, 1000000.00, 340.00, 0.30, 0.00),
(15, 1000000.01, 99999999.99, 490.00, 0.18, 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `balances`
--

CREATE TABLE `balances` (
  `idBalance` int(10) NOT NULL,
  `codigo` char(10) NOT NULL,
  `desde` date NOT NULL,
  `hasta` date NOT NULL,
  `balance` decimal(12,2) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `estado` varchar(50) NOT NULL DEFAULT 'Histórico'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`idCliente`);

--
-- Indexes for table `tabla_tarifaria`
--
ALTER TABLE `tabla_tarifaria`
  ADD PRIMARY KEY (`idTarifa`);

--
-- Indexes for table `balances`
--
ALTER TABLE `balances`
  ADD PRIMARY KEY (`idBalance`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `clientes`
--
ALTER TABLE `clientes`
  MODIFY `idCliente` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tabla_tarifaria`
--
ALTER TABLE `tabla_tarifaria`
  MODIFY `idTarifa` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `balances`
--
ALTER TABLE `balances`
  MODIFY `idBalance` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;