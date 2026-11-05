# PubMedQA selective prediction pilot

## Research question and protocol

Can a simple biomedical text classifier meet a development accuracy target while answering a useful fraction of questions?

Use the official 1,000-record expert-labeled PQA-L dataset, pinned by revision and SHA-256. A deterministic PMID hash within each label yields 599 training, 199 development and 202 test records. This custom split differs from the official leaderboard split. Fit Laplace-smoothed multinomial naive Bayes on question and abstract-context words only. Learn vocabulary and priors on training records. Exclude long answers, labels, MeSH and reasoning annotations from input features.

Select the margin threshold on development data only: maximize answer count subject to at least 70% empirical accuracy and at least 20 answered development examples. If no threshold qualifies, abstain everywhere. Target and minimum were written before the first run; no hyperparameter search or subsequent threshold adjustment was performed. The margin is a ranking heuristic, not a calibrated probability. No clinical reliability is implied by the 70% experimental target.

## Results

| Policy | Test answers | Correct | Accuracy | Coverage |
|---|---:|---:|---:|---:|
| Training-majority label | 202 | 111 | 54.95% | 100% |
| Naive Bayes, always answer | 202 | 106 | 52.48% | 100% |
| Development-gated classifier | 0 | — | Undefined | 0% |

The unfiltered classifier gets 114/199 development answers correct (57.29%). No development threshold qualifies. On test it correctly predicts 89/111 yes labels, 17/69 no labels and 0/22 maybe labels. All-abstention is a failure to provide useful coverage, not a claim of 100% safety or accuracy. The classifier underperforms the majority baseline by 2.48 percentage points.

## Evidence and limits

`pubmedqa.json` records source/hash, all split IDs, class counts, selection settings, confusion matrices and test predictions. Fourteen total repository tests pass, including five new tests for feature leakage, split integrity, training-only vocabulary and abstention behavior. Rerunning the evaluator produces byte-identical JSON.

This is an AI-assisted, conventional ML pilot on real public biomedical data, not an LLM evaluation, adversarial-attack study or clinical system. A single custom split and unremoved potential near-duplicate/topic overlap limit inference. The selected threshold search provides no statistical guarantee. Model input construction is tested; no clinical claim is verified.

Next: inspect development errors, add an evidence-aware model and compare question-only versus context-aware inputs with a fresh evaluation set. Do not tune on these 202 test labels. Evaluate risk versus coverage and performance on maybe labels; retain the baseline and report failures. Connect to authorization safeguards only after testing the model's evidence verification independently.
