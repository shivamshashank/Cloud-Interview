### Personal introduction — about 90 seconds

- **Education:** Hi, I’m Shivam. I completed my MSc in Computer Science with Distinction at the University of Birmingham, following my BTech at IIT.
- **Experience:** My background combines software development, cloud engineering, and applied research. At HPE, I worked with Docker, Kubernetes, containerd, and observability tools including Prometheus, Grafana, OpenTelemetry, and Loki.
- **Contribution:** I contributed to Jenkins CI/CD improvements that reduced deployment time by around 40%, through work including multi-stage Docker builds, parallel testing, and automated checks.
- **Reliability:** I also worked on an NGINX ingress upgrade, checking compatibility and validating routing and application behaviour.
- **Earlier work:** Before HPE, I worked as a mobile engineer at Unbox using Flutter and Cardano serialization.
- **Dissertation:** I built CloudGraph, a prototype investigating whether evidence from a Kubernetes knowledge graph could help verify AI-generated incident explanations.
- **Direction:** I want to build reliable software and own features from design through implementation, testing, and delivery. I enjoy explaining decisions and measuring results.

**Memory order:** Education → experience → contribution → project → next role.

### Dissertation overview — about 90 seconds

- **Problem:** An AI can produce a convincing root-cause explanation without enough evidence. CloudGraph investigates how to check the individual claims in that explanation.
- **Architecture:** The system connects Kubernetes resources and incident evidence in Neo4j, with Qdrant supporting vector retrieval. Python services handle retrieval, investigation, and verification; a Go CLI supports deployment and reporting.
- **Generation:** Five specialists examine monitoring, logs, deployments, topology, and security. Their findings feed a consensus stage that produces an incident explanation.
- **Verification:** I compared Graph-Provenance Claim Scoring, or GPCS, against self-consistency: evidence-based scoring versus checking whether claims recur across repeated generations.
- **Experiment:** The saved benchmark contains 18 RCAEval scenarios across three retrieval conditions: 54 runs and 1,950 primary-explanation claims.
- **Finding:** Only 93 claims were judgeable under the automatic correctness policy. The results did not establish that either verifier reliably distinguished correct claims from incorrect ones.
- **Learning:** Evidence reachability is not proof of truth. Better labels and evaluation controls are necessary before claiming improved diagnosis accuracy.

**Memory order:** Problem → architecture → generation → verification → experiment → finding.

### Eight follow-up questions and answers

*Based on the local CloudGraph implementation, tests, archived claims, and preprint audit. The code establishes system behaviour, not individual authorship of every line or which issue you personally found hardest.*

**1. Why did you use both Neo4j and Qdrant?**

- **Neo4j** stores entities and relationships; **Qdrant** retrieves semantically relevant evidence using 384-dimensional `all-MiniLM-L6-v2` embeddings.
- The hybrid ranker combines vector similarity, graph proximity, and recency with weights of **0.50, 0.30, and 0.20**.
- The goal was to combine semantic and structural context, but the evaluation did not establish an accuracy advantage.

**2. What did you implement, and in which language?**

- The application uses **Python**, with FastAPI, ingestion adapters, graph retrieval, hybrid ranking, claim scoring, and evaluation scripts. Separate Python services run five specialists and combine their findings.
- The **Go CLI** handles deployment, reporting, and uninstall commands; Docker, Kubernetes, and Helm support deployment.
- A concrete module is `GraphProvenanceClaimScorer`: it retrieves evidence and returns claim scores and verdicts. The project integrates existing databases and models rather than implementing or training them.

**3. How did you connect Kubernetes objects, logs, and deployment events?**

- Pods use Kubernetes `metadata.uid` as their graph ID. Logs link through that ID using `GENERATES`; pod-to-node links match `nodeName` using `RUNS_ON`.
- Pod-name prefixes link services and deployments through `BELONGS_TO` and `MANAGES`. Argo CD revisions match Git commit SHAs; Git webhook linking also uses repository/deployment-name matching.
- Service/deployment identities are name-based, with namespace stored separately. Prefix matching and these identities can create cross-namespace ambiguity.

**4. How did you select evidence for the incident window?**

- Traversal uses explicit start/end times or the seed/incident time fields. Its timestamp fallback is **one hour before and after**, configurable through `GRAPHRAG_TIME_WINDOW_SECONDS`.
- Benchmark recency uses the scenario’s `inject_time`, and retrieval supports `scenario_id` filtering to focus on the relevant incident.
- Limits remain: untimestamped nodes can pass, some fallback/specialist paths lack scenario scoping, and live-discovery logs use ingestion time rather than parsed event time.

**5. How did claim checking work?**

- An LLM extracts claims from the explanation’s **title, summary, and cause**, with sentence splitting as fallback. Both verifiers reuse the same primary claim list.
- **GPCS** scores retrieved evidence using relevance, graph proximity, reliability, and a path penalty. **Self-consistency** checks recurrence across two additional generations; recurrence is not proof of correctness.
- A separate deterministic labeller assigns `consistent`, `contradicted`, or `unverifiable` using causal language and benchmark fault/service information. These are proxy labels, not human judgments.

**6. What did the evaluation establish—and what did it fail to establish?**

- **18 scenarios × 3 conditions = 54 runs and 1,950 claims.** NONE omits additional retrieval but retains observations/specialist evidence; RAW supplies unranked evidence; HYBRID supplies ranked evidence.
- The automatic policy labelled **36 consistent, 57 contradicted, and 1,857 unverifiable**—only **4.8%** were judgeable. GPCS flagged more claims, but better correctness discrimination was not established.
- These results come from seeded benchmark evidence. The separate live demo exercises ingestion, not production accuracy; its discovered metrics are synthetic.

**7. What was the hardest implementation problem?**

- A documented challenge was **claim alignment**: extracting an explanation twice could produce different statements under identical IDs such as `claim-1`, making verifier comparisons misleading.
- The implementation extracts primary claims once and passes the same list to `score_claims(claims=...)`. A regression test rejects re-extraction and checks that claim IDs and text are preserved.
- The lesson is that reliable evaluation needs consistent inputs across components. Use this as a concrete challenge; the repository cannot establish which issue you personally found hardest.

**8. What would you improve first, and why?**

- Improve claim-level labels and independent review, then close scenario-scoping and cleanup gaps so evaluation results are trustworthy.
- Replace prefix matching with namespace-aware identities, owner references, and service selectors; preserve event times and ingest measured live metrics.
- Run graph-only/vector-only/hybrid comparisons and a matched-compute single-model comparison. These are proposed experiments; measure correctness, coverage, latency, and cost separately.

### Source notes for revision

- [Discovery and identifiers](/Users/shivam_shashank/CloudGraph/services/api/app/adapters/k8s_discovery.py), [entity linking](/Users/shivam_shashank/CloudGraph/services/api/app/adapters/graph_constructor.py), [webhooks](/Users/shivam_shashank/CloudGraph/services/api/app/adapters/webhooks.py).
- [Time-window traversal](/Users/shivam_shashank/CloudGraph/services/api/app/retrieval/graph_traversal.py), [claim scorer](/Users/shivam_shashank/CloudGraph/services/api/app/research/gpcs.py), [regression tests](/Users/shivam_shashank/CloudGraph/services/api/tests/test_gpcs.py).
- [Archived claims](/Users/shivam_shashank/CloudGraph/experiment-1-benchmark/results/claims.csv), [preprint audit and corrections](/Users/shivam_shashank/CloudGraph/output/pdf/READ-ME-FIRST.md).
