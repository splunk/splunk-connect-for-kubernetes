# Splunk Collect for Kubernetes Metrics #

`splunk-kubernetes-metrics` is a [Helm](https://github.com/kubernetes/helm) chart that creates a kubernetes deployment along with other kubernetes objects in a kubernetes cluster to collect the metrics and metric aggregations and send them to [splunk](https://www.splunk.com/).

The deployment runs a daemonset and a deployment which runs a pod that has one container on each node. [Fluentd metrics plugin](https://github.com/splunk/fluent-plugin-kubernetes-metrics) collects the metrics, formats the metrics for Splunk ingestion by assuring the metrics have proper metric_name, dimensions, etc., and then sends the metrics to a splunk instance with the [Splunk HEC output plugin](https://github.com/splunk/fluent-plugin-splunk-hec) over [Splunk HEC](http://docs.splunk.com/Documentation/Splunk/7.2.4/Data/AboutHEC).

Although it works well by itself, this chart is a part of [`splunk-connect-for-kubernetes`](https://github.com/splunk/splunk-connect-for-kubernetes). If you want a full Splunk monitoring solution for kubernetes, check it out.

## Install ##

See also [Using Helm](https://docs.helm.sh/using_helm/#using-helm).

First, you have to create a metric index in your splunk instance/cluster, and link it to the HTTP input you want to use.

Then, prepare a values file. You can also check the [examples](examples) for quick start.

Once you have a values file, you can simply install the chart with a release name (optional) by running

Helm 2
```bash
$ helm install --name my-splunk-metrics -f my_values.yaml https://github.com/splunk/splunk-connect-for-kubernetes/releases/download/1.4.3/splunk-kubernetes-metrics-1.4.3.tgz
```

Helm 3
```bash
$ helm install my-splunk-metrics -f my_values.yaml https://github.com/splunk/splunk-connect-for-kubernetes/releases/download/1.4.3/splunk-kubernetes-metrics-1.4.3.tgz
```
## Uninstall ##

To uninstall/delete a deployment with name `my-splunk-metrics`:

Helm 2
```bash
$ helm delete --purge my-splunk-metrics
```

Helm 3
```bash
$ helm delete my-splunk-metrics
```
The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration ##

The [values.yaml](values.yaml) list all supported configurable parameters for this chart, along with detailed explanation. Read through it to understand how to configure this chart. Also there are some examples in the [examples](examples) directory.

## Components ##

The following table lists all components (i.e. kubernetes objects) of this chart and their responsibilities.

Component | Description | Template
--- | --- | ---
`Deployment` | deploys daemonset that runs fluentd plugins and fluentd to collect metrics. | [deployment.yaml](templates/deployment.yaml)
`DeploymentMetricsAggregator` | deploys deployment that runs fluentd plugins and fluentd to collect metrics and calculates aggregations. | [deploymentMetricsAggregator.yaml](templates/deploymentMetricsAggregator.yaml)
`ConfigMap` | contains configuration files for fluentd. | [configmap.yaml](templates/configmap.yaml)
`ConfigMapMetricsAggregator` | contains configuration files for fluentd for Metrics Aggregator. | [configmap.yaml](templates/configmap.yaml)
`Secret` | stores credentials like the Splunk HEC token, and SSL certs and keys for HTTPS connection, etc. | [secret.yaml](templates/secret.yaml)
`ServiceAccount` | a service account to run the daemonset. | [serviceaccount.yaml](templates/serviceaccount.yaml)
`ClusterRoleBinding` | binds the kubelet-summary-api-read cluster role to the service account. | [clusterRoleBinding.yaml](templates/clusterrolebinding.yaml)
`ClusterRoleBindingAggregator` | binds the kube-api-aggregator cluster role to the service account. | [ClusterRoleBindingAggregator.yaml](templates/ClusterRoleBindingAggregator.yaml)
`ClusterRole` | cluster role which gives access to "nodes", "nodes/stats", "nodes/metrics". | [clusterRole.yaml](templates/clusterrole.yaml)
`ClusterRoleAggregator` | cluster role which gives access to "nodes", "nodes/stats", "nodes/proxy" and "pods". | [ClusterRoleAggregator.yaml](templates/clusterroleaggregator.yaml)

Note: when `rbac.create` is set to `false` (it should be when RBAC is not enabled in the kubernetes cluster), the `ClusterRoleBinding` won't be created.

## License ##

See [LICENSE.md](LICENSE.md).
