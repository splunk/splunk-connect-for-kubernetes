# Splunk Connect for Kubernetes #

Splunk Connect for Kubernetes (the connector), is a [Helm](https://github.com/kubernetes/helm) chart that once installed, will create Kubernetes objects in a Kubernetes cluster to collect the cluster's data and send them to [splunk](https://www.splunk.com/) so that you can get insights from your cluster.

The connector contains three Helm Charts to manage Splunk Connect for Kubernetes:

* splunk-kubernetes-logging: Daemonset that runs [fluentd](https://www.fluentd.org/) to collect logs for both Kubernetes system components (e.g. kubelet, apiserver, etc.), and applications which are running in the cluster. See [README](charts/splunk-kubernetes-logging/README.md) for details.
* splunk-kubernetes-objects: Deployment that runs Fluentd to collect data of Kubernetes objects, e.g. namespaces, nodes, pods, etc. See [README](charts/splunk-kubernetes-objects/README.md) for details.
* splunk-kubernetes-metrics: Deployment and Daemonset that runs Fluentd to collect metrics from Kubernetes. [README](/helm-chart/splunk-kubernetes-metrics/README.md)

## Install ##

See also [Using Helm](https://docs.helm.sh/using_helm/#using-helm).

* Add Splunk chart repo 

`helm repo add splunk https://splunk.github.io/splunk-connect-for-kubernetes/`

* Get values file in your working directory 

`helm show values splunk/splunk-connect-for-kubernetes > values.yaml`

* Prepare this Values file. Check the Values files in each sub-chart for details. You can also check the [examples](examples) for quick start.
Once you have a Values file, you can simply install the chart with by running

Helm 2
```bash
$ helm install --name my-splunk-connect -f my_values.yaml splunk/splunk-connect-for-kubernetes
```
Helm 3
```bash
helm install my-splunk-connect -f my_values.yaml splunk/splunk-connect-for-kubernetes
```

## Uninstall ##

To uninstall/delete deployment with name `my-splunk-connect`:

Helm 2
```bash
$ helm delete --purge my-splunk-connect
```

Helm 3
```bash
$ helm delete my-splunk-connect
```

The command removes all the Kubernetes components associated with the Chart and deletes the release.

### About RBAC ###

If this is the first time you use Helm, and you have RBAC (Role Based Access Control) enabled in your Kubernetes cluster, before you install Helm, you should read [this doc](https://docs.helm.sh/using_helm/#role-based-access-control) carefully, otherwise you will encounter RBAC related issue when you try to install the chart.


## Configuration ##

This chart does not contain any configurable parameters for itself. The Values file is used to configure the sub-charts. All the sub-charts support [`global`](https://docs.helm.sh/chart_template_guide/#global-chart-values) for [Splunk HEC](http://docs.splunk.com/Documentation/Splunk/7.0.1/Data/AboutHEC) configurations. If you have the same HEC endpoint for all sub-charts, use `global` values will make your values file simpler.

See also:
* [Overriding Values from a Parent Chart](https://docs.helm.sh/chart_template_guide/#overriding-values-from-a-parent-chart) for how to configure sub-charts in the parent chart.
* [charts/splunk-kubernetes-logging/values.yaml](https://github.com/splunk/splunk-connect-for-kubernetes/blob/main/helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-logging/values.yaml) for configurable parameters for `splunk-kubernetes-logging`.
* [charts/splunk-kubernetes-objects/values.yaml](https://github.com/splunk/splunk-connect-for-kubernetes/blob/main/helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-objects/values.yaml) for configurable parameters for `splunk-kubernetes-objects`.
* [charts/splunk-kubernetes-metrics/values.yaml](https://github.com/splunk/splunk-connect-for-kubernetes/blob/main/helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-metrics/values.yaml) for configurable parameters for `splunk-kubernetes-metrics`.

## License ##

See [LICENSE](../../LICENSE).
