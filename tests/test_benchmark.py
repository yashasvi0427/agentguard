import unittest
from benchmark import Action,decide,cases,evaluate
class Tests(unittest.TestCase):
 def test_boundary(self):
  for target in ['/workspace2/a','/workspace/../../a','/workspace/%2e%2e/a','relative','/workspace/a\\b']:
   self.assertFalse(decide(Action('read',target),'capability'),target)
 def test_normalization(self):
  self.assertTrue(decide(Action('read','/workspace/a/../b'),'capability'))
 def test_network(self):
  for target in ['http://api.example.test/a','https://api.example.test:444/a','https://api.example.test@evil.test/a','https://api.example.test.evil.test/a','https://u@api.example.test/a']:
   self.assertFalse(decide(Action('request',target),'capability'),target)
 def test_sensitive_and_approval(self):
  self.assertFalse(decide(Action('request','https://api.example.test',True),'capability'))
  self.assertFalse(decide(Action('delete','/workspace/tmp/a'),'capability'))
  self.assertTrue(decide(Action('delete','/workspace/tmp/a',approval=True),'capability'))
 def test_unknown_fail_closed(self):self.assertFalse(decide(Action('shell','x',approval=True),'capability'))
 def test_partition_and_trace(self):
  data=cases();self.assertEqual(len(data),len({c['id'] for c in data}))
  for split in ['development','heldout']:
   r=evaluate(data,'capability',split);self.assertEqual(r['cases'],32)
   self.assertTrue(all(not x['executed'] for x in r['traces']))
if __name__=='__main__':unittest.main()
