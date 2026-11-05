"""Fetch pinned public source data; never sends local records to a service."""
import hashlib,urllib.request
from pathlib import Path
from pubmedqa_eval import SOURCE,REV
EXPECTED='8b3276be8942ebbd77f3ddcda12c1749bf0e490045a736fd8438ee40cf37a41d'
def main():
 root=Path('data/pubmedqa');root.mkdir(parents=True,exist_ok=True)
 with urllib.request.urlopen(SOURCE,timeout=60) as response:raw=response.read()
 if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise ValueError('Dataset hash mismatch')
 (root/'ori_pqal.json').write_bytes(raw)
 print(f'Verified PubMedQA revision {REV}: {len(raw)} bytes')
if __name__=='__main__':main()
