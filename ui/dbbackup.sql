-- MySQL dump 10.13  Distrib 5.1.62, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Production
-- ------------------------------------------------------
-- Server version	5.1.62-0ubuntu0.10.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add book',8,'add_book'),(23,'Can change book',8,'change_book'),(24,'Can delete book',8,'delete_book'),(25,'Can add processing session',9,'add_processingsession'),(26,'Can change processing session',9,'change_processingsession'),(27,'Can delete processing session',9,'delete_processingsession');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'gilani','','','gilani@email.gwu.edu','pbkdf2_sha256$10000$xFWQYDnlHNaK$+cMbpWxK6ICNvJqrGOONbK5Gck8+nLL+mqh+gE79XA0=',1,1,1,'2012-05-15 17:41:02','2012-04-10 20:53:29'),(2,'admin','','','','pbkdf2_sha256$10000$V96576pKXNN7$2zdU3v0WO4gJPoPXULlNxDdR+et7l7qBPaLUWqIrBJI=',1,1,1,'2012-05-07 17:58:27','2012-04-25 18:10:36'),(3,'marzieh','','','','pbkdf2_sha256$10000$0I4kuSH3huHO$pJec7vZI1p8Dp/jEXQvbCy516PPNwiQWemxFssZ1e7k=',0,1,0,'2012-04-25 18:18:15','2012-04-25 18:18:15'),(4,'abid','','','','pbkdf2_sha256$10000$ouQ2HfZborqK$gx9aWLN5jh6Zfrr3jNqX+/87RcsRUJ/EOb4+IVYFTrM=',0,1,0,'2012-05-03 20:33:22','2012-04-25 18:18:28'),(5,'nishita','','','','pbkdf2_sha256$10000$kNJx06fBmPHD$bbEnV/PgsjQtK0S0xMGyABCmEwg5hQVNKF70YBg3Qpw=',0,1,0,'2012-05-01 12:58:14','2012-04-25 18:18:49'),(6,'greg','','','','pbkdf2_sha256$10000$CZCnLizDK3ZH$Qx56jAb4GehbFTE5ShROms9rTtT6uscAeYB+No7xGH0=',1,1,1,'2012-05-15 15:25:48','2012-04-25 18:19:04'),(7,'mohammad','','','','pbkdf2_sha256$10000$2I6qm5mIZcMu$3Nr48fvb0eP8z27luaUDaKSMKP5OTIeIZ4yXD+8g6zw=',0,1,0,'2012-05-03 21:19:12','2012-05-02 21:10:44'),(8,'test','','','','pbkdf2_sha256$10000$t1yU65HkEQ0A$4WwqlJdkl53ShdM7b1Jh1+ci4UBgec4JXKtml1VVQrE=',0,1,0,'2012-05-09 20:34:34','2012-05-09 16:35:36');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_f0ee9890` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_67e79cb` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_refs_id_c8665aa` (`user_id`),
  KEY `content_type_id_refs_id_288599e6` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2012-04-25 18:10:36',1,3,'2','admin',1,''),(2,'2012-04-25 18:11:09',1,3,'2','admin',2,'Changed password, is_staff and is_superuser.'),(3,'2012-04-25 18:18:15',2,3,'3','marzieh',1,''),(4,'2012-04-25 18:18:28',2,3,'4','abid',1,''),(5,'2012-04-25 18:18:49',2,3,'5','nishita',1,''),(6,'2012-04-25 18:19:04',2,3,'6','greg',1,''),(7,'2012-04-25 19:01:16',2,3,'6','greg',2,'Changed password, is_staff and is_superuser.'),(8,'2012-05-02 21:10:44',6,3,'7','mohammad',1,''),(9,'2012-05-09 16:35:36',1,3,'8','test',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'book','ui','book'),(9,'processing session','ui','processingsession');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('888e9c0e703d53e33b4cf2f1c6e960e6','ODNjNjlhYTUxYTliNDYyODRmNjVlMTY5NGVlZWEzNmViZGMyZjQzNDqAAn1xAS4=\n','2012-05-18 02:03:33'),('3b07c9d0026cd89fd00555f8febf2da2','MDNlMGY1N2YzZWIyYTE0YjcwNjNhYTFlODVlODg3YWZkMGNhMWEwODqAAn1xAShVB3VzZXJfaWRx\nAmNkamFuZ28uZGIubW9kZWxzLmJhc2UKbW9kZWxfdW5waWNrbGUKcQNjZGphbmdvLmNvbnRyaWIu\nYXV0aC5tb2RlbHMKVXNlcgpxBF1jZGphbmdvLmRiLm1vZGVscy5iYXNlCnNpbXBsZV9jbGFzc19m\nYWN0b3J5CnEFh1JxBn1xByhVCHVzZXJuYW1lcQhYBgAAAGdpbGFuaXEJVQpmaXJzdF9uYW1lcQpY\nAAAAAFUJbGFzdF9uYW1lcQtYAAAAAFUJaXNfYWN0aXZlcQyIVQZfc3RhdGVxDWNkamFuZ28uZGIu\nbW9kZWxzLmJhc2UKTW9kZWxTdGF0ZQpxDimBcQ99cRAoVQZhZGRpbmdxEYlVAmRicRJVB2RlZmF1\nbHRxE3ViVQVlbWFpbHEUWBQAAABnaWxhbmlAZW1haWwuZ3d1LmVkdXEVVQdiYWNrZW5kcRZVKWRq\nYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kcRdVDGlzX3N1cGVydXNlcnEY\niFUIaXNfc3RhZmZxGYhVCmxhc3RfbG9naW5xGmNkYXRldGltZQpkYXRldGltZQpxG1UKB9wFARUK\nLQiqz2NkamFuZ28udXRpbHMudGltZXpvbmUKVVRDCnEcKVJxHYZScR5VCHBhc3N3b3JkcR9YTQAA\nAHBia2RmMl9zaGEyNTYkMTAwMDAkeEZXUVlEbmxITmFLJCtjTWJwV3hLNklDTnZKcXJHT09OYks1\nR2NrOCtuTEwrbXFoK2dFNzlYQTA9cSBVAmlkcSGKAQFVC2RhdGVfam9pbmVkcSJoG1UKB9wEChQ1\nHQAAAGgdhlJxI3ViVRJfYXV0aF91c2VyX2JhY2tlbmRxJGgXVQ1fYXV0aF91c2VyX2lkcSWKAQF1\nLg==\n','2012-05-15 21:10:45'),('59fe78bb36961325848baecce4464607','ODk1YjcyYTVkMDQyMzlmODg4MTdjZWUxMDhhMjExMGVlY2I2MjBmYjqAAn1xAShVB3VzZXJfaWRx\nAmNkamFuZ28uZGIubW9kZWxzLmJhc2UKbW9kZWxfdW5waWNrbGUKcQNjZGphbmdvLmNvbnRyaWIu\nYXV0aC5tb2RlbHMKVXNlcgpxBF1jZGphbmdvLmRiLm1vZGVscy5iYXNlCnNpbXBsZV9jbGFzc19m\nYWN0b3J5CnEFh1JxBn1xByhVCHVzZXJuYW1lcQhYBQAAAGFkbWlucQlVCmZpcnN0X25hbWVxClgA\nAAAAVQlsYXN0X25hbWVxC1gAAAAAVQlpc19hY3RpdmVxDIhVBl9zdGF0ZXENY2RqYW5nby5kYi5t\nb2RlbHMuYmFzZQpNb2RlbFN0YXRlCnEOKYFxD31xEChVBmFkZGluZ3ERiVUCZGJxElUHZGVmYXVs\ndHETdWJVBWVtYWlscRRYAAAAAFUHYmFja2VuZHEVVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tl\nbmRzLk1vZGVsQmFja2VuZHEWVQxpc19zdXBlcnVzZXJxF4hVCGlzX3N0YWZmcRiIVQpsYXN0X2xv\nZ2lucRljZGF0ZXRpbWUKZGF0ZXRpbWUKcRpVCgfcBBkSIg8KJhJjZGphbmdvLnV0aWxzLnRpbWV6\nb25lClVUQwpxGylScRyGUnEdVQhwYXNzd29yZHEeWE0AAABwYmtkZjJfc2hhMjU2JDEwMDAwJFY5\nNjU3NnBLWE5ONyQyemRVM3YwV080Z0pQb1BYVUxsTnhEZFIrZXQ3bDdxQlBhTFVXcUlyQkpJPXEf\nVQJpZHEgigECVQtkYXRlX2pvaW5lZHEhaBpVCgfcBBkSCiQAAABoHIZScSJ1YlUSX2F1dGhfdXNl\ncl9iYWNrZW5kcSNoFlUNX2F1dGhfdXNlcl9pZHEkigECdS4=\n','2012-05-09 18:34:15'),('579ecb3db2584c5ca806a1ecee7c96df','NmFmMmRjMDYyMmRkYWFmZGFkNzVkNDdhYmY1NGUwMDA4ZGUwOGNmMjqAAn1xAShVB3VzZXJfaWRx\nAmNkamFuZ28uZGIubW9kZWxzLmJhc2UKbW9kZWxfdW5waWNrbGUKcQNjZGphbmdvLmNvbnRyaWIu\nYXV0aC5tb2RlbHMKVXNlcgpxBF1jZGphbmdvLmRiLm1vZGVscy5iYXNlCnNpbXBsZV9jbGFzc19m\nYWN0b3J5CnEFh1JxBn1xByhVCHVzZXJuYW1lcQhYBAAAAGFiaWRxCVUKZmlyc3RfbmFtZXEKWAAA\nAABVCWxhc3RfbmFtZXELWAAAAABVCWlzX2FjdGl2ZXEMiFUGX3N0YXRlcQ1jZGphbmdvLmRiLm1v\nZGVscy5iYXNlCk1vZGVsU3RhdGUKcQ4pgXEPfXEQKFUGYWRkaW5ncRGJVQJkYnESVQdkZWZhdWx0\ncRN1YlUFZW1haWxxFFgAAAAAVQdiYWNrZW5kcRVVKWRqYW5nby5jb250cmliLmF1dGguYmFja2Vu\nZHMuTW9kZWxCYWNrZW5kcRZVDGlzX3N1cGVydXNlcnEXiVUIaXNfc3RhZmZxGIlVCmxhc3RfbG9n\naW5xGWNkYXRldGltZQpkYXRldGltZQpxGlUKB9wEHhYwEQf23mNkamFuZ28udXRpbHMudGltZXpv\nbmUKVVRDCnEbKVJxHIZScR1VCHBhc3N3b3JkcR5YTQAAAHBia2RmMl9zaGEyNTYkMTAwMDAkb3VR\nMkhmWmJvcnFLJGd4OWFXTE41amg2WmZycjNqTnFYKy84N1Jjc1JVSi9FT2I0K0lWWUZUck09cR9V\nAmlkcSCKAQRVC2RhdGVfam9pbmVkcSFoGlUKB9wEGRISHAAAAGgchlJxInViVRJfYXV0aF91c2Vy\nX2JhY2tlbmRxI2gWVQ1fYXV0aF91c2VyX2lkcSSKAQR1Lg==\n','2012-05-14 22:48:17'),('5d5dbc111443d79b78f2be83626c1759','MTg3ODRhYmMyNDA4MGY5MTQ1MGYyYWRhZWY2ZGIwYmY2Y2ZkOWI0NzqAAn1xAShVB3VzZXJfaWRx\nAmNkamFuZ28uZGIubW9kZWxzLmJhc2UKbW9kZWxfdW5waWNrbGUKcQNjZGphbmdvLmNvbnRyaWIu\nYXV0aC5tb2RlbHMKVXNlcgpxBF1jZGphbmdvLmRiLm1vZGVscy5iYXNlCnNpbXBsZV9jbGFzc19m\nYWN0b3J5CnEFh1JxBn1xByhVCHVzZXJuYW1lcQhYBwAAAG5pc2hpdGFxCVUKZmlyc3RfbmFtZXEK\nWAAAAABVCWxhc3RfbmFtZXELWAAAAABVCWlzX2FjdGl2ZXEMiFUGX3N0YXRlcQ1jZGphbmdvLmRi\nLm1vZGVscy5iYXNlCk1vZGVsU3RhdGUKcQ4pgXEPfXEQKFUGYWRkaW5ncRGJVQJkYnESVQdkZWZh\ndWx0cRN1YlUFZW1haWxxFFgAAAAAVQdiYWNrZW5kcRVVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kcRZVDGlzX3N1cGVydXNlcnEXiVUIaXNfc3RhZmZxGIlVCmxhc3Rf\nbG9naW5xGWNkYXRldGltZQpkYXRldGltZQpxGlUKB9wFAQw6DgijsmNkamFuZ28udXRpbHMudGlt\nZXpvbmUKVVRDCnEbKVJxHIZScR1VCHBhc3N3b3JkcR5YTQAAAHBia2RmMl9zaGEyNTYkMTAwMDAk\na05KeDA2ZkJtUEhEJGJiRW5WL1Bnc2pRdEswUzB4TUd5QUJDbUV3ZzVoUVZOS0Y3MFlCZzNRcHc9\ncR9VAmlkcSCKAQVVC2RhdGVfam9pbmVkcSFoGlUKB9wEGRISMQAAAGgchlJxInViVRJfYXV0aF91\nc2VyX2JhY2tlbmRxI2gWVQ1fYXV0aF91c2VyX2lkcSSKAQV1Lg==\n','2012-05-15 12:58:14'),('3998861050301fad539d33ebe11a3e6b','ODNjNjlhYTUxYTliNDYyODRmNjVlMTY5NGVlZWEzNmViZGMyZjQzNDqAAn1xAS4=\n','2012-05-17 02:04:29'),('72abde0c5b6a78047c98a109b487979d','ODNjNjlhYTUxYTliNDYyODRmNjVlMTY5NGVlZWEzNmViZGMyZjQzNDqAAn1xAS4=\n','2012-05-17 23:12:41'),('e28756e9dec1540541f8c80377e7f97b','ODNjNjlhYTUxYTliNDYyODRmNjVlMTY5NGVlZWEzNmViZGMyZjQzNDqAAn1xAS4=\n','2012-05-19 21:26:04'),('d32d800e970dece5d57e23738307fd4c','YmM1OTEwMDgzZDk2OTExNTRkNmVjYzkyZjI0MWNiY2M2MzFhNDdiMzqAAn1xAShVB3VzZXJfaWRx\nAmNkamFuZ28uZGIubW9kZWxzLmJhc2UKbW9kZWxfdW5waWNrbGUKcQNjZGphbmdvLmNvbnRyaWIu\nYXV0aC5tb2RlbHMKVXNlcgpxBF1jZGphbmdvLmRiLm1vZGVscy5iYXNlCnNpbXBsZV9jbGFzc19m\nYWN0b3J5CnEFh1JxBn1xByhVCHVzZXJuYW1lcQhYBAAAAGdyZWdxCVUKZmlyc3RfbmFtZXEKWAAA\nAABVCWxhc3RfbmFtZXELWAAAAABVCWlzX2FjdGl2ZXEMiFUGX3N0YXRlcQ1jZGphbmdvLmRiLm1v\nZGVscy5iYXNlCk1vZGVsU3RhdGUKcQ4pgXEPfXEQKFUGYWRkaW5ncRGJVQJkYnESVQdkZWZhdWx0\ncRN1YlUFZW1haWxxFFgAAAAAVQdiYWNrZW5kcRVVKWRqYW5nby5jb250cmliLmF1dGguYmFja2Vu\nZHMuTW9kZWxCYWNrZW5kcRZVDGlzX3N1cGVydXNlcnEXiFUIaXNfc3RhZmZxGIhVCmxhc3RfbG9n\naW5xGWNkYXRldGltZQpkYXRldGltZQpxGlUKB9wFDw8ZMAryNWNkamFuZ28udXRpbHMudGltZXpv\nbmUKVVRDCnEbKVJxHIZScR1VCHBhc3N3b3JkcR5YTQAAAHBia2RmMl9zaGEyNTYkMTAwMDAkQ1pD\nbkxpekRLM1pIJFF4NTZqQWI0R2VoYkZURTVTaFJPbXM5clR0VDZ1c2NBZVlCK05vN3hHSDA9cR9V\nAmlkcSCKAQZVC2RhdGVfam9pbmVkcSFoGlUKB9wEGRITBAAAAGgchlJxInViVQ1fYXV0aF91c2Vy\nX2lkcSOKAQZVEl9hdXRoX3VzZXJfYmFja2VuZHEkaBZ1Lg==\n','2012-05-29 15:25:48'),('ad31b15d1757f0f0ab72d7036fa6742f','NDM4YWNlOGU0M2JmMjAwMWM5MGUwYmYyZjUxZmI1NDliMzlkZjU4YjqAAn1xAShVB3VzZXJfaWRx\nAmNkamFuZ28uZGIubW9kZWxzLmJhc2UKbW9kZWxfdW5waWNrbGUKcQNjZGphbmdvLmNvbnRyaWIu\nYXV0aC5tb2RlbHMKVXNlcgpxBF1jZGphbmdvLmRiLm1vZGVscy5iYXNlCnNpbXBsZV9jbGFzc19m\nYWN0b3J5CnEFh1JxBn1xByhVCHVzZXJuYW1lcQhYBgAAAGdpbGFuaXEJVQpmaXJzdF9uYW1lcQpY\nAAAAAFUJbGFzdF9uYW1lcQtYAAAAAFUJaXNfYWN0aXZlcQyIVQZfc3RhdGVxDWNkamFuZ28uZGIu\nbW9kZWxzLmJhc2UKTW9kZWxTdGF0ZQpxDimBcQ99cRAoVQZhZGRpbmdxEYlVAmRicRJVB2RlZmF1\nbHRxE3ViVQVlbWFpbHEUWBQAAABnaWxhbmlAZW1haWwuZ3d1LmVkdXEVVQdiYWNrZW5kcRZVKWRq\nYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kcRdVDGlzX3N1cGVydXNlcnEY\niFUIaXNfc3RhZmZxGYhVCmxhc3RfbG9naW5xGmNkYXRldGltZQpkYXRldGltZQpxG1UKB9wFDxEp\nAgwHPWNkamFuZ28udXRpbHMudGltZXpvbmUKVVRDCnEcKVJxHYZScR5VCHBhc3N3b3JkcR9YTQAA\nAHBia2RmMl9zaGEyNTYkMTAwMDAkeEZXUVlEbmxITmFLJCtjTWJwV3hLNklDTnZKcXJHT09OYks1\nR2NrOCtuTEwrbXFoK2dFNzlYQTA9cSBVAmlkcSGKAQFVC2RhdGVfam9pbmVkcSJoG1UKB9wEChQ1\nHQAAAGgdhlJxI3ViVQ1fYXV0aF91c2VyX2lkcSSKAQFVEl9hdXRoX3VzZXJfYmFja2VuZHElaBd1\nLg==\n','2012-05-29 17:41:02');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ui_book`
--

DROP TABLE IF EXISTS `ui_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ui_book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `barcode` varchar(50) NOT NULL,
  `totalPages` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=48 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ui_book`
--

LOCK TABLES `ui_book` WRITE;
/*!40000 ALTER TABLE `ui_book` DISABLE KEYS */;
INSERT INTO `ui_book` VALUES (1,'39020025956601',0),(2,'32882019308751',0),(4,'60720340 R',0),(7,'10000006951',0),(5,'60540620R',0),(6,'64320030RX1',0),(8,'64320030RX3',0),(9,'64321030RX2',0),(10,'64950480RX2',0),(11,'64321030RX1',0),(12,'101305069X1',0),(13,'60440690R',0),(14,'66921050RX4',0),(15,'101305069X2',0),(16,'66921050RX2',0),(17,'66921050RX1',0),(18,'66921050RX3',0),(19,'32882018661416',0),(20,'2543040RX3',0),(21,'63540650RX1',0),(22,'65340650RX2',0),(23,'63540650RX3',0),(24,'32882019290694',0),(27,'32882019068660',0),(26,'32882019395162',0),(28,'32882019070369',0),(29,'39020025954879',0),(30,'2543040RX2',0),(31,'2546081RX2',0),(32,'32882019395253',0),(33,'32882019395287',0),(34,'2546081RX1',0),(35,'2543040RX1',0),(36,'101530407X1',0),(37,'101530407X2',0),(38,'101530400X2',0),(39,'101530400X1',0),(40,'2546033RX1',0),(41,'101492998X2',0),(42,'101492998X1',0),(43,'2551043RX2',0),(44,'2551043RX1',0),(45,'2567022RX1',0),(46,'32882013620631',0),(47,'32882013534444',0);
/*!40000 ALTER TABLE `ui_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ui_processingsession`
--

DROP TABLE IF EXISTS `ui_processingsession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ui_processingsession` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `pagesDone` int(11) NOT NULL,
  `comments` longtext NOT NULL,
  `task` varchar(4) NOT NULL,
  `operationComplete` tinyint(1) DEFAULT NULL,
  `startTime` datetime NOT NULL,
  `endTime` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `book_id_refs_id_88a54f1c` (`book_id`),
  KEY `user_id_refs_id_77f0ea3c` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ui_processingsession`
--

LOCK TABLES `ui_processingsession` WRITE;
/*!40000 ALTER TABLE `ui_processingsession` DISABLE KEYS */;
INSERT INTO `ui_processingsession` VALUES (1,4,6,346,'book had many pages to deskew and computer had latency problems','QC',1,'2012-04-25 19:21:30','2012-04-25 19:42:49'),(2,9,6,150,'150','QC',1,'2012-05-02 18:41:40','2012-05-02 19:41:45'),(3,6,6,1002,'L','QC',1,'2012-05-02 17:42:35','2012-05-02 19:42:39'),(4,10,7,478,'complete','QC',1,'2012-05-02 20:13:04','2012-05-02 22:13:11'),(5,11,7,431,'I started cleaning after tif 187','QC',1,'2012-05-02 22:18:06','2012-05-03 00:30:28'),(6,9,4,434,'complete.','QC',1,'2012-05-02 22:30:28','2012-05-03 02:20:09'),(7,12,7,272,'tif 272','QC',1,'2012-05-03 00:37:32','2012-05-03 02:20:10'),(8,13,6,400,'computer latency issues','QC',1,'2012-05-03 15:08:45','2012-05-03 18:36:56'),(9,14,6,102,'done','QC',1,'2012-05-03 19:00:28','2012-05-03 19:43:39'),(10,15,6,145,'QC','QC',1,'2012-05-03 19:30:54','2012-05-03 20:01:05'),(11,12,4,664,'Have taken break for 30min.','QC',1,'2012-05-03 17:20:31','2012-05-03 21:35:53'),(12,17,4,200,'First 200 pages are cleaned.','QC',1,'2012-05-03 22:30:47','2012-05-04 00:12:31'),(13,16,7,360,'cleaned till tif 360','QC',1,'2012-05-03 22:18:16','2012-05-04 02:16:03'),(14,18,7,72,'cleaned till tif 72','QC',1,'2012-05-04 02:17:11','2012-05-04 02:58:20'),(15,17,6,920,'complete','QC',1,'2012-05-04 15:00:09','2012-05-04 21:20:21'),(16,18,6,1176,'complete','QC',1,'2012-05-05 18:00:15','2012-05-05 22:14:59'),(17,19,1,300,'good','QC',1,'2012-05-07 20:26:53','2012-05-07 21:26:59'),(18,20,6,410,'','QC',1,'2012-05-08 15:00:19','2012-05-08 19:03:50'),(19,16,6,1096,'book was QC Marzieh, I double checked for quality','QC',1,'2012-05-08 19:10:02','2012-05-08 19:32:09'),(20,21,6,664,'','QC',1,'2012-05-08 19:39:01','2012-05-08 21:51:21'),(21,22,6,628,'had to fix many pages in this book','QC',1,'2012-05-08 22:07:34','2012-05-08 22:18:53'),(22,23,6,744,'just went in to check the quality','QC',1,'2012-05-08 21:27:16','2012-05-08 22:27:22'),(26,27,1,300,'','QC',1,'2012-04-09 19:29:53','2012-04-09 20:29:57'),(24,26,1,300,'test','QC',1,'2012-05-09 15:29:08','2012-05-09 16:29:24'),(25,24,1,300,'test','QC',1,'2012-05-09 16:07:28','2012-05-09 17:07:31'),(27,28,8,300,'test','QC',1,'2012-05-09 18:48:30','2012-05-09 19:48:34'),(28,29,1,200,'test','QC',1,'2012-05-09 18:51:19','2012-05-09 19:51:22'),(29,30,6,478,'','QC',1,'2012-05-09 15:00:52','2012-05-09 20:28:01'),(30,32,1,300,'test','QC',1,'2012-05-09 20:32:58','2012-05-09 21:33:02'),(31,33,8,300,'test','QC',1,'2012-05-09 20:35:35','2012-05-09 21:35:37'),(32,31,6,464,'','QC',1,'2012-05-09 20:59:33','2012-05-09 21:59:38'),(33,35,6,472,'','QC',1,'2012-05-10 13:07:52','2012-05-10 15:07:55'),(34,34,6,464,'','QC',1,'2012-05-10 14:13:32','2012-05-10 15:42:00'),(35,36,6,363,'','QC',1,'2012-05-10 15:45:47','2012-05-10 19:07:30'),(36,36,6,526,'total amount of images in this book is 526','QC',1,'2012-05-10 18:26:40','2012-05-10 21:05:42'),(37,37,6,538,'','QC',1,'2012-05-10 19:17:14','2012-05-10 21:17:17'),(38,32,1,300,'good','QC',1,'2012-05-11 01:16:10','2012-05-11 02:16:13'),(39,38,6,558,'','QC',1,'2012-05-11 15:04:27','2012-05-11 15:36:11'),(40,39,6,602,'','QC',1,'2012-05-11 15:50:38','2012-05-11 21:37:26'),(41,40,6,264,'','QA',1,'2012-05-12 18:58:09','2012-05-12 22:47:18'),(42,41,6,1152,'','QC',1,'2012-05-13 17:47:40','2012-05-13 18:59:39'),(43,42,6,1100,'','QC',1,'2012-05-13 19:07:19','2012-05-13 21:09:42'),(44,43,6,180,'','QC',1,'2012-05-13 21:44:59','2012-05-13 22:45:06'),(45,43,6,330,'book has a total of 330 pages','QC',1,'2012-05-14 17:00:36','2012-05-14 19:22:23'),(46,45,6,514,'','QC',1,'2012-05-15 13:27:45','2012-05-15 16:27:51'),(47,46,1,300,'test','QC',1,'2012-05-15 17:22:34','2012-05-15 18:22:37'),(48,47,1,300,'test','QC',1,'2012-05-15 18:42:03','2012-05-15 19:42:07');
/*!40000 ALTER TABLE `ui_processingsession` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-05-15 13:50:48
