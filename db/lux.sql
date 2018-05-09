/*
 Navicat Premium Data Transfer

 Source Server         : 本机
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : localhost:3306
 Source Schema         : lux

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 09/05/2018 18:09:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP DATABASE IF EXISTS lux;
CREATE DATABASE lux DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;

USE lux;

-- ----------------------------
-- Table structure for tbl_admin
-- ----------------------------
DROP TABLE IF EXISTS `tbl_admin`;
CREATE TABLE `tbl_admin`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `status` int(1) NOT NULL COMMENT '状态',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'token',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '备注',
  `createDate` datetime(0) NOT NULL COMMENT '创建时间',
  `updateDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_admin
-- ----------------------------
INSERT INTO `tbl_admin` VALUES (1, 'admin1', 'admin1', 1, 'zwoqgqod-c392-ingy-6cyl-stvk7nadyrpe', '1', '2018-03-29 15:41:03', NULL);

-- ----------------------------
-- Table structure for tbl_announcement
-- ----------------------------
DROP TABLE IF EXISTS `tbl_announcement`;
CREATE TABLE `tbl_announcement`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '内容',
  `status` int(11) NOT NULL COMMENT '状态',
  `userId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '发布人id',
  `createDate` datetime(0) NOT NULL COMMENT '创建时间',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_announcement
-- ----------------------------
INSERT INTO `tbl_announcement` VALUES (1, '测试12', 0, '1', '2018-04-02 14:33:54', '测试12');
INSERT INTO `tbl_announcement` VALUES (2, '测试公告2', 1, '1', '2018-04-02 14:34:08', '关于xxx论坛上线公告2');
INSERT INTO `tbl_announcement` VALUES (3, '测试公告3', 1, '1', '2018-04-02 14:41:12', '关于xxx论坛上线公告3');
INSERT INTO `tbl_announcement` VALUES (4, '测试公告4', 1, '1', '2018-04-02 14:41:25', '关于xxx论坛上线公告4');
INSERT INTO `tbl_announcement` VALUES (5, '测试公告5', 1, '1', '2018-04-02 14:41:36', '关于xxx论坛上线公告5');
INSERT INTO `tbl_announcement` VALUES (6, '测试公告6', 1, '1', '2018-04-02 14:41:44', '关于xxx论坛上线公告6');
INSERT INTO `tbl_announcement` VALUES (7, '测试公告7', 1, '1', '2018-04-02 14:41:50', '关于xxx论坛上线公告7');
INSERT INTO `tbl_announcement` VALUES (8, '测试公告8', 1, '1', '2018-04-02 14:41:59', '关于xxx论坛上线公告8');
INSERT INTO `tbl_announcement` VALUES (9, '测试公告9', 1, '1', '2018-04-02 14:42:05', '关于xxx论坛上线公告9');
INSERT INTO `tbl_announcement` VALUES (10, '测试公告10', 1, '1', '2018-04-02 14:42:15', '关于xxx论坛上线公告10');
INSERT INTO `tbl_announcement` VALUES (11, '测试公告11', 1, '1', '2018-04-02 14:42:32', '关于xxx论坛上线公告11');
INSERT INTO `tbl_announcement` VALUES (12, '测试12', 1, '1', '2018-04-02 15:38:42', '测试12');
INSERT INTO `tbl_announcement` VALUES (13, '测试', 1, '1', '2018-04-04 15:29:44', '测试');
INSERT INTO `tbl_announcement` VALUES (14, '测试', 1, '1', '2018-05-09 17:49:07', '测试');

-- ----------------------------
-- Table structure for tbl_article
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article`;
CREATE TABLE `tbl_article`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文章标题',
  `imgId` int(255) NULL DEFAULT NULL COMMENT '文章图片id',
  `type` int(11) NOT NULL COMMENT '文章分类',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文章内容',
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章来源',
  `readCount` int(11) NULL DEFAULT NULL COMMENT '阅读量',
  `likeCount` int(11) NULL DEFAULT NULL COMMENT '点赞量',
  `status` int(11) NOT NULL COMMENT '状态',
  `userId` int(11) NOT NULL COMMENT '发布人id',
  `createDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `updateDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_article
-- ----------------------------
INSERT INTO `tbl_article` VALUES (1, 'title_test', 2, 1, 'test_test', '1', 9, 1, 1, 1, '2018-03-24 23:59:52', '2018-05-09 17:10:45');
INSERT INTO `tbl_article` VALUES (2, '测试2', 333, 1, '测试2', '测试2', 2, 1, 1, 1, '2018-03-26 22:42:14', '2018-03-30 11:34:07');
INSERT INTO `tbl_article` VALUES (3, '测试3', 333, 1, '测试3', '测试3', 1, 1, 1, 1, '2018-03-29 16:24:20', NULL);
INSERT INTO `tbl_article` VALUES (4, '测试4', 333, 1, '测试4', '测试4', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (5, '测试5', 333, 1, '测试5', '测试5', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (6, '测试6', 333, 2, '测试6', '测试6', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (7, '测试7', 333, 3, '测试7', '测试7', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (8, '测试8', 333, 4, '测试8', '测试8', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (9, '测试9', 333, 1, '测试9', '测试9', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (10, '测试10', 333, 1, '测试10', '测试10', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (11, '测试11', 333, 1, '测试11', '测试11', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (12, '测试12', 333, 1, '测试12', '测试12', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (13, '测试13', 333, 1, '测试13', '测试13', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (14, '测试14', 333, 1, '测试14', '测试14', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (15, '测试15', 333, 1, '测试15', '测试15', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (16, '测试16', 333, 1, '测试16', '测试16', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (17, '测试17', 333, 1, '测试17', '测试17', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (18, '测试18', 333, 1, '测试18', '测试18', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (19, '测试19', 333, 1, '测试19', '测试19', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (20, '测试20', 333, 1, '测试20', '测试20', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (21, '测试21', 333, 1, '测试21', '测试21', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (22, '测试22', 333, 1, '测试22', '测试22', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (23, '测试23', 333, 1, '测试23', '测试23', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (24, '测试24', 333, 1, '测试24', '测试24', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (25, '测试25', 333, 1, '测试25', '测试25', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (26, '测试26', 333, 1, '测试26', '测试26', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (27, '测试27', 333, 1, '测试27', '测试27', 1, 1, 1, 1, '2018-03-29 17:24:20', NULL);
INSERT INTO `tbl_article` VALUES (30, 'title', 1, 2, 'test', '123', 0, 0, 1, 1, '2018-04-04 15:28:09', NULL);
INSERT INTO `tbl_article` VALUES (31, 'title', 1, 2, 'test', '123', 0, 0, 1, 1, '2018-04-04 15:29:00', NULL);
INSERT INTO `tbl_article` VALUES (32, 'title', 1, 2, 'test', '123', 0, 0, 1, 1, '2018-05-09 17:08:34', NULL);

-- ----------------------------
-- Table structure for tbl_article_browsing_history
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article_browsing_history`;
CREATE TABLE `tbl_article_browsing_history`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userId` int(11) NOT NULL COMMENT '用户id',
  `articleId` int(11) NOT NULL COMMENT '文章id',
  `status` int(11) NOT NULL,
  `createDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `updateDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_article_browsing_history
-- ----------------------------
INSERT INTO `tbl_article_browsing_history` VALUES (1, 1, 2, 1, '2018-03-29 16:20:02', '2018-05-09 16:37:37');
INSERT INTO `tbl_article_browsing_history` VALUES (2, -1, 1, 1, '2018-03-30 09:56:12', '2018-05-09 16:37:37');
INSERT INTO `tbl_article_browsing_history` VALUES (3, 1, 1, 1, '2018-03-30 11:11:55', '2018-05-09 16:37:37');
INSERT INTO `tbl_article_browsing_history` VALUES (4, -1, 2, 1, '2018-03-30 11:22:50', '2018-05-09 16:37:37');
INSERT INTO `tbl_article_browsing_history` VALUES (5, 2, 1, 1, '2018-04-02 10:35:47', '2018-05-09 16:37:37');

-- ----------------------------
-- Table structure for tbl_article_collect
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article_collect`;
CREATE TABLE `tbl_article_collect`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userId` int(11) NOT NULL COMMENT '用户id',
  `articleId` int(11) NOT NULL COMMENT '文章id',
  `status` int(11) NOT NULL,
  `createDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `updateDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_article_collect
-- ----------------------------
INSERT INTO `tbl_article_collect` VALUES (1, 1, 1, 1, '2018-03-30 11:37:18', NULL);

-- ----------------------------
-- Table structure for tbl_article_comment
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article_comment`;
CREATE TABLE `tbl_article_comment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userId` int(11) NOT NULL COMMENT '用户id',
  `articleId` int(11) NOT NULL COMMENT '文章id',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '内容',
  `status` int(11) NOT NULL COMMENT '状态',
  `createDate` datetime(0) NOT NULL COMMENT '创建时间',
  `updateDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  `fid` int(11) NULL DEFAULT NULL COMMENT '当前评论的父评论id，即回复某个评论的评论id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_article_comment
-- ----------------------------
INSERT INTO `tbl_article_comment` VALUES (1, 1, 1, '文章id为1的评论', 1, '2018-03-26 22:45:44', NULL, NULL);
INSERT INTO `tbl_article_comment` VALUES (2, 1, 2, '1234', 1, '2018-03-26 22:45:52', NULL, NULL);
INSERT INTO `tbl_article_comment` VALUES (3, 1, 1, '评论id为1的回复内容', 1, '2018-03-27 20:12:12', NULL, 1);
INSERT INTO `tbl_article_comment` VALUES (4, 1, 1, '评论id为3的回复内容', 1, '2018-03-27 20:25:28', NULL, 3);
INSERT INTO `tbl_article_comment` VALUES (5, 1, 2, 'test', 1, '2018-03-30 11:19:16', NULL, NULL);
INSERT INTO `tbl_article_comment` VALUES (6, 1, 2, 'tes11111t', 1, '2018-03-30 11:25:28', NULL, NULL);
INSERT INTO `tbl_article_comment` VALUES (9, 1, 2, 'reply comment 5111', 1, '2018-03-30 11:33:57', NULL, 5);
INSERT INTO `tbl_article_comment` VALUES (10, 1, 2, 'tes11111t', 1, '2018-04-04 15:27:39', NULL, NULL);
INSERT INTO `tbl_article_comment` VALUES (11, 1, 2, 'reply comment 5111', 1, '2018-04-04 15:27:42', NULL, 5);
INSERT INTO `tbl_article_comment` VALUES (12, 1, 2, 'tes11111t', 1, '2018-05-09 16:10:20', NULL, NULL);
INSERT INTO `tbl_article_comment` VALUES (13, 1, 1, 'test', 1, '2018-05-09 16:12:09', NULL, 5);
INSERT INTO `tbl_article_comment` VALUES (14, 1, 2, 'tes11111t', 1, '2018-05-09 16:37:46', NULL, NULL);
INSERT INTO `tbl_article_comment` VALUES (15, 1, 1, 'test', 1, '2018-05-09 16:37:53', NULL, 5);

-- ----------------------------
-- Table structure for tbl_article_like
-- ----------------------------
DROP TABLE IF EXISTS `tbl_article_like`;
CREATE TABLE `tbl_article_like`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userId` int(11) NOT NULL COMMENT '用户id',
  `articleId` int(11) NOT NULL COMMENT '文章id',
  `status` int(11) NOT NULL,
  `createDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `updateDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_article_like
-- ----------------------------
INSERT INTO `tbl_article_like` VALUES (1, 1, 2, 0, '2018-03-30 11:39:02', NULL);
INSERT INTO `tbl_article_like` VALUES (2, 1, 1, 1, '2018-03-30 11:39:24', NULL);

-- ----------------------------
-- Table structure for tbl_carouse
-- ----------------------------
DROP TABLE IF EXISTS `tbl_carouse`;
CREATE TABLE `tbl_carouse`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL COMMENT '0：url内容；1：文章类型内容',
  `imgId` int(11) NOT NULL COMMENT '图片id',
  `status` int(11) NOT NULL COMMENT '0：无效；1：有效',
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `createDate` datetime(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_carouse
-- ----------------------------
INSERT INTO `tbl_carouse` VALUES (1, 0, 1, 0, '', 'http://www.google.com/', '2018-04-03 22:59:55');
INSERT INTO `tbl_carouse` VALUES (2, 0, 1, 2, '测试测试', '', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (3, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (4, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (5, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (6, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (7, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (8, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (9, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (10, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (11, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (12, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (13, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (14, 1, 1, 1, NULL, 'http://www.baidu.com/', '2018-04-03 23:14:43');
INSERT INTO `tbl_carouse` VALUES (20, 0, 1, 1, '', 'http://www.google.com/', '2018-04-03 23:51:56');
INSERT INTO `tbl_carouse` VALUES (21, 0, 1, 1, '', 'http://www.google.com/', '2018-04-04 15:29:56');
INSERT INTO `tbl_carouse` VALUES (22, 0, 1, 1, '', 'http://www.google.com/', '2018-05-09 17:57:58');

-- ----------------------------
-- Table structure for tbl_image_sources
-- ----------------------------
DROP TABLE IF EXISTS `tbl_image_sources`;
CREATE TABLE `tbl_image_sources`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '路径',
  `status` int(11) NULL DEFAULT NULL COMMENT '状态',
  `createDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `updateDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_image_sources
-- ----------------------------
INSERT INTO `tbl_image_sources` VALUES (1, 'e205xsh4-5wk5-1v26-yrks-eeaaxs2b2ap5.png', 1, '2018-03-30 17:41:33', NULL);
INSERT INTO `tbl_image_sources` VALUES (2, 'oi51ymvi-kqe0-uajr-54kc-hruqbbuhqof0.jpg', 1, '2018-03-30 17:42:16', NULL);
INSERT INTO `tbl_image_sources` VALUES (3, 'x8yq1imy-1gf0-k8k8-lp5e-szvthxnww3bl.png', 1, '2018-04-04 15:25:20', NULL);

-- ----------------------------
-- Table structure for tbl_user
-- ----------------------------
DROP TABLE IF EXISTS `tbl_user`;
CREATE TABLE `tbl_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '账户',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '昵称',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'token',
  `status` int(11) NOT NULL COMMENT '状态',
  `signature` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '个性签名',
  `sex` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '学别',
  `education` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '学历',
  `age` int(11) NULL DEFAULT NULL COMMENT '年龄',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `cellphone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '手机号',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地址',
  `wechat` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '微信',
  `imgId` int(11) NULL DEFAULT NULL COMMENT '头像id',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `createDate` datetime(0) NOT NULL COMMENT '创建时间',
  `updateDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_user
-- ----------------------------
INSERT INTO `tbl_user` VALUES (1, 'test', 'test', 'snake', 'xlq710os-spxf-ih9k-g2xy-ekuh25oqpj0x', 1, 'signature', '男', 'education', 22, 'test@qq.com', '15000000000', 'test', 'snake', 1, 'greate full!', '2018-04-04 14:41:54', '2018-05-09 17:40:20');
INSERT INTO `tbl_user` VALUES (7, 'user33', '123', 'nickname', NULL, 1, '', '', '', NULL, '', '', '', '', NULL, '', '2018-05-09 17:37:58', NULL);
INSERT INTO `tbl_user` VALUES (8, 'user3322', '123', 'user33', NULL, 1, '', '', '', NULL, '', '', '', '', NULL, '', '2018-05-09 17:38:25', NULL);

SET FOREIGN_KEY_CHECKS = 1;
