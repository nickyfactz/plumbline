import unittest
from documents import Service, Context, AccessDenied
from api import dispatch

class ExistingTests(unittest.TestCase):
    def setUp(self):
        self.s = Service(); self.s.set_member('u','w',True)
        self.s.add_document('a','w','one'); self.c=Context('u','w')
    def test_owner_lifecycle(self):
        self.assertEqual(self.s.update(self.c,'a','two')['text'],'two')
        self.assertEqual(self.s.export(self.c,['a'])[0]['text'],'two')
        self.assertIsNone(self.s.delete(self.c,'a'))
    def test_copy(self):
        self.s.read(self.c,'a')['text']='mutated'
        self.assertEqual(self.s.read(self.c,'a')['text'],'one')
    def test_adapter_and_workspace(self):
        self.assertEqual(dispatch(self.s,self.c,'read',{'id':'a'})['status'],200)
        with self.assertRaises(AccessDenied): self.s.read(Context('u','other'),'a')
