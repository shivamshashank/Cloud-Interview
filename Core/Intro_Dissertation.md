### Two-minute introduction

**1. Education — University of Birmingham**
- Hi, I’m Shivam.
- I completed my **MSc in Computer Science with Distinction at the University of Birmingham**.
- My background combines research with practical software and cloud engineering.

**2. HPE — Containers and observability**
- At HPE, I worked with **Docker, Kubernetes, and containerd**.
- I also worked on **Prometheus, Grafana, OpenTelemetry, and Loki**, using metrics, logs, and traces to understand system behaviour and investigate issues.

**3. HPE — CI/CD improvements**
- I contributed to **Jenkins CI/CD improvements that reduced deployment time by around 40%**.
- These included **multi-stage Docker builds, parallel testing, and automated linting and formatting**.
- My focus was making builds and validation faster and more consistent.

**4. HPE — NGINX ingress upgrade**
- I worked on upgrading **NGINX ingress between major versions**.
- This involved checking compatibility and validating routing and application behaviour after the upgrade.

**5. Earlier experience — Unbox and IIT**
- Before HPE, I worked as a **mobile engineer at Unbox**, using **Flutter and Cardano serialization**.
- I completed my **BTech at IIT**, which gave me my technical foundation.

**6. Why Huawei SIR**
- I want to combine my engineering experience with deeper **systems and AI infrastructure research**.
- I enjoy understanding a problem, building an improvement, and measuring whether it works.

**Memory order:**  
**UoB → HPE containers → observability → CI/CD → NGINX → Unbox → IIT → SIR**




### Two-minute dissertation introduction — CloudGraph

**1. Topic — What I studied**
- My MSc dissertation at the **University of Birmingham** focused on **CloudGraph**, a system for supporting cloud incident investigation.
- I explored whether combining **service relationships with relevant evidence** could help an AI produce better-supported root-cause explanations.

**2. Problem — Why it matters**
- In Kubernetes, an incident can involve several services and dependencies.
- Logs, deployment changes, and infrastructure information are scattered across different tools.
- An AI can generate a convincing explanation without enough evidence, so I wanted to make its reasoning easier to check.

**3. Approach — What I built**
- I built a pipeline that connects **Kubernetes objects, logs, and deployment events**.
- I used **Neo4j** to represent relationships and changes over time, and **Qdrant** for vector-based retrieval.
- The system retrieves evidence relevant to the affected service and incident window, then generates an explanation and checks its individual claims.

**4. Evaluation — How I tested it**
- I compared different retrieval approaches across matched incident scenarios.
- I examined whether the generated claims could be checked against the available evidence.
- This helped distinguish a plausible explanation from one supported by the data.

**5. Findings — What I learned**
- The evaluation did **not establish the accuracy improvement I had hoped for**.
- Many claims could not be judged from the available evidence, and graph relationships alone did not establish correctness.
- My main lesson was that better retrieval needs reliable ground truth and sufficient evidence to evaluate it properly.

**6. Next steps — Why it relates to SIR**
- I would improve the labelled evidence and compare graph, text-only, and hybrid retrieval under controlled conditions.
- I would also measure latency and retrieval cost alongside claim quality.
- This project strengthened my ability to **form a research question, build a prototype, evaluate it, and explain its limitations**—skills I want to develop further at SIR.

**Memory order:**  
**Topic → problem → build → evaluation → findings → next steps**