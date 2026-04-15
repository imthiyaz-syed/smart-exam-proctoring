/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - face_biometric
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE IF NOT EXISTS `face_biometric` DEFAULT CHARACTER SET latin1;

USE `face_biometric`;

/*Table structure for table `exam_paper` */

DROP TABLE IF EXISTS `exam_paper`;

CREATE TABLE `exam_paper` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `a` varchar(100) DEFAULT NULL,
  `b` text,
  `c` text,
  `d` text,
  `e` text,
  `f` text,
  `g` text,
  `hh` text,
  `i` varchar(100) DEFAULT NULL,
  `exam_name` varchar(100) DEFAULT NULL,
  `exam_date` varchar(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Table structure for table `faculty_registration` */

DROP TABLE IF EXISTS `faculty_registration`;

CREATE TABLE `faculty_registration` (
  `otp` varchar(250) DEFAULT NULL,
  `username` varchar(250) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `department` varchar(250) DEFAULT NULL,
  `emp_id` varchar(250) DEFAULT NULL,
  `pwd` varchar(250) DEFAULT NULL,
  `mobile` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `finalresults` */

DROP TABLE IF EXISTS `finalresults`;

CREATE TABLE `finalresults` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `sid` text,
  `semail` text,
  `ename` text,
  `edate` text,
  `ca` text,
  `ua` text,
  `status` varchar(100) DEFAULT NULL,
  `head_status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Table structure for table `qsn_ans` */

DROP TABLE IF EXISTS `qsn_ans`;

CREATE TABLE `qsn_ans` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `qsn` varchar(100) DEFAULT NULL,
  `opt1` varchar(100) DEFAULT NULL,
  `opt2` varchar(100) DEFAULT NULL,
  `opt3` varchar(100) DEFAULT NULL,
  `opt4` varchar(100) DEFAULT NULL,
  `ans` varchar(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `subject` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Table structure for table `results` */

DROP TABLE IF EXISTS `results`;

CREATE TABLE `results` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `sid` text,
  `sname` text,
  `semail` text,
  `ename` text,
  `edate` text,
  `ca` text,
  `ua` text,
  `status` text,
  `head_status` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Table structure for table `user_registration` */

DROP TABLE IF EXISTS `user_registration`;

CREATE TABLE `user_registration` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `sid` int(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `uname` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  `d1` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
