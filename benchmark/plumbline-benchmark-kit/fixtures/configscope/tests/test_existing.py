import json
import tempfile
import unittest
from pathlib import Path
from config import resolve, load, dump

class ExistingTests(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(resolve({}), {'timeout':30, 'theme':'light', 'retries':2})
    def test_legacy(self):
        self.assertEqual(resolve({'timeout':9})['timeout'], 9)
    def test_invalid(self):
        for data in ({'unknown':1}, {'timeout':True}, {'retries':-1}, {'theme':'other'}):
            with self.assertRaises(ValueError): resolve(data)
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'c.json'; dump({'theme':'dark'}, p)
            self.assertEqual(load(p)['theme'], 'dark')
            self.assertEqual(json.loads(p.read_text()), {'theme':'dark'})
