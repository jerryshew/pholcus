#!/usr/bin/env python
# coding=utf8
import json
import time, datetime
from model.setting import withBase, withData, base, data, _BASE_R, _BASE_W, RDB, WDB
from webcrawl.character import unicode2utf8
from flask import Blueprint, request, Response, render_template, g
from rest import api
from model.base import Article, Creator
from model.log import Statistics

@api.route('/article', methods=['POST'])
@api.route('/article/<aid>', methods=['POST'])
@withBase(RDB, resutype='DICT')
def article(aid=None):
    user = request.user
    condition = request.form.get('condition', '{}')
    condition = json.loads(condition)
    data = request.form.get('data', '{}')
    data = json.loads(data)
    projection = request.form.get('projection', '{}')
    projection = json.loads(projection)

    limit = request.form.get('limit', 'one')

    if aid is not None:
        condition['_id'] = aid
    if data:
        if '_id' in condition:
            Article.update(user, condition, data)
            aid = condition['_id']
        else:
            aid = Article.insert(data)
        result = json.dumps({'stat':1, 'desc':'Article %s is set successfully.' % name, 'aid':aid}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    else:
        if limit == 'one':
            result = Article.queryOne(user, condition)
        else:
            result = list(Article.queryAll(user, condition))
        result = json.dumps({'stat':1, 'desc':'', 'article':result}, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
    return result
        