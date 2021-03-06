#!/usr/bin/env python
# coding=utf8
import ConfigParser
from dbskit import parse, extract, pack
from dbskit.mysql import CFG as mysql_cfg, orm as mysql_orm
from dbskit.mongo import CFG as mongo_cfg, orm as mongo_orm
from dbskit.mysql.suit import withMysql, withMysqlQuery, withMysqlCount, dbpc as mysql_dbpc
from dbskit.mongo.suit import withMongo, withMongoQuery, withMongoCount, dbpc as mongo_dbpc

config=ConfigParser.ConfigParser()
config.read('../pholcus.cfg')

base = parse(config.items("base"))

if base['type'] == 'mysql':
    basecfg = mysql_cfg
    baseconn = mysql_dbpc
    baseorm = mysql_orm
    withBase = withMysql
else:
    basecfg = mongo_cfg
    baseconn = mongo_dbpc
    baseorm = mongo_orm
    withBase = withMongo
basecfg.R = basecfg.W = base['name']
basecfg._LIMIT = base['limit']
basecfg._BUFFER = base['buffer']
basecfg._SETTING = extract(base)

data = parse(config.items("data"))
if data['type'] == 'mysql':
    datacfg = mysql_cfg
    dataconn = mysql_dbpc
    dataorm = mysql_orm
    withData = withMysql
    withDataQuery = withMysqlQuery
    withDataCount = withMysqlCount
else:
    datacfg = mongo_cfg
    dataconn = mongo_dbpc
    dataorm = mongo_orm
    withData = withMongo
    withDataQuery = withMongoQuery
    withDataCount = withMongoCount
datacfg.R = datacfg.W = data['name']
datacfg._LIMIT = data['limit']
datacfg._BUFFER = data['buffer']
datacfg._SETTING = extract(data)

WORKQUEUE = parse(config.items("work-queue"))
LOGSPAN = config.getint("log", "span")
if LOGSPAN % 3600 == 0:
    TIMEND = 13
elif LOGSPAN % 60 == 0:
    TIMEND = 16
else:
    TIMEND = 19