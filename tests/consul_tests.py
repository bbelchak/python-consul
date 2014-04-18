import unittest
from mock import patch
from consul.kv import Key, KV

TEST_KEY_DATA = {
    'CreateIndex': 100,
    'ModifyIndex': 200,
    'Key': 'zip',
    'Flags': 0,
    'Value': "dGVzdA=="
}


class KeyTestCase(unittest.TestCase):
    def test_value(self):
        self.assertEqual(Key(TEST_KEY_DATA).value, 'test')


class KVTestCase(unittest.TestCase):
    def setUp(self):
        self.kv = KV('localhost')

    @patch('requests.get')
    def test_get_one(self, get_mock):
        get_mock.return_value.json.return_value = TEST_KEY_DATA
        rv = self.kv.get('zip')
        self.assertEqual(Key(TEST_KEY_DATA).value, rv.value)

    @patch('requests.get')
    def test_get_several(self, get_mock):
        get_mock.return_value.json.return_value = [TEST_KEY_DATA, TEST_KEY_DATA]
        rv = self.kv.get('zip', recurse=True)
        self.assertEqual(len(rv), 2)
        self.assertEqual(rv[0].value, Key(TEST_KEY_DATA).value)


