# Docker + Kubernetes + NGINX — definitions to remember

Short interview definitions: **term → function**, with examples where useful.

## Docker fundamentals

- **Docker →** Tools for building, distributing, and running containerized applications.
- **Docker Engine →** Daemon and APIs managing Docker images, containers, networks, and volumes; uses containerd internally.
- **Docker CLI →** Command-line client sending requests to Docker Engine; example: `docker ps` lists running containers.
- **Image →** Packaged filesystem and metadata containing an app and dependencies; a template for creating containers.
- **Container →** Instance of an image with an execution environment and writable layer; it can be running or stopped.
- **Dockerfile →** Build recipe containing instructions such as FROM, RUN, and COPY; the recipe is not itself the image.
- **FROM →** Selects a base image or begins a new build stage.
- **RUN →** Executes a command during image building; it does not run on every container start.
- **COPY / ADD →** COPY adds build-context files; ADD has extra features such as local archive extraction and supported remote sources.
- **CMD →** Default startup command or arguments, overridable when starting a container.
- **ENTRYPOINT →** Main startup executable, often combined with CMD for default arguments.
- **WORKDIR / ENV →** Set the working directory / environment values; ordinary ENV values are not a safe way to embed secrets.
- **EXPOSE →** Documents an intended container port; it does not publish that port to the host.
- **Image layer →** Reusable filesystem change forming part of an image; metadata-only instructions need not add filesystem content.
- **Build cache →** Reuses unchanged build work; changed inputs invalidate affected work and dependent steps.
- **Multi-stage build →** Build with full tooling in one stage, then copy only runtime outputs into a final stage.
- **.dockerignore →** Excludes unnecessary or sensitive files from the build context.
- **Registry →** Service storing and distributing images, such as a private registry or Docker Hub.
- **Tag / digest →** Tag is a movable readable label; digest identifies specific manifest content.
- **Writable layer →** Container-specific filesystem changes; removed when the container is removed.
- **Volume / bind mount →** Volume is storage managed through Docker; a bind mount exposes a selected host path.
- **Docker network →** Configures container connectivity; bridge networks are common for containers on one host.
- **Port publishing →** Maps a host port to a container port; `-p 8080:80` exposes container port 80 through host port 8080.
- **Docker Compose →** Describes and runs a multi-container application with services, networks, and volumes.
- **containerd →** Manages image and container lifecycle operations; used by Docker and commonly by Kubernetes.
- **CRI / OCI runtime →** CRI is kubelet’s runtime interface; an OCI runtime such as runc creates low-level container processes.

## Kubernetes access and control plane

- **kubectl →** Kubernetes CLI for creating, inspecting, updating, and deleting resources.
- **kubeconfig →** Stores cluster endpoints, credentials, and contexts for Kubernetes API access.
- **API server →** Receives API requests; authenticates, authorizes, and runs admission and validation before accepted state is persisted.
- **Authentication / authorization →** Authentication checks who you are; authorization checks what actions you may perform.
- **Admission controllers →** Modify or reject API requests according to cluster rules before storage.
- **etcd →** Consistent key-value store holding cluster state; not the application’s database.
- **Controller →** Compares desired with observed state and acts to reduce differences repeatedly.
- **Controller manager →** Runs core control loops such as Deployment, ReplicaSet, and node controllers.
- **Scheduler →** Chooses eligible nodes for unscheduled Pods using resources and placement constraints.
- **Cloud controller manager →** Connects Kubernetes to cloud-specific node, route, and load-balancer functionality where configured.
- **Cluster / node →** Cluster is the whole managed setup; a node is a physical or virtual machine participating in it.
- **Kubelet →** Node agent coordinating assigned containers, probes, and status reporting through the runtime and API.

## Workloads

- **Pod →** Smallest deployable unit; containers share networking and may share volumes, but do not automatically share every filesystem or process view.
- **Deployment →** Manages interchangeable replicas, versions, and rolling updates, commonly for stateless apps.
- **ReplicaSet →** Maintains the desired number of matching Pods; usually managed by a Deployment.
- **StatefulSet →** Provides stable Pod identities and storage associations; does not itself implement database replication or backups.
- **DaemonSet →** Runs a Pod on each eligible node, useful for networking or log-collection agents.
- **Job →** Runs work toward successful completion, such as a batch calculation.
- **CronJob →** Creates Jobs on a schedule; consider overlap, missed runs, and safe retries.
- **Init container →** Runs setup before application containers; regular init containers must finish successfully.
- **Sidecar →** Supporting container alongside an app, such as a proxy or telemetry helper.
- **Namespace →** Scopes and organizes resources; namespace separation alone is not a complete security boundary.

## Services and networking

- **Service →** Stable addressing and routing configuration for backends, commonly selecting Pods through labels.
- **ClusterIP →** Service type with a cluster-internal virtual IP; the default Service type.
- **NodePort →** Exposes a Service through a port on node addresses, subject to networking and access rules.
- **LoadBalancer →** Requests an external load balancer from the configured infrastructure integration.
- **Headless Service →** Service without a ClusterIP; DNS commonly returns backend addresses directly.
- **Ingress →** HTTP/HTTPS routing rules for hostnames and paths; requires a controller to implement them.
- **Ingress controller →** Watches routing resources and configures a proxy to forward incoming traffic to backends.
- **EndpointSlice →** Records Service backend addresses, ports, and endpoint conditions such as readiness.
- **Kube-proxy →** Watches Services and EndpointSlices and programs node forwarding rules; it usually does not relay every packet itself.
- **CNI →** Interface for configuring container networking; implementations supply Pod network connectivity.
- **Calico →** Networking implementation providing Pod connectivity and network-policy enforcement; details depend on the chosen configuration.
- **CoreDNS →** Common Kubernetes DNS server resolving Service names and forwarding other lookups.
- **NetworkPolicy →** Defines allowed Pod traffic; enforcement requires support from the networking implementation.
- **port / targetPort →** Service port is where clients connect; targetPort is the selected backend port.

## Health and configuration

- **Startup probe →** Checks initialization; delays configured readiness and liveness probes until success.
- **Readiness probe →** Checks whether the container is ready to serve; failure normally makes the Pod ineligible for regular Service traffic.
- **Liveness probe →** Checks container health; repeated failure can trigger that container’s restart.
- **Restart policy →** Controls restarts of terminated containers within a Pod; not the same as replacing the whole Pod.
- **ConfigMap →** Holds non-secret configuration delivered through environment variables or mounted files.
- **Secret →** Holds sensitive values; base64 encoding is not encryption, so storage protection and access controls matter.
- **ServiceAccount →** Identity for workloads interacting with the Kubernetes API or approved external identity integrations.
- **Role / ClusterRole →** Define permissions; Role is namespace-scoped, while ClusterRole can define permissions for broader use.
- **RoleBinding / ClusterRoleBinding →** Assign permissions to identities within a namespace / across the cluster respectively.
- **Labels / selectors →** Labels are identifying tags; selectors find resources matching those tags.
- **Annotations →** Additional metadata for information and tool configuration; not used like labels for ordinary selection.

## Storage

- **Volume →** Storage mounted into containers; durability and lifetime depend on its type.
- **emptyDir →** Pod-local temporary storage shared by containers; survives container restarts but is removed when the Pod leaves the node.
- **PV →** PersistentVolume: cluster resource representing storage capacity, access modes, and related properties.
- **PVC →** PersistentVolumeClaim: request for storage that binds to a suitable PV.
- **StorageClass →** Defines provisioning choices; can enable compatible claims to create storage dynamically.
- **CSI →** Standard interface integrating storage drivers with Kubernetes.
- **Access modes →** Describe mounting patterns such as ReadWriteOnce and ReadWriteMany; support depends on the storage driver/system.
- **Reclaim policy →** Determines how a PV is handled after its claim is released, commonly Retain or Delete.

## Resources, placement, and availability

- **Requests / limits →** Requests guide scheduling; CPU limits can throttle, while memory-limit enforcement can cause OOM kills.
- **HPA →** Horizontal Pod Autoscaler: adjusts replica count using configured metrics.
- **VPA →** Vertical Pod Autoscaler: additional component recommending or adjusting resource requests.
- **Cluster Autoscaler →** Adds or removes nodes using scheduling needs and configured infrastructure integration.
- **Metrics Server →** Provides recent CPU/memory usage for kubectl top and resource-based autoscaling; not a long-term monitoring store.
- **ResourceQuota →** Limits aggregate resource consumption or object counts in a namespace.
- **LimitRange →** Sets defaults and constraints for individual resource requests and limits within a namespace.
- **PodDisruptionBudget →** Constrains certain voluntary disruptions; does not prevent unexpected hardware or node failures.
- **Rolling update →** Gradually replaces old replicas while new replicas become ready.
- **maxSurge / maxUnavailable →** Deployment update settings controlling extra replicas / permitted unavailable replicas.
- **Taint / toleration →** Taints discourage or prevent placement; matching tolerations permit placement but do not guarantee it.
- **Node affinity →** Required or preferred node placement using node properties.
- **Pod affinity / anti-affinity →** Places Pods near / away from matching Pods using topology rules.

## Troubleshooting and deployment tools

- **Pending →** Pod setup is incomplete; inspect events for scheduling, image, or storage issues.
- **CrashLoopBackOff →** Container repeatedly exits, so Kubernetes delays further restart attempts.
- **ImagePullBackOff →** Image pulling fails and retries are delayed; check names, credentials, registry availability, and network access.
- **OOMKilled →** Container terminated by an out-of-memory mechanism; inspect usage, limits, and node conditions.
- **Eviction →** Removal of a Pod, for example because of node resource pressure or an explicit eviction request.
- **Events →** Resource-related messages explaining scheduling, pulls, restarts, and failures.
- **Helm →** Packages parameterized Kubernetes templates as charts; direct Helm use manages releases.
- **Kustomize →** Produces final YAML from existing manifests using bases, overlays, and patches.
- **Argo CD →** Compares declared configuration with live cluster state and synchronizes according to policy.

## NGINX fundamentals

- **NGINX →** Web server and reverse proxy that can serve files, forward requests, balance traffic, and terminate TLS.
- **Reverse proxy →** Receives client requests and forwards them to backends; remember: front desk for the application.
- **Static content →** Files served directly, such as images, CSS, and JavaScript, without calling an application backend.
- **Upstream →** Named group of backend servers used for proxying or load balancing.
- **Round-robin / least_conn →** Distribute requests in rotation / favor backends with fewer active connections; workload affects which works better.
- **Master / worker processes →** Master manages configuration and workers; workers handle connections and requests.
- **Event-driven I/O →** Workers react to ready connections instead of dedicating a blocking thread to each connection.
- **worker_processes / worker_connections →** Set worker count / per-worker connection ceiling; proxied requests also consume upstream connections.

## NGINX configuration

- **nginx.conf →** Main configuration file, often including additional files; actual paths depend on installation.
- **http block →** Contains HTTP-wide settings and HTTP virtual servers.
- **server block →** Defines a virtual server using listeners and hostname rules.
- **listen / server_name →** listen sets address/port; server_name matches the requested host among relevant virtual servers.
- **default_server →** Fallback server for a listener when no hostname rule matches; it is a listen setting.
- **location block →** Selects handling for a request URI, such as serving files or forwarding `/api/`.
- **Location matching →** Exact matches win; longest prefix and regex rules are then considered with modifiers such as `^~` affecting selection.
- **root / alias →** root appends the request URI to a filesystem path; alias replaces the matched location path.
- **try_files →** Checks candidate files/directories, then uses a configured fallback such as an internal redirect or status.
- **return / rewrite →** return sends a response or redirect; rewrite changes URI handling according to its rules.

## NGINX proxy behaviour

- **proxy_pass →** Forwards requests to an upstream address.
- **proxy_pass trailing slash →** In a simple prefix location, a URI such as `/` replaces the matched prefix; omitting a URI normally preserves the path.
- **proxy_set_header →** Sets a header sent to the backend, such as Host.
- **X-Forwarded-For / Proto →** Carry client-address chain / original scheme; trust them only from configured trusted proxies.
- **TLS termination →** NGINX handles client TLS; backend encryption is configured separately.
- **Upstream keepalive →** Reuses backend connections, reducing repeated setup work; configure suitable protocol and headers.
- **proxy_connect_timeout →** Limits opening the upstream connection.
- **proxy_read_timeout / send_timeout →** Limit gaps between upstream reads / writes, not the whole request’s duration.
- **Response buffering →** Holds backend response data temporarily; can help slow clients but affect streaming.
- **Proxy caching →** Reuses eligible backend responses; configure safe keys, expiry, and bypass rules for private data.

## NGINX troubleshooting and Kubernetes integration

- **Access log →** Records requests, statuses, and configured timings; useful for finding affected routes and slow responses.
- **Error log →** Records configuration, connection, and upstream failures; correlate with request and backend logs.
- **request_time / upstream_response_time →** Total request-handling time / upstream response time; compare to locate where delay accumulates.
- **502 Bad Gateway →** Proxy could not obtain a valid backend response; inspect upstream connection and response errors.
- **504 Gateway Timeout →** An upstream operation timed out; identify the timed-out step in logs.
- **499 →** NGINX log status indicating the client closed before the response completed.
- **nginx -t →** Validates configuration syntax and attempts to open referenced files; it does not test every backend or route.
- **nginx -T →** Also prints effective configuration; useful for includes, but output can contain sensitive configuration.
- **Graceful reload →** `nginx -s reload` requests new configuration; new workers start while old workers finish existing work.
- **NGINX ingress controller →** Watches Kubernetes resources and configures NGINX routing; exact annotations and behaviour depend on the controller implementation.
- **Ingress annotations →** Controller-specific metadata affecting routing or proxy settings; validate support before upgrades.
- **Ingress TLS Secret →** Kubernetes Secret supplying certificate/key material to a compatible controller; protect access and monitor expiry.
- **Controller ConfigMap →** Controller-supported global settings; different from an application’s ConfigMap and specific to the implementation.
- **Ingress upgrade →** Check exact controller/chart versions, compatibility, TLS/routes, metrics, and rollback before promoting the change.

## NGINX memory flows

```text
Standalone: client → listener/server match → location match
            → static file OR upstream application → response

Kubernetes configuration: Ingress/Service/EndpointSlice changes
                          → ingress controller → generated NGINX routing

Request: client → load balancer → NGINX ingress → application backend → response
```

The ingress may connect directly to Pod endpoints or use Service forwarding, depending on configuration. Manage controller-generated settings through supported Kubernetes resources rather than editing generated files.

**Safe configuration change →** validate (`nginx -t`) → graceful reload → test routes/TLS → check errors and latency.

References: [NGINX beginner’s guide](https://nginx.org/en/docs/beginners_guide.html), [request processing](https://nginx.org/en/docs/http/request_processing.html), [proxy directives](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).

## End-to-end memory flows

```text
kubectl → API server authenticates/authorizes/validates → accepted state in etcd
Deployment controller → ReplicaSet controller → Pod objects
Scheduler records node assignment → kubelet → containerd → runtime starts containers
Pod networking is set up through CNI; required storage is prepared before use
Readiness → Pod status → EndpointSlices → kube-proxy → Service forwarding rules
```

Controllers, scheduler, and kubelet exchange state through the API server; this is the logical sequence, not a chain of direct calls. Service forwarding is configured alongside workload execution.

```text
Typical request: client → load balancer → ingress controller
                → Service forwarding → eligible Pod → response
```

Some ingress controllers connect directly to Pod endpoints, and some clusters replace kube-proxy with another dataplane.

References: [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/), [Kubernetes components](https://kubernetes.io/docs/concepts/overview/components/), [Services](https://kubernetes.io/docs/concepts/services-networking/service/), [probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/).
