# Terraform + Ansible + Jenkins — definitions to remember

Short interview definitions: **term → function**, with examples where useful.

## Terraform — provision and manage infrastructure

- **Terraform →** Infrastructure-as-code tool describing desired resources and managing them through provider APIs. Example: create a network and virtual machines.
- **Infrastructure as Code (IaC) →** Manage infrastructure using versioned configuration so changes can be reviewed, repeated, and automated.
- **HCL →** Terraform’s configuration language, used in `.tf` files to describe resources, inputs, and expressions.
- **Provider →** Plugin translating Terraform operations into API calls for a platform such as AWS, Kubernetes, or GitHub.
- **Resource →** An object Terraform manages, such as a VM or bucket; a resource block describes its desired configuration.
- **Data source →** Reads information from a provider without declaring that object as a managed resource. Example: look up an existing image.
- **Input variable →** Parameter supplied to a configuration or module, such as region or instance size.
- **.tfvars →** File supplying variable values; keep real secrets out of committed variable files.
- **Local value →** Named expression reused within a module to reduce repetition; not an externally supplied input.
- **Output →** Exposes selected values from a module, such as a created server’s address.
- **Module →** Reusable group of Terraform configuration files; a root module can call child modules.
- **State →** Maps configured resource instances to real objects and records metadata; remember: Terraform’s ownership record.
- **Backend →** Configures where state is stored and related backend capabilities; a backend is different from a resource provider.
- **Remote state →** State stored in a shared backend, useful for team access; protect it because state can contain secrets.
- **State locking →** Prevents conflicting state-changing operations when the backend supports locking and it is configured appropriately.
- **Drift →** Real infrastructure differs from Terraform’s recorded or configured expectations, often after manual changes.
- **Dependency graph →** Determines operation ordering from resource references and explicit dependencies; independent work can run concurrently.
- **depends_on →** Declares a dependency that Terraform cannot infer from ordinary value references; use only when needed.
- **count / for_each →** Create multiple instances using numeric indexes / stable map keys or set values; key-based identity can simplify changes.
- **Lifecycle rules →** Customize resource lifecycle behaviour, such as create_before_destroy, prevent_destroy, and ignore_changes.
- **prevent_destroy →** Rejects a planned destruction while the lifecycle rule applies; removing the resource configuration also removes that protection.
- **ignore_changes →** Ignores selected attribute differences for update planning; useful for shared ownership but can hide unwanted drift.
- **Workspace →** Separate state instance for one configuration; CLI workspaces alone are not strong environment or permission isolation.
- **Import →** Adds an existing object’s binding to Terraform management; review configuration and plan before allowing subsequent changes.
- **Moved block →** Records an address change so Terraform can preserve a resource binding during refactoring instead of recreating it.
- **Sensitive value →** Redacts supported display output; marking a value sensitive does not automatically keep it out of state or encrypt it.
- **Provider lock file →** `.terraform.lock.hcl` records selected provider versions and checksums; it is different from a state lock.
- **Partial apply →** Some operations succeeded before others failed; inspect the error and current plan rather than assume everything was rolled back.
- **Rollback →** Usually restore a known-good configuration, inspect a new plan, then apply; Terraform has no universal undo for data or destructive changes.

## Terraform commands

- **terraform init →** Initializes the working directory, backend, modules, and provider installation; it does not provision the declared resources.
- **terraform fmt →** Formats configuration consistently; formatting alone does not validate the intended infrastructure.
- **terraform validate →** Checks configuration syntax and internal consistency; it does not prove remote permissions, quota, or deployment success.
- **terraform plan →** Proposes changes by comparing configuration with state and normally refreshed resource information; review replacements and deletions.
- **Saved plan →** `terraform plan -out=reviewed.plan` writes a plan that can later be applied; protect it because it may contain sensitive data.
- **terraform apply →** Executes planned changes and updates state; applying a reviewed saved plan avoids silently planning a different change set.
- **terraform destroy →** Plans and removes managed infrastructure in scope; it does not just delete the local state file.
- **terraform output →** Displays root-module outputs; explicit output commands can reveal sensitive values, so handle results carefully.
- **terraform state →** Commands for inspecting or deliberately changing state bindings; prefer supported commands over editing state JSON.
- **terraform state rm →** Makes Terraform forget a binding without deleting the real object; configuration left in place can propose a replacement later.

## Ansible — configure machines and orchestrate tasks

- **Ansible →** Automation tool for configuration and orchestration, such as installing packages, writing files, and managing services.
- **Agentless →** Typically connects through SSH on Linux or appropriate Windows transports without a persistent Ansible agent; target requirements still apply.
- **Control node →** Machine running Ansible and initiating automation against managed nodes.
- **Managed node →** Target machine or device Ansible configures; example: an application server.
- **Inventory →** Defines target hosts, groups, and connection information; answers “which machines?”
- **Static / dynamic inventory →** Static lists hosts explicitly; dynamic inventory plugins discover them from systems such as cloud APIs.
- **Host group →** Named set of inventory hosts, such as webservers, used for targeting and shared variables.
- **Playbook →** YAML file containing plays that describe automation; remember: the overall recipe.
- **Play →** Maps a set of tasks and settings to selected hosts; a playbook can contain several plays.
- **Task →** One action invoking a module, such as ensuring a package is installed.
- **Module →** Reusable unit performing an action, such as package, template, or service management.
- **Collection →** Package distributing Ansible content such as modules, plugins, and roles.
- **Role →** Reusable organization of tasks, handlers, variables, and files; example: an nginx role.
- **Idempotency →** Repeated execution leaves the same intended state when nothing has changed; module choice and task design determine this.
- **Variables →** Values customizing automation, such as application port or package version; precedence determines which value wins.
- **group_vars / host_vars →** Conventional locations for variables shared by a host group / specific to a host.
- **Facts →** Information gathered or set about hosts, such as OS family and network addresses; available facts depend on collection settings.
- **Gather facts →** Collects host information, commonly through the setup module; can be disabled or limited when unnecessary.
- **Jinja2 template →** File with expressions replaced by variable values; useful for generating an nginx.conf for each environment.
- **Handler →** Task normally triggered when a notifying task reports a change; multiple notifications usually run it once at the relevant flush point.
- **notify →** Names a handler to trigger after a changed task; example: a changed config notifies an NGINX reload handler.
- **become →** Privilege escalation for tasks needing another user’s permissions, commonly sudo to root.
- **when →** Conditional deciding whether a task runs; example: install a package only on a matching OS family.
- **loop →** Repeats a task over items, such as a list of packages or users.
- **register →** Stores a task’s result in a variable for later decisions or reporting.
- **changed_when / failed_when →** Customize whether a task reports a change or failure; useful for accurately interpreting command results.
- **Tags →** Labels allowing selected tasks to be included or skipped during a run.
- **Ansible Vault →** Encrypts supported files or values used by Ansible; different from HashiCorp Vault, which is a separate secret-management service.
- **no_log →** Suppresses task output containing sensitive data; it does not replace encryption or secure handling elsewhere.
- **Check mode →** `--check` predicts changes where modules support it; it is not a guarantee that a real run will succeed or have no side effects.
- **Diff mode →** `--diff` shows supported before/after changes; avoid exposing secret file contents in logs.
- **Ad hoc command →** Runs a simple module action without writing a playbook; example: test connectivity with the ping module.
- **Ansible ping →** Checks Ansible connectivity and required execution support; it is not an ICMP network ping.
- **command / shell →** command executes without normal shell interpretation; shell supports pipes and redirection but needs careful quoting and idempotency design.
- **serial →** Runs a play in batches of hosts, useful for gradual configuration changes rather than updating every server together.
- **Delegation →** Runs a task on a different host, such as performing a load-balancer action from the control node.
- **Block / rescue / always →** Groups tasks, handles eligible failures, and performs cleanup; rescue does not automatically undo earlier changes.
- **ansible-playbook →** Command running a playbook; example: `ansible-playbook -i inventory.ini site.yml`.

## Jenkins — automate build, test, and delivery

- **Jenkins →** Automation server coordinating jobs for building, testing, packaging, and delivering software.
- **CI →** Continuous Integration: frequently integrate code and automatically validate it with builds and tests.
- **Continuous delivery / deployment →** Delivery keeps changes ready for release; deployment automatically releases qualifying changes to the target environment.
- **Controller →** Schedules work, manages configuration, and coordinates jobs; builds are usually assigned to agents.
- **Agent →** Machine or execution environment performing assigned build work and requiring the relevant tools.
- **Executor →** Execution slot on a Jenkins node; more executors allow more concurrent work but also increase resource contention.
- **Job →** Configured unit of automation, such as a Pipeline or a traditional freestyle project.
- **Build / run →** One execution of a job with its own status, logs, and outputs.
- **Pipeline →** Workflow defined as code, describing stages and steps for automation.
- **Jenkinsfile →** Pipeline definition stored with the source code so changes can be versioned and reviewed.
- **Declarative Pipeline →** Structured Pipeline syntax using blocks such as pipeline, agent, stages, and post.
- **Scripted Pipeline →** Groovy-based Pipeline syntax allowing flexible control flow; Declarative can also use script blocks where needed.
- **agent directive →** Selects where Pipeline work executes, such as a node with a matching label or a configured container environment.
- **Stage →** Named phase such as Checkout, Test, Build, or Publish; makes progress and failures easier to locate.
- **Step →** Individual action inside a Pipeline, such as checkout, sh, or publishing a report.
- **SCM checkout →** Fetches the source revision used by a run; associate built artifacts with the exact commit.
- **Webhook →** Event notification from a system such as Git hosting that can trigger Jenkins work.
- **Multibranch Pipeline →** Discovers configured branches or pull requests containing a Jenkinsfile and manages their Pipeline jobs.
- **Credentials store →** Stores secrets referenced by ID; permissions and trust controls still determine who can use them.
- **withCredentials →** Makes selected credentials available within a Pipeline scope; log masking cannot protect against malicious trusted code.
- **Shared library →** Reusable Pipeline functions or classes used across repositories; version and review changes because many jobs may depend on them.
- **parallel →** Runs independent branches of work concurrently; isolate shared resources and verify enough agent capacity exists.
- **Workspace →** Working directory holding checked-out code and intermediate files; reused workspaces may retain stale data unless managed.
- **Artifact →** Build output such as an image, binary, or report; releases need identifiable versions and durable storage.
- **stash / unstash →** Temporarily transfers files between stages or agents within the same Pipeline run.
- **archiveArtifacts →** Retains selected build outputs for later retrieval, subject to configured retention and storage.
- **Test report →** Structured test results published for inspection, commonly using the junit step for supported report files.
- **post →** Actions after Pipeline or stage execution according to conditions, such as always or failure; useful for reports and cleanup.
- **timeout →** Bounds how long a block may run, helping prevent indefinitely stuck builds.
- **retry →** Repeats a block a limited number of times; use for suitable transient failures, not to conceal persistent test or product failures.
- **input →** Pauses a Pipeline for human input or approval where the delivery process requires it.
- **when →** Condition controlling whether a Declarative stage runs, such as publishing only from main.
- **Build queue →** Jobs waiting for suitable capacity or constraints; inspect labels, offline agents, executors, and concurrency limits.
- **disableConcurrentBuilds →** Prevents overlapping runs of the same Pipeline job; does not automatically coordinate different jobs sharing an environment.
- **parameters / environment →** Parameters are run inputs; environment supplies process variables. Ordinary variables are not a substitute for secret storage.
- **Build retention →** Policy controlling how long runs and artifacts remain available; balance audit needs with storage use.
- **Image digest →** Content identifier for a published image; promoting the same digest avoids rebuilding different artifacts between environments.
- **Deployment verification →** Checks rollout, exact version, application requests, errors, and latency; a green Jenkins run alone does not prove service health.
- **Rollback →** Restores a known-good application/configuration when possible; databases and external effects may need a separate recovery procedure.
- **GitOps handoff →** Jenkins builds/tests/publishes and updates reviewed Git configuration; Argo CD reconciles the cluster when it owns deployment.

## How the tools fit together

| Tool | Main responsibility | Simple example |
| --- | --- | --- |
| Terraform | Provision and manage infrastructure | Create network and servers |
| Ansible | Configure hosts and orchestrate tasks | Install NGINX and write its configuration |
| Jenkins | Coordinate automated workflows | Run checks, tests, builds, and release steps |

Their capabilities overlap. Assign clear ownership rather than letting several tools manage the same resource independently.

## Memory flows

```text
TERRAFORM: configuration → init → fmt/validate → plan → review → apply → verify
           Provider calls infrastructure APIs; state records managed object bindings.

ANSIBLE:   inventory + playbook → control node connects → tasks/modules run
           → changed tasks notify handlers → verify resulting configuration

JENKINS:   Git event → queued run → suitable agent → checkout → checks/tests
           → build → publish versioned artifact → deploy or GitOps handoff → verify
```

**Combined example →** Jenkins runs a reviewed Terraform workflow to create servers, then Ansible configures them, and application delivery uses the resulting environment. This is one possible design, not a requirement that every deployment rerun every tool.

**Remember →** Terraform builds the infrastructure; Ansible configures it; Jenkins coordinates the workflow.

## Official references

- [Terraform language](https://developer.hashicorp.com/terraform/language)
- [Terraform state](https://developer.hashicorp.com/terraform/language/state)
- [Terraform CLI](https://developer.hashicorp.com/terraform/cli/commands)
- [Ansible playbooks](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)
- [Ansible inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html)
- [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- [Jenkins Pipeline syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
