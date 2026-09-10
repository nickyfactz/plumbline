import unittest
from jobs import Store, StateError

class ExistingTests(unittest.TestCase):
    def setUp(self):
        self.s = Store(':memory:')
        self.addCleanup(self.s.close)
    def test_success(self):
        self.assertEqual(self.s.submit('a'), {'id':'a', 'state':'queued', 'attempt':1})
        self.s.start('a')
        self.assertEqual(self.s.complete('a')['state'], 'complete')
        self.assertEqual(self.s.history('a'), [{'number':1, 'state':'complete'}])
    def test_failure(self):
        self.s.submit('a'); self.s.start('a')
        self.assertEqual(self.s.fail('a')['state'], 'failed')
    def test_invalid_and_missing(self):
        self.s.submit('a')
        with self.assertRaises(StateError): self.s.complete('a')
        with self.assertRaises(KeyError): self.s.get('missing')
