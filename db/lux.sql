/*
Navicat MySQL Data Transfer

Source Server         : 本机
Source Server Version : 50721
Source Host           : 127.0.0.1:3306
Source Database       : lux

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-03-27 21:41:30
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_admin
-- ----------------------------

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
  `headImage` varchar(255) DEFAULT NULL COMMENT '文章图片路径',
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article
-- ----------------------------
INSERT INTO `tbl_article` VALUES ('1', '测试', 'iyojdz01-f2wm-v9mt-1s0i-hbpidjz6ljxx.JPG', '1', '测试', '测试', '9', '1', '1', '1', '2018-03-24 23:59:52', '2018-03-27 21:14:41');
INSERT INTO `tbl_article` VALUES ('2', '123', 'xx', '1', '123', '123', '3', '1', '1', '1', '2018-03-26 22:42:14', '2018-03-27 21:14:27');

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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article_browsing_history
-- ----------------------------
INSERT INTO `tbl_article_browsing_history` VALUES ('1', '1', '1', '1', '2018-03-25 00:00:11', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('2', '-1', '1', '1', '2018-03-27 21:08:51', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('3', '-1', '1', '1', '2018-03-27 21:09:16', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('4', '-1', '1', '1', '2018-03-27 21:09:50', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('5', '-1', '1', '1', '2018-03-27 21:10:30', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('6', '-1', '1', '1', '2018-03-27 21:11:20', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('7', '-1', '1', '1', '2018-03-27 21:11:46', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('8', '1', '1', '1', '2018-03-27 21:12:09', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('9', '-1', '2', '1', '2018-03-27 21:13:20', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('10', '1', '2', '1', '2018-03-27 21:13:40', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('11', '2', '2', '1', '2018-03-27 21:14:27', null);
INSERT INTO `tbl_article_browsing_history` VALUES ('12', '2', '1', '1', '2018-03-27 21:14:41', null);

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article_collect
-- ----------------------------

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
  `fatherId` int(11) DEFAULT NULL COMMENT '当前评论的父评论id，即回复某个评论的评论id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article_comment
-- ----------------------------
INSERT INTO `tbl_article_comment` VALUES ('1', '1', '1', '文章id为1的评论', '1', '2018-03-26 22:45:44', null, null);
INSERT INTO `tbl_article_comment` VALUES ('2', '1', '2', '1234', '1', '2018-03-26 22:45:52', null, null);
INSERT INTO `tbl_article_comment` VALUES ('3', '1', '1', '评论id为1的回复内容', '1', '2018-03-27 20:12:12', null, '1');
INSERT INTO `tbl_article_comment` VALUES ('4', '1', '1', '评论id为3的回复内容', '1', '2018-03-27 20:25:28', null, '3');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article_like
-- ----------------------------

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_image_sources
-- ----------------------------

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_user
-- ----------------------------
INSERT INTO `tbl_user` VALUES ('1', 'user', 'user', 'snake', '1', 'signature', '男', 'education', '22', 'test@qq.com', '15000000000', 'test', 'snake', '', 'greate full!', '2018-03-24 23:38:48', '2018-03-27 14:23:34');
INSERT INTO `tbl_user` VALUES ('2', 'user1', 'user1', 'None', '1', '', '', '', null, '', '', '', '', '', '', '2018-03-26 23:09:03', null);
INSERT INTO `tbl_user` VALUES ('3', 'user2', 'user2', 'None', '1', '', '', '', null, '', '', '', '', '', '', '2018-03-26 23:10:55', null);
INSERT INTO `tbl_user` VALUES ('4', 'user3', 'user3', 'None', '1', '', '', '', null, '', '', '', '', '', '', '2018-03-26 15:15:46', null);
INSERT INTO `tbl_user` VALUES ('5', 'user3', 'user3', 'None', '1', '', '', '', null, '', '', '', '', '', '', '2018-03-27 00:54:30', null);
