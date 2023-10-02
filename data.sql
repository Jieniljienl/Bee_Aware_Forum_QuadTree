-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: new_schema_1
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `create_Time` datetime DEFAULT NULL,
  `question_id` int DEFAULT NULL,
  `answer_to_id` int DEFAULT NULL,
  `author_id` int DEFAULT NULL,
  `reply_info` varchar(200) DEFAULT NULL,
  `last_to_user` varchar(100) DEFAULT NULL,
  `NumOfLikes` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `answer_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
  CONSTRAINT `answer_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
INSERT INTO `answer` VALUES (1,'How to do it?','2023-10-01 22:02:45',1,NULL,1,NULL,NULL,0),(2,'You can google it?','2023-10-01 22:03:31',1,1,2,'to \'How to do it?\'','Ziyang Wang',0),(3,'Just a joke','2023-10-01 22:03:59',1,2,2,'to \'You can google it?\'','Yuzhou',0),(4,'Sorry, I have no idea','2023-10-01 22:04:21',1,3,2,'to \'Just a joke\'','Yuzhou',0),(5,'HAHA','2023-10-01 22:04:35',1,4,2,'to \'Sorry, I have no idea\'','Yuzhou',0),(6,'crazy!','2023-10-01 22:05:10',1,4,1,'to \'Sorry, I have no idea\'','Yuzhou',0),(7,'Google it!','2023-10-01 22:06:25',1,NULL,1,NULL,NULL,0);
/*!40000 ALTER TABLE `answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `tag` text NOT NULL,
  `create_Time` datetime DEFAULT NULL,
  `NumOfLikes` int NOT NULL,
  `NumOfView` int NOT NULL,
  `author_id` int DEFAULT NULL,
  `image_filename` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,'How to keep bee','I\'m a beginner of beekeeping. How to do it??','beekeeping','2023-10-01 21:57:02',0,16,1,'beekeeping.jpg'),(2,'I like honey!','Sweet honey!','honey','2023-10-01 22:02:26',0,1,1,'R.jpg');
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL,
  `address` varchar(500) NOT NULL,
  `birthday` date DEFAULT NULL,
  `introduction` varchar(500) NOT NULL,
  `email` varchar(100) NOT NULL,
  `join_time` datetime DEFAULT NULL,
  `level` int NOT NULL,
  `exp` int NOT NULL,
  `image_filename` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Ziyang Wang','pbkdf2:sha256:260000$WFTifBbjp47YZNjX$40025e62d117a36b6f64614d94b8d2a21d1bb9a5433140b9ed5e9403bc482f4d','None','2000-01-01','None','n11399813@qut.edu.au.com','2023-10-01 21:52:08',0,90,'OIP.jpg'),(2,'Yuzhou','pbkdf2:sha256:260000$pKwbo5SS4odyfLIW$dcc783188d43687d4057657862c7c7da040ecbafe54a70670b4a579440423272','None','2000-01-01','None','562975503@qq.com','2023-10-01 21:52:31',0,40,'OIP.jpg'),(3,'Lizhong','pbkdf2:sha256:260000$SnZI6GG7sWuGlH6T$5e5437eaa0943238096472b2e39b5d97ecae580ddec2155ef1bc88d6fa358508','None','2000-01-01','None','wzy0421328593@outlook.com','2023-10-01 21:52:54',0,0,'OIP.jpg'),(4,'Zihanji','pbkdf2:sha256:260000$eOo4AHOnjF0NvN85$bcc4a1a09a0e2be535fa87910884fec95ee29b66ae0bb946f3abaf26967a7fd6','None','2000-01-01','None','2001@qut.edu.au','2023-10-01 21:53:24',0,0,'OIP.jpg');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_question_history`
--

DROP TABLE IF EXISTS `user_question_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_question_history` (
  `user_id` int NOT NULL,
  `question_id` int NOT NULL,
  `created_time` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`question_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `user_question_history_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `user_question_history_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_question_history`
--

LOCK TABLES `user_question_history` WRITE;
/*!40000 ALTER TABLE `user_question_history` DISABLE KEYS */;
INSERT INTO `user_question_history` VALUES (1,1,'2023-10-01 22:06:25'),(1,2,'2023-10-01 22:02:30'),(2,1,'2023-10-01 22:04:43');
/*!40000 ALTER TABLE `user_question_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_question_save`
--

DROP TABLE IF EXISTS `user_question_save`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_question_save` (
  `user_id` int NOT NULL,
  `question_id` int NOT NULL,
  `created_time` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`question_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `user_question_save_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `user_question_save_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_question_save`
--

LOCK TABLES `user_question_save` WRITE;
/*!40000 ALTER TABLE `user_question_save` DISABLE KEYS */;
INSERT INTO `user_question_save` VALUES (1,1,'2023-10-01 22:00:12');
/*!40000 ALTER TABLE `user_question_save` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-01 22:08:38
