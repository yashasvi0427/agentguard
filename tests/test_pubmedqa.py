import unittest
from pubmedqa_eval import tokens,partition,NaiveBayes,choose_threshold,summarize
class PubMedTests(unittest.TestCase):
 def test_no_answer_leakage(self):
  r={'QUESTION':'question','CONTEXTS':['public context'],'LONG_ANSWER':'secret answer','final_decision':'yes'}
  self.assertEqual(tokens(r),['question','public','context'])
 def test_partition_disjoint_complete_deterministic(self):
  data={str(i):{'final_decision':['yes','no','maybe'][i%3]} for i in range(60)}
  s=partition(data);self.assertEqual(s,partition(dict(reversed(list(data.items())))))
  self.assertEqual(len(set(sum(s.values(),[]))),60)
  self.assertEqual(sum(map(len,s.values())),60)
 def test_vocabulary_train_only(self):
  d={'a':{'QUESTION':'apple','CONTEXTS':[],'final_decision':'yes'},'b':{'QUESTION':'secret','CONTEXTS':[],'final_decision':'no'}}
  m=NaiveBayes().fit(d,['a']);self.assertNotIn('secret',m.vocab)
 def test_failed_target_abstains(self):
  rows=[{'margin':.5,'correct':False,'truth':'yes','prediction':'no'}]*20
  self.assertIsNone(choose_threshold(rows));self.assertEqual(summarize(rows,None,True)['answered'],0)
 def test_tied_threshold_and_empty_selection(self):
  rows=[{'margin':.5,'correct':True,'truth':'yes','prediction':'yes'}]*20
  t=choose_threshold(rows);self.assertEqual(t,.5);self.assertEqual(summarize(rows,t,True)['answered'],20)
if __name__=='__main__':unittest.main()
