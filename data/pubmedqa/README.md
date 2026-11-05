# PubMedQA provenance

Official repository: https://github.com/pubmedqa/pubmedqa
Pinned revision: 1cbae8e92f72f20c8d3747cbb3bf5bc53554d997
File: data/ori_pqal.json (1,000 expert-labeled records)
SHA-256: 8b3276be8942ebbd77f3ddcda12c1749bf0e490045a736fd8438ee40cf37a41d
Upstream MIT license is preserved in LICENSE. Cite Jin, Dhingra, Liu, Cohen and Lu (2019), “PubMedQA: A Dataset for Biomedical Research Question Answering,” EMNLP-IJCNLP, https://aclanthology.org/D19-1259/ .

Run `python3 fetch_pubmedqa.py` from the repository root. Raw abstract text is downloaded locally and excluded from Git. Committed results contain identifiers, labels and prediction statistics, not abstracts or patient records. Source labels describe answers in this dataset, not clinical advice.
