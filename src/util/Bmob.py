# -*- coding: UTF-8 -*
'''
Created on 2015年7月2日

@author: RobinTang

https://github.com/sintrb/Bmob-Py

'''
import json
import copy
import functools
import requests
from urllib import parse
from .config import *

def _urljoin(func):
    @functools.wraps(func)
    def _wrapper(self, resource_path, *args, **kwargs):
        url = self.apiurl + '/' + resource_path
        return func(self, url, *args, **kwargs)
    return _wrapper


def urlencode(params):
    if isinstance(params, dict):
        return parse.urlencode(params)
    elif isinstance(params, list):
        return parse.quote(''.join(params))
    else:
        return parse.quote(params)


class BmobSDK(object):
    '''
    BmobSDK, create with Application ID and REST API Key. You can use she same Application with BmobSDK.setup() method.
    '''
    context = None

    def __init__(self, appid, restkey, apiurl='http://api.bmob.cn/1/classes'):
        super(BmobSDK, self).__init__()
        self.appid = appid
        self.restkey = restkey
        self.apiurl = apiurl
        self._http_headers = {
                "x-Bmob-Application-Id": self.appid,
                "X-Bmob-REST-API-Key": self.restkey,
                "Content-Type": "application/json"}
        # https://stackoverflow.com/questions/24873927/python-requests-module-and-connection-reuse
        # 连接重用，防止出现连接数过多抛出异常
        # https://2.python-requests.org//en/latest/user/advanced/#session-objects
        self.session = requests.Session()
    @_urljoin
    def get(self, url):
        return self.session.get(url, headers=self._http_headers)

    @_urljoin
    def post(self, url, **kwargs):
        return self.session.post(url, json=kwargs.get('data'), headers=self._http_headers)

    @_urljoin
    def put(self, url, **kwargs):
        return self.session.put(url, json=kwargs.get('data'), headers=self._http_headers)

    @_urljoin
    def delete(self, url, **kwargs):
        return self.session.delete(url, headers=self._http_headers)

    
    @staticmethod
    def setup(appid, restkey):
        BmobSDK.context = BmobSDK(appid, restkey)


class Query(object):
    '''
    Bmob Query
    '''

    def __init__(self, clz, context=None):
        super(Query, self).__init__()
        if not context:
            context = BmobSDK.context
        if not context:
            raise BaseException("No BmobSDK context setuped!")
        self.context = context
        self.clz = clz
        self.q = {}
        self.w = {}  # where
        self.items = None

    def copy(self):
        q = Query(self.clz, self.context)
        q.q = copy.deepcopy(self.q)
        q.w = copy.deepcopy(self.w)
        return q

    def get_urlencode(self):
        if self.w:
            self.q['where'] = json.dumps(self.w)
        elif 'where' in self.q:
            del self.q['where']
        return urlencode(self.q)

    def order(self, o):
        self.q['order'] = o
        return self.copy()

    def limit(self, l):
        self.q['limit'] = l
        return self.copy()

    def skip(self, s):
        self.q['skip'] = s
        return self.copy()

    def count(self):
        if not self.items is None:
            return len(self.items)
        else:
            self.limit(0)
            self.q['count'] = 1
            path = '/'.join([self.clz.__name__, '?' + self.get_urlencode()])
            return self.context.get(path).json()['count']

    def get_kw(self, k):
        if k in self.w:
            return self.w[k]
        else:
            self.w[k] = {}
            return self.w[k]

    def w_eq(self, k, v):
        '''equal'''
        self.w[k] = v
        return self.copy()

    def w_lt(self, k, v):
        '''less than'''
        self.get_kw(k)['$lt'] = v
        return self.copy()

    def w_lte(self, k, v):
        '''less than or equal'''
        self.get_kw(k)['$lte'] = v
        return self.copy()

    def w_gt(self, k, v):
        '''greater than'''
        self.geet_kw(k)['$gt'] = v
        return self.copy()

    def w_gte(self, k, v):
        '''greater than or equal'''
        self.get_kw(k)['$gte'] = v
        return self.copy()

    def w_ne(self, k, v):
        '''not equal'''
        self.get_kw(k)['$ne'] = v
        return self.copy()

    def w_in(self, k, v):
        '''in'''
        self.get_kw(k)['$in'] = v
        return self.copy()

    def w_nin(self, k, v):
        '''not in'''
        self.get_kw(k)['$nin'] = v
        return self.copy()

    def w_exists(self, k, v):
        self.get_kw(k)['$exists'] = v
        return self.copy()

    def w_select(self, k, v):
        self.get_kw(k)['$select'] = v
        return self.copy()

    def w_dontSelect(self, k, v):
        self.get_kw(k)['$dontSelect'] = v
        return self.copy()

    def w_all(self, k, v):
        self.get_kw(k)['$all'] = v
        return self.copy()

    def w_regex(self, k, v):
        self.get_kw(k)['$regex'] = v
        return self.copy()

    def exec_query(self):
        rs = []
        path = '/'.join([self.clz.__name__, '?' + self.get_urlencode()])
        for r in self.context.get(path).json()['results']:
            rs.append(self.clz(**r))
        self.items = rs
        return self.items

    def first(self):
        q = self.copy()
        q.limit(1)
        rs = q.exec_query()
        return len(rs) and rs[0] or None

    def __getslice__(self, s, e):
        if self.items is None:
            self.exec_query()
        return self.items.__getslice__(s, e)

    def __iter__(self):
        if self.items is None:
            self.exec_query()
        return iter(self.items)

    def __getitem__(self, k):
        if self.items is None:
            self.exec_query()
        return self.items.__getitem__(k)

    def __len__(self):
        return self.count()


class BmobModel(object):
    '''
    Basic Bmob model, all other Bmob model must inherit this class.
    '''

    def __init__(self, context=None, objectId=None, **kwargs):
        super(BmobModel, self).__init__()
        # check objectId
        if isinstance(context, str):
            objectId = context
            context = None

        if not context:
            context = BmobSDK.context
        if not context:
            raise BaseException("No BmobSDK context setuped!")
        self.context = context
        self.objectId = objectId
        if self.objectId:
            # get object by id
            path = '/'.join([self.get_modelname(), self.objectId])
            for k, v in self.context.get(path).json().items():
                setattr(self, k, v)
        else:
            for k, v in kwargs.items():
                setattr(self, k, v)

    def get_attrs(self):
        return [k for k in type(self).__dict__ if not k.startswith('__')]

    def get_dict(self):
        ks = self.get_attrs()
        clz = type(self)
        dic = {}
        tps = [type(v) for v in [1, 1, 1.0, '1', (1, 2), [1, 2], {'1': '1'}, {1, 2}]]
        return dict([(k, type(getattr(clz, k))(getattr(self, k)))
                     for k in ks if type(getattr(clz, k)) in tps])

    def get_modelname(self):
        return type(self).__name__

    def save(self):
        data = self.get_dict()
        #jdata = json.dumps(data)
        if self.objectId:
            path = '/'.join([self.get_modelname(), self.objectId])
            for k, v in self.context.put(path, data=data).json().items():
                setattr(self, k, v)
        else:
            path = self.get_modelname()
            for k, v in self.context.post(path, data=data).json().items():
                setattr(self, k, v)

    def delete(self):
        if self.objectId:
            path = '/'.join([self.get_modelname(), self.objectId])
            res = self.context.delete(path).json()['msg'] == 'ok'
            if res:
                self.objectId = None
            return res
        else:
            return True

    def query(self):
        return Query(type(self))


