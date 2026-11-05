"""Real-data selective prediction baseline; stdlib only, no LLM/API inference.

Inputs: QUESTION and CONTEXTS only. LONG_ANSWER, labels, MeSH and reasoning
annotations are excluded from features. Custom split, not a leaderboard score.
"""
import argparse,collections,hashlib,json,math,re
from pathlib import Path
LABELS=('yes','no','maybe')
REV='1cbae8e92f72f20c8d3747cbb3bf5bc53554d997'
SOURCE=f'https://raw.githubusercontent.com/pubmedqa/pubmedqa/{REV}/data/ori_pqal.json'

def tokens(record):
 text=record['QUESTION']+' '+' '.join(record['CONTEXTS'])
 return re.findall(r'[a-z]+',text.lower())

def partition(data):
 # Seeded hash of identifier, sorted within each label, provides exact stratification.
 groups={label:[] for label in LABELS}
 for pid,row in data.items():
  if row['final_decision'] not in groups:raise ValueError('Unknown label')
  groups[row['final_decision']].append(pid)
 out={'train':[],'development':[],'test':[]}
 for ids in groups.values():
  ids.sort(key=lambda pid:hashlib.sha256(('agentguard-pubmedqa-v1:'+pid).encode()).hexdigest())
  a=int(len(ids)*.6);b=a+int(len(ids)*.2)
  out['train']+=ids[:a];out['development']+=ids[a:b];out['test']+=ids[b:]
 return {k:sorted(v) for k,v in out.items()}

class NaiveBayes:
 def fit(self,data,ids):
  self.docs=collections.Counter();self.counts={c:collections.Counter() for c in LABELS};self.vocab=set()
  for pid in ids:
   row=data[pid];c=row['final_decision'];words=tokens(row);self.docs[c]+=1;self.counts[c].update(words);self.vocab.update(words)
  self.totals={c:sum(v.values()) for c,v in self.counts.items()};return self
 def predict(self,row):
  words=collections.Counter(t for t in tokens(row) if t in self.vocab)
  scores={c:math.log((self.docs[c]+1)/(sum(self.docs.values())+len(LABELS)))+sum(n*math.log((self.counts[c][w]+1)/(self.totals[c]+len(self.vocab))) for w,n in words.items()) for c in LABELS}
  ordered=sorted(LABELS,key=lambda c:scores[c],reverse=True)
  # Length-normalized log-likelihood margin is a ranking signal, NOT a probability.
  return ordered[0],(scores[ordered[0]]-scores[ordered[1]])/max(1,sum(words.values()))

def choose_threshold(rows,target=.7,min_count=20):
 candidates=[]
 for threshold in sorted({r['margin'] for r in rows}):
  kept=[r for r in rows if r['margin']>=threshold]
  if len(kept)>=min_count and sum(r['correct'] for r in kept)/len(kept)>=target:candidates.append((len(kept),threshold))
 return max(candidates)[1] if candidates else None

def summarize(rows,threshold=None,selective=False):
 kept=[r for r in rows if not selective or (threshold is not None and r['margin']>=threshold)]
 confusion={true:{pred:0 for pred in LABELS} for true in LABELS}
 for r in kept:confusion[r['truth']][r['prediction']]+=1
 return {'total':len(rows),'answered':len(kept),'abstained':len(rows)-len(kept),'coverage':len(kept)/len(rows) if rows else 0,'accuracy':sum(r['correct'] for r in kept)/len(kept) if kept else None,'errors':sum(not r['correct'] for r in kept),'confusion':confusion}

def main():
 p=argparse.ArgumentParser();p.add_argument('--data',type=Path,default=Path('data/pubmedqa/ori_pqal.json'));p.add_argument('--output',type=Path,default=Path('results/pubmedqa.json'));args=p.parse_args()
 raw=args.data.read_bytes();data=json.loads(raw)
 if len(data)!=1000:raise ValueError('Expected 1,000 expert-labeled records')
 split=partition(data);model=NaiveBayes().fit(data,split['train']);majority=model.docs.most_common(1)[0][0]
 def predict(ids):
  out=[]
  for pid in ids:
   guess,margin=model.predict(data[pid]);truth=data[pid]['final_decision']
   out.append({'pmid':pid,'truth':truth,'prediction':guess,'margin':margin,'correct':guess==truth})
  return out
 dev=predict(split['development']);threshold=choose_threshold(dev);test=predict(split['test'])
 baseline=[{**r,'prediction':majority,'correct':majority==r['truth']} for r in test]
 report={'source':SOURCE,'upstream_revision':REV,'dataset_sha256':hashlib.sha256(raw).hexdigest(),'features':['QUESTION','CONTEXTS'],'excluded_features':['LONG_ANSWER','final_decision','MESHES','reasoning annotations'],'split':split,'split_sizes':{k:len(v) for k,v in split.items()},'label_counts':{s:dict(collections.Counter(data[i]['final_decision'] for i in ids)) for s,ids in split.items()},'method':'Laplace-smoothed multinomial naive Bayes; normalized margin; no hyperparameter search','selection':{'target_development_accuracy':.7,'minimum_development_answers':20,'threshold':threshold,'threshold_selected_on':'development only'},'development_full':summarize(dev),'development_selected':summarize(dev,threshold,True),'test_majority':summarize(baseline),'test_full':summarize(test),'test_selected':summarize(test,threshold,True),'test_traces':test,'limitations':['Custom stratified split, not the official benchmark split.','Single partition, no external or prospective validation.','Confidence margin is not a calibrated probability.','Development target does not guarantee test accuracy.','Abstract-level answer labels are not clinical correctness or semantic evidence verification.','Possible topic/near-duplicate overlap is not removed.','No LLM or adversarial prompt-injection measurement.']}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('split','test_traces','limitations','excluded_features')},indent=2))
if __name__=='__main__':main()
