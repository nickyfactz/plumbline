import copy
import unittest
from documents import Service, Context, AccessDenied
from api import dispatch

class Acceptance(unittest.TestCase):
    def setUp(self):
        self.s=Service(); self.c=Context('u','w')
        self.s.add_document('a','w','A'); self.s.add_document('b','w','B')
        self.s.add_document('foreign','other','SECRET')
        self.s.set_member('u','w','owner')
    def test_A01_A02_matrix(self):
        operations={'read':lambda:self.s.read(self.c,'a'),
                    'export':lambda:self.s.export(self.c,['a']),
                    'update':lambda:self.s.update(self.c,'a','x'),
                    'bulk':lambda:self.s.bulk_update(self.c,[('a','x')]),
                    'delete':lambda:self.s.delete(self.c,'a')}
        permissions={'viewer':{'read','export'},'editor':{'read','export','update','bulk'},
                     'owner':set(operations),True:set(operations)}
        for role in ('viewer','editor','owner',True,False,None,'bogus'):
            for name,fn in operations.items():
                self.s.add_document('a','w','A'); self.s.set_member('u','w',role)
                with self.subTest(role=role,operation=name):
                    if name in permissions.get(role,set()): fn()
                    else:
                        with self.assertRaises(AccessDenied): fn()
    def test_A02_revocation(self):
        self.s.read(self.c,'a'); self.s.set_member('u','w',None)
        with self.assertRaises(AccessDenied): self.s.update(self.c,'a','x')
    def test_A03_cross_workspace(self):
        for key in ('foreign','missing'):
            for fn in (lambda:self.s.read(self.c,key),lambda:self.s.update(self.c,key,'x'),
                       lambda:self.s.delete(self.c,key),lambda:self.s.export(self.c,['a',key])):
                with self.assertRaises(AccessDenied): fn()
        self.assertEqual(self.s.documents['foreign']['text'],'SECRET')
    def test_A04_atomic_late_denial(self):
        before=copy.deepcopy(self.s.documents)
        with self.assertRaises(AccessDenied): self.s.bulk_update(self.c,[('a','new'),('foreign','x')])
        self.assertEqual(self.s.documents,before)
    def test_A05_duplicate_and_malformed(self):
        invalid=[[('a','x'),('a','y')],[('a','x'),('b',3)],[('a','x'),('b',)],
                 [('a','x'),(8,'y')], [('a','x'),'bx'], {'a':'x'}]
        for batch in invalid:
            before=copy.deepcopy(self.s.documents)
            with self.assertRaises(ValueError): self.s.bulk_update(self.c,batch)
            self.assertEqual(self.s.documents,before)
    def test_A05_order_and_copies(self):
        got=self.s.bulk_update(self.c,[('b','two'),('a','one')])
        self.assertEqual([x['id'] for x in got],['b','a'])
        got[0]['text']='bad'; self.assertEqual(self.s.read(self.c,'b')['text'],'two')
    def test_A06_invalid_single_and_unicode(self):
        with self.assertRaises(ValueError): self.s.update(self.c,'a',None)
        self.assertEqual(self.s.read(self.c,'a')['text'],'A')
        self.assertEqual(self.s.update(self.c,'a','こんにちは')['text'],'こんにちは')
        self.assertEqual(self.s.update(self.c,'a','')['text'],'')
    def test_A07_export(self):
        self.s.set_member('u','w','viewer')
        got=self.s.export(self.c,['b','a','b'])
        self.assertEqual([x['id'] for x in got],['b','a','b'])
        got[0]['text']='bad'; self.assertEqual(got[2]['text'],'B')
        with self.assertRaises(AccessDenied): self.s.export(self.c,['a','foreign'])
    def test_A08_empty_still_authorized(self):
        self.s.set_member('u','w','viewer')
        self.assertEqual(self.s.export(self.c,[]),[])
        with self.assertRaises(AccessDenied): self.s.bulk_update(self.c,[])
        self.s.set_member('u','w',None)
        with self.assertRaises(AccessDenied): self.s.export(self.c,[])
        self.s.set_member('u','w','editor')
        self.assertEqual(self.s.bulk_update(self.c,[]),[])
    def test_A09_body_spoofing(self):
        self.s.set_member('u','w','viewer')
        body={'id':'a','text':'x','user':'admin','workspace':'other','role':'owner'}
        self.assertEqual(dispatch(self.s,self.c,'update',body),{'status':403,'error':'forbidden'})
        self.assertEqual(self.s.read(self.c,'a')['text'],'A')
    def test_A09_adapter_error_mapping(self):
        self.assertEqual(dispatch(self.s,self.c,'bulk',{'updates':[('a','x'),('b',3)]}),
                         {'status':400,'error':'invalid input'})
        self.assertEqual(self.s.read(self.c,'a')['text'],'A')
        self.assertEqual(dispatch(self.s,self.c,'export',{'ids':['foreign']})['status'],403)
