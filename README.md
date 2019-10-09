
[![CircleCI](https://circleci.com/gh/git-lfs/git-lfs.svg?style=shield&circle-token=856152c2b02bfd236f54d21e1f581f3e4ebf47ad)](https://circleci.com/gh/splunk/splunk-connect-for-kubernetes)
# What does Splunk Connect for Kubernetes do?

Splunk Connect for Kubernetes provides a way to import and search your Kubernetes logging, object, and metrics data in Splunk. Splunk is a proud contributor to Cloud Native Computing Foundation (CNCF) and Splunk Connect for Kubernetes utilizes and supports multiple CNCF components in the development of these tools to get data into Splunk.


## Prerequisites

* Splunk Enterprise 7.0 or later
* An HEC token. See the following topics for more information:
  * http://docs.splunk.com/Documentation/Splunk/7.2.4/Data/UsetheHTTPEventCollector
  * http://docs.splunk.com/Documentation/Splunk/7.2.4/Data/ScaleHTTPEventCollector
* You should be familiar with your Kubernetes configuration and know where your log info is collected in Kubernetes.
* You must have administrator access to your Kubernetes cluster.
* To install using Helm (recommended), make sure you are running Helm in your Kubernetes configuration. See https://github.com/kubernetes/helm
* Have a minimum of two Splunk indexes ready to collect the log data, one for both logs and Kubernetes objects, and one for metrics. You can also create separate indexes for logs and objects, in which case you will need three Splunk indexes.

## Before you begin
Splunk Connect for Kubernetes supports installation using Helm. Ensure that you thoroughly read the Prerequisites and Installation and Deployment documentation before you start your deployment of Splunk Connect for Kubernetes.

Make sure you do the following before you install:

1. Create a minimum of two Splunk indexes:
* One events index, which will handle logs and objects (you may also create two separate indexes for logs and objects).
* One metrics index.
If you do not configure these indexes, Kubernetes Connect for Splunk uses the defaults created in your HEC token.

2. Create a HEC token if you do not already have one. If you are installing the connector on Splunk Cloud, file a ticket with Splunk Customer Service and they will deploy the indexes for your environment and generate your HEC token.

## Deploy with Helm

Helm, maintained by the CNCF, allows the Kubernetes administrator to install, upgrade, and manage the applications running in their Kubernetes clusters.  For more information on how to use and configure Helm Charts, please the the Helm [site](https://helm.sh/) and [repository](https://github.com/kubernetes/helm) for tutorials and product documentation. Helm is the   only method that Splunk supports for installing Splunk Connect for Kubernetes.

To install and configure defaults with Helm:

```
$ helm install --name my-release -f my_values.yaml https://github.com/splunk/splunk-connect-for-kubernetes/releases/download/1.2.0/splunk-connect-for-kubernetes-1.2.0.tgz
```

To learn more about using and modifying charts, see:
* https://github.com/splunk/splunk-connect-for-kubernetes/tree/master/helm-chart
* https://docs.helm.sh/using_helm/#using-helm.

## Configuration variables for Helm

To learn more about using and modifying charts, see:
* [The values file for logging](https://github.com/splunk/splunk-connect-for-kubernetes/blob/master/helm-chart/splunk-kubernetes-logging/values.yaml)
* [The values file for metrics](https://github.com/splunk/splunk-connect-for-kubernetes/blob/master/helm-chart/splunk-kubernetes-metrics/values.yaml)
* [The values file for objects](https://github.com/splunk/splunk-connect-for-kubernetes/blob/master/helm-chart/splunk-kubernetes-objects/values.yaml)

## Deploy using YAML

You can grab the manifest YAML files and use them to create the Kubernetes objects needed to deploy Splunk Connect for Kubernetes. Please note that installation and debugging for Splunk Connect for Kubernetes through YAML is community-supported only.

When you use YAML to deploy Splunk Connect for Kubernetes, the installation does not create the default configuration that is created when you install using Helm. To deploy the connector using YAML, you must know how to configure your Kubernetes variables to work with the connector. If you are not familiar with this process, we recommend that you use the Helm installation method.

To configure the Splunk Connector for Kubernetes using YAML files:

1. Grab the Charts and Manifest files from https://github.com/splunk/splunk-connect-for-kubernetes

2. Read through all YAML files in the Manifests folder and make any necessary changes. Note that the YAML files in the Manifests folder are examples and are not expected to be used as provided.

3. Verify that your Kubernetes logs are recognized by the Splunk Connect for Kubernetes.

# Architecture

Splunk Connect for Kubernetes deploys a daemonset on each node. And in the daemonset, a Fluentd container runs and does the collecting job. Splunk Connector for Kubernetes collects three types of data:

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

Splunk Connect for Kubernetes uses the Kubernetes [node logging agent](https://kubernetes.io/docs/concepts/cluster-administration/logging/#using-a-node-logging-agent) to collect logs. Splunk deploys a daemonset on each of these nodes. Each daemonset holds a Fluentd container to collect the data. The following plugins are enabled in that Fluentd container:

* [in_systemd](https://rubygems.org/gems/fluent-plugin-systemd) reads logs from systemd journal if systemd is available on the host.
* [in_tail](https://docs.fluentd.org/v1.0/articles/in_tail) reads logs from file system.
* [filter_jq_transformer](https://rubygems.org/gems/fluent-plugin-jq) transforms the raw events to a Splunk-friendly format and generates source and sourcetypes.
* [out_splunk_hec](https://github.com/splunk/fluent-plugin-splunk-hec) sends the translated logs to Splunk indexes through the HTTP Event Collector input (HEC).

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

Make sure your Splunk configuration has a metrics index that is able to receive the data. See [Get started with metrics](http://docs.splunk.com/Documentation/Splunk/7.2.4/Metrics/GetStarted) in the Splunk Enterprise documentaiton.

If you want to learn more about how metrics are monitored in a Kubernetes cluster, see Tools for [Monitoring Compute, Storage, and Network Resources](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-usage-monitoring/).

If you want to learn more about which metrics tha are collected and metric names used with Splunk Connect for Kubernetes, view the metrics [schema](https://github.com/splunk/fluent-plugin-kubernetes-metrics).

# Performance

Some parameters used with Splunk Connect for Kubernetes can have an impact on overall performance of log ingestion, objects, or metrics. In general, the more filters that are added to one of the streams, the greater the performance impact.

Splunk Connect for Kubernetes can exceed the default throughput of HEC. To best address capacity needs, Splunk recommends that you monitor the HEC throughput and back pressure on Splunk Connect for Kubernetes deployments and be prepared to add additional nodes as needed.

# Processing Multi-Line Logs

One possible filter option is to enable the processing of multi-line events. This feature is currently experimental and considered to be community supported.

# Namespace to Index Routing

Splunk Connect for Kubernetes has the functionality to route logs and metrics from different namespaces to Splunk indexers of the same name. This can be configured by
using the two configurable parameters `indexRouting` and `indexRoutingDefaultIndex`

`indexRouting` is a boolean configurable that enables the feature
`indexRoutingDefaultIndex` is the Splunk index used for the events from the default Kubernetes namespace

Warning: Before enabling this feature it is essential to have Splunk indexes created which map to your Kubernetes namespaces.

For example:
Consider the following kubernetes namespace to splunk index topology.
* (Namespace) -> (Splunk Index)
* kube-system -> kube-system
* kube-public -> kube-public
* default -> indexRoutingDefaultIndex
For this topology to work appropriately we have to create the splunk indexes "kube-system", "kube-public" and the value of indexRoutingDefaultIndex.

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
Splunk Connect For Kubernetes is supported through Splunk Support assuming the customer has a current Splunk support entitlement. For customers that do not have a current Splunk support entitlement, please file an issue at create a new issue at [Create a new issue in splunk connect for kubernetes project](https://github.com/splunk/splunk-connect-for-kubernetes/issues/new)
The current maintainers of this project are the DataEdge team at Splunk. You can reach us at [DataEdge@splunk.com](mailto:DataEdge@splunk.com).

# License

See [LICENSE](https://github.com/splunk/splunk-connect-for-kubernetes/blob/master/LICENSE).
