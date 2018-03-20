/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50720
Source Host           : localhost:3306
Source Database       : lux

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-03-20 11:36:31
*/

SET FOREIGN_KEY_CHECKS=0;

DROP DATABASE IF EXISTS lux;
CREATE DATABASE lux DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;

USE lux;


-- ----------------------------
-- Table structure for tbl_test
-- ----------------------------
DROP TABLE IF EXISTS `tbl_test`;
CREATE TABLE `tbl_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_test
-- ----------------------------
INSERT INTO `tbl_test` VALUES ('1', 'test1');
INSERT INTO `tbl_test` VALUES ('2', 'update test');
INSERT INTO `tbl_test` VALUES ('3', 'update test');
INSERT INTO `tbl_test` VALUES ('7', 'test4');
INSERT INTO `tbl_test` VALUES ('8', 'test4');
INSERT INTO `tbl_test` VALUES ('9', 'test4');
INSERT INTO `tbl_test` VALUES ('10', 'test4');
INSERT INTO `tbl_test` VALUES ('11', 'test4');
INSERT INTO `tbl_test` VALUES ('12', 'test4');
INSERT INTO `tbl_test` VALUES ('13', 'test4');
INSERT INTO `tbl_test` VALUES ('14', 'test4');
INSERT INTO `tbl_test` VALUES ('15', 'insert test');
INSERT INTO `tbl_test` VALUES ('16', 'insert test');
