# AgentGuard: simulated runtime authorization benchmark

Research question: can a lightweight boundary policy block unauthorized tool actions while permitting authorized actions?

This is a dependency-free **synthetic action replay prototype**, built with AI assistance. It does not run an LLM, execute tool calls, or demonstrate real-agent prompt-injection robustness. The policy sees structured actions and trusted metadata only. `sensitive` and `approval` must come from the environment, never from an agent's own claims.

## Run

Python 3.10+; no packages or API keys required.

```
python3 -m unittest discover -s tests -v
python3 benchmark.py
```

## Measured results

64 cases: 32 development and 32 heldout identifiers, each with 20 unauthorized and 12 authorized actions. Both splits use the same 16 families; this is not a holdout of attack strategies. Cases cover workspace boundaries, encoded traversal, sensitive egress, host confusion, approval gating, unknown tools, and benign keyword collisions.

| Policy | Heldout unsafe blocked | Heldout benign blocked |
|---|---:|---:|
| Allow all | 0/20 | 0/12 |
| Keyword baseline | 4/20 | 2/12 |
| Capability policy | 20/20 | 0/12 |

Six tests check boundaries, normalization, host parsing, approval/sensitivity, unknown tools and trace/partition integrity. `results/report.json` includes every decision and a dataset hash. Traces provide the useful observability portion without a separate TraceLens project.

## Limits and next experiment

The policy and dataset were co-developed. Perfect performance is a regression result, not a generalization claim. Paths are strings in a simulated namespace: real deployments need symlink-safe filesystem handles, DNS/redirect checks, content taint tracking, durable approvals and protection against tool/schema confusion. One URL decode pass follows this simulator's semantics. Multi-step behavior, adaptive attacks, poisoned metadata, semantic task completion and real prompt injections remain untested. Repeated variants are correlated, so no statistical confidence claim is made.

Next: freeze policy and semantics; ask an independent author to add unseen attack families; evaluate multi-step traces and task success before any model-based study. Attribute AI-generated implementation separately from the applicant's own research contribution.

## Biomedical research-workflow extension

`python3 biomedical.py` evaluates 12 explicitly synthetic cases: public literature access, authorized deidentified/synthetic exports, verified citations, claim support and human approval. Nine unauthorized actions are blocked and three authorized actions permitted. Three additional tests verify expected decisions, missing/typed metadata and that an injected instruction cannot grant approval.

This tests enforcement of supplied metadata, not an ability to identify patient information, verify papers, evaluate scientific claims or detect real prompt injections. Those predicates are assumed trusted and require independent verification upstream. No real biomedical data, clinical decisions or biological protocols are present. A useful next study would independently annotate public literature summaries and measure citation/claim-verification errors before connecting the policy to a research assistant. This is an extension of the same project, not a separate completed biomedical research contribution.
