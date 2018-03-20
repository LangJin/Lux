/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50720
Source Host           : localhost:3306
Source Database       : lux

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-03-20 16:19:23
*/

SET FOREIGN_KEY_CHECKS=0;


DROP DATABASE IF EXISTS lux;
CREATE DATABASE lux DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;

USE lux;


-- ----------------------------
-- Table structure for tbl_admin_info
-- ----------------------------
DROP TABLE IF EXISTS `tbl_admin_info`;
CREATE TABLE `tbl_admin_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '管理员id',
  `username` varchar(255) NOT NULL COMMENT '管理员用户名',
  `password` varchar(255) NOT NULL COMMENT '管理员密码',
  `phoneNum` varchar(255) DEFAULT NULL COMMENT '管理员手机号',
  `registDate` datetime NOT NULL COMMENT '账户注册时间',
  `status` int(255) DEFAULT '1' COMMENT '账号状态1， 1正常；0禁止；3退休xxx',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for tbl_aritcle_like
-- ----------------------------
DROP TABLE IF EXISTS `tbl_aritcle_like`;
CREATE TABLE `tbl_aritcle_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '点赞id',
  `articleId` int(11) NOT NULL COMMENT '点赞的文章id',
  `date` datetime NOT NULL COMMENT '点赞时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for tbl_article
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article`;
CREATE TABLE `tbl_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `title` varchar(255) NOT NULL COMMENT '文章标题',
  `content` text NOT NULL COMMENT '文章内容',
  `headerImage` varchar(255) NOT NULL COMMENT 'header图路径',
  `creteDate` datetime NOT NULL COMMENT '创建时间',
  `type` int(11) NOT NULL COMMENT '文章类型 1:xx模块 2:xxx模块 3:xx模块',
  `isValid` int(11) unsigned zerofill NOT NULL DEFAULT '00000000001' COMMENT '文章是否有效，1为有效，0为无效',
  `userId` int(11) NOT NULL COMMENT '文章所属用户id',
  `isRcommend` int(11) DEFAULT '0' COMMENT '是否在首页推荐',
  `recommendStartDate` datetime DEFAULT NULL COMMENT '推荐开始日期',
  `recommendEndDate` datetime DEFAULT NULL COMMENT '推荐结束日期',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for tbl_article_collect
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article_collect`;
CREATE TABLE `tbl_article_collect` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '收藏id',
  `articleId` int(11) NOT NULL COMMENT '收藏的文章id',
  `date` datetime DEFAULT NULL COMMENT '收藏时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for tbl_article_comment
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article_comment`;
CREATE TABLE `tbl_article_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `content` text NOT NULL COMMENT '评论内容',
  `articeId` int(11) NOT NULL COMMENT '评论文章id',
  `date` datetime NOT NULL COMMENT '评论时间',
  `isValid` int(11) NOT NULL DEFAULT '1' COMMENT '是否有效，1有效，0无效；当文章删除后，评论也应该删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
-- Table structure for tbl_user_info
-- ----------------------------
DROP TABLE IF EXISTS `tbl_user_info`;
CREATE TABLE `tbl_user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `username` varchar(255) NOT NULL COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码',
  `email` varchar(255) DEFAULT NULL COMMENT '邮箱',
  `phoneNum` varchar(255) DEFAULT NULL COMMENT '电话',
  `registIP` varchar(255) DEFAULT NULL COMMENT '注册ip',
  `registDate` datetime NOT NULL COMMENT '注册时间',
  `userPhoto` varchar(255) DEFAULT NULL COMMENT '用户头像地址',
  `status` int(11) DEFAULT NULL COMMENT '用户账号状态，1正常，0封禁',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
