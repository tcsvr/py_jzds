/*
Navicat MySQL Data Transfer

Source Server         : 本地
Source Server Version : 50726
Source Host           : localhost:3306
Source Database       : is_shenzhen90_com

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2022-10-31 15:45:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ba_jz_shop
-- ----------------------------
DROP TABLE IF EXISTS `ba_jz_shop`;
CREATE TABLE `ba_jz_shop` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '店铺名称',
  `url` varchar(100) NOT NULL COMMENT '店铺地址',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ba_jz_shop
-- ----------------------------
INSERT INTO `ba_jz_shop` VALUES ('1', '静和医疗美容(人民广场店)', 'https://www.dianping.com/shop/G7Yc9UhIsKP88luu');
INSERT INTO `ba_jz_shop` VALUES ('2', '上海鹏爱医疗美容(人民广场店)', 'https://www.dianping.com/shop/l9pH11K90f0a9dDA');
INSERT INTO `ba_jz_shop` VALUES ('3', '上海薇琳医疗美容医院', 'https://www.dianping.com/shop/l5kzDxpJs4vd1LGQ');
INSERT INTO `ba_jz_shop` VALUES ('4', '上海芙艾东银门诊(陆家嘴店)', 'https://www.dianping.com/shop/H3jIjng6tblpk41Y');
