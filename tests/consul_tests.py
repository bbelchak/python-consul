import unittest
from mock import patch
from consul.kv import Key, KV
from consul.agent import Agent

TEST_KEY_DATA = {
    'CreateIndex': 100,
    'ModifyIndex': 200,
    'Key': 'zip',
    'Flags': 0,
    'Value': "dGVzdA=="
}

LIVE_ADDRESS = '127.0.0.1'
LIVE_TESTS_ENABLED = True


class KeyTestCase(unittest.TestCase):
    def test_value(self):
        self.assertEqual(Key(TEST_KEY_DATA, None).value, 'test')


class KVTestCase(unittest.TestCase):
    def setUp(self):
        self.kv = KV('localhost')

    @patch('requests.get')
    def test_get_one(self, get_mock):
        get_mock.return_value.json.return_value = [TEST_KEY_DATA]
        get_mock.return_value.status_code = 200
        rv = self.kv.get('zip')
        self.assertEqual(Key(TEST_KEY_DATA, self.kv).value, rv.value)

    @patch('requests.get')
    def test_get_several(self, get_mock):
        get_mock.return_value.json.return_value = [TEST_KEY_DATA, TEST_KEY_DATA]
        get_mock.return_value.status_code = 200
        rv = self.kv.get('zip', recurse=True)
        self.assertEqual(len(rv), 2)
        self.assertEqual(rv[0].value, Key(TEST_KEY_DATA, self.kv).value)


if LIVE_TESTS_ENABLED:
    class KVLiveTestCase(unittest.TestCase):
        def setUp(self):
            self.kv = KV(LIVE_ADDRESS)
            self.kv.put('zip', 'test')
            self.kv.put('zip/what', 'test')

        def test_put(self):
            rv = self.kv.put('test_put', 'test')
            self.assertTrue(rv)

        def test_delete(self):
            rv = self.kv.delete('zip')
            self.assertTrue(rv)
            rv = self.kv.get('zip')
            self.assertIsNone(rv)

        def test_get_one(self):
            rv = self.kv.get('zip')
            self.assertEqual(Key(TEST_KEY_DATA, self.kv).value, rv.value)

        def test_get_several(self):
            rv = self.kv.get('zip', recurse=True)
            self.assertEqual(len(rv), 2)
            self.assertEqual(rv[0].value, Key(TEST_KEY_DATA, self.kv).value)

        def tearDown(self):
            self.kv.delete('zip')

    class AgentLiveTestCase(unittest.TestCase):
        def setUp(self):
            self.agent = Agent(LIVE_ADDRESS)

        def test_register_check(self):
            check_data = {
                "ID": "mem",
                "Name": "Memory utilization",
                "Notes": "Ensure we don't oversubscribe memory",
                "Script": "/bin/uname -a",
                "Interval": 3600
            }
            self.agent.register_check(check_data)
            checks = self.agent.checks()
            self.assertNotEqual({}, checks)
            data = self.agent.deregister_check('mem')
            checks = self.agent.checks()
            self.assertEqual({}, checks)
