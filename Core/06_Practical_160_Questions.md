# 160 practical questions — cloud engineering, infrastructure, and operations

Use these to practise **what you would do, why, and what you would check next**. Each question has a short answer and a **2–3 line example**.

Examples use a lab namespace `demo`, Pod `api-123`, container `api`, Deployment/Service `api`, and sample domains or files. Replace them with your actual names. Commands are examples, not actions executed against your systems. Linux commands assume the tools are installed; privileged inspection may require sudo.

**Snippet labels:** shell commands can run with the stated prerequisites; YAML/HCL/Groovy examples are fragments unless described as complete; `text` blocks marked **pseudocode** show the idea rather than executable syntax. Never paste a fragment as a complete deployment. Configuration examples use YAML flow style where helpful to stay within three lines.

## Topic map

| Questions | Topic |
| --- | --- |
| 1–10 | Linux |
| 11–20 | Networking and cloud paths |
| 21–30 | Docker and containerd |
| 31–50 | Kubernetes |
| 51–58 | NGINX |
| 59–65 | Prometheus |
| 66–70 | Grafana |
| 71–75 | Loki and OpenTelemetry |
| 76–85 | Terraform |
| 86–93 | Ansible |
| 94–100 | Jenkins |
| 101–120 | AWS services and troubleshooting |
| 121–130 | Operational Python/Bash |
| 131–138 | Git collaboration and recovery |
| 139–148 | Security, recovery, and cost |
| 149–156 | Architecture and end-to-end exercises |
| 157–160 | CV evidence and incident explanations |

## 1. Linux — inspect and debug

### 1. A Linux service is not starting. What do you inspect?

- **Approach:** Read the service status and recent journal entries before restarting blindly.
- **Check:** Look for the first exit reason, missing configuration, permission error, or port conflict.

```bash
systemctl status api.service
journalctl -u api.service -n 50 --no-pager
```

### 2. How do you find a process using excessive CPU?

- **Approach:** Find the busy process, then inspect its individual threads; 1234 is an example PID.
- **Check:** Identify sustained hot threads and compare with CPU quotas before choosing a profiler.

```bash
top
top -H -p 1234
```

### 3. How do you investigate growing memory use?

- **Approach:** Compare system memory with per-process RSS, then collect an application heap profile if needed.
- **Check:** Growth under repeated equal workloads is more useful evidence than one large RSS reading.

```bash
free -h
ps -eo pid,comm,rss --sort=-rss | head
```

### 4. Disk space is full, but du finds little data. What next?

- **Approach:** Compare filesystem usage, visible files, and deleted files still open by processes.
- **Check:** An open deleted log can retain disk blocks; identify the owner before changing its logging lifecycle.

```bash
df -h /var
sudo du -xh /var --max-depth=1
sudo lsof +L1
```

### 5. How do you check whether inode exhaustion caused a write failure?

- **Approach:** Inspect inode usage separately from byte capacity.
- **Check:** Many tiny files can exhaust inodes even when the filesystem still has free bytes.

```bash
df -i /var
df -h /var
```

### 6. A readable file gives Permission denied. How do you debug it?

- **Approach:** Check the process identity and permissions on every parent directory.
- **Check:** Directory traversal, ACLs, or security policy can block access despite the file’s own read bit.

```bash
id
namei -l /srv/api/config.yaml
getfacl /srv/api/config.yaml
```

### 7. How do you gracefully stop a stuck application?

- **Approach:** Request termination first and inspect whether it exits; use force only after checking the impact.
- **Check:** SIGTERM permits cleanup; SIGKILL cannot be handled. PID 1234 must identify the intended process.

```bash
kill -TERM 1234
ps -p 1234 -o pid,stat,cmd
```

### 8. How do you identify storage-related waiting?

- **Approach:** Inspect device statistics and system task/CPU states over several samples.
- **Check:** High latency or queues plus blocked work suggests I/O waiting; utilization alone is not a diagnosis.

```bash
iostat -xz 1 3
vmstat 1 3
```

### 9. How do you investigate failed file operations in a process?

- **Approach:** Trace relevant file-related system calls for the target process, using a bounded capture.
- **Check:** Look for errors such as ENOENT or EACCES; attaching a tracer can add overhead.

```bash
sudo timeout 10s strace -f -e trace=file -p 1234
# Inspect failing paths and error codes.
```

### 10. How can you inspect a process’s namespaces and resource group?

- **Approach:** Inspect namespace membership and cgroup information for the target PID.
- **Check:** Separate isolation problems from resource-budget problems; cgroup paths depend on the host setup.

```bash
sudo lsns -p 1234
cat /proc/1234/cgroup
```

References: [Linux manuals](https://man7.org/linux/man-pages/).

## 2. Networking — locate the broken hop

### 11. An application cannot resolve a hostname. What do you check?

- **Approach:** Query DNS and inspect the configured resolver from the failing environment.
- **Check:** A correct lookup on your laptop does not prove DNS works inside the failing container.

```bash
dig api.example.com
cat /etc/resolv.conf
```

### 12. A host cannot reach another network. How do you inspect the route?

- **Approach:** Ask Linux which route/interface/source it selects for a sample destination.
- **Check:** Check the gateway and interface; route existence does not prove firewall or remote reachability.

```bash
ip route
ip route get 203.0.113.10
```

### 13. How do you verify whether the API is listening on the right port?

- **Approach:** Inspect listening sockets and test locally.
- **Check:** A listener bound only to 127.0.0.1 cannot normally receive traffic arriving at a non-loopback address.

```bash
sudo ss -lntp
curl -v http://127.0.0.1:8080/health
```

### 14. How do you separate DNS, connection, and response delays?

- **Approach:** Use curl timing fields to identify where the request spends time.
- **Check:** Values are cumulative milestones: derive phase durations by subtraction and allow for connection reuse.

```bash
curl -sS -o /dev/null -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} first=%{time_starttransfer} total=%{time_total}\n' https://api.example.com
# Compare phase timings across repeated requests.
```

### 15. How do you inspect a TLS certificate problem?

- **Approach:** Connect using the correct server name and check trust, hostname, chain, and expiry.
- **Check:** Use the hostname verification flag; successful encryption alone does not prove the certificate is trusted.

```bash
openssl s_client -connect api.example.com:443 -servername api.example.com -verify_hostname api.example.com -verify_return_error </dev/null
# Read certificate verification errors and the presented chain.
```

### 16. How do you inspect Linux firewall and NAT rules?

- **Approach:** List rules and counters without changing them.
- **Check:** INPUT concerns this host, FORWARD concerns routed traffic; check the actual backend if the host uses nftables.

```bash
sudo iptables -L -n -v
sudo iptables -t nat -L -n -v
```

### 17. How do you check connection tracking during a NAT problem?

- **Approach:** Inspect tracked flows and compare with failing connections; conntrack tooling/permissions are required.
- **Check:** Look for missing or unexpected mappings and table pressure, not only total connection counts.

```bash
sudo conntrack -L -p tcp
sudo conntrack -S
```

### 18. A private AWS instance cannot download updates. How do you check NAT routing?

- **Approach:** Pseudocode: verify the private route, public NAT placement, internet route, and access rules.
- **Check:** The NAT must be available; security groups, NACL return traffic, and DNS must also allow the request.

```text
Private subnet: default IPv4 route → available public NAT gateway
NAT subnet: default route → internet gateway; NAT has Elastic IP
Check security groups, NACLs, DNS, and the actual destination
```

### 19. How do you capture evidence of a connection timeout?

- **Approach:** Capture only relevant traffic for a bounded time from the failing host.
- **Check:** Repeated SYNs without replies suggest loss/drop somewhere; a reset indicates active rejection, but neither alone locates the responsible device.

```bash
sudo timeout 10s tcpdump -ni any -c 30 'host 203.0.113.10 and tcp port 443'
# Compare SYN, SYN-ACK, resets, and retransmissions.
```

### 20. How do you test a backend while preserving the HTTPS hostname?

- **Approach:** Override DNS for one curl request without changing the URL hostname.
- **Check:** This preserves Host and TLS SNI; compare the selected backend with the normal path and keep certificate verification enabled.

```bash
curl -v --resolve api.example.com:443:203.0.113.10 https://api.example.com/health
curl -v https://api.example.com/health
```

References: [AWS NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html), [Netfilter](https://www.netfilter.org/).

## 3. Docker and containerd — build and inspect

### 21. How do you build and run a local application image?

- **Approach:** Build from the Dockerfile and publish a host port to the container’s listening port.
- **Check:** The app must actually listen on port 8080 on an appropriate interface; EXPOSE alone does not publish it.

```bash
docker build -t api:demo .
docker run --rm --name api -p 8080:8080 api:demo
```

### 22. A container exits immediately. What do you inspect?

- **Approach:** Use a retained failed container named api to read logs and termination details.
- **Check:** The startup command, exit code, environment, permissions, and dependencies matter; --rm containers disappear after exit.

```bash
docker logs api
docker inspect api --format '{{json .State}}'
```

### 23. How do you enter a running container to investigate?

- **Approach:** Execute a shell or a specific command inside the container.
- **Check:** This requires a running container and the binary to exist; minimal images may have no shell.

```bash
docker exec -it api sh
docker exec api cat /etc/resolv.conf
```

### 24. How would you write a multi-stage build?

- **Approach:** Pseudocode: compile/test in a builder, then copy only required outputs into a runtime stage.
- **Check:** The real Dockerfile needs valid paths, dependencies, and startup settings; smaller runtime images do not guarantee faster compilation.

```text
Builder stage: copy source → install build dependencies → compile /out/api
Runtime stage: use minimal compatible base → COPY --from=builder /out/api /api
Set non-root user and ENTRYPOINT ["/api"] as appropriate
```

### 25. How do you stop source edits from invalidating dependency installation unnecessarily?

- **Approach:** Dockerfile fragment for a Node app: copy dependency manifests first, then source afterward.
- **Check:** Use a suitable Node base and WORKDIR before this fragment; lockfile changes should invalidate npm ci.

```dockerfile
COPY package*.json ./
RUN npm ci
COPY . .
```

### 26. How do you reduce the Docker build context?

- **Approach:** Example .dockerignore content excluding unnecessary local files.
- **Check:** Use project-appropriate rules; excluding .env does not remove secrets copied or embedded through other means.

```text
.git
node_modules
.env
```

### 27. How do you persist data outside a container’s writable layer?

- **Approach:** Create a named volume and mount it at the application’s data directory.
- **Check:** The app must use /data; removing the container normally leaves the named volume, but explicit volume deletion can remove data.

```bash
docker volume create api-data
docker run --rm --mount source=api-data,target=/data api:demo
```

### 28. Two containers cannot communicate. What do you inspect?

- **Approach:** Compare their network membership, DNS names, and actual listening port.
- **Check:** Use a shared user-defined network where appropriate; localhost refers to the calling container’s own network namespace.

```bash
docker inspect api --format '{{json .NetworkSettings.Networks}}'
docker network inspect app-net
```

### 29. How do you check container resource limits and consumption?

- **Approach:** Compare observed usage with configured memory/CPU limits.
- **Check:** A low host-wide load does not rule out container CPU throttling or a restrictive memory allowance.

```bash
docker stats --no-stream api
docker inspect api --format 'memory={{.HostConfig.Memory}} nanoCPUs={{.HostConfig.NanoCpus}}'
```

### 30. How do you inspect containers on a Kubernetes node using containerd?

- **Approach:** Use crictl configured for the node’s CRI endpoint to inspect containers and runtime information.
- **Check:** crictl targets CRI; ctr uses containerd’s lower-level API and namespace model, so it is not a drop-in replacement.

```bash
sudo crictl ps -a
sudo crictl info
```

References: [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/), [Docker networking](https://docs.docker.com/engine/network/).

## 4. Kubernetes — operate and troubleshoot

### 31. How do you use kubectl exec to debug an application?

- **Approach:** Run a shell or a specific command in the intended Pod and container.
- **Check:** Specify the namespace/container; exec requires a running container, suitable RBAC, and the requested binary.

```bash
kubectl exec -n demo -it api-123 -c api -- sh
kubectl exec -n demo api-123 -c api -- cat /etc/resolv.conf
```

### 32. What if the application image has no shell or curl?

- **Approach:** Use an approved ephemeral debug container sharing the Pod network where permitted.
- **Check:** Availability depends on RBAC, admission policy, runtime support, and image access; tool access does not automatically expose every app file.

```bash
kubectl debug -n demo -it api-123 --image=busybox:1.36 --target=api
# Use the added container's tools to inspect Pod networking.
```

### 33. How do you read current and previous container logs?

- **Approach:** Read recent logs, then the preceding instance after a restart.
- **Check:** Previous logs only exist when a previous container instance is retained; central logging is needed for broader history.

```bash
kubectl logs -n demo api-123 -c api --tail=50
kubectl logs -n demo api-123 -c api --previous
```

### 34. How do you investigate CrashLoopBackOff?

- **Approach:** Read events/termination details and the previous instance’s logs before changing probes or limits.
- **Check:** Find whether the app exits, a probe fails, or configuration/dependencies are missing; deleting the Pod usually does not fix the cause.

```bash
kubectl describe pod -n demo api-123
kubectl logs -n demo api-123 -c api --previous
```

### 35. A Pod is Pending. What do you inspect?

- **Approach:** Inspect events for placement constraints, resource shortages, taints, or unbound storage.
- **Check:** Compare the required resources and affinity with eligible nodes; Pending is a phase rather than a single cause.

```bash
kubectl describe pod -n demo api-123
kubectl get nodes -o wide
```

### 36. How do you diagnose an OOMKilled container?

- **Approach:** Inspect termination state and current resource usage, then compare limits with memory profiles over time.
- **Check:** kubectl top needs a metrics API and may miss the peak that caused the kill; inspect historical data too.

```bash
kubectl describe pod -n demo api-123
kubectl top pod -n demo api-123 --containers
```

### 37. How is a Pod IP assigned, and how do you inspect it?

- **Approach:** The runtime sets up a Pod sandbox and invokes the configured CNI networking; its IPAM mechanism allocates address(es), and kubelet reports Pod status.
- **Check:** Normally containers share the Pod network namespace/IP; hostNetwork and dual-stack setups differ. Kube-proxy does not allocate Pod IPs.

```bash
kubectl get pod -n demo api-123 -o wide
kubectl get pod -n demo api-123 -o jsonpath='{.status.podIPs}'
```

### 38. A Service has no working backends. How do you investigate?

- **Approach:** Compare Service selectors/ports with Pod labels, readiness, and EndpointSlices.
- **Check:** An empty endpoint list commonly points to label/readiness issues; correct endpoints shift attention to connectivity and app listeners.

```bash
kubectl describe service -n demo api
kubectl get pods -n demo --show-labels
kubectl get endpointslice -n demo -l kubernetes.io/service-name=api
```

### 39. How do you test Service DNS and connectivity inside a Pod?

- **Approach:** Run name resolution and an HTTP request from a container with the required tools.
- **Check:** This BusyBox-style example assumes nslookup/wget exist; distinguish DNS lookup failure from connection or application failure.

```bash
kubectl exec -n demo api-123 -- nslookup api.demo.svc.cluster.local
kubectl exec -n demo api-123 -- wget -qO- http://api:8080/health
```

### 40. How do you write a readiness probe?

- **Approach:** YAML fragment under a container: check an app endpoint before considering the Pod ready.
- **Check:** Readiness failure normally removes regular Service eligibility; it does not restart the container. Tune timings to app behaviour.

```yaml
readinessProbe:
  httpGet: {path: /ready, port: 8080}
  periodSeconds: 5
```

### 41. How do you configure CPU and memory requests and limits?

- **Approach:** YAML fragment under a container setting its resource requirements and boundaries.
- **Check:** 200m means 0.2 CPU; requests guide scheduling, while limits can cause CPU throttling or memory OOM handling.

```yaml
resources:
  requests: {cpu: 200m, memory: 256Mi}
  limits: {cpu: "1", memory: 512Mi}
```

### 42. How do you deploy a new image and verify the rollout?

- **Approach:** Set the lab Deployment’s image, wait for rollout, then test application traffic.
- **Check:** A completed rollout still needs latency/error checks; under GitOps, change the source configuration rather than fight reconciliation.

```bash
kubectl set image -n demo deployment/api api=registry.example.com/api:v2
kubectl rollout status -n demo deployment/api --timeout=120s
kubectl get pods -n demo -l app=api -o wide
```

### 43. A PVC remains Pending. What do you inspect?

- **Approach:** Read claim events and compare StorageClass, requested size/access mode, and placement constraints.
- **Check:** WaitForFirstConsumer can intentionally delay binding until a consuming Pod is scheduled; do not assume every Pending claim is broken.

```bash
kubectl describe pvc -n demo api-data
kubectl get storageclass
kubectl get pv
```

### 44. How do you check StatefulSet identity and storage?

- **Approach:** Inspect the StatefulSet’s Pods, volume claims, and template configuration.
- **Check:** Stable names and claims support identity continuity, but application replication and backup still need separate handling.

```bash
kubectl get statefulset,pods,pvc -n demo
kubectl describe statefulset -n demo db
```

### 45. How do you create a one-off Job and inspect scheduled Jobs?

- **Approach:** Create a lab Job from an existing CronJob template, then inspect its execution.
- **Check:** Check concurrency and side effects before manually launching work; retries must be safe for the task.

```bash
kubectl create job -n demo backup-manual --from=cronjob/backup
kubectl get jobs,cronjobs -n demo
kubectl logs -n demo job/backup-manual
```

### 46. How do you check whether a DaemonSet covers eligible nodes?

- **Approach:** Compare desired/current/ready counts and inspect selectors and tolerations.
- **Check:** Not every cluster node is necessarily eligible; node labels, taints, and placement rules explain intentional exclusions.

```bash
kubectl get daemonset -n demo -o wide
kubectl describe daemonset -n demo log-agent
```

### 47. Pod-to-Pod traffic fails. How do you investigate NetworkPolicy?

- **Approach:** Inspect policies and namespace/Pod labels for both endpoints.
- **Check:** Policy enforcement needs a supporting network implementation; allowed egress and ingress must both permit the connection, including DNS where needed.

```bash
kubectl get networkpolicy -n demo
kubectl describe networkpolicy -n demo api-policy
kubectl get namespace demo --show-labels
```

### 48. An application gets Forbidden from the Kubernetes API. What next?

- **Approach:** Inspect the relevant workload identity and whether it can perform the exact verb on the resource.
- **Check:** Impersonation checks require your own permission to impersonate; grant minimum scope rather than defaulting to cluster-admin.

```bash
kubectl auth can-i get pods -n demo --as=system:serviceaccount:demo:api
kubectl get rolebinding -n demo
```

### 49. How do you check a Kustomize change before Argo CD applies it?

- **Approach:** Render the overlay locally, then inspect proposed differences against a lab cluster.
- **Check:** Argo can use a different Kustomize version/options; after Git promotion, verify its sync and health separately.

```bash
kubectl kustomize k8s/overlays/demo
kubectl diff -k k8s/overlays/demo
```

### 50. How do you access an internal Service locally for debugging?

- **Approach:** Forward a local port to a Service-selected Pod, then call localhost in a second terminal.
- **Check:** Port-forward is a temporary debugging connection; it does not validate the normal external ingress path.

```bash
kubectl port-forward -n demo service/api 18080:8080
# In another terminal: curl http://127.0.0.1:18080/health
```

References: [kubectl exec](https://kubernetes.io/docs/tasks/debug/debug-application/get-shell-running-container/), [cluster networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/), [Services](https://kubernetes.io/docs/concepts/services-networking/service/), [probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/).

## 5. NGINX — configure and investigate

### 51. How do you write a minimal reverse-proxy route?

- **Approach:** NGINX fragment inside an http context: listen on 8080 and proxy /api/ to the backend.
- **Check:** The backend name must resolve; without a URI in proxy_pass, the simple example preserves the /api/ path.

```nginx
server { listen 8080;
  location /api/ { proxy_pass http://api:8080; }
}
```

### 52. How does a trailing slash change the backend path?

- **Approach:** Compare these alternative location fragments, not two rules to install together.
- **Check:** For this simple prefix example, the first forwards /api/users; the second replaces /api/ and forwards /users.

```nginx
location /api/ { proxy_pass http://backend; }
# Alternative: strip the matching /api/ prefix.
location /api/ { proxy_pass http://backend/; }
```

### 53. How do you safely apply a changed nginx.conf?

- **Approach:** Validate first, then reload the tested configuration and inspect real requests.
- **Check:** A syntax pass does not prove routing/TLS/backend behaviour; these assume the intended installation and permissions.

```bash
sudo nginx -t
sudo nginx -s reload
curl -v http://127.0.0.1:8080/api/health
```

### 54. How do you investigate a 502 or 504 response?

- **Approach:** Correlate proxy errors with a direct request from the proxy’s network context to the upstream.
- **Check:** 502 suggests an invalid/unavailable response; 504 a timeout. Check the log’s exact operation and target rather than increasing timeouts immediately.

```bash
sudo tail -n 50 /var/log/nginx/error.log
curl -v http://api:8080/health
```

### 55. How do you configure upstream timeouts?

- **Approach:** NGINX fragment inside the proxying location: bound connection establishment and data-operation gaps.
- **Check:** Read/send timeouts concern gaps between operations, not a single end-to-end request deadline.

```nginx
proxy_connect_timeout 2s;
proxy_read_timeout 30s;
proxy_send_timeout 30s;
```

### 56. How do you preserve original request details for the backend?

- **Approach:** Set forwarded host, client chain, and scheme in the proxying location.
- **Check:** This assumes NGINX sees the intended scheme; trusted-proxy configuration is needed behind another TLS terminator, and client-supplied headers must not be blindly trusted.

```nginx
proxy_set_header Host $host;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

### 57. How do you define a group of backend servers?

- **Approach:** Define an upstream inside http, then reference that name from a server/location.
- **Check:** The default method distributes requests using round-robin; both names must resolve and listen on the configured ports.

```nginx
upstream api_pool { server api1:8080; server api2:8080; }
server { listen 8080; location / { proxy_pass http://api_pool; } }
```

### 58. Ingress works before an upgrade but fails afterward. What do you inspect?

- **Approach:** Read Ingress status/events and logs for the actual controller implementation and namespace.
- **Check:** Compare supported annotations/settings, generated routes, Service endpoints, certificates, and chart/controller compatibility.

```bash
kubectl describe ingress -n demo api
kubectl logs -n ingress-system deployment/controller --tail=100
kubectl get endpointslice -n demo -l kubernetes.io/service-name=api
```

References: [NGINX proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html), [request processing](https://nginx.org/en/docs/http/request_processing.html).

## 6. Prometheus — scrape, query, and alert

### 59. How do you configure Prometheus to scrape an application?

- **Approach:** prometheus.yml fragment: declare a job and its reachable metrics endpoint target.
- **Check:** The app must expose compatible metrics on the default /metrics path; static targets suit this small example, while clusters often use discovery.

```yaml
scrape_configs:
  - job_name: api
    static_configs: [{targets: ["api:8080"]}]
```

### 60. Prometheus reports a target down. How do you investigate?

- **Approach:** Check the target’s scrape error and try its endpoint from the Prometheus network context.
- **Check:** A failed scrape can be networking, auth, TLS, path, or format; up=1 only means scraping works, not that all app requests succeed.

```bash
curl -v http://api:8080/metrics
# In Prometheus, query: up{job="api"}
```

### 61. How do you calculate requests per second?

- **Approach:** Use rate on a counter over a suitable window, then aggregate by service.
- **Check:** Check the actual metric/label names; apply rate before sum so resets can be handled per series.

```promql
sum by (service) (
  rate(http_requests_total[5m])
)
```

### 62. How do you calculate an HTTP 5xx error ratio?

- **Approach:** Divide the 5xx request rate by the total rate using matching service groups.
- **Check:** The status label and metric must exist; no traffic or absent 5xx series needs deliberate handling in real alerts.

```promql
sum by (service) (rate(http_requests_total{status=~"5.."}[5m]))
/
sum by (service) (rate(http_requests_total[5m]))
```

### 63. How do you calculate p95 latency across replicas?

- **Approach:** For a classic histogram measured in seconds, aggregate bucket rates while retaining le before estimating the quantile.
- **Check:** Do not average instance percentiles; bucket resolution and volume affect the estimate. Native histogram queries differ.

```promql
histogram_quantile(0.95,
  sum by (le, service) (rate(http_request_duration_seconds_bucket[5m]))
)
```

### 64. How do you write a basic alert for a failed scrape?

- **Approach:** YAML fragment inside a rule group’s rules list: require a target’s up value to stay zero.
- **Check:** A missing target may vanish instead of becoming up=0; add appropriate absence/discovery checks separately.

```yaml
- alert: ApiScrapeFailed
  expr: up{job="api"} == 0
  for: 2m
```

### 65. How do you test a rule file before deployment?

- **Approach:** Run Prometheus tooling against the rule file and configured unit-test cases.
- **Check:** Syntax validation does not prove business correctness; include zero traffic, missing data, resets, and firing/recovery cases in rule tests.

```bash
promtool check rules alerts.yml
promtool test rules alerts.test.yml
```

References: [Prometheus configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/), [query functions](https://prometheus.io/docs/prometheus/latest/querying/functions/), [rule testing](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/).

## 7. Grafana — create dashboards and investigate

### 66. How do you create a Grafana dashboard from scratch?

- **Approach:** Pseudocode for the UI: add a Prometheus data source, create a dashboard/visualization, and enter a query.
- **Check:** Select requests/second as the unit for request rate; verify returned data, choose a time range, and save with a clear name.

```text
Connections → data sources → add Prometheus → set reachable URL → test/save
Dashboards → new dashboard → add visualization → select that data source
Query: sum(rate(http_requests_total[5m])) → set unit → save dashboard
```

### 67. How do you provision a Prometheus data source using a file?

- **Approach:** Grafana provisioning YAML stored under its configured datasources provisioning directory.
- **Check:** Grafana’s server must reach this URL; this example assumes a Prometheus hostname and suitable network/auth configuration.

```yaml
apiVersion: 1
datasources:
  - {name: Prometheus, type: prometheus, access: proxy, url: "http://prometheus:9090"}
```

### 68. How do you add a service filter to a dashboard?

- **Approach:** Pseudocode: create a Prometheus query variable and reference it in panel queries.
- **Check:** The metric must carry a service label; regex matching works with configured multi-value/all selections.

```text
Dashboard settings → Variables → query variable named service
Prometheus variable: label values of service from http_requests_total
Panel query: sum(rate(http_requests_total{service=~"$service"}[5m]))
```

### 69. A Grafana panel is blank. What do you inspect?

- **Approach:** Pseudocode: test the data source, remove filters, expand the time range, and inspect the executed query.
- **Check:** Separate connection/permission errors from an empty query result; time zones, variables, and label names often explain missing data.

```text
Test data source → open Explore → query up
Set a wider time range → remove service/environment filters
Inspect panel query/error → compare with backend query result
```

### 70. How do you create a Grafana alert and notification route?

- **Approach:** Pseudocode: define a supported metric query and condition, then route its labels to a contact point.
- **Check:** Set no-data/error handling, duration, and ownership, and test notification delivery; avoid duplicating equivalent Prometheus alerts.

```text
Alerting → create rule → select query → define condition and duration
Set labels, owner/runbook, and no-data/error behaviour
Configure contact point + matching notification policy → test
```

References: [Create Grafana dashboards](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/create-dashboard/), [provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/).

## 8. Loki and OpenTelemetry — connect logs and traces

### 71. How do you send container logs to Loki?

- **Approach:** Pseudocode: configure an approved collector to discover logs, attach bounded labels, and send to Loki.
- **Check:** The collector must have source access and correct Loki endpoint/auth; verify ingestion before assuming Grafana is the failure.

```text
Collector discovers container logs → reads new entries
Attach bounded labels: service, environment, namespace → send to Loki
Grafana Explore → select Loki → query {service="api"}
```

### 72. How do you find error logs for a service?

- **Approach:** Select the Loki stream labels and filter line content within the incident time window.
- **Check:** Matching is case-sensitive in this example; use actual labels and inspect log context around errors.

```logql
{service="api", environment="demo"}
|= "error"
```

### 73. How do you filter structured JSON logs by severity?

- **Approach:** Parse each line as JSON, exclude parse failures, and filter the extracted level field.
- **Check:** Log format/field names must match; this keeps severity filtering out of unbounded indexed-label choices.

```logql
{service="api"} | json
| __error__="" | level="error"
```

### 74. How do you calculate an error-log rate?

- **Approach:** Use a log range query counting matching lines per second, then aggregate streams.
- **Check:** Error-log rate is not automatically request-error ratio: one request can emit multiple lines or none.

```logql
sum(rate(
  {service="api"} |= "error" [5m]
))
```

### 75. How do you connect an error log to a distributed trace?

- **Approach:** Pseudocode: emit trace IDs in logs, propagate context, and link to a configured trace backend in Grafana.
- **Check:** OpenTelemetry generates/transports telemetry; Loki stores logs, while a separate backend stores traces. Sampling can leave no retained trace.

```text
Application logs trace_id and propagates trace context downstream
Collector exports spans → configured trace backend; collector sends logs → Loki
Grafana log trace-ID link → corresponding trace → inspect slow/error spans
```

References: [Loki LogQL](https://grafana.com/docs/loki/latest/query/), [OpenTelemetry propagation](https://opentelemetry.io/docs/concepts/context-propagation/).

## 9. Terraform — write, plan, and manage infrastructure

### 76. How do you write a Terraform resource configuration?

- **Approach:** HCL resource example: with an initialized AWS provider and suitable credentials, declare a security group in an existing VPC.
- **Check:** Supply the real VPC variable. This creates a group, not an automatically attached application firewall; review the plan and access rules.

```hcl
resource "aws_security_group" "api" {
  vpc_id = var.vpc_id
}
```

### 77. How do you parameterize infrastructure and expose a result?

- **Approach:** Define an input variable and output referencing the resource from the previous example.
- **Check:** An output exposes a value, while the variable controls input; type checking catches some configuration mistakes.

```hcl
variable "vpc_id" { type = string }
output "api_security_group_id" { value = aws_security_group.api.id }
```

### 78. How do you validate and review a Terraform change?

- **Approach:** Initialize providers/backend, format, validate, then generate a saved plan; assume init has been completed for the three commands below.
- **Check:** Read creates, updates, replacements, and deletions; the saved plan can contain secrets and must be protected.

```bash
terraform fmt -check
terraform validate
terraform plan -out=reviewed.plan
```

### 79. How do you apply exactly the reviewed plan?

- **Approach:** Initialize the directory first and apply the saved plan approved for this environment.
- **Check:** Use the correct backend/account; if the plan becomes stale or context changes, regenerate and review rather than bypassing safeguards.

```bash
terraform init
terraform apply reviewed.plan
terraform output
```

### 80. How do you configure shared remote state?

- **Approach:** Pseudocode: use an existing secured backend and supported locking; backend creation is a separate bootstrap concern.
- **Check:** Restrict access, protect backups/version history, and configure encryption. A Terraform sensitive flag does not encrypt the state.

```text
Backend configuration → existing protected state store + environment-specific key
Enable supported locking and restricted access → terraform init
Verify state ownership, backup/versioning, and encryption settings
```

### 81. How do you detect a manual infrastructure change?

- **Approach:** Plan against the real provider to inspect differences, then decide which state is intended.
- **Check:** A normal plan can propose reverting drift; a refresh-only plan reviews state updates without proposing infrastructure reconciliation.

```bash
terraform plan
terraform plan -refresh-only
```

### 82. How do you import an existing resource?

- **Approach:** Bind the existing object to its intended address after writing matching configuration.
- **Check:** Example uses a placeholder security-group ID; import does not prove the next plan is safe and does not automatically generate configuration with this CLI form.

```bash
terraform import aws_security_group.api sg-0123456789abcdef0
terraform plan
```

### 83. How do you create a reusable Terraform module?

- **Approach:** A root-module HCL fragment calls a local module that defines its own resources, inputs, and outputs.
- **Check:** The directory must exist and required inputs must be supplied; this minimal call assumes suitable module defaults. Inspect the resulting plan.

```hcl
module "network" {
  source = "./modules/network"
}
```

### 84. How do you create several similar resources with stable identities?

- **Approach:** Pseudocode: use for_each keys rather than numeric positions where key-based identity suits the resource.
- **Check:** The actual HCL needs a complete resource block and initialized provider; removing a key proposes removal of that instance.

```text
Declare aws_security_group.tier with for_each = toset(["web", "api"])
Set name from each.key and vpc_id from the supplied VPC variable
Review separate plan instances: tier["web"] and tier["api"]
```

### 85. An apply failed after creating some objects. What do you do?

- **Approach:** Inspect the error, state, and a fresh plan; a partial failure is not an automatic rollback.
- **Check:** Fix the actual cause and review remaining actions. Do not edit state by hand or rerun destroy as a generic recovery step.

```bash
terraform state list
terraform plan
```

References: [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan), [state](https://developer.hashicorp.com/terraform/language/state), [modules](https://developer.hashicorp.com/terraform/language/modules).

## 10. Ansible — write inventory and configuration

### 86. How do you write an Ansible inventory?

- **Approach:** INI inventory groups target hosts and specifies how to connect; this example uses documentation-only addresses.
- **Check:** Use actual reachable addresses and authorized SSH credentials, not plaintext passwords in a shared inventory.

```ini
[web]
web1 ansible_host=192.0.2.10 ansible_user=ubuntu
web2 ansible_host=192.0.2.11 ansible_user=ubuntu
```

### 87. How do you write ansible.cfg?

- **Approach:** Minimal configuration chooses an inventory path and number of concurrent worker processes.
- **Check:** Relative inventory paths are resolved according to Ansible configuration behaviour; keep host-key verification enabled and use the intended config file.

```ini
[defaults]
inventory = ./inventory.ini
forks = 5
```

### 88. How do you write a playbook to install NGINX?

- **Approach:** Complete compact YAML playbook: target the web group, escalate privileges, and ensure the package is present.
- **Check:** This assumes appropriate package metadata, permissions, and host support; package installation alone does not guarantee the service is running.

```yaml
- hosts: web
  become: true
  tasks: [{name: Install NGINX, ansible.builtin.package: {name: nginx, state: present}}]
```

### 89. How do you ensure a service is running and enabled?

- **Approach:** Task fragment inside a playbook’s tasks list ensures the service is started and enabled.
- **Check:** The play needs suitable privileges and the service must exist; repeated runs should not restart an already healthy service unnecessarily.

```yaml
- name: Keep NGINX running
  ansible.builtin.service:
    {name: nginx, state: started, enabled: true}
```

### 90. How do you render configuration and reload only when it changes?

- **Approach:** Pseudocode showing a template task notifying a handler; the actual playbook requires correctly nested tasks and handlers.
- **Check:** Validate the generated config before reload and use accurate changed reporting; handlers normally combine repeated notifications.

```text
Task: render nginx.conf.j2 → target nginx.conf; validate with nginx -t
On actual file change: notify handler named Reload NGINX
Handler: reload nginx service using become permissions
```

### 91. How do you check connectivity and preview a playbook?

- **Approach:** Use Ansible ping, syntax checking, and supported check/diff modes before a real run.
- **Check:** Ping tests Ansible execution, not ICMP; check mode is incomplete for some modules, and diff output may expose secrets.

```bash
ansible web -i inventory.ini -m ansible.builtin.ping
ansible-playbook -i inventory.ini site.yml --syntax-check
ansible-playbook -i inventory.ini site.yml --check --diff
```

### 92. How do you keep Ansible variables containing passwords encrypted?

- **Approach:** Use Ansible Vault to encrypt the variable file and provide the password through an approved method at execution.
- **Check:** Vault protects stored content; suppress sensitive task output and protect decrypted data too. It is different from HashiCorp Vault.

```bash
ansible-vault encrypt secrets.yml
ansible-playbook -i inventory.ini site.yml --ask-vault-pass
```

### 93. How do you roll out configuration one server at a time?

- **Approach:** Play fragment uses serial to run a batch of one host, with work factored into a role.
- **Check:** The actual role must exist. Add health checks and failure handling; serial alone does not guarantee a failed update stops the entire rollout.

```yaml
- hosts: web
  serial: 1
  roles: [nginx]
```

References: [Ansible playbooks](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html), [inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html), [configuration](https://docs.ansible.com/ansible/latest/reference_appendices/config.html).

## 11. Jenkins — implement and troubleshoot workflows

### 94. How do you write a minimal Jenkins Pipeline?

- **Approach:** Complete compact Declarative Pipeline checking out the configured SCM revision and running Go tests.
- **Check:** The agent needs Git/Go and repository access; an explicitly isolated, suitably labelled agent is preferable for real workloads.

```groovy
pipeline { agent any
  stages { stage('Test') { steps { checkout scm; sh 'go test ./...' } } }
}
```

### 95. How do you run independent checks in parallel?

- **Approach:** Scripted-Pipeline fragment inside a node or Declarative script block runs tests and linting concurrently.
- **Check:** Both branches need the tools and separate resources where necessary; shared agent capacity can limit actual speedup.

```groovy
parallel(
  tests: { sh 'go test ./...' }, lint: { sh 'golangci-lint run' }
)
```

### 96. How do you provide a secret to one Pipeline step?

- **Approach:** Pipeline fragment binds a stored secret text credential within a narrow scope, while shell single quoting avoids Groovy interpolation.
- **Check:** The script must handle API_TOKEN without printing it; masking does not protect secrets from untrusted build code.

```groovy
withCredentials([string(credentialsId: 'api-token', variable: 'API_TOKEN')]) {
  sh './scripts/publish.sh'
}
```

### 97. How do you ensure reports are collected after test failures?

- **Approach:** Declarative post fragment publishes existing JUnit-format XML reports even after a failed stage.
- **Check:** The test runner must generate matching files; Go test alone does not produce JUnit XML without suitable tooling.

```groovy
post { always {
  junit 'reports/*.xml'
} }
```

### 98. A Jenkins build is stuck in the queue. What do you inspect?

- **Approach:** Pseudocode: read the queue reason, required labels, and available executors.
- **Check:** An online agent is insufficient if its labels do not match or another concurrency restriction blocks the job.

```text
Open queued run → inspect queue reason and requested agent label
Check matching agents online + free executors + tool availability
Check job concurrency restrictions, locks, and upstream dependencies
```

### 99. How do you build an image and hand it to Argo CD safely?

- **Approach:** Pseudocode: publish one tested image, record its digest, and update the reviewed desired state.
- **Check:** Use scoped credentials, verify Argo sync plus real traffic, and revert Git for recovery; avoid a competing direct kubectl deployment.

```text
Jenkins: checkout exact commit → test → build/scan → push image → record digest
Review Git change setting the environment image digest → merge
Argo CD syncs → verify health, errors, latency, and running version
```

### 100. How do you demonstrate a claimed 40% pipeline-time improvement?

- **Approach:** Pseudocode: define the timing boundary and compare representative before/after runs using recorded stage durations.
- **Check:** Separate queue/approval delays from execution, include failures/variation, and attribute your work accurately; 10 to 6 minutes is illustrative.

```text
Define start/end and comparable run set → collect Jenkins stage timings
Compare before/after; identify changes and check reliability stayed acceptable
Reduction = (old - new) / old × 100; example: (10 - 6) / 10 × 100 = 40%
```

References: [Jenkins Pipeline syntax](https://www.jenkins.io/doc/book/pipeline/syntax/), [credentials](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#handling-credentials).

## 12. AWS — use and troubleshoot managed services

### 101. How do you confirm which AWS account and identity a command uses?

- **Approach:** Check caller identity and configured CLI sources before debugging or changing resources.
- **Check:** Confirm account, role, Region, and intended profile; a successful login to the wrong account is still the wrong context.

```bash
aws sts get-caller-identity
aws configure list
```

### 102. An EC2 instance is unreachable. Where do you start?

- **Approach:** Inspect instance and infrastructure status before checking routes, security groups, NACLs, and the OS listener.
- **Check:** Replace the example ID; passing status checks does not prove the application or SSH is healthy.

```bash
aws ec2 describe-instance-status --instance-ids i-0123456789abcdef0 --include-all-instances
aws ec2 describe-instances --instance-ids i-0123456789abcdef0
```

### 103. EC2 user data did not install the app. What do you inspect?

- **Approach:** On a cloud-init-based instance, inspect completion and bootstrap logs.
- **Check:** User-data execution depends on image/settings and is not guaranteed to rerun on every reboot; avoid logging credentials.

```bash
sudo cloud-init status --long
sudo tail -n 60 /var/log/cloud-init-output.log
```

### 104. An ALB returns errors even though the application process is running. What next?

- **Approach:** Pseudocode: check target health and the exact health-check request from the load balancer’s path.
- **Check:** Verify target port, protocol, path, success codes, security groups, and readiness; process existence is insufficient.

```text
Inspect target group health reason and registered targets
Test health path on target port; check ALB-to-target permissions
Compare ALB status/timing with backend logs and recent changes
```

### 105. An Auto Scaling Group keeps replacing instances. How do you investigate?

- **Approach:** Read scaling activities and compare the group’s health-check and launch configuration.
- **Check:** Bootstrap failures, bad health checks, quotas, or insufficient warm-up can create replacement loops.

```bash
aws autoscaling describe-scaling-activities --auto-scaling-group-name demo-api --max-records 10
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names demo-api
```

### 106. A Route 53 change seems ineffective. What do you compare?

- **Approach:** Query the authoritative server and the resolver used by the affected client; replace the sample authoritative name.
- **Check:** Check delegation, record type, alias target, TTL, and caches; one resolver’s answer does not prove all clients have updated.

```bash
dig @ns-123.awsdns-45.net api.example.com A
dig api.example.com A
```

### 107. An application gets S3 AccessDenied. What do you inspect?

- **Approach:** Confirm the actual identity and test the required object operation rather than assuming bucket listing is equivalent.
- **Check:** Inspect identity/bucket/endpoint policies and applicable denies; SSE-KMS reads may also need decryption permissions. Use a known non-sensitive lab object.

```bash
aws sts get-caller-identity
aws s3api head-object --bucket demo-artifacts --key health.txt
```

### 108. How do you recover an older version of an S3 object?

- **Approach:** List versions, then retrieve the chosen version into a separate recovery file.
- **Check:** The bucket must have retained that version and you need version-access permissions; writing it back as current is a separate reviewed operation.

```bash
aws s3api list-object-versions --bucket demo-artifacts --prefix config.json
aws s3api get-object --bucket demo-artifacts --key config.json --version-id VERSION_ID recovered-config.json
```

### 109. An EC2 application cannot use its intended IAM role. What do you check?

- **Approach:** Inspect the instance profile association and confirm the caller from the actual workload context.
- **Check:** Check SDK credential precedence and role policies; credentials in environment variables can override the expected instance role.

```bash
aws ec2 describe-iam-instance-profile-associations --filters Name=instance-id,Values=i-0123456789abcdef0
aws sts get-caller-identity
```

### 110. A Lambda function times out. How do you investigate?

- **Approach:** Inspect configured timeout, memory, networking, and logs for a bounded period.
- **Check:** Separate initialization, execution, and dependency waits; concurrency pressure and retries can worsen the symptom.

```bash
aws lambda get-function-configuration --function-name demo-api
aws logs tail /aws/lambda/demo-api --since 10m
```

### 111. API Gateway returns 5xx while Lambda works in a direct test. What next?

- **Approach:** Pseudocode: reproduce the actual request and inspect integration/access logs.
- **Check:** Check event format, integration permissions, response shape, and timeout differences; direct invocation bypasses parts of the API path.

```text
Call deployed API with the same method, path, headers, and payload
Inspect access/integration logs and correlated Lambda request
Check mapping, invoke permission, response format, and dependency timing
```

### 112. An ECS service cannot keep tasks running. What do you inspect?

- **Approach:** Read service events and locate stopped tasks, then inspect a selected task’s stopped reason and container exit details.
- **Check:** Image pull, task/execution roles, networking, health checks, and memory limits are different possible causes.

```bash
aws ecs describe-services --cluster demo --services api
aws ecs list-tasks --cluster demo --service-name api --desired-status STOPPED
aws ecs describe-tasks --cluster demo --tasks TASK_ARN
```

### 113. You cannot access an EKS cluster. How do you investigate?

- **Approach:** Confirm the AWS identity, update the intended kubeconfig context, then inspect nodes if authorized.
- **Check:** Check endpoint connectivity, cluster access configuration, and Kubernetes RBAC; AWS API access alone does not grant every Kubernetes permission.

```bash
aws sts get-caller-identity
aws eks update-kubeconfig --name demo-cluster --region eu-west-2
kubectl get nodes
```

### 114. A private application cannot connect to RDS. What do you check?

- **Approach:** Inspect database state/endpoint, then test TCP from the actual application network.
- **Check:** Check DNS, database port, routes, and security groups before database credentials; a successful TCP connection does not prove SQL authentication.

```bash
aws rds describe-db-instances --db-instance-identifier demo-db
nc -vz demo-db.example.eu-west-2.rds.amazonaws.com 5432
```

### 115. How would you restore an RDS backup safely?

- **Approach:** Pseudocode: restore to a new isolated DB, validate, then perform a controlled application cutover.
- **Check:** Restoration and DNS/secret changes take time; include data correctness, engine compatibility, and rollback in the exercise.

```text
Choose snapshot/time within available retention → restore new isolated DB
Validate schema, sample records, integrity, and application transactions
Measure recovery → approve endpoint/secret change → verify traffic
```

### 116. EC2 memory is missing from CloudWatch. How do you investigate?

- **Approach:** Pseudocode: confirm whether guest-memory collection was installed and configured.
- **Check:** Standard EC2 metrics do not automatically include guest memory; inspect agent permissions, collection configuration, namespace, and dimensions.

```text
Check CloudWatch agent installation, configuration, and service logs
Verify workload role allows publishing intended custom metrics
Query correct namespace/dimensions/time range for collected memory metric
```

### 117. How do you find who changed an AWS resource?

- **Approach:** Inspect CloudTrail events for the relevant resource and period.
- **Check:** Event history has scope/retention limits and does not include every data event by default; confirm the identity/session and exact action.

```bash
aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=demo-db --max-results 10
# Check event time, API action, identity, and requested changes.
```

### 118. An SQS worker falls behind. How do you investigate?

- **Approach:** Pseudocode: compare queue age/depth, consumer throughput, failures, and visibility timeout.
- **Check:** Add workers only if dependencies can handle the load; retries and duplicate processing can amplify work.

```text
Graph oldest-message age, visible/in-flight counts, and worker completions
Inspect failures, visibility timeout, processing duration, and DLQ
Fix bottleneck or scale with bounded concurrency; verify backlog drains
```

### 119. An encrypted object cannot be read despite S3 permission. What next?

- **Approach:** Identify encryption/key metadata and check the caller’s permissions and relevant key policy.
- **Check:** KMS permission is a separate requirement when applicable; an enabled key alone does not grant access.

```bash
aws s3api head-object --bucket demo-artifacts --key health.txt
aws kms describe-key --key-id KEY_ARN
```

### 120. How do you verify traffic uses a VPC endpoint as intended?

- **Approach:** Pseudocode: inspect endpoint type, route/DNS behaviour, service support, and policies.
- **Check:** Gateway and interface endpoints work differently; do not assume creating an endpoint automatically reroutes every existing connection.

```text
Identify endpoint type/service → inspect route tables or private DNS
Check endpoint policy, identity permissions, and applicable network controls
Test from workload context and use flow/service evidence to verify path
```

References: [AWS IAM practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html), [RDS recovery](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html), [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/).

## 13. Operational Python and Bash

### 121. How do you summarize errors from a JSON-lines log file?

- **Approach:** Parse each line and count matching records; this small example assumes every line is valid JSON.
- **Check:** A production script needs a policy for malformed lines, encoding, file size, and sensitive output; streaming avoids loading the whole log.

```python
import json
with open("app.jsonl") as logs:
    print(sum(json.loads(line).get("level") == "error" for line in logs))
```

### 122. How do you call an HTTP API with timeouts and status checks?

- **Approach:** Use a client timeout and fail on unsuccessful HTTP status before interpreting the response.
- **Check:** This requires the requests package; connect/read limits are not automatically a whole-workflow deadline, and JSON decoding can fail.

```python
import requests
response = requests.get("https://api.example.com/health", timeout=(3, 10))
response.raise_for_status(); print(response.json())
```

### 123. How do you list every page of AWS resources with Python?

- **Approach:** Use the SDK paginator instead of assuming the first response contains all resources.
- **Check:** Example uses boto3 with approved credentials/region; handle API failures and inspect the correct account before reporting inventory.

```python
import boto3
for page in boto3.client("ec2").get_paginator("describe_instances").paginate():
    print([i["InstanceId"] for r in page["Reservations"] for i in r["Instances"]])
```

### 124. How would you add safe retries to an operational script?

- **Approach:** Pseudocode: retry only suitable transient failures within bounded attempts and an overall deadline.
- **Check:** Do not retry auth/config errors blindly; side-effecting requests need idempotency or a reliable outcome check.

```text
Attempt request with timeout; return on success
For retryable failure: remaining budget? → backoff with jitter → retry
For permanent failure/exhausted budget: record context and exit nonzero
```

### 125. How do you run a command safely from Python?

- **Approach:** Pass an argument list and set a timeout plus explicit failure handling.
- **Check:** This avoids ordinary shell interpolation; validate user-controlled arguments and handle nonzero exits or timeout exceptions in real scripts.

```python
import subprocess
result = subprocess.run(["kubectl", "get", "pods", "-n", "demo"], capture_output=True, text=True, timeout=15, check=True)
print(result.stdout)
```

### 126. How do you make a small script accept explicit inputs?

- **Approach:** Use argparse to name required inputs and give users clear help.
- **Check:** Validate the resulting value before using it in file paths, cloud scope, or destructive operations.

```python
import argparse
parser = argparse.ArgumentParser(); parser.add_argument("--namespace", required=True)
args = parser.parse_args(); print(args.namespace)
```

### 127. How do you process a filename containing spaces in Bash?

- **Approach:** Quote path expansions and pass -- to tools that support it to separate options from filenames.
- **Check:** This protects ordinary splitting/globbing; avoid constructing command strings and passing them to eval.

```bash
log_file="/tmp/api logs.jsonl"
wc -l -- "$log_file"
```

### 128. How do you clean up temporary files after a shell script?

- **Approach:** Create a temporary file and register EXIT cleanup; Bash error controls do not replace explicit error handling.
- **Check:** SIGKILL/power failure bypass cleanup; keep secret data exposure and permissions in mind.

```bash
set -euo pipefail
tmp_file=$(mktemp)
trap 'rm -f -- "$tmp_file"' EXIT
```

### 129. How do you emit useful operational logs without leaking credentials?

- **Approach:** Record action, scope, outcome, and duration rather than tokens or full sensitive payloads.
- **Check:** Python logging needs handlers/format setup in a complete script; choose clear exit status for failures as well.

```python
import logging
logging.basicConfig(level=logging.INFO)
logging.info("action=inventory namespace=%s result=%s", "demo", "success")
```

### 130. How would you test an automation script before wider use?

- **Approach:** Pseudocode: separate parsing/decision logic from external effects and test both successes and failures.
- **Check:** Include malformed data, empty pages, throttling, timeouts, duplicates, and partial completion; mock tests do not replace a scoped integration test.

```text
Unit-test parsing/decisions with valid, missing, and malformed fields
Mock API pages and errors; verify retries, exit status, and secret redaction
Run read-only or dry-run in lab → review output → scoped integration test
```

References: [Python subprocess](https://docs.python.org/3/library/subprocess.html), [argparse](https://docs.python.org/3/library/argparse.html), [boto3 paginators](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html).

## 14. Git — collaborate without losing work

### 131. How do you create a reviewable infrastructure change?

- **Approach:** Start a branch from the intended base, make the change, and review the diff before committing.
- **Check:** A branch alone does not isolate cloud resources; use the correct backend/environment and include validation results in review.

```bash
git switch -c improve-api-config
git diff --check
git diff
```

### 132. How do you inspect exactly what will be committed?

- **Approach:** Review staged files and content separately from unstaged changes.
- **Check:** Check generated files, secrets, replacements, and unintended formatting churn before writing the commit.

```bash
git status --short
git diff --cached --stat
git diff --cached
```

### 133. How do you resolve a merge conflict?

- **Approach:** Inspect the conflicting files, preserve the intended behaviour from both changes, and test before completing the merge.
- **Check:** Do not remove conflict markers without understanding the changes; stage only the files you resolved.

```bash
git status
git diff --name-only --diff-filter=U
# Edit conflicts, test, git add resolved paths, then git merge --continue.
```

### 134. How do you undo a bad commit already shared with the team?

- **Approach:** Create a revert commit and review it through the normal process; the example variable identifies the actual bad commit.
- **Check:** Merge commits and dependent changes can need special handling; reverting application code does not undo database effects.

```bash
git show "$bad_commit"
git revert "$bad_commit"
```

### 135. How do you temporarily save local changes before switching tasks?

- **Approach:** Stash tracked and untracked work, then restore deliberately on the intended branch.
- **Check:** Stash does not replace remote backup; apply may conflict and deliberately keeps the stash until you remove it.

```bash
git stash push -u -m "pause local work"
git stash list
git stash apply
```

### 136. How do you bring one fix onto another branch?

- **Approach:** Inspect the commit, switch to the target branch, then cherry-pick it.
- **Check:** Check dependencies, resolve conflicts, and test; the new commit identity differs from the original.

```bash
git show "$fix_commit"
git switch release-demo
git cherry-pick "$fix_commit"
```

### 137. How do you inspect incoming changes before integrating them?

- **Approach:** Fetch without immediately modifying the working tree, then compare with the intended remote branch.
- **Check:** Choose merge or rebase according to team policy after reviewing history; avoid rewriting others’ shared work without coordination.

```bash
git fetch origin
git log --oneline HEAD..origin/main
git diff HEAD...origin/main
```

### 138. A secret was committed to Git. What do you do?

- **Approach:** Pseudocode: revoke/rotate first, then remove exposure and coordinate history cleanup where required.
- **Check:** Deleting a line or adding .gitignore does not remove history, copies, logs, or already compromised credentials.

```text
Revoke/rotate credential → identify affected access and audit activity
Remove tracked secret; coordinate repository/history cleanup as required
Update secret delivery and scanning; verify old credential no longer works
```

References: [Git revert](https://git-scm.com/docs/git-revert), [Git documentation](https://git-scm.com/docs).

## 15. Security, restore drills, and cost

### 139. How do you rotate a database secret without breaking the app?

- **Approach:** Pseudocode: prepare compatible credentials, update consumers safely, test, then retire old credentials.
- **Check:** Exact sequencing depends on database/rotation support and cached connections; protect a working recovery path.

```text
Create/enable replacement credential using supported rotation workflow
Update consumers → refresh connections → verify authenticated transactions
Retire old credential after confirmation; monitor failures and recovery path
```

### 140. How do you review least-privilege permissions?

- **Approach:** Pseudocode: map real operations to actions/resources and test the reduced policy in the intended context.
- **Check:** Explicit denies, trust, resource policies, boundaries, and organization rules can also affect the result; do not assume every denial is a missing allow.

```text
List required operations/resources → inspect observed activity and current policies
Create scoped allow/conditions → validate policy → test representative access
Verify unauthorized actions remain blocked; monitor regressions
```

### 141. How do you prove a backup is actually usable?

- **Approach:** Pseudocode: perform an isolated restore and application-level checks instead of relying only on a successful backup job.
- **Check:** Check integrity, data freshness, permissions/keys, and dependencies; record recovery duration and cleanup of the temporary environment.

```text
Restore retained backup into isolated test destination
Validate schema/files, sample records, integrity, and real transactions
Record usable recovery point + elapsed time → document findings and cleanup
```

### 142. How do you define and measure RTO and RPO?

- **Approach:** Pseudocode: define business targets before selecting recovery mechanisms and measure a complete drill.
- **Check:** RTO includes relevant detection, restore, configuration, and cutover; RPO concerns the age of recoverable data, not how long restore runs.

```text
Define tolerated outage (RTO) and data-loss window (RPO)
Record failure time, recovery-point time, and verified service-restoration time
Compare measured loss/downtime with targets and fix unmet dependencies
```

### 143. How do you investigate a sudden AWS bill increase?

- **Approach:** Pseudocode: compare spend by service/account/Region/time and correlate with deployments and usage.
- **Check:** Billing data can lag; review NAT/transfer, logs, snapshots, object versions, idle compute, and unexpected public exposure or misuse where supported by evidence.

```text
Cost Explorer: compare current period with comparable baseline
Break down service/Region/account/tags → inspect corresponding usage changes
Confirm owner and impact → apply scoped fix → verify subsequent spend trend
```

### 144. How do you decide whether an instance can be downsized?

- **Approach:** Pseudocode: profile representative peaks and constraints, then test a smaller option rather than deciding from average CPU.
- **Check:** Memory, disk/network throughput, burst credits, licensing, and availability requirements may dominate; retain rollback capacity.

```text
Collect peak/percentile CPU, memory, I/O, network, and latency over representative periods
Choose smaller compatible instance → load-test or canary with rollback ready
Verify errors, tails, headroom, and total cost before wider rollout
```

### 145. How do you configure useful budget monitoring?

- **Approach:** Pseudocode: define budgets and anomaly notifications with owners and thresholds.
- **Check:** Budget notifications do not universally stop spending; separately review any automated budget actions and their outage risk.

```text
Set account/service/environment budget with relevant cost scope
Configure actual/forecast alerts and tested owner notifications
Review anomalies and response procedure; confirm any action is explicitly configured
```

### 146. How do you safely reduce S3 retention costs?

- **Approach:** Inspect lifecycle rules and versioning first, then design changes using recovery and access requirements.
- **Check:** Expiry can permanently remove recoverable versions; archival transition may add restore delay/minimum-duration costs. The commands below only inspect.

```bash
aws s3api get-bucket-lifecycle-configuration --bucket demo-artifacts
aws s3api get-bucket-versioning --bucket demo-artifacts
```

### 147. How do you verify encryption and access controls together?

- **Approach:** Pseudocode: inspect storage encryption/key settings, TLS verification, and actual permitted/denied access.
- **Check:** Encryption does not replace authorization; losing the key can make encrypted backups unusable.

```text
Inspect encryption/key configuration and verify TLS certificate checks
Test intended role can access required data; unrelated identity cannot
Verify recovery includes key availability, policies, and audit evidence
```

### 148. How do you test availability across an AZ failure scenario?

- **Approach:** Pseudocode for a controlled lab: reduce one zone’s capacity and observe failover without risking production.
- **Check:** Check load-balancer health, spare capacity, database behaviour, and dependency placement; multiple replicas in one zone are insufficient.

```text
Map app/database/dependency placement across AZs and define success criteria
In isolated lab, simulate loss of one zone's app capacity → observe routing/scaling
Measure errors and recovery; verify database/dependencies and restore capacity
```

References: [AWS IAM practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html), [RDS restore guidance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html), [Well-Architected framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html).

## 16. Architecture and end-to-end exercises

### 149. How would you design a small highly available web application?

- **Approach:** Pseudocode: start with traffic, availability, data, and budget requirements, then select the simplest fitting design.
- **Check:** Explain each hop, failure boundary, access rule, and deployment/restore procedure rather than listing products.

```text
DNS → HTTPS load balancer → stateless app replicas across AZs
App → private database; scoped identities and explicit network access
Add health checks, scaling, telemetry, backups, and tested recovery
```

### 150. How would you choose EC2, ECS, EKS, or Lambda?

- **Approach:** Pseudocode: compare workload control, execution pattern, team skills, and operational responsibility.
- **Check:** No service is universally cheapest or simplest; account for constraints, idle/peak demand, portability, and support burden.

```text
VM/OS control needed? → consider EC2
Container orchestration needed? → compare ECS and Kubernetes/EKS requirements
Event-driven short-lived execution fits limits? → evaluate Lambda and dependency cost
```

### 151. How do you make an application safe to scale horizontally?

- **Approach:** Pseudocode: remove essential instance-local state and make shared dependencies capacity-aware.
- **Check:** Sessions, file writes, duplicate work, and database pools can break scaling even when the HTTP app starts successfully.

```text
Identify session/files/cache state → externalize required durable/shared state
Bound per-replica DB connections and work concurrency; design duplicate-safe operations
Add replica → test same user flows, balancing, errors, latency, and shutdown
```

### 152. How do you use a queue without repeatedly processing the same work?

- **Approach:** Pseudocode: make processing duplicate-safe and acknowledge only after the required effect is durable.
- **Check:** Visibility/acknowledgment settings depend on the queue; crashes between effect and acknowledgment need a consistent deduplication design.

```text
Receive message with unique operation ID → check durable processing state
Apply effect with appropriate transactional/deduplication protection
Acknowledge after success; bounded retries and DLQ for persistent failure
```

### 153. How would you introduce a cache safely?

- **Approach:** Pseudocode: define key/freshness rules and failure behaviour before choosing technology.
- **Check:** Measure hit ratio and backend load; avoid serving one user’s private content to another or allowing synchronized expiry to overload dependencies.

```text
Define safe cache key, TTL, invalidation, and authorization boundaries
On miss, fetch authoritative data with bounded load; cache eligible result
Test stale data, eviction, cache outage, and stampede behaviour
```

### 154. How do you plan a canary release with a rollback condition?

- **Approach:** Pseudocode: deploy an identifiable version to a small traffic share and compare against the old version.
- **Check:** Require enough representative traffic and compatible data changes; success thresholds and rollback ownership should exist before release.

```text
Deploy known digest to small traffic share; retain working version
Compare route-level errors, p95/p99, and key user outcomes
Promote gradually or revert desired state when predefined gates fail
```

### 155. How do you run a realistic capacity test?

- **Approach:** Pseudocode: use representative arrivals/data and increase load while tracking saturation and errors.
- **Check:** Closed-loop generators can hide queueing by slowing their own arrivals; choose a model fitting the real workload and report achieved load.

```text
Define workload, arrival/concurrency model, dataset, warm-up, and success criteria
Increase load in steps → measure achieved throughput, errors, p95/p99, and resource pressure
Find saturation and recovery behaviour; repeat controlled runs and report variation
```

### 156. What would your complete cloud-engineering lab demonstrate?

- **Approach:** Pseudocode: one reproducible system from provisioning to fault recovery, with documented cleanup.
- **Check:** Capture evidence of actual behaviour, not only green tool output; use isolated scoped resources and control cost.

```text
Versioned infra/config → reviewed plan → provision → build/test → deploy app
Add dashboards/alerts → run traffic → introduce one controlled fault → diagnose/restore
Verify requests/data → record timings and limits → clean up lab resources
```

## 17. Personal experience — defend the evidence

### 157. How do you explain the 40% deployment-time reduction convincingly?

- **Approach:** Pseudocode for your evidence card: use actual timing records and identify the changes you owned.
- **Check:** Do not invent per-change savings or claim linting inherently accelerates execution; distinguish end-to-end time from individual stage runtime.

```text
Define start/end; list comparable before/after runs and failed-run treatment
Show actual changes: multi-stage build, parallel tests, checks; identify personal ownership
Calculate reduction from recorded data; explain variability and team contribution
```

### 158. How do you explain the 35% incident-resolution improvement?

- **Approach:** Pseudocode: identify what incident-resolution metric the CV figure describes and how it was collected.
- **Check:** Credit the wider observability/process effort appropriately; one illustrative incident does not statistically prove the overall percentage.

```text
Define incident set, period, severity mix, and timing boundary from records
Explain your observability contribution plus one actual investigation
Show measurement and attribution limits; avoid claiming unsupported causality
```

### 159. How do you present the NGINX ingress upgrade as a real engineering story?

- **Approach:** Pseudocode: fill the version, config, test, and rollout details from your work records.
- **Check:** Name the exact controller distribution; do not substitute a generic sample upgrade or invented compatibility incident.

```text
Record actual old/new chart/controller versions and reason for upgrade
Explain changed settings, compatibility checks, route/TLS tests, and personal contribution
Describe actual rollout, verification, rollback preparation, and observed result
```

### 160. How do you distinguish implemented, demonstrated, and evaluated project claims?

- **Approach:** Pseudocode: prepare an evidence table for CloudGraph/CloudInferOps with code, runs, measurements, and limitations.
- **Check:** A live demo proves a path ran, not general correctness or production MTTR reduction; planned features need an explicit label.

```text
Implemented: point to working code/config and your ownership
Demonstrated/evaluated: identify scenario, dataset, baseline, metrics, and result
Planned/limited: state missing validation and the next test without claiming completion
```

## Rehearsal checklist

For each question, practise explaining **the first action, expected evidence, next step, and verification**. Commands and small fragments were checked for structure; they were not deployed against live clusters, cloud accounts, or servers. Complete configurations need their surrounding files, permissions, dependencies, and environment-specific values.

## How to use this guide

Read the definitions in files 01–05, then practise the scenarios in this guide. Explain your assumptions, the evidence you expect, and how you would verify the result. AWS commands assume the CLI, valid scoped credentials, a selected Region, and the named lab resources; mutating procedures are examples, not actions performed by this guide.
