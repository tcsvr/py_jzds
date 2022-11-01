/*
Navicat MySQL Data Transfer

Source Server         : 本地
Source Server Version : 50726
Source Host           : localhost:3306
Source Database       : is_shenzhen90_com

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2022-10-31 15:46:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ba_jz_contend
-- ----------------------------
DROP TABLE IF EXISTS `ba_jz_contend`;
CREATE TABLE `ba_jz_contend` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pid` int(10) DEFAULT NULL COMMENT '店铺id',
  `sale` int(10) DEFAULT '0' COMMENT '日销售量',
  `sales` int(10) DEFAULT NULL COMMENT '总销售量',
  `time` int(10) DEFAULT NULL COMMENT '时间',
  `city` varchar(50) DEFAULT NULL COMMENT '城市',
  `rprice` int(10) DEFAULT '0' COMMENT '涨价',
  `tprice` int(10) DEFAULT '0' COMMENT '降价',
  `shelves` int(10) DEFAULT '0' COMMENT '上架',
  `tshelves` int(10) DEFAULT '0' COMMENT '下架',
  `con` int(10) DEFAULT '0' COMMENT '项目总数',
  PRIMARY KEY (`id`),
  KEY `pid` (`pid`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=utf8 COMMENT='竞争店铺数据';

-- ----------------------------
-- Records of ba_jz_contend
-- ----------------------------
INSERT INTO `ba_jz_contend` VALUES ('1', '1', '40', '665', '1666540800', '上海', '0', '0', '1', '1', '0');
INSERT INTO `ba_jz_contend` VALUES ('2', '1', '0', '6660', '1666540800', '上海', '0', '0', '0', '0', '0');
INSERT INTO `ba_jz_contend` VALUES ('3', '1', '0', '6660', '1666540800', '上海', '0', '0', '0', '0', '0');
INSERT INTO `ba_jz_contend` VALUES ('4', '1', '0', '13402', '1666540800', '上海', '0', '0', '0', '0', '116');
INSERT INTO `ba_jz_contend` VALUES ('5', '1', '5479', '11145', '1666540800', '上海', '0', '0', '4', '1', '116');
INSERT INTO `ba_jz_contend` VALUES ('6', '1', '6', '11151', '1666627200', '上海', '0', '0', '0', '0', '116');
INSERT INTO `ba_jz_contend` VALUES ('7', '2', '0', '7631', '1666627200', '上海', '0', '0', '0', '0', '75');
INSERT INTO `ba_jz_contend` VALUES ('8', '4', '0', '5989', '1666627200', '上海', '0', '0', '0', '0', '45');
INSERT INTO `ba_jz_contend` VALUES ('9', '3', '0', '45116', '1666627200', '上海', '0', '0', '0', '0', '176');
INSERT INTO `ba_jz_contend` VALUES ('10', '1', '4', '11175', '1666713600', '上海', '0', '0', '0', '0', '116');
INSERT INTO `ba_jz_contend` VALUES ('11', '2', '1', '7641', '1666713600', '上海', '1', '0', '0', '0', '75');
INSERT INTO `ba_jz_contend` VALUES ('12', '3', '34', '45136', '1666713600', '上海', '0', '0', '1', '1', '176');
INSERT INTO `ba_jz_contend` VALUES ('13', '4', '1', '5998', '1666713600', '上海', '0', '0', '0', '0', '45');
INSERT INTO `ba_jz_contend` VALUES ('22', '1', '5', '11171', '1666886400', '上海', '0', '0', '0', '0', '116');
INSERT INTO `ba_jz_contend` VALUES ('23', '2', '3', '7644', '1666886400', '上海', '0', '0', '0', '0', '73');
INSERT INTO `ba_jz_contend` VALUES ('24', '3', '24', '45226', '1666886400', '上海', '1', '0', '2', '1', '176');
INSERT INTO `ba_jz_contend` VALUES ('25', '4', '9', '6050', '1666886400', '上海', '1', '1', '0', '1', '44');
INSERT INTO `ba_jz_contend` VALUES ('26', '1', '5', '11224', '1666972800', '上海', '0', '0', '1', '0', '116');
INSERT INTO `ba_jz_contend` VALUES ('27', '2', '0', '7677', '1666972800', '上海', '0', '0', '1', '1', '74');
INSERT INTO `ba_jz_contend` VALUES ('28', '3', '583', '45888', '1666972800', '上海', '0', '0', '5', '0', '177');
INSERT INTO `ba_jz_contend` VALUES ('29', '4', '0', '6117', '1666972800', '上海', '0', '0', '0', '0', '44');
INSERT INTO `ba_jz_contend` VALUES ('30', '1', '0', '11224', '1667059200', '上海', '0', '0', '0', '1', '116');
INSERT INTO `ba_jz_contend` VALUES ('31', '2', '0', '7677', '1667059200', '上海', '0', '0', '0', '0', '74');
INSERT INTO `ba_jz_contend` VALUES ('32', '3', '0', '45889', '1667059200', '上海', '0', '0', '0', '0', '177');
INSERT INTO `ba_jz_contend` VALUES ('33', '4', '0', '6117', '1667059200', '上海', '0', '0', '0', '1', '44');
INSERT INTO `ba_jz_contend` VALUES ('34', '1', '0', '11224', '1667145600', '上海', '0', '0', '0', '0', '116');
INSERT INTO `ba_jz_contend` VALUES ('35', '2', '0', '7677', '1667145600', '上海', '0', '0', '0', '0', '74');
INSERT INTO `ba_jz_contend` VALUES ('36', '3', '0', '45888', '1667145600', '上海', '0', '0', '0', '0', '177');
INSERT INTO `ba_jz_contend` VALUES ('37', '4', '0', '6117', '1667145600', '上海', '0', '0', '0', '0', '44');
