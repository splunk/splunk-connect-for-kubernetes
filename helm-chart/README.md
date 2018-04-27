# Splunk Connector for Kubernetes #

Splunk Connector for Kubernetes, `splunk-connector`, is a [Helm](https://github.com/kubernetes/helm) chart that once installed, will create Kubernetes objects in a Kubernetes cluster to collect the cluster's data and send them to [splunk](https://www.splunk.com/) so that you can get insights from your cluster.

`splunk-connector` contains three Helm Charts to manage Splunk Connect for Kubernetes:

* splunk-kubernetes-logging: Daemonset that runs [fluentd](https://www.fluentd.org/) to collect logs for both Kubernetes system components (e.g. kubelet, apiserver, etc.), and applications which are running in the cluster. See [README](charts/splunk-kubernetes-logging/README.md) for details.
* splunk-kubernetes-objects: Deployment that runs Fluentd to collect data of Kubernetes objects, e.g. namespaces, nodes, pods, etc. See [README](charts/splunk-kubernetes-objects/README.md) for details.
* splunk-kubernetes-metrics: Deployment that runs [heapster](https://github.com/kubernetes/heapster) and Fluentd together to collect metrics. See [README](charts/splunk-kubernetes-metrics/README.md) for details.

## Install ##

See also [Using Helm](https://docs.helm.sh/using_helm/#using-helm).

First, prepare a Values file. Check the Values files in each sub-chart for details. You can also check the [examples](examples) for quick start.

Once you have a Values file, you can simply install the chart with the release name `my-release` (optional) by running

```bash
$ helm install --name my-release -f my_values.yaml stable/splunk-connector
```

## Uninstall ##

To uninstall/delete the my-release deployment:

```bash
$ helm delete --purge my-release
```

The command removes all the Kubernetes components associated with the Chart and deletes the release.

## Configuration ##

This chart does not contain any configurable parameters for itself. The Values file is used to configure the sub-charts. All the sub-charts support [`global`](https://docs.helm.sh/chart_template_guide/#global-chart-values) for [Splunk HEC](http://docs.splunk.com/Documentation/Splunk/7.0.1/Data/AboutHEC) configurations. If you have the same HEC endpoint for all sub-charts, use `global` values will make your values file simpler.

See also:
* [Overriding Values from a Parent Chart](https://docs.helm.sh/chart_template_guide/#overriding-values-from-a-parent-chart) for how to configure sub-charts in the parent chart.
* [charts/splunk-kubernetes-logging/values.yaml](charts/splunk-kubernetes-logging/values.yaml) for configurable parameters for `splunk-kubernetes-logging`.
* [charts/splunk-kubernetes-objects/values.yaml](charts/splunk-kubernetes-objects/values.yaml) for configurable parameters for `splunk-kubernetes-objects`.
* [charts/splunk-kubernetes-metrics/values.yaml](charts/splunk-kubernetes-metrics/values.yaml) for configurable parameters for `splunk-kubernetes-metrics`.

## License ##

[SPLUNK PRE-RELEASE SOFTWARE LICENSE AGREEMENT](https://www.splunk.com/en_us/legal/splunk-pre-release-software-license-agreement.html)
