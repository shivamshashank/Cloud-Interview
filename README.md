# ☁️ Cloud Engineer Interview Preparation

**A study hub for cloud-engineer roles around two years of experience.**

![Focus: Cloud Engineering](https://img.shields.io/badge/Focus-Cloud_Engineering-2563eb?style=for-the-badge)
![Core Guides: 6](https://img.shields.io/badge/Core_Guides-6-16a34a?style=for-the-badge)
![Practical Questions: 160](https://img.shields.io/badge/Practical_Questions-160-f59e0b?style=for-the-badge)
![DSA Topic Files: 14](https://img.shields.io/badge/DSA_Topic_Files-14-8b5cf6?style=for-the-badge)

Learn the concepts, practise the commands, and explain the evidence behind your decisions. The guides use short definitions, examples, and troubleshooting scenarios; the DSA files support coding practice.

**Quick navigation:** [📘 Core guides](#-core-guides) · [🧩 DSA](#-data-structures--algorithms) · [🗺️ Study order](#-suggested-study-order) · [✅ Readiness](#-interview-readiness)

## 📘 Core guides

| # | Guide | What you will study |
| --- | --- | --- |
| 01 | [🐧 Linux + Networking](Core/01_Linux_Networking_Definitions.md) | Processes, memory, permissions, diagnostics, TCP/IP, DNS, routes, NAT, firewalls, and cloud networks |
| 02 | [🐳 Docker + Kubernetes + NGINX](Core/02_Docker_Kubernetes_NGINX_Definitions.md) | Images, containers, runtimes, workloads, networking, storage, probes, ingress, and reverse proxies |
| 03 | [📊 Prometheus + Grafana + Loki](Core/03_Prometheus_Grafana_Loki_Definitions.md) | Metrics, logs, traces, queries, dashboards, alerts, and OpenTelemetry integration |
| 04 | [⚙️ Terraform + Ansible + Jenkins](Core/04_Terraform_Ansible_Jenkins_Definitions.md) | Infrastructure state, configuration automation, inventory, playbooks, Pipelines, and delivery workflows |
| 05 | [☁️ AWS + Scripting + Git + Reliability](Core/05_AWS_Scripting_Git_Reliability_Definitions.md) | AWS services and IAM, Python/Bash, Git, security, backups, recovery, cost, architecture, and CV evidence |
| 06 | [🛠️ 160 Practical Questions](Core/06_Practical_160_Questions.md) | What to do, what to inspect, and a 2–3 line example for each scenario |

### 🎤 Introduction and dissertation

[Open the introduction and CloudGraph rehearsal notes](Core/Intro_Dissertation.md) to practise your background, HPE experience, dissertation, findings, and motivation.

Use your actual records for versions, contribution boundaries, measurements, and project outcomes.

### 🔎 Practical question navigator

Open [the practical guide](Core/06_Practical_160_Questions.md) and use these question ranges:

| Questions | Topic | Example task |
| --- | --- | --- |
| 1–10 | 🐧 Linux | Diagnose a failed service or full filesystem |
| 11–20 | 🌐 Networking | Separate DNS, TLS, route, and firewall failures |
| 21–30 | 🐳 Docker and containerd | Inspect an exited container or resource limits |
| 31–50 | ☸️ Kubernetes | Debug a Pod, inspect IP assignment, or investigate Service endpoints |
| 51–58 | 🚦 NGINX | Configure proxying and investigate upstream errors |
| 59–65 | 📈 Prometheus | Configure scraping, query metrics, and test alerts |
| 66–70 | 📊 Grafana | Create dashboards, variables, and notification routes |
| 71–75 | 🪵 Loki and OpenTelemetry | Query logs and connect them to traces |
| 76–85 | 🏗️ Terraform | Write configuration, review plans, and inspect drift |
| 86–93 | 🔧 Ansible | Write inventory/configuration and run playbooks |
| 94–100 | 🏭 Jenkins | Write Pipelines, parallelize checks, and handle credentials |
| 101–120 | ☁️ AWS | Investigate IAM, EC2, ALB, S3, ECS/EKS, Lambda, and RDS |
| 121–130 | 🐍 Python and Bash | Handle JSON, API timeouts, pagination, and command execution |
| 131–138 | 🌿 Git | Review changes, resolve conflicts, and recover safely |
| 139–148 | 🔐 Security, recovery, and cost | Rotate credentials, test restores, and investigate spend |
| 149–156 | 🧱 Architecture and labs | Design, deploy, test, and recover a complete application |
| 157–160 | 🎤 Personal experience | Explain your contribution and support your CV claims |

## 🧩 Data structures & algorithms

Start with the [Python interview guide](Python_Interview_Guide.md) for mutability, functions, `self`, `__init__`, dataclasses, decorators, generators, exceptions, typing, concurrency, and short practice questions.

![Language: Python](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Practice: Explain • Solve • Verify](https://img.shields.io/badge/Practice-Explain%20%E2%80%A2%20Solve%20%E2%80%A2%20Verify-64748b?style=flat-square)

| # | File | Main patterns |
| --- | --- | --- |
| 01 | [🗂️ Arrays + Hashing](DSA/01_Arrays_Hashing.py) | Hash maps, prefix sums, array and matrix operations |
| 02 | [↔️ Two Pointers + Sliding Window](DSA/02_TwoPointers_SlidingWindow.py) | Pointer movement and expanding/shrinking windows |
| 03 | [🔍 Binary Search + Greedy](DSA/03_BinarySearch_Greedy.py) | Search boundaries, answer-space search, and greedy choices |
| 04 | [🗓️ Intervals](DSA/04_Intervals.py) | Merge, overlap, insertion, and scheduling problems |
| 05 | [⛰️ Heap](DSA/05_Heap.py) | Top-k, priority queues, and streaming statistics |
| 06 | [🔗 Linked Lists](DSA/06_LinkedList.py) | Pointer manipulation, cycles, merging, and reordering |
| 07 | [🌳 Trees](DSA/07_Trees.py) | Traversal, recursion, BSTs, and tree construction |
| 08 | [🕸️ Graphs](DSA/08_Graphs.py) | Graph traversal and connectivity problems |
| 09 | [🧰 Class Design](DSA/09_Class_Design.py) | Stateful data structures and object design |
| 10 | [🔄 Backtracking](DSA/10_Backtracking.py) | Recursive exploration and reversing choices |
| 11 | [🧠 Dynamic Programming](DSA/11_Dynamic_Programming.py) | States, transitions, and reuse of subproblem results |
| 12 | [🎯 Miscellaneous](DSA/12_Miscellaneous.py) | Additional problem-solving exercises |
| 13 | [💡 Bit Manipulation](DSA/13_Bit.py) | Binary representation and bitwise operations |
| 14 | [Stacks + Tries](DSA/14_Stacks_Tries.py) | Bracket validation, minimum stack, and prefix search |

[DSA practice priorities and test instructions](DSA/README.md).

[📋 Open the problem tracker](DSA/leetcode_progress.md) for the recorded problem list and completion status. Tracker status is not a correctness guarantee; check implementations and edge cases as you practise.

**Coding routine →** Clarify inputs → explain an approach → implement without looking → test edge cases → discuss time and space complexity.

## 🗺️ Suggested study order

1. **Build the foundation:** Core 01 → 02. Explain the request path and container/Kubernetes lifecycle aloud.
2. **Learn how to observe and automate:** Core 03 → 04. Connect signals to debugging and tools to deployment responsibilities.
3. **Practise cloud operations:** Core 05. Focus on the provider services and operational tasks named in the target job description.
4. **Apply the concepts:** Work through Core 06. Predict what each command should reveal and explain your next step.
5. **Practise coding regularly:** Start with arrays/hashing, strings/windows, binary search, and common traversal patterns; expand according to the interview format.
6. **Rehearse your experience:** Explain one real incident, the CI/CD improvement, the ingress upgrade, and your dissertation with evidence and limitations.

### 🧪 One end-to-end exercise

```text
Define requirements → provision infrastructure → build/test → deploy
→ configure metrics/logs/alerts → generate traffic → introduce a lab fault
→ diagnose → recover → verify requests/data → document → clean up
```

Small snippets are learning examples. Complete exercises need their surrounding configuration, dependencies, permissions, environment values, and verification. Run infrastructure changes in an appropriate lab environment.

## ✅ Interview readiness

- [ ] Explain DNS → load balancer → application → database, including access controls and failure points.
- [ ] Write a small configuration or operational script without copying the answer.
- [ ] Diagnose a failed Pod, denied AWS call, slow request, or broken deployment using evidence.
- [ ] Explain rollback, backup restoration, secret rotation, and the main cost drivers.
- [ ] Defend CV measurements and distinguish personal contributions from team outcomes.
- [ ] Solve relevant coding exercises independently and test their edge cases.
- [ ] Adapt preparation to the specific role and interview format.

**Remember:** Definitions help recall; practical exercises build skill; evidence makes interview answers credible.
