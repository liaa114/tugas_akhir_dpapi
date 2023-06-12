-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 12, 2023 at 09:16 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_api`
--

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `nim` int(11) NOT NULL,
  `no` int(11) NOT NULL,
  `nama` varchar(250) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `alamat` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`nim`, `no`, `nama`, `email`, `alamat`) VALUES
(212102001, 1, 'Agus Prianto', 'agusap083@gmail.com', 'Bogor'),
(212102002, 2, 'Balqis', 'balqis05@gmail.com', 'Bandung'),
(212102003, 3, 'Bayu Saputra', 'bayusp83@gmail.com', 'Bogor'),
(212102004, 4, 'Jaya Lukmanul Hakim', 'jayalh83@gmail.com', 'Sukabumi'),
(212102005, 5, 'Mirna Sari Dewi', 'msd007@gmail.com', 'Jakarta'),
(212102006, 6, 'Muldiyana', 'muldiana3764@gmail.com', 'Jakarta'),
(212102007, 7, 'Neng Rahmawati', 'rhmwt3746@gmail.com', 'Sukabumi'),
(212102008, 8, 'Siti Sopiah', 'sitsop14@gmail.com', 'Wonosobo'),
(212102009, 9, 'Samsul Bahri', 'Samsul93@gmail.com', 'Bekasi'),
(212102010, 10, 'Tania Larasati', 'tanials87@gmail.com', 'Samarinda'),
(212102011, 11, 'Yogi Sopian', 'ygspn@gmail.com', 'Kepulauan Riau'),
(212102012, 12, 'Terens Yofu', 'terens83@gmail.com', 'Maluku'),
(212102014, 14, 'reihan', 'rh@gmail.com', 'Yogyakarta');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(250) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin123'),
(2, 'resti', 'dosen123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`nim`),
  ADD UNIQUE KEY `index` (`no`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
