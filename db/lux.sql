/*
Navicat MySQL Data Transfer

Source Server         : 192.168.1.88_3306
Source Server Version : 50721
Source Host           : 192.168.1.88:3306
Source Database       : lux

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-03-20 23:44:10
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
  `headIMG` varchar(255) DEFAULT NULL COMMENT '文章图片路径',
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article
-- ----------------------------

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article_browsing_history
-- ----------------------------

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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_article_comment
-- ----------------------------

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tbl_user
-- ----------------------------
