# Prometheus + Grafana + Loki — definitions to remember

Short interview definitions: **term → function**. OpenTelemetry terms explain how the signals connect.

## Shared observability terms

- **Observability →** Understanding a system’s internal behaviour through signals such as metrics, logs, and traces.
- **Monitoring →** Watching known measurements and conditions to detect problems; observability supports investigating unexpected behaviour too.
- **Metric →** Numeric measurement over time, such as request count, CPU use, or latency distribution.
- **Log →** Record of an event with details and a timestamp, such as a failed database connection.
- **Trace →** Related spans showing the path of a request across operations and services.
- **Span →** One operation within a trace, with timing, attributes, and relationships to other work.
- **Trace ID →** Identifier connecting spans in one trace; recording it in logs helps link logs to traces.
- **Correlation →** Connecting signals using service, environment, time, request, or trace identifiers to investigate the same behaviour.
- **Instrumentation →** Application code or libraries emitting measurements, logs, or spans.
- **Telemetry →** Data emitted about system behaviour, including metrics, logs, and traces.
- **Latency →** Time taken for an operation; state whether you measure queueing, execution, or the complete request.
- **p50 / p95 / p99 →** Latencies below which approximately 50%, 95%, or 99% of observed requests fall; do not average percentiles across instances.
- **Throughput →** Work completed per unit time, such as requests per second.
- **Error ratio →** Failed requests divided by total requests over a chosen interval; define which statuses count as failures.
- **Saturation →** How close a resource or queue is to capacity, such as exhausted connection pools or a growing work queue.
- **RED / USE →** RED = rate, errors, duration for services; USE = utilization, saturation, errors for resources.
- **SLI / SLO / SLA →** SLI measures service behaviour; SLO sets a target; SLA is an agreement that may include consequences for missing commitments.
- **Error budget →** Allowed amount of failure under an SLO; a 99.9% availability target permits 0.1% unavailability for its defined window.
- **Runbook →** Short instructions explaining how to investigate and respond to an alert.

## Prometheus — collect, store, and query metrics

- **Prometheus →** Usually scrapes numeric metrics, stores time series, runs PromQL queries, and evaluates configured rules.
- **Metrics endpoint →** HTTP endpoint exposing measurements in a supported format, commonly `/metrics`.
- **Scrape →** Prometheus fetches measurements from a target; remember: pull the numbers.
- **Target →** Endpoint Prometheus is configured or discovers to scrape, such as an application instance.
- **Scrape interval →** How often a target is queried; shorter intervals improve resolution but increase overhead.
- **Service discovery →** Automatically finds scrape targets from an environment such as Kubernetes rather than maintaining every address manually.
- **Exporter →** Exposes measurements from another system in Prometheus format, such as node_exporter for host statistics.
- **Time series →** Timestamped samples identified by a metric name and a particular label set.
- **Label →** Key-value dimension distinguishing series, such as service or status code.
- **Cardinality →** Number of distinct series/label combinations; unbounded user IDs or raw paths can overload storage and queries.
- **Counter →** Value increasing with events until a reset; example: total requests since process startup.
- **Gauge →** Value that can increase or decrease; example: current active connections.
- **Histogram →** Records a distribution such as latency; classic histograms expose bucket counts, sum, and count.
- **Summary →** Records count and sum and may calculate quantiles in the application; those quantiles cannot generally be aggregated across instances.
- **PromQL →** Prometheus query language used to select and calculate values from time series.
- **rate() →** Estimates a counter’s average increase per second over a window, accounting for resets; use it before aggregation.
- **increase() →** Estimates a counter’s total increase over a window, accounting for resets and extrapolation; not always an exact integer count.
- **histogram_quantile() →** Estimates a quantile from a histogram; accuracy depends on the histogram’s resolution and sample distribution.
- **up metric →** Reports whether a target scrape succeeded; successful scraping does not prove the application is serving users correctly.
- **Recording rule →** Periodically evaluates a query and stores its result as another series for reuse.
- **Alerting rule →** Evaluates a condition and creates an alert when its criteria are met, optionally after a `for` duration.
- **Alertmanager →** Groups, deduplicates, routes, silences, and inhibits alerts before sending notifications.
- **Silence / inhibition →** Silence mutes matching alerts for a period; inhibition suppresses certain alerts when another relevant alert is active.
- **Retention →** How long or how much data is kept; local retention and remote storage can have different policies.
- **Remote write →** Sends metric samples to a configured remote storage endpoint.

## Grafana — visualize and investigate

- **Grafana →** Queries configured data sources and displays results in dashboards or Explore; it is not itself the usual metrics/log storage backend.
- **Data source →** Connection to a backend such as Prometheus for metrics or Loki for logs.
- **Panel →** One visualization, such as an error-rate graph, log view, or current-value display.
- **Dashboard →** Collection of panels giving an overview of a service or system.
- **Variable →** Reusable dashboard input such as environment or service, used to filter panel queries.
- **Time range →** Window shown by the dashboard; align it across signals when investigating an incident.
- **Explore →** Workspace for interactive queries and troubleshooting without first building a dashboard.
- **Annotation →** Marker on a time graph, such as a deployment or configuration change.
- **Provisioning →** Creates or manages supported Grafana configuration from files or automation for repeatability.
- **Grafana alerting →** Evaluates supported data-source queries and conditions and sends notifications through configured policies.
- **Contact point →** Notification destination/integration, such as email or a supported incident-management service.
- **Notification policy →** Routes and groups Grafana-managed alert notifications according to labels and configured rules.
- **No data / query error →** Conditions where an alert query returns no useful data or fails; explicitly configure handling rather than assume the service is healthy.

## Loki — collect, store, and query logs

- **Loki →** Log aggregation backend storing log data and indexing stream labels rather than every word in log messages.
- **Log collector →** Agent reading logs, adding metadata, and sending them to Loki; the actual collector depends on the deployment.
- **Log stream →** Group of log entries sharing the same label set, such as one service in one environment.
- **Loki labels →** Indexed metadata used to narrow log searches; keep labels bounded, such as service and namespace.
- **LogQL →** Loki query language for selecting, filtering, parsing, and calculating from logs.
- **Stream selector →** Selects streams by labels; example: `{service="api"}`.
- **Line filter →** Selects lines containing text; example: `{service="api"} |= "error"`.
- **Parser →** Extracts fields from log content, for example with a JSON parser, so queries can filter structured details.
- **Structured logs →** Logs with named fields such as level, message, and trace_id; easier to query than inconsistent free text.
- **Ingestion timestamp / event time →** Ingestion is when data arrives; event time is when the logged event occurred. Delays and clock differences affect correlation.
- **Log retention →** Policy controlling how long logs remain available; configure deletion and storage appropriately.
- **Log-derived metric →** A numeric result calculated from log entries, such as the rate of lines matching an error condition.
- **High-cardinality log labels →** Labels such as unique request IDs create many streams; keep those details in content or suitable metadata instead.

## OpenTelemetry — how the signals connect

- **OpenTelemetry →** APIs, SDKs, instrumentation, and tooling for generating and transporting telemetry; not a long-term storage backend.
- **SDK →** Application library configuring telemetry collection, processing, sampling, and export.
- **Collector →** Receives, processes, and exports telemetry to configured backends; it is separate from application instrumentation.
- **Receiver / processor / exporter →** Collector components accepting data / transforming or batching it / sending it onward.
- **Context propagation →** Carries trace context across calls, commonly through headers, connecting downstream spans to the same trace.
- **Sampling →** Retains selected traces to control cost; missing traces may reflect sampling rather than missing requests.
- **Trace backend →** Stores and queries traces; must be configured separately, such as Tempo or Jaeger where used.

## End-to-end memory flows

```text
METRICS: Application/exporter metrics endpoint → Prometheus scrapes and stores
         → Grafana queries Prometheus → metric panels

LOGS:    Application/container logs → configured collector → Loki stores
         → Grafana queries Loki → log panels or Explore

TRACES:  Instrumented application → optional OpenTelemetry Collector
         → configured trace backend → Grafana queries traces

ALERTS:  Prometheus alerting rules → Alertmanager → notifications
         Grafana alert rules → Grafana notification policies → contact points
```

Prometheus and Grafana alerting are separate paths; use clear ownership to avoid duplicate notifications. Exact pipelines depend on the configured integrations.

**Incident flow →** Alert → affected service and time window → Grafana metric graph → Loki logs → trace ID and trace backend → suspected cause → verify.

References: [Prometheus metric types](https://prometheus.io/docs/tutorials/understanding_metric_types/), [PromQL functions](https://prometheus.io/docs/prometheus/latest/querying/functions/), [Grafana introduction](https://grafana.com/docs/grafana/latest/introduction/), [Loki documentation](https://grafana.com/docs/loki/latest/), [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/).
