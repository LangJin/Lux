/*
Navicat MySQL Data Transfer

Source Server         : 本机
Source Server Version : 50721
Source Host           : localhost:3306
Source Database       : lux

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-03-30 21:34:35
*/

SET FOREIGN_KEY_CHECKS=0;

DROP DATABASE IF EXISTS lux;
CREATE DATABASE lux DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;

USE lux;


-- ----------------------------
-- Table structure for tbl_admin
-- ----------------------------
DROP TABLE IF EXISTS `tbl_admin`;
CREATE TABLE `tbl_admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `username` varchar(255) NOT NULL COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码',
  `status` int(1) NOT NULL COMMENT '状态',
  `token` varchar(255) NOT NULL COMMENT 'token',
  `remark` varchar(255) NOT NULL COMMENT '备注',
  `createDate` datetime NOT NULL COMMENT '创建时间',
  `updateDate` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_admin
-- ----------------------------
INSERT INTO `tbl_admin` VALUES ('1', 'admin1', 'admin1', '1', 'ry8sp0w9-t6q2-wi9z-3fon-tubr9olmerpd', '1', '2018-03-29 15:41:03', null);

-- ----------------------------
-- Table structure for tbl_announcement
-- ----------------------------
DROP TABLE IF EXISTS `tbl_announcement`;
CREATE TABLE `tbl_announcement` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `content` text NOT NULL COMMENT '内容',
  `status` int(11) NOT NULL COMMENT '状态',
  `userId` varchar(255) NOT NULL COMMENT '发布人id',
  `createDate` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_announcement
-- ----------------------------

-- ----------------------------
-- Table structure for tbl_article
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article`;
CREATE TABLE `tbl_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `title` varchar(255) NOT NULL COMMENT '文章标题',
  `imgId` int(255) DEFAULT NULL COMMENT '文章图片id',
  `type` int(11) NOT NULL COMMENT '文章分类',
  `content` text NOT NULL COMMENT '文章内容',
  `source` varchar(255) DEFAULT NULL COMMENT '文章来源',
  `readCount` int(11) DEFAULT NULL COMMENT '阅读量',
  `likeCount` int(11) DEFAULT NULL COMMENT '点赞量',
  `status` int(11) NOT NULL COMMENT '状态',
  `userId` int(11) NOT NULL COMMENT '发布人id',
  `createDate` datetime DEFAULT NULL COMMENT '创建时间',
  `updateDate` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article
-- ----------------------------
INSERT INTO `tbl_article` VALUES ('1', '测试1', '333', '1', '测试1', '测试1', '2', '1', '1', '1', '2018-03-24 23:59:52', '2018-03-30 11:37:29');
INSERT INTO `tbl_article` VALUES ('2', '测试2', '333', '1', '测试2', '测试2', '2', '1', '1', '1', '2018-03-26 22:42:14', '2018-03-30 11:34:07');
INSERT INTO `tbl_article` VALUES ('3', '测试3', '333', '1', '测试3', '测试3', '1', '1', '1', '1', '2018-03-29 16:24:20', null);
INSERT INTO `tbl_article` VALUES ('4', '测试4', '333', '1', '测试4', '测试4', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('5', '测试5', '333', '1', '测试5', '测试5', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('6', '测试6', '333', '2', '测试6', '测试6', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('7', '测试7', '333', '3', '测试7', '测试7', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('8', '测试8', '333', '4', '测试8', '测试8', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('9', '测试9', '333', '1', '测试9', '测试9', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('10', '测试10', '333', '1', '测试10', '测试10', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('11', '测试11', '333', '1', '测试11', '测试11', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('12', '测试12', '333', '1', '测试12', '测试12', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('13', '测试13', '333', '1', '测试13', '测试13', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('14', '测试14', '333', '1', '测试14', '测试14', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('15', '测试15', '333', '1', '测试15', '测试15', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('16', '测试16', '333', '1', '测试16', '测试16', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('17', '测试17', '333', '1', '测试17', '测试17', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('18', '测试18', '333', '1', '测试18', '测试18', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('19', '测试19', '333', '1', '测试19', '测试19', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('20', '测试20', '333', '1', '测试20', '测试20', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('21', '测试21', '333', '1', '测试21', '测试21', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('22', '测试22', '333', '1', '测试22', '测试22', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('23', '测试23', '333', '1', '测试23', '测试23', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('24', '测试24', '333', '1', '测试24', '测试24', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('25', '测试25', '333', '1', '测试25', '测试25', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('26', '测试26', '333', '1', '测试26', '测试26', '1', '1', '1', '1', '2018-03-29 17:24:20', null);
INSERT INTO `tbl_article` VALUES ('27', '测试27', '333', '1', '测试27', '测试27', '1', '1', '1', '1', '2018-03-29 17:24:20', null);

-- ----------------------------
-- Table structure for tbl_article_browsing_history
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article_browsing_history`;
CREATE TABLE `tbl_article_browsing_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userId` int(11) NOT NULL COMMENT '用户id',
  `articleId` int(11) NOT NULL COMMENT '文章id',
  `status` int(11) NOT NULL,
  `createDate` datetime DEFAULT NULL COMMENT '创建时间',
  `updateDate` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article_browsing_history
-- ----------------------------
INSERT INTO `tbl_article_browsing_history` VALUES ('1', '1', '2', '1', '2018-03-29 16:20:02', '2018-03-30 11:37:29');
INSERT INTO `tbl_article_browsing_history` VALUES ('2', '-1', '1', '1', '2018-03-30 09:56:12', '2018-03-30 11:37:29');
INSERT INTO `tbl_article_browsing_history` VALUES ('3', '1', '1', '1', '2018-03-30 11:11:55', '2018-03-30 11:37:29');
INSERT INTO `tbl_article_browsing_history` VALUES ('4', '-1', '2', '1', '2018-03-30 11:22:50', '2018-03-30 11:37:29');

-- ----------------------------
-- Table structure for tbl_article_collect
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article_collect`;
CREATE TABLE `tbl_article_collect` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userId` int(11) NOT NULL COMMENT '用户id',
  `articleId` int(11) NOT NULL COMMENT '文章id',
  `status` int(11) NOT NULL,
  `createDate` datetime DEFAULT NULL COMMENT '创建时间',
  `updateDate` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article_collect
-- ----------------------------
INSERT INTO `tbl_article_collect` VALUES ('1', '1', '1', '1', '2018-03-30 11:37:18', null);

-- ----------------------------
-- Table structure for tbl_article_comment
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article_comment`;
CREATE TABLE `tbl_article_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userId` int(11) NOT NULL COMMENT '用户id',
  `articleId` int(11) NOT NULL COMMENT '文章id',
  `content` text NOT NULL COMMENT '内容',
  `status` int(11) NOT NULL COMMENT '状态',
  `createDate` datetime NOT NULL COMMENT '创建时间',
  `updateDate` datetime DEFAULT NULL COMMENT '修改时间',
  `fid` int(11) DEFAULT NULL COMMENT '当前评论的父评论id，即回复某个评论的评论id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article_comment
-- ----------------------------
INSERT INTO `tbl_article_comment` VALUES ('1', '1', '1', '文章id为1的评论', '1', '2018-03-26 22:45:44', null, null);
INSERT INTO `tbl_article_comment` VALUES ('2', '1', '2', '1234', '1', '2018-03-26 22:45:52', null, null);
INSERT INTO `tbl_article_comment` VALUES ('3', '1', '1', '评论id为1的回复内容', '1', '2018-03-27 20:12:12', null, '1');
INSERT INTO `tbl_article_comment` VALUES ('4', '1', '1', '评论id为3的回复内容', '1', '2018-03-27 20:25:28', null, '3');
INSERT INTO `tbl_article_comment` VALUES ('5', '1', '2', 'test', '1', '2018-03-30 11:19:16', null, null);
INSERT INTO `tbl_article_comment` VALUES ('6', '1', '2', 'tes11111t', '1', '2018-03-30 11:25:28', null, null);
INSERT INTO `tbl_article_comment` VALUES ('9', '1', '2', 'reply comment 5111', '1', '2018-03-30 11:33:57', null, '5');

-- ----------------------------
-- Table structure for tbl_article_like
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article_like`;
CREATE TABLE `tbl_article_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userId` int(11) NOT NULL COMMENT '用户id',
  `articleId` int(11) NOT NULL COMMENT '文章id',
  `status` int(11) NOT NULL,
  `createDate` datetime DEFAULT NULL COMMENT '创建时间',
  `updateDate` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article_like
-- ----------------------------
INSERT INTO `tbl_article_like` VALUES ('1', '1', '2', '0', '2018-03-30 11:39:02', null);
INSERT INTO `tbl_article_like` VALUES ('2', '1', '1', '1', '2018-03-30 11:39:24', null);

-- ----------------------------
-- Table structure for tbl_image_sources
-- ----------------------------
DROP TABLE IF EXISTS `tbl_image_sources`;
CREATE TABLE `tbl_image_sources` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `path` varchar(255) DEFAULT NULL COMMENT '路径',
  `status` int(11) DEFAULT NULL COMMENT '状态',
  `createDate` datetime DEFAULT NULL COMMENT '创建时间',
  `updateDate` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_image_sources
-- ----------------------------
INSERT INTO `tbl_image_sources` VALUES ('1', 'e205xsh4-5wk5-1v26-yrks-eeaaxs2b2ap5.png', '1', '2018-03-30 17:41:33', null);
INSERT INTO `tbl_image_sources` VALUES ('2', 'oi51ymvi-kqe0-uajr-54kc-hruqbbuhqof0.jpg', '1', '2018-03-30 17:42:16', null);

-- ----------------------------
-- Table structure for tbl_user
-- ----------------------------
DROP TABLE IF EXISTS `tbl_user`;
CREATE TABLE `tbl_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `username` varchar(255) NOT NULL COMMENT '账户',
  `password` varchar(255) DEFAULT NULL COMMENT '密码',
  `nickname` varchar(255) DEFAULT NULL COMMENT '昵称',
  `status` int(11) NOT NULL COMMENT '状态',
  `signature` varchar(255) DEFAULT NULL COMMENT '个性签名',
  `sex` varchar(255) DEFAULT NULL COMMENT '学别',
  `education` varchar(255) DEFAULT NULL COMMENT '学历',
  `age` int(11) DEFAULT NULL COMMENT '年龄',
  `email` varchar(255) DEFAULT NULL COMMENT '邮箱',
  `cellphone` varchar(255) DEFAULT NULL COMMENT '手机号',
  `address` varchar(255) DEFAULT NULL COMMENT '地址',
  `wechat` varchar(255) DEFAULT NULL COMMENT '微信',
  `headImage` varchar(255) DEFAULT NULL COMMENT '头像',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `createDate` datetime NOT NULL COMMENT '创建时间',
  `updateDate` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_user
-- ----------------------------
INSERT INTO `tbl_user` VALUES ('1', 'user', 'user', 'snake', '1', 'signature', '男', 'education', '24', 'test@qq.com', '15000000000', 'test', 'snake', '', 'greate full!', '2018-03-24 23:38:48', '2018-03-30 11:11:16');
INSERT INTO `tbl_user` VALUES ('2', 'user1', 'user1', 'None', '1', '', '', '', null, '', '', '', '', '', '', '2018-03-26 23:09:03', null);
INSERT INTO `tbl_user` VALUES ('3', 'user2', 'user2', 'None', '1', '', '', '', null, '', '', '', '', '', '', '2018-03-26 23:10:55', null);
INSERT INTO `tbl_user` VALUES ('4', 'user3', 'user3', 'None', '1', '', '', '', null, '', '', '', '', '', '', '2018-03-26 15:15:46', null);
INSERT INTO `tbl_user` VALUES ('5', 'user3', 'user3', 'None', '1', '', '', '', null, '', '', '', '', '', '', '2018-03-27 00:54:30', null);
INSERT INTO `tbl_user` VALUES ('6', 'user33', '123', 'user33', '1', '', '', '', null, '', '', '', '', '', '', '2018-03-30 11:10:03', null);
