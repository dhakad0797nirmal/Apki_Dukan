-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 10, 2021 at 05:54 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 7.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `new_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `address_table`
--

CREATE TABLE `address_table` (
  `a_id` int(10) NOT NULL,
  `u_id` varchar(10) NOT NULL,
  `u_name` varchar(20) NOT NULL,
  `u_mob` varchar(10) NOT NULL,
  `u_address` varchar(255) NOT NULL,
  `u_city` varchar(10) NOT NULL,
  `u_pin` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `address_table`
--

INSERT INTO `address_table` (`a_id`, `u_id`, `u_name`, `u_mob`, `u_address`, `u_city`, `u_pin`) VALUES
(1, '9826371288', 'manglesh', '983376383', 'mig 2 indira nagar', 'ujjain', '13121'),
(2, '9826371288', 'almas', '98723', 'alirajpur', 'alirajpur', '456001'),
(3, '9826371288', 'pjs', '565456', 'dhodhar', 'ujjain', '13121'),
(4, '9981283198', 'danny', '323232', 'shuji gali shujalpur', 'beena', '1212'),
(15, '9981283198', 'pankaj solanki', '9981283198', '69,mig 2 indira nagar', 'ujjain', '234567'),
(16, '9981283198', 'pankaj solanki', '9981283198', '69,mig 2 indira nagar', 'ujjain', '456001'),
(17, '9981283198', 'dsdssd', '9981283198', '69,mig 2 indira nagar', 'ujjain', '456001'),
(18, '9981283198', 'kamlnath', '9981283198', '69,mig 2 indira nagar', 'ujjain', '456001'),
(19, '9826371288', 'ameer khusro', '9823451234', '69,mig 2 indira nagar', 'ujjain', '456001'),
(20, '9826371238', 'ramu', '9826454555', '69,mig 2 indira nagar', 'ujjain', '456001'),
(21, '1234567890', 'dsdssd', '9842634545', '69,mig 2 indira nagar', 'ujjain', '456001'),
(22, '0987654321', 'raju bhai', '9981283198', '69,mig 2 indira nagar', 'ujjain', '456001');

-- --------------------------------------------------------

--
-- Table structure for table `category_table`
--

CREATE TABLE `category_table` (
  `c_id` int(20) NOT NULL,
  `c_name` varchar(10) NOT NULL,
  `c_img` varchar(300) NOT NULL,
  `c_description` varchar(200) NOT NULL,
  `c_status` tinyint(10) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `category_table`
--

INSERT INTO `category_table` (`c_id`, `c_name`, `c_img`, `c_description`, `c_status`) VALUES
(2, 'category0', 'https://i.ibb.co/88XVH55/new-add-2.png', 'demo desc', 1),
(3, 'category 1', 'http://localhost:5000/static/images/product/JNUPHOTO.jpg', 'some description', 1),
(4, 'category2', 'https://i.ibb.co/ct2BJ22/Screenshot-2019-06-28-14-02-03-008-com-appsomniacs-da2.png', 'some demo description', 1),
(5, 'category3', 'http://localhost:5000/static/images/product/nitt_slogan.PNG', 'demo description', 1);

-- --------------------------------------------------------

--
-- Table structure for table `order_table`
--

CREATE TABLE `order_table` (
  `o_id` int(10) NOT NULL,
  `a_id` int(10) NOT NULL,
  `o_date` varchar(30) NOT NULL,
  `o_status` varchar(10) NOT NULL,
  `o_item` varchar(300) NOT NULL,
  `o_total` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `order_table`
--

INSERT INTO `order_table` (`o_id`, `a_id`, `o_date`, `o_status`, `o_item`, `o_total`) VALUES
(232, 2, 'may 2019 2', 'delivered', '[{\"10\":\"10\"}]', 100),
(337, 15, '2021-05-23', 'delivered', '[{\"10\": 1, \"12\": \"1\", \"18\": \"1\"}]', 120134),
(338, 17, '2021-05-23', 'rejected', '[{\"10\": 3}]', 360000),
(339, 18, '2021-05-23', 'delivered', '[{\"10\": 1}]', 120000),
(340, 18, '2021-05-23', 'pending', '[{\"10\": 1}]', 120000),
(341, 3, '2021-05-23', 'rejected', '[{\"12\": 5, \"15\": 6}]', 682),
(342, 1, '2021-05-23', 'cancelled', '[{\"10\": 1, \"12\": 1}]', 120122),
(343, 19, '2021-05-24', 'cancelled', '[{\"12\": 5, \"18\": 5}]', 670),
(344, 2, '2021-05-24', 'cancelled', '[{\"10\": 1, \"15\": 1}]', 120012),
(345, 20, '2021-05-25', 'rejected', '[{\"12\": 4, \"15\": 1, \"18\": 1}]', 512),
(346, 20, '2021-05-25', 'cancelled', '[{\"12\": 5}]', 610),
(347, 21, '2021-05-25', 'pending', '[{\"16\": 48}]', 576),
(348, 22, '2021-05-25', 'pending', '[{\"12\": 6}]', 732),
(349, 4, '2021-05-27', 'pending', '[{\"12\": 7}]', 854);

-- --------------------------------------------------------

--
-- Table structure for table `product_table`
--

CREATE TABLE `product_table` (
  `p_id` int(20) NOT NULL,
  `p_name` varchar(30) NOT NULL,
  `p_img` varchar(300) NOT NULL,
  `c_id` int(20) NOT NULL,
  `p_price` float NOT NULL,
  `p_description` varchar(100) NOT NULL,
  `p_quantity` varchar(10) NOT NULL,
  `p_status` tinyint(1) NOT NULL DEFAULT 1,
  `p_in_stock` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product_table`
--

INSERT INTO `product_table` (`p_id`, `p_name`, `p_img`, `c_id`, `p_price`, `p_description`, `p_quantity`, `p_status`, `p_in_stock`) VALUES
(10, 'product1', 'http://127.0.0.1:5000/static/images/product/photo1.png', 3, 10, 'not avilable', '1 pieces', 1, 1),
(12, 'product2', 'http://127.0.0.1:5000/static/images/product/photo2.png', 2, 122, 'not avilable', '2 kg', 1, 1),
(15, 'product3', 'http://127.0.0.1:5000/static/images/product/photo3.png', 5, 122, 'not avilable', '1 kg', 1, 1),
(16, 'product4', 'http://127.0.0.1:5000/static/images/product/photo4.png', 4, 12, 'not avilable', '1 kg', 1, 1),
(17, 'product5', 'http://127.0.0.1:5000/static/images/product/photo5.png', 4, 123, 'not avilable', '1 kg', 1, 1),
(18, 'product5', 'http://localhost:5000/static/images/product/IMG_20190614_132046.jpg', 5, 120, 'not avilable', '1 kg', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user_table`
--

CREATE TABLE `user_table` (
  `u_id` varchar(10) NOT NULL,
  `otp` varchar(10) NOT NULL,
  `u_name` varchar(30) NOT NULL,
  `cart` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_table`
--

INSERT INTO `user_table` (`u_id`, `otp`, `u_name`, `cart`) VALUES
('0987654321', '', 'kharchu lala', '[{\"10\": 1, \"12\": 9}]'),
('1234567890', '', 'vikram makhija', '[{\"10\": 1}]'),
('9826371238', '', 'khatri babu', ''),
('9826371288', '2121', '', '[{\"10\": 1, \"16\": 44}]'),
('9981283198', '3232', '', '[{\"15\": \"1\", \"18\": 1}]');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address_table`
--
ALTER TABLE `address_table`
  ADD PRIMARY KEY (`a_id`),
  ADD KEY `text` (`u_id`);

--
-- Indexes for table `category_table`
--
ALTER TABLE `category_table`
  ADD PRIMARY KEY (`c_id`),
  ADD UNIQUE KEY `c_id` (`c_id`);

--
-- Indexes for table `order_table`
--
ALTER TABLE `order_table`
  ADD PRIMARY KEY (`o_id`),
  ADD KEY `xyz` (`a_id`);

--
-- Indexes for table `product_table`
--
ALTER TABLE `product_table`
  ADD PRIMARY KEY (`p_id`),
  ADD UNIQUE KEY `p_id` (`p_id`),
  ADD KEY `c_id` (`c_id`);

--
-- Indexes for table `user_table`
--
ALTER TABLE `user_table`
  ADD PRIMARY KEY (`u_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `address_table`
--
ALTER TABLE `address_table`
  MODIFY `a_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `category_table`
--
ALTER TABLE `category_table`
  MODIFY `c_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `order_table`
--
ALTER TABLE `order_table`
  MODIFY `o_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=350;

--
-- AUTO_INCREMENT for table `product_table`
--
ALTER TABLE `product_table`
  MODIFY `p_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `address_table`
--
ALTER TABLE `address_table`
  ADD CONSTRAINT `text` FOREIGN KEY (`u_id`) REFERENCES `user_table` (`u_id`);

--
-- Constraints for table `order_table`
--
ALTER TABLE `order_table`
  ADD CONSTRAINT `xyz` FOREIGN KEY (`a_id`) REFERENCES `address_table` (`a_id`);

--
-- Constraints for table `product_table`
--
ALTER TABLE `product_table`
  ADD CONSTRAINT `product_table_ibfk_1` FOREIGN KEY (`c_id`) REFERENCES `category_table` (`c_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
