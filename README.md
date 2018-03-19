# Splunk Connector for Kubernetes #

Splunk Connector for Kubernetes, `splunk-connector`, is a [Helm](https://github.com/kubernetes/helm) chart that once installed, will create kubernetes objects in a kubernetes cluster to collect the cluster's data and send them to [splunk](https://www.splunk.com/). So that you can get insights of your cluster with Splunk.

`splunk-connector` containers three Helm charts to do the job. These three charts and their responsiblities are:

* splunk-kubernetes-logging: a daemonset runs [fluentd](https://www.fluentd.org/) to collects logs for both kubernetes system components (e.g. kubelet, apiserver, etc.), and applications which are running in the cluster. See its [README](charts/splunk-kubernetes-logging/README.md) for details.
* splunk-kubernetes-objects: a deployment runs fluentd to collect data of kubernetes objects, e.g. namespaces, nodes, pods, etc. See its [README](charts/splunk-kubernetes-objects/README.md) for details.
* splunk-kubernetes-metrics: a deployment runs [heapster](https://github.com/kubernetes/heapster) and fluentd together to collect metrics. See its [README](charts/splunk-kubernetes-metrics/README.md) for details.

## Install ##

See also [Using Helm](https://docs.helm.sh/using_helm/#using-helm).

First, prepare a values file. Check the values files in each sub-chart for details. You can also check the [examples](examples) for quick start.

Once you have a values file, you can simply install the chart with the release name `my-release` (optional) by running

```bash
$ helm install --name my-release -f my_values.yaml stable/splunk-connector
```

## Uninstall ##

To uninstall/delete the my-release deployment:

```bash
$ helm delete --purge my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration ##

This chart does not contain any configurable parameters for itself. The values file is used to configure the sub-charts. All the sub-charts support [`global`](https://docs.helm.sh/chart_template_guide/#global-chart-values) for [Splunk HEC](http://docs.splunk.com/Documentation/Splunk/7.0.1/Data/AboutHEC) configurations. If you have the same HEC endpoint for all sub-charts, use `global` values will make your values file simpler.

See also:
* [Overriding Values from a Parent Chart](https://docs.helm.sh/chart_template_guide/#overriding-values-from-a-parent-chart) for how to configure sub-charts in the parent chart.
* [charts/splunk-kubernetes-logging/values.yaml](charts/splunk-kubernetes-logging/values.yaml) for configurable parameters for `splunk-kubernetes-logging`.
* [charts/splunk-kubernetes-objects/values.yaml](charts/splunk-kubernetes-objects/values.yaml) for configurable parameters for `splunk-kubernetes-objects`.
* [charts/splunk-kubernetes-metrics/values.yaml](charts/splunk-kubernetes-metrics/values.yaml) for configurable parameters for `splunk-kubernetes-metrics`.
