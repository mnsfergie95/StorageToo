-- MariaDB dump 10.18  Distrib 10.4.17-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: storagetoo
-- ------------------------------------------------------
-- Server version	10.4.17-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `lessee`
--

DROP TABLE IF EXISTS `lessee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lessee` (
  `lessee_id` int(11) NOT NULL AUTO_INCREMENT,
  `unit_id` int(11) NOT NULL,
  `lesseename` varchar(30) NOT NULL,
  `addrl1` varchar(30) DEFAULT NULL,
  `addrl2` varchar(30) DEFAULT NULL,
  `city` varchar(30) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `zip` int(11) DEFAULT NULL,
  `phone` varchar(15) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`lessee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lessee`
--

LOCK TABLES `lessee` WRITE;
/*!40000 ALTER TABLE `lessee` DISABLE KEYS */;
INSERT INTO `lessee` VALUES (1,11,'John Smith','786 Sunset Dr.','','Hillsboro','OR',0,'503-974-9294',1),(2,13,'Clyde Kessler','234 Drury Lane','','Sparta','OR',97832,'503-203-3829',1),(3,1,'Susan Castle','828 Hood Ave.','','Sandy','OR',0,'503-234-4323',1),(4,22,'Eric Rock','6 Skyline','','Hood Village','OR',96020,'5037565647',1),(5,12,'djdj','87 d kk','','clckak','OR',97328,'9711828389',0),(6,13,'jfjk','873 kdkd','kkd','slal','OR',97303,'9712883948',0);
/*!40000 ALTER TABLE `lessee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_attempts`
--

DROP TABLE IF EXISTS `login_attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_attempts` (
  `ip` varchar(20) DEFAULT NULL,
  `attempts` int(11) DEFAULT 0,
  `lastlogin` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_attempts`
--

LOCK TABLES `login_attempts` WRITE;
/*!40000 ALTER TABLE `login_attempts` DISABLE KEYS */;
/*!40000 ALTER TABLE `login_attempts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment` (
  `pmt_id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(5,2) DEFAULT NULL,
  `pmt_date` date DEFAULT NULL,
  `NextDueDate` date DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`pmt_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,80.00,'2020-10-03','2020-11-01',11),(2,80.00,'2020-10-04','2020-11-01',13),(3,120.00,'2020-10-08','2020-11-01',1),(4,80.00,'2020-11-06','2020-12-01',11),(5,40.00,'2020-11-16','2020-12-01',13),(6,80.00,'2020-11-17','2020-12-01',1),(7,55.00,'2020-11-24','2020-12-01',13),(8,80.00,'2022-12-04','2021-01-01',11),(9,120.00,'2023-07-25','2023-09-01',1),(10,120.00,'2023-08-25','2023-10-01',1),(11,120.00,'2023-09-25','2023-11-01',1),(12,80.00,'2023-10-24','2023-12-01',13);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pricing`
--

DROP TABLE IF EXISTS `pricing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pricing` (
  `sizeid` int(11) NOT NULL,
  `monthly_price` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`sizeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pricing`
--

LOCK TABLES `pricing` WRITE;
/*!40000 ALTER TABLE `pricing` DISABLE KEYS */;
INSERT INTO `pricing` VALUES (1,120.00),(2,100.00),(3,80.00),(4,60.00);
/*!40000 ALTER TABLE `pricing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sizes`
--

DROP TABLE IF EXISTS `sizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sizes` (
  `sizeid` int(11) NOT NULL,
  `descr` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`sizeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sizes`
--

LOCK TABLES `sizes` WRITE;
/*!40000 ALTER TABLE `sizes` DISABLE KEYS */;
INSERT INTO `sizes` VALUES (1,'large'),(2,'medium'),(3,'small'),(4,'compact');
/*!40000 ALTER TABLE `sizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unit`
--

DROP TABLE IF EXISTS `unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unit` (
  `unitid` int(11) NOT NULL AUTO_INCREMENT,
  `sizeid` int(11) DEFAULT NULL,
  `label` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`unitid`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unit`
--

LOCK TABLES `unit` WRITE;
/*!40000 ALTER TABLE `unit` DISABLE KEYS */;
INSERT INTO `unit` VALUES (1,1,'a1'),(2,1,'a2'),(3,1,'a3'),(4,1,'a4'),(5,1,'a5'),(6,2,'b1'),(7,2,'b2'),(8,2,'b3'),(9,2,'b4'),(10,2,'b5'),(11,3,'c1'),(12,3,'c2'),(13,3,'c3'),(14,3,'c4'),(15,3,'c5'),(16,4,'cc1'),(17,4,'cc2'),(18,4,'cc3'),(19,4,'cc4'),(20,4,'cc5');
/*!40000 ALTER TABLE `unit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) DEFAULT NULL,
  `pwd` binary(72) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'demo','wBggc34LhscSYyGR5RYGZdMNEw==wı*µƒÔêY]?åÉ Ú+[ˇ√LO/üî«ÁkıÂÊLhn≠«ËÉ“\rk'),(2,'james','2jCMUUxHKi5h6yV7mRqKRÓ0©ea—”.i ﬂíhc∫ÒÃP¨ú≠Îó÷:8Ãqõ¶1ÀßpÅËµ\0\0\0\0\0\0\0\0'),(3,'admin','zYPAAJS0vJKjCPGLAFddxv35xg==GÊœà÷“3éL¸“ª¯ÍvÄÓ÷¨_ºá˘öU\\Ó;á8yNYç®ó	%™®ˆÔ');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-26 15:05:27
