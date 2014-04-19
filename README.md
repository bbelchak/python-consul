python-consul
=============

A Python client library for Hashicorp's Consul

KV
==

You can interact with the KV API by doing the following:

```python
In [1]: from consul.kv import KV

In [2]: kv = KV('192.168.2.201')

In [3]: kv.put('keyname', 'test')
Out[3]: True

In [4]: kv.put('keyname/child', 'cooltest')
Out[4]: True

In [5]: kv.get('keyname', recurse=True)
Out[5]: [<consul.kv.Key at 0x105997790>, <consul.kv.Key at 0x105997a50>]

In [6]: kv.get('keyname')
Out[6]: <consul.kv.Key at 0x1067f56d0>
```

A `Key` is an object that looks like:

```python
In [7]: kv.get('keyname').__dict__

Out[7]: {'_value': u'dGVzdA==',
 'create_index': 456,
 'flags': 0,
 'key': u'keyname',
 'kv': <consul.kv.KV at 0x105997c50>,
 'modify_index': 456}
 ```

The `value` that comes back from Consul is base64 encoded, but when you access
the `value` attribute on the object, it will decode it for you.

PUT
---

You can add keys to the KV store by calling `put` on the KV object. This takes two parameters:
`key` and `value`.

Examples:

```python
In [4]: kv.put('keyname/child', 'cooltest')
Out[4]: True
```

DELETE
------

You can delete any key by using the `delete` function on the KV object. You can optionally pass `recurse=True`
and it will delete all of the child keys of the key you've specified.

```python
In [4]: kv.delete('keyname', recurse=True)
Out[4]: True
```

GET
---

You can get any individual key by calling the `get` function. You can also recursively
get all keys by providing the `recurse=True` kwarg.

```python
In [5]: kv.get('keyname', recurse=True)
Out[5]: [<consul.kv.Key at 0x105997790>, <consul.kv.Key at 0x105997a50>]
```

Contributing
============

Pull requests are very welcome! Make sure your patches are well tested.
Ideally create a topic branch for every separate change you make. For
example:

1. Fork the repo
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

