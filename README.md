# What does Splunk Connect for Kubernetes do?

Splunk Connect for Kubernetes provides a way to import and search your Kubernetes logging, object, and metrics data in your Splunk platform deployment.  Splunk Connect for Kubernetes supports importing and searching your container logs on the following technologies:


* [Amazon Web Services (AWS) Elastic Container Service (ECS) and AWS Fargate, using Firelens.](https://github.com/splunk/splunk-connect-for-kubernetes/tree/develop/firelens) 
* Amazon Elastic Kubernetes Service (Amazon EKS)
* Azure Kubernetes Service (AKS)
* Google Kubernetes Engine (GKE)
* Openshift


Splunk Inc. is a proud contributor to the Cloud Native Computing Foundation (CNCF). Splunk Connect for Kubernetes utilizes and supports multiple CNCF components in the development of these tools to get data into Splunk.


## Prerequisites

* Splunk Enterprise 7.0 or later
* An HEC token. See the following topics for more information:
  * http://docs.splunk.com/Documentation/Splunk/7.2.4/Data/UsetheHTTPEventCollector
  * http://docs.splunk.com/Documentation/Splunk/7.2.4/Data/ScaleHTTPEventCollector
* You should be familiar with your Kubernetes configuration and know where your log information is collected in your Kubernetes deployment.
* Administrator access to your Kubernetes cluster.
* To install using Helm (best practice), verify you are running Helm in your Kubernetes configuration. See https://github.com/kubernetes/helm for more information.
* A minimum of two Splunk platform indexes ready to collect the log data. One for both logs and Kubernetes objects, and one for metrics. You can also create separate indexes for logs and objects, but you will need three Splunk platform indexes.

## Before you begin
Splunk Connect for Kubernetes supports installation using Helm. Read the Prerequisites and Installation and Deployment documentation before you start your deployment of Splunk Connect for Kubernetes.

Perform the following steps before you install:

1. Create a minimum of two Splunk platform indexes:
* One events index, which will handle logs and objects (you may also create two separate indexes for logs and objects).
* One metrics index.
If you do not configure these indexes, Kubernetes Connect for Splunk uses the defaults created in your HTTP Event Collector (HEC) token.

2. Create a HEC token if you do not already have one. If you are installing the connector on Splunk Cloud, file a ticket with Splunk Customer Service and they will deploy the indexes for your environment, and generate your HEC token.

## Deploy with Helm

Helm, maintained by the CNCF, allows the Kubernetes administrator to install, upgrade, and manage the applications running in their Kubernetes clusters.  For more information on how to use and configure Helm Charts,  see the Helm [site](https://helm.sh/) and [repository](https://github.com/kubernetes/helm) for tutorials and product documentation. Helm is the only method that the Splunk software supports for installing Splunk Connect for Kubernetes.

To install and configure defaults with Helm:

* Add Splunk chart repo 
```bash
helm repo add splunk https://splunk.github.io/splunk-connect-for-kubernetes/
```

* Get values file in your working directory 

Helm 2
```bash
helm inspect values splunk/splunk-connect-for-kubernetes > values.yaml
```
Helm 3
```bash
helm show values splunk/splunk-connect-for-kubernetes > values.yaml
```

* Prepare this Values file. Once you have a Values file, you can simply install the chart with by running

Helm 2
```bash
helm install --name my-splunk-connect -f my_values.yaml splunk/splunk-connect-for-kubernetes
```
Helm 3
```bash
helm install my-splunk-connect -f my_values.yaml splunk/splunk-connect-for-kubernetes

```

To learn more about using and modifying charts, see:
* https://github.com/splunk/splunk-connect-for-kubernetes/tree/main/helm-chart
* https://docs.helm.sh/using_helm/#using-helm.

## Configuration variables for Helm

To learn more about using and modifying charts, see:
* [The values file for logging](https://github.com/splunk/splunk-connect-for-kubernetes/blob/main/helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-logging/values.yaml)
* [The values file for metrics](https://github.com/splunk/splunk-connect-for-kubernetes/blob/main/helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-metrics/values.yaml)
* [The values file for objects](https://github.com/splunk/splunk-connect-for-kubernetes/blob/main/helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-objects/values.yaml)

## Deploy using YAML (unsupported)

> Only deploying by Helm is supported by Splunk.

You can grab the manifest YAML files and use them to create the Kubernetes objects needed to deploy Splunk Connect for Kubernetes. Please note that installation and debugging for Splunk Connect for Kubernetes through YAML is community-supported only.

When you use YAML to deploy Splunk Connect for Kubernetes, the installation does not create the default configuration that is created when you install using Helm. To deploy the connector using YAML, you must know how to configure your Kubernetes variables to work with the connector. If you are not familiar with this process, we recommend that you use the Helm installation method.

To configure the Splunk Connector for Kubernetes using YAML files:

1. Grab the Charts and Manifest files from https://github.com/splunk/splunk-connect-for-kubernetes

2. Read through all YAML files in the Manifests folder and make any necessary changes. Note that the YAML files in the Manifests folder are examples and are not expected to be used as provided.

3. Verify that your Kubernetes logs are recognized by the Splunk Connect for Kubernetes.

# Architecture

Splunk Connect for Kubernetes deploys a DaemonSet on each node. And in the DaemonSet, a Fluentd container runs and does the collecting job. Splunk Connector for Kubernetes collects three types of data:

* Logs: Splunk Connect for Kubernetes collects two types of logs:
  * Logs from Kubernetes system components (https://kubernetes.io/docs/concepts/overview/components/)
  * Applications (container) logs
* [Objects](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)
* Metrics

To collect the data, Splunk leverages:

* [Fluentd](https://www.fluentd.org/)
* [JQ plugin](https://rubygems.org/gems/fluent-plugin-jq) for transforming data
* [Splunk HEC output plug-in](https://github.com/splunk/fluent-plugin-splunk-hec): The [HTTP Event Collector](http://dev.splunk.com/view/event-collector/SP-CAAAE6M) collects all data sent to Splunk for indexing.
* For Splunk Connect for Kubernetes, Splunk uses the [node logging agent](https://kubernetes.io/docs/concepts/cluster-administration/logging/#using-a-node-logging-agent) method. See the [Kubernetes Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/) for an overview of the types of Kubernetes logs from which you may wish to collect data as well as information on how to set up those logs.

## Logs

Splunk Connect for Kubernetes uses the Kubernetes [node logging agent](https://kubernetes.io/docs/concepts/cluster-administration/logging/#using-a-node-logging-agent) to collect logs. Splunk deploys a DaemonSet on each of these nodes. Each DaemonSet holds a Fluentd container to collect the data. The following plugins are enabled in that Fluentd container:

* [in_systemd](https://rubygems.org/gems/fluent-plugin-systemd) reads logs from systemd journal if systemd is available on the host.
* [in_tail](https://docs.fluentd.org/v1.0/articles/in_tail) reads logs from file system.
* [filter_jq_transformer](https://rubygems.org/gems/fluent-plugin-jq) transforms the raw events to a Splunk-friendly format and generates source and sourcetypes.
* [out_splunk_hec](https://github.com/splunk/fluent-plugin-splunk-hec) sends the translated logs to your Splunk platform indexes through the HTTP Event Collector input (HEC).

## Kubernetes Objects

Splunk Connect for Kubernetes collects Kubernetes objects that can help users access cluster status. Splunk deploys code in the Kubernetes cluster that collects the object data. That deployment contains one pod that runs Fluentd which contains the following plugins to help push data to Splunk:

* [in_kubernetes_objects](https://github.com/splunk/fluent-plugin-kubernetes-objects) collects object data by calling the Kubernetes API (by https://github.com/abonas/kubeclient). in-kubernetes-objects supports two modes:
  * watch mode: the Kubernetes API sends new changes to the plugin. In this mode, only the changed data is collected.
  * pull mode: the plugin queries the Kubernetes API periodically. In this mode, all data is collected.
* [filter_jq_transformer](https://rubygems.org/gems/fluent-plugin-jq) transforms the raw data into a Splunk-friendly format and generates sources and sourcetypes.
* [out_splunk_hec](https://github.com/splunk/fluent-plugin-splunk-hec) sends the data to Splunk via HTTP Event Collector input (HEC).

## Metrics

Splunk Connect for Kubernetes deploys daemonsets on the Kubernetes cluster. These daemonsets have exactly one pod, which runs one container:

* [Fluentd metrics plugin](https://github.com/splunk/fluent-plugin-kubernetes-metrics) collects the metrics, formats the metrics for Splunk ingestion by assuring the metrics have proper metric_name, dimensions, etc., and then sends the metrics to Splunk using out_splunk_hec using Fluentd engine.

Make sure your Splunk configuration has a metrics index that is able to receive the data. See [Get started with metrics](http://docs.splunk.com/Documentation/Splunk/7.2.4/Metrics/GetStarted) in the Splunk Enterprise documentation.

If you want to learn more about how metrics are monitored in a Kubernetes cluster, see Tools for [Monitoring Compute, Storage, and Network Resources](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-usage-monitoring/).

If you want to learn more about which metrics are collected and metric names used with Splunk Connect for Kubernetes, view the metrics [schema](https://github.com/splunk/fluent-plugin-kubernetes-metrics).

# Performance

Some parameters used with Splunk Connect for Kubernetes can have an impact on overall performance of log ingestion, objects, or metrics. In general, the more filters that are added to one of the streams, the greater the performance impact.

Splunk Connect for Kubernetes can exceed the default throughput of HEC. To best address capacity needs, Splunk recommends that you monitor the HEC throughput and back pressure on Splunk Connect for Kubernetes deployments and be prepared to add additional nodes as needed.

# Processing multiline Logs

One possible filter option is to enable the processing of multiline events. This feature is currently experimental and considered to be community supported.

# Configuring multiline fluentd filters to line break multiline logs

Configure apache tomcat multiline logs using the following steps:


1. Develop a multiline filter with the proper regex and test the regex using a site such as https://rubular.com/

```bash
<filter tail.containers.var.log.containers.toolbox*toolbox*.log>
        @type concat
        key log
        timeout_label @SPLUNK
        stream_identity_key stream
        multiline_start_regexp /^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}|^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}|^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\s-\s-/
        multiline_end_regexp /\\n$/
        separator ""
        flush_interval 5s
</filter>
```

2. Add the multiline filter to your deployment's [logging configmap](https://github.com/splunk/splunk-connect-for-kubernetes/blob/develop/manifests/splunk-kubernetes-logging/configMap.yaml), using the [customFilters](https://github.com/splunk/splunk-connect-for-kubernetes/blob/develop/helm-chart/splunk-connect-for-kubernetes/values.yaml#L440) parameter.

3. Save your changes.

# Managing SCK Log Ingestion by Using Annotations

Manage Splunk Connect for Kubernetes Logging with these supported annotations.

* Use `splunk.com/index` annotation on pod and/or namespace to tell which Splunk platform indexes to ingest to. Pod annotation will take precedence over namespace annotation when both are annotated.
  ex) `kubectl annotate namespace kube-system splunk.com/index=k8s_events`
* Set `splunk.com/exclude` annotation to `true` on pod and/or namespace to exclude its logs from ingested to your Splunk platform deployment.
* Use `splunk.com/sourcetype` annotation on pod to overwrite `sourcetype` field. If not set, it is dynamically generated to be `container:CONTAINER_NAME`. Note that the sourcetype will be prefixed with `.Values.sourcetypePrefix` (default: `kube:`).

Regarding excluding container logs: If possible, it is more efficient to exclude it using `fluentd.exclude_path` option.

# Searching for SCK metadata in Splunk
Splunk Connect for Kubernetes sends events to Splunk which can contain extra meta-data attached to each event. Metadata values such as "pod", "namespace", "container_name","container_id", "cluster_name" will appear as fields when viewing the event data inside Splunk.
There are two solutions for running searches in Splunk on meta-data.

* Modify search to use`fieldname::value` instead of `fieldname=value`.
* Configure `fields.conf` on your downstream Splunk system to have your meta-data fields available to be searched using `fieldname=value`. Example: [fields.conf.example](https://github.com/splunk/splunk-connect-for-kubernetes/blob/develop/fields.conf.example)

For more information on index time field extraction please view this [guide](https://docs.splunk.com/Documentation/Splunk/latest/Data/Configureindex-timefieldextraction#Where_to_put_the_configuration_changes_in_a_distributed_environment).

# Sending logs to ingest API
Splunk Connect for Kubernetes can be used to send events to [Splunk Ingest API](https://sdc.splunkbeta.com/reference/api/ingest/v1beta2). In the ingest_api section of the yaml file you are using to deploy, the following configuration options have to be configured:</br>
* serviceClientIdentifier - Splunk Connect for Kubernetes uses the client identifier to make authorized requests to the ingest API.
* serviceClientSecretKey - Splunk Connect for Kubernetes uses the client secret key to make authorized requests to the ingest API.
* tokenEndpoint - This value indicates which endpoint Splunk Connect for Kubernetes should look to for the authorization token necessary for making requests to the ingest API.
* ingestAPIHost - Indicates which url/hostname to use for requests to the ingest API.
* tenant - Indicates which tenant Splunk Connect for Kubernetes should use for requests to the ingest API.
* eventsEndpoint - Indicates which endpoint to use for requests to the ingest API.
* debugIngestAPI - Set to True if you want to debug requests and responses to ingest API.

# Maintenance And Support
Splunk Connect For Kubernetes is supported through Splunk Support assuming the customer has a current Splunk support entitlement ([Splunk Support](https://www.splunk.com/en_us/about-splunk/contact-us.html#tabs/tab_parsys_tabs_CustomerSupport_4)). For customers that do not have a current Splunk support entitlement, please search [open and closed issues](https://github.com/splunk/splunk-connect-for-kubernetes/issues?q=is%3Aissue) and create a new issue if not already there.
The current maintainers of this project are the DataEdge team at Splunk.

# License

See [LICENSE](https://github.com/splunk/splunk-connect-for-kubernetes/blob/main/LICENSE).
