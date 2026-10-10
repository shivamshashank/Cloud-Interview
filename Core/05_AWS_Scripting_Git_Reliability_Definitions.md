# AWS + Operational Scripting + Git + Reliability — definitions to remember

Short interview definitions: **term → function**, with examples and practical preparation targets for cloud-engineer roles.

## AWS — identity, accounts, and networking

- **AWS account / Region / Availability Zone →** Account is an administrative boundary; Region is a geographic deployment area; an AZ is an isolated location within a Region. Multi-AZ reduces some local failure risks.
- **IAM user / role →** A user is an identity that can have credentials; a role is assumed to obtain temporary credentials. Prefer suitable roles/federation over embedded long-lived keys.
- **IAM policy →** JSON permissions defining allowed or denied actions, resources, and conditions; explicit denies override applicable allows.
- **Role trust policy →** Defines who may assume a role; the role’s permission policies define what the resulting session can do.
- **STS →** Security Token Service issues temporary credentials; use get-caller-identity to confirm the actual account and identity before debugging permissions.
- **Instance profile →** Container for an IAM role attached to EC2; applications can obtain temporary role credentials without storing static keys.
- **Least privilege →** Grant only the actions, resources, and conditions needed; broad administrator access hides permission problems instead of solving them.
- **Cross-account access →** Typically needs appropriate trust/resource permissions and caller permissions; access can also be constrained by organization policies and boundaries.
- **VPC / subnet →** VPC is a logically isolated network; each AWS subnet belongs to one AZ. Use routes and access controls to shape connectivity.
- **Security group / NACL →** Security groups are stateful allow rules at associated interfaces; NACLs are stateless subnet-boundary filters with allow/deny rules.
- **Public / private subnet →** Public has a direct route to an internet gateway; private does not. A route alone does not grant resource access.
- **Public NAT gateway →** Lets private IPv4 resources initiate internet connections and receive replies; needs suitable routing, public addressing, and access rules.
- **VPC endpoint →** Private access path to supported services without requiring a public internet path; endpoint types, policies, and costs differ.
- **Route 53 →** AWS DNS service; records can route a name to application endpoints. DNS changes are subject to caching and TTLs.
- **Alias record →** Route 53 record type extension pointing to supported AWS targets; useful for load balancers and some zone-apex cases.

## AWS — compute and application delivery

- **EC2 →** Virtual server service; choose image, instance type, storage, networking, and role. You still manage the guest OS and application.
- **AMI / user data →** AMI provides the machine image; user data can bootstrap an instance. Verify cloud-init or relevant bootstrap logs rather than assume setup succeeded.
- **EBS →** Block storage associated with an AZ; volumes and snapshots need deliberate lifecycle and backup management.
- **EC2 Auto Scaling Group →** Maintains a desired instance population and can adjust it using scaling policies; health checks and warm-up affect replacement behaviour.
- **Launch template →** Versioned instance-launch configuration, including image, instance type, networking, and supported bootstrap settings.
- **ALB →** Application Load Balancer routes HTTP/HTTPS requests by rules such as host/path to target groups.
- **Target group →** Backend registration and health-check configuration for load balancing; a running server can still be an unhealthy target.
- **NLB →** Network Load Balancer handles transport-level traffic; choose it when its protocol and connection behaviour fit the requirement.
- **ECS / EKS →** ECS orchestrates AWS container workloads; EKS provides managed Kubernetes control-plane functionality. Operational responsibilities differ.
- **Fargate →** Managed compute option for supported ECS/EKS workloads, reducing server management while still requiring workload sizing and configuration.
- **ECS task definition / service →** Task definition specifies containers and resources; a service maintains tasks and integrates deployment and health behaviour.
- **ECR →** Container image registry; image-pull permissions, network access, tags/digests, and scanning configuration all matter.
- **Lambda →** Runs functions on demand; configuration includes runtime, execution role, memory, timeout, and concurrency. Cold starts and dependencies affect latency.
- **API Gateway →** Managed API entry point supporting authentication, routing/integration, throttling, and other features depending on API type.
- **Systems Manager Session Manager →** Managed administrative sessions where prerequisites, agent, permissions, and connectivity are configured; can avoid public SSH exposure.

## AWS — storage, databases, monitoring, and messaging

- **S3 →** Object storage using buckets and keys; not a normal POSIX filesystem. Access uses identity/resource policies and related controls.
- **S3 versioning →** Preserves object versions and delete markers for recovery; it does not eliminate the need to manage retention and deletion permissions.
- **S3 lifecycle →** Rules transitioning or expiring eligible objects/versions; review restore delay and minimum-storage costs for archival classes.
- **S3 Block Public Access →** Controls limiting public exposure; use alongside correct policies and ownership settings rather than as a substitute for all authorization.
- **KMS →** Managed cryptographic key service; encrypted data access may require both storage and KMS permissions. Key availability/deletion affects recoverability.
- **RDS →** Managed relational database service; AWS handles supported platform operations, while you still manage schema, query behaviour, access, and recovery planning.
- **Multi-AZ / read replica →** Multi-AZ deployment primarily supports availability; read replicas support read scaling and replication scenarios. Capabilities differ by engine/deployment type.
- **RDS snapshot / point-in-time recovery →** Restore a database from a snapshot or an available time in the retained recovery window, typically into a new DB instance; test application cutover.
- **CloudWatch →** Metrics, logs, alarms, and related operational tooling; EC2 guest memory needs suitable collection rather than appearing as a standard host metric automatically.
- **CloudTrail →** Records supported AWS API/account activity for auditing; it is different from application request logs and metric monitoring.
- **SNS / SQS →** SNS distributes notifications to subscribers; SQS buffers messages for consumers. Delivery semantics require duplicate-safe processing where applicable.
- **Dead-letter queue →** Destination for messages that cannot be processed successfully under configured policies; investigate and replay deliberately.
- **Secrets Manager / Parameter Store →** Services for secrets or configuration with differing capabilities; choose access, encryption, rotation, and caching behaviour explicitly.
- **AWS SDK / boto3 →** Python client libraries for AWS APIs; credentials, region, pagination, service errors, retries, and quotas all need handling.

## Operational Python and Bash

- **Operational script →** Automates a real task such as log inspection or resource reporting; correctness includes failure handling, safe scope, and useful output.
- **JSON / YAML parsing →** Convert structured data into usable objects with supported libraries; validate fields and types rather than assume every record is complete.
- **API timeout →** Bounds waiting on a request; include connection/read timeouts and an overall deadline where needed.
- **Pagination →** Fetches all result pages using tokens or SDK paginators; reading only the first response can silently omit resources.
- **Retries with backoff/jitter →** Repeat suitable transient failures a limited number of times, spacing attempts; retrying side effects needs idempotency protection.
- **Structured logging →** Emit consistent fields such as action, resource, outcome, and duration; redact credentials and sensitive payloads.
- **Exit code →** Communicates success/failure to callers and CI; shell convention uses zero for success and nonzero for failure.
- **subprocess.run →** Runs external commands from Python; use argument lists, timeouts, captured output, and explicit failure handling rather than interpolating untrusted shell text.
- **argparse →** Python standard-library CLI argument parsing; makes script inputs, defaults, and help explicit.
- **Bash quoting →** Quote variable expansions such as "$path" to avoid unintended splitting and globbing; do not use eval for ordinary parameter handling.
- **set -euo pipefail →** Common Bash error controls, with important context-specific exceptions; still check expected failures and command outcomes explicitly.
- **trap →** Runs cleanup for selected shell events, such as removing temporary files on exit; cannot handle SIGKILL or guarantee recovery from all failures.
- **Dry-run mode →** Shows intended changes without applying them where supported; preview output still needs review and may not simulate every runtime condition.
- **Unit / integration tests →** Unit tests isolate logic; integration tests check real component boundaries. Test malformed input, timeouts, pagination, and partial failures.

## Git — collaborate and recover

- **Working tree / index / commit →** Working tree is editable files; index is staged content; commit is a recorded snapshot with history.
- **Branch →** Movable name for a commit lineage; use a short-lived branch to prepare a reviewable change.
- **fetch / pull →** fetch updates remote-tracking information; pull fetches and integrates according to the selected merge/rebase behaviour.
- **Merge →** Combines histories; conflicts require understanding both changes, resolving files, testing, and completing the merge.
- **Rebase →** Replays commits on a new base and changes their identities; coordinate before rewriting history used by others.
- **Revert →** Creates a new commit reversing a selected commit’s change; commonly suitable for undoing shared history without erasing it.
- **Reset →** Moves branch/HEAD and optionally index/files depending on mode; hard reset can discard local work and is different from revert.
- **Cherry-pick →** Applies a selected commit’s change to the current branch; can conflict and creates a new commit identity.
- **Stash →** Temporarily saves working changes; untracked files need the relevant option. Restoring can conflict and is not a backup strategy.
- **Pull request review →** Checks behaviour, scope, tests, security, and operational impact before integration; CI success alone does not replace review.
- **.gitignore →** Prevents matching untracked files from being added by default; does not remove already tracked secrets or their history.

## Security, reliability, recovery, and cost

- **Shared responsibility →** Cloud provider and customer responsibilities depend on the service; managed services do not remove responsibility for identity, data, or configuration.
- **Encryption in transit / at rest →** Protect network traffic / stored data; manage trust, keys, access, and recovery, not just the encryption switch.
- **Secret rotation →** Replace credentials safely, update consumers, verify use, and retire old values; simply issuing a new value is not a complete rotation.
- **RTO / RPO →** Recovery Time Objective is target restoration duration; Recovery Point Objective is tolerable data loss measured in time.
- **Backup / replication →** Backup supports recovery to retained points; replication copies changes and can also spread corruption or deletion.
- **Restore test →** Recover into an isolated destination, check data and application behaviour, measure duration, and document cutover requirements.
- **Disaster recovery →** Plan for restoring service after major disruption using chosen recovery targets, dependencies, and tested procedures.
- **Health check →** Measures a defined condition, not universal correctness; distinguish process alive, instance healthy, and real user journey working.
- **Blue-green / canary →** Blue-green switches between complete versions; canary exposes a limited share first. Both need rollback signals and data compatibility planning.
- **Connection pool / backpressure →** Pools reuse bounded connections; backpressure limits intake when capacity is exhausted, avoiding unbounded waiting.
- **Capacity / load test →** Measures behaviour under representative arrivals and concurrency; include overload, errors, tails, and recovery, not only best-case throughput.
- **Cost allocation tags →** Assign spend to service, owner, or environment where enabled/supported; combine with usage and billing data.
- **Rightsizing →** Match resources to measured needs while retaining suitable headroom; low average CPU alone does not prove downsizing is safe.
- **Commitment discounts / Spot →** Commitments trade flexibility for discounts; Spot accepts interruption risk. Assess stable demand and recovery before choosing either.
- **Budgets / cost anomaly detection →** Notifications and analysis help identify spend issues; a budget is not automatically a universal hard spending cap.
- **NAT/data-transfer/storage costs →** Traffic paths, retained logs, snapshots, and object versions can drive spend; optimize with measurements and access requirements.

## Architecture and practical interview evidence

- **Simple highly available web system →** DNS → load balancer → application replicas across AZs → database; protect private dependencies and explain each failure boundary.
- **Stateless application →** Avoids keeping essential per-user state only on one instance, making replacement and horizontal scaling easier.
- **Cache →** Reuses results to reduce repeated work; define expiry, invalidation, hit/miss behaviour, and correctness requirements.
- **Queue worker →** Processes asynchronous work from a queue; bound concurrency and handle duplicates, retries, poison messages, and completion acknowledgments.
- **End-to-end lab →** Provision infrastructure, deploy an app, add monitoring, introduce a controlled failure, diagnose it, restore service, and retain evidence.
- **Incident explanation →** Use symptom → impact → evidence → cause → my action → verification → prevention; select an incident that actually happened.
- **40% deployment-time claim →** Define start/end events and comparable runs, show recorded timings, and distinguish your changes from team outcomes.
- **35% incident-resolution claim →** Define the incident population, timing metric, period, and attribution; do not claim one dashboard alone caused the entire reduction.
- **NGINX upgrade evidence →** Record actual distribution/chart/controller versions, changed settings, tests, rollout, and recovery path; do not invent version numbers.
- **Project evidence →** Separate implemented, demonstrated, evaluated, and planned features; a working demo is different from measured correctness or production reliability.

## Practical targets — what you should be able to demonstrate

1. **AWS:** Trace a request from DNS through a load balancer to a private app and database; explain identities, routes, health checks, scaling, and failure handling.
2. **Python/Bash:** Parse JSON/logs, call an API with timeouts, handle all pages, report failures clearly, and test edge cases.
3. **Git:** Resolve a conflict, review a diff, and revert a bad shared change without discarding other work.
4. **Recovery/security/cost:** Restore a backup, rotate a secret, verify least privilege, and explain the largest cost drivers of your example system.
5. **CV:** Rehearse one real incident, the CI/CD improvement, and the ingress upgrade with your exact contribution and evidence.

## One end-to-end lab to rehearse

```text
Define traffic, availability, RTO/RPO, and budget targets
→ Terraform provisions the chosen lab infrastructure
→ Ansible or image/bootstrap configuration prepares the environment
→ CI builds/tests and publishes an identifiable artifact
→ deploy app → configure metrics/logs/alerts → test real requests
→ introduce one controlled fault → investigate → recover → verify
```

This is a learning plan, not infrastructure created by these notes. Use isolated lab resources and record setup, cleanup, timings, findings, and limitations.

## Personal evidence cards — fill from your records

| Story | Facts to prepare |
| --- | --- |
| CI/CD improvement | Exact timing boundary, sample of runs, before/after values, stages changed, your work versus team work |
| Incident resolution | Real symptom, user impact, commands/queries, supported cause, action, verification, measurement definition |
| NGINX ingress upgrade | Actual old/new versions, compatibility change, configuration, route/TLS tests, rollout and rollback |
| CloudGraph / CloudInferOps | Implemented components, your ownership, tested scenario, evaluated outcome, limits and planned work |

## Official references

[AWS IAM practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html), [EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html), [S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html), [RDS recovery](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html), [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html), [Python subprocess](https://docs.python.org/3/library/subprocess.html), [Git revert](https://git-scm.com/docs/git-revert).
