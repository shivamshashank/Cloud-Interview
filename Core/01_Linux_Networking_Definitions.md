# Linux + Networking — definitions to remember

Short interview definitions: **term → function**, with examples where useful.

## Linux fundamentals

- **Linux →** An operating-system family built around the Linux kernel; distributions package it with tools and services.
- **Kernel →** Manages CPU, memory, devices, and system calls. Think: the operating system’s resource manager.
- **Shell →** Command interpreter that runs commands and scripts, such as Bash or Zsh.
- **Terminal →** Interface through which you interact with a shell; the terminal and shell are different components.
- **Process →** A running program instance with its own virtual address space and process ID.
- **Thread →** Execution unit inside a process; threads share process memory and open files but have their own stacks.
- **PID / PPID →** Process ID and parent process ID; identify a process and the process that created it.
- **System call →** Controlled request from a program to the kernel, such as read, write, or opening a socket.
- **Context switch →** CPU changes which thread or process it runs, saving and restoring execution state; this introduces overhead.
- **Scheduler →** Kernel component choosing which runnable task gets CPU time; different from the Kubernetes node scheduler.
- **Daemon →** A background service process, such as an SSH server.
- **systemd →** Service manager on many Linux systems; manages startup, dependencies, and service supervision.
- **systemctl →** Tool for inspecting and controlling systemd services; example: `systemctl status nginx`.
- **journalctl →** Tool for reading systemd journal logs; example: `journalctl -u nginx`.
- **Environment variable →** A named value supplied to a process, such as PATH; child processes can inherit exported values.
- **PATH →** Directories the shell searches for executable commands when you do not give an explicit path.

## Memory and resources

- **Virtual memory →** Each process’s address-space view, mapped by the kernel to physical memory or backing storage.
- **Page →** A fixed-size unit used for memory management; page sizes depend on the system and configuration.
- **Page fault →** Memory access needs kernel handling, such as creating a mapping or loading a page; not always an error.
- **RSS →** Resident Set Size: process pages currently in physical memory; shared pages can appear in multiple processes’ RSS.
- **Page cache →** RAM used to cache file data, making repeated reads faster; much of it can be reclaimed when needed.
- **Swap →** Backing storage used to move certain memory pages out of RAM; heavy swapping can increase latency.
- **OOM killer →** Kernel mechanism that can terminate a process when memory cannot be satisfied; container limits can trigger local OOM handling.
- **Namespace →** Isolates a process’s view of resources such as process IDs, networks, and mount points.
- **Cgroup →** Accounts for and constrains resources for groups of processes; remember: namespace = view, cgroup = budget.
- **CPU throttling →** A task is prevented from using more CPU time than its configured allowance, potentially increasing latency.
- **Load average →** Average runnable and certain uninterruptible-wait tasks over 1, 5, and 15 minutes; high load does not always mean high CPU.
- **Mutex →** Lock protecting a shared section of work so concurrent threads do not modify it unsafely.
- **Atomic operation →** An indivisible operation on a value; it does not automatically make a multi-step workflow safe.
- **Race condition →** Correctness depends on the timing of concurrent operations; example: unsynchronized updates lose a counter increment.
- **Deadlock →** Tasks wait on one another in a cycle and cannot progress; consistent lock ordering can help prevent it.

## Files, permissions, and process communication

- **File descriptor →** Process-local number referring to an open file, socket, or pipe; 0, 1, and 2 normally mean stdin, stdout, and stderr.
- **Inode →** Stores file metadata and references to data; the filename is stored separately in a directory.
- **Hard link →** Another directory entry for the same inode; removing one name does not remove data while another link remains.
- **Symbolic link →** A file pointing to another path; it can become broken if the target path disappears.
- **Mount →** Makes a filesystem available at a directory in the filesystem tree.
- **File permissions →** Read, write, and execute permissions for owner, group, and others; directory execute permission allows traversal.
- **chmod / chown →** Change permissions / ownership; example: `chmod 600 secret.txt` grants the owner read/write only.
- **sudo →** Runs an authorized command as another user, commonly root; permissions come from sudo policy.
- **Pipe →** Connects one command’s standard output to another’s standard input; example: `ps aux` piped to `head`.
- **Redirection →** Sends output to a file or input from a file; `>` overwrites and `>>` appends.
- **Signal →** Notification to a process, used for events or termination requests.
- **SIGTERM / SIGKILL →** TERM requests termination and allows handling; KILL forces termination and cannot be caught.
- **Socket →** Endpoint for communication, locally or over a network; programs access sockets using file descriptors.
- **epoll →** Linux facility reporting readiness events for many file descriptors; useful for event-driven network servers.

## Linux troubleshooting tools

- **ps / top →** Show processes; top provides a live view of activity and resource consumption.
- **free →** Summarizes memory and swap; consider available memory and cache rather than only the free column.
- **df / du →** df reports filesystem space; du estimates file usage. Deleted files held open can explain differences.
- **lsof →** Lists open files and sockets; `lsof +L1` helps find deleted files still held open.
- **vmstat →** Reports system activity such as runnable tasks, memory, swapping, and CPU states.
- **iostat →** Reports storage activity and latency-related statistics; interpret queues and workload, not just utilization.
- **strace →** Shows system calls and signals; useful for failures or waits involving files, sockets, and kernel operations.
- **perf →** Linux performance-analysis tools for CPU sampling and counters; capabilities depend on permissions and hardware.
- **ss →** Shows sockets and listeners; `ss -lnt` lists listening TCP sockets.
- **ip addr / ip route →** Inspect interface addresses / routing tables on Linux.
- **curl →** Tests HTTP endpoints and connection behaviour; `curl -v` shows connection, TLS, and HTTP details.
- **tcpdump →** Captures packets for investigating traffic, handshakes, resets, and retransmissions.

## Networking fundamentals

- **IP address →** Logical address assigned to a network interface, used to route packets.
- **MAC address →** Link-layer address used for local frame delivery; remote traffic uses the next hop’s MAC, not the remote server’s MAC.
- **Port →** Number identifying a TCP or UDP application endpoint; HTTPS commonly uses TCP port 443.
- **DNS →** Resolves names into records, including addresses; remember: name → address.
- **Subnet →** Logical IP address range defined by a network prefix; a network neighbourhood.
- **CIDR →** Slash notation describing network-prefix length; IPv4 /26 contains 64 total addresses, with usable counts depending on the environment.
- **Router →** Forwards packets between networks using routes; remember: between networks.
- **Switch →** Typically forwards Ethernet frames within a local network using MAC addresses; remember: local delivery.
- **Default gateway →** Next-hop router used for destinations matched by the default route.
- **Route table →** Rules choosing the next hop for destination prefixes; the longest matching prefix normally wins.
- **TCP →** Reliable ordered byte stream with flow and congestion control; it does not preserve application message boundaries.
- **UDP →** Sends datagrams without built-in delivery or ordering guarantees; protocols above it can add reliability.
- **TCP handshake →** SYN → SYN-ACK → ACK establishes TCP connection state before normal data transfer.
- **TLS →** Encrypts traffic, protects integrity, and authenticates the server, optionally the client; HTTPS uses TLS.
- **HTTP / HTTPS →** HTTP carries web requests and responses; HTTPS protects that exchange with TLS.
- **ARP / NDP →** ARP resolves local IPv4 neighbors to link-layer addresses; IPv6 uses Neighbor Discovery instead.
- **MTU →** Maximum packet size supported by a link at its layer; path-MTU problems can make large transfers stall.
- **Latency / bandwidth / throughput →** Latency = delay; bandwidth = capacity; throughput = achieved transfer or processing rate.
- **Packet loss →** Packets fail to reach their destination; can trigger retransmissions or lost application data depending on the protocol.
- **Flow / congestion control →** Flow control protects receiver capacity; congestion control adjusts sending to network conditions.
- **TIME_WAIT →** Normal TCP state after active close that helps handle delayed packets from an old connection.

## Cloud networks and Linux packet handling

- **VPS →** Virtual Private Server: a virtual machine with its own OS and allocated resources on shared hardware. VPS = computer.
- **VPC →** Virtual Private Cloud: logically isolated cloud network with subnets, routes, and access controls. VPC = network.
- **Internet gateway →** In AWS, connects a VPC to the internet; resources also need appropriate routes, addresses, and security rules.
- **Public / private subnet →** In AWS, public has a direct route to an internet gateway; private does not. Routing alone does not grant access.
- **Public NAT gateway →** Lets private resources initiate internet connections and receive replies without unsolicited inbound connections through it.
- **NAT →** Translates packet IP addresses and sometimes ports; it is not a firewall by itself.
- **SNAT / DNAT →** Source NAT changes the sender address; destination NAT changes the destination, often for port forwarding.
- **Firewall →** Allows or blocks traffic using rules such as address, port, protocol, or connection state.
- **Netfilter →** Linux kernel framework for packet filtering, NAT, connection tracking, and related packet processing.
- **iptables →** Command-line tool configuring Linux packet rules; the kernel processes the packets.
- **INPUT / OUTPUT / FORWARD →** iptables chains for traffic to this host / generated by this host / passing through this host.
- **PREROUTING / POSTROUTING →** Netfilter hooks before route selection / after routing; commonly used for destination / source NAT.
- **Conntrack →** Tracks network flows so stateful rules and NAT can recognize replies and related connection state.
- **nftables →** Linux packet-filtering framework and tooling succeeding the legacy iptables framework; deployed backends vary.
- **Security group →** AWS interface/resource-associated allow rules; stateful, so replies to allowed traffic are automatically permitted.
- **Network ACL →** AWS subnet-boundary filter with allow/deny rules; stateless, so both directions require suitable rules.
- **VPN →** Protected tunnel across another network, useful for accessing private resources remotely.
- **Bastion host →** Hardened administrative entry point used to reach private servers.
- **Reverse proxy →** Receives client requests, forwards them to backends, and returns responses; NGINX is an example.
- **Load balancer →** Distributes traffic among backend instances; one component can also be a reverse proxy.
- **502 / 504 / 499 →** At NGINX: upstream response failure / upstream timeout / client closed early, respectively; inspect logs for the cause.

## Memory flows

```text
Private IPv4 server → public NAT gateway → internet gateway → internet
Client → reverse proxy/load balancer → application → response
```

Routes choose the path; access controls decide what traffic is allowed.

References: [Linux manuals](https://man7.org/linux/man-pages/), [Netfilter](https://www.netfilter.org/), [AWS NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html), [AWS VPC](https://aws.amazon.com/vpc/faqs/).
