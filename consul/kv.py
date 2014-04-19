from base64 import b64decode
import requests
from consul.base import BaseAPI


class Key(object):
    def __init__(self, data, kv):
        self.create_index = data['CreateIndex']
        self.modify_index = data['ModifyIndex']
        self.flags = data['Flags']
        self.key = data['Key']
        self._value = data['Value']
        self.kv = kv

    @property
    def value(self):
        return b64decode(self._value)


class KV(BaseAPI):
    endpoint = 'kv'

    def _make_url(self, key):
        return '{0}/{1}'.format(self._url, key)

    def put(self, key, data=None, **params):
        return requests.put(self._make_url(key), data=data, **params).json()

    def get(self, key, **params):
        rv = requests.get(self._make_url(key), params=params)
        if rv.status_code == 200:
            rv = rv.json()
            if len(rv) > 1:
                return [Key(x, self) for x in rv]
            return Key(rv[0], self)
        return None

    def delete(self, key, **params):
        return requests.delete(self._make_url(key), **params)
