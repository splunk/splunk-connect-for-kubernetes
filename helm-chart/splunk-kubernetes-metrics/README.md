# Splunk Collect for Kubernetes Metrics #

`splunk-kubernetes-metrics` is a [Helm](https://github.com/kubernetes/helm) chart that creates a kubernetes deployment along with other kubernetes objects in a kubernetes cluster to collect the cluster's metrics and send them to [splunk](https://www.splunk.com/).

The deployment runs a pod that has two containers. One is [heapster](https://github.com/kubernetes/heapster), it collects the kubernetes metrics, and sends them to [fluend](https://www.fluentd.org/), which is the other container running in the same pod, over UDP, and finally the metrics will be sent to a splunk instance with the [Splunk HEC output plugin](https://github.com/splunk/fluent-plugin-splunk-hec) over [Splunk HEC](http://docs.splunk.com/Documentation/Splunk/7.1.0/Data/AboutHEC).

Although it works well by itself, this chart is a part of [`splunk-connect-for-kubernetes`](https://github.com/splunk/splunk-connect-for-kubernetes). If you want a full Splunk monitoring solution for kubernetes, check it out.

## Install ##

See also [Using Helm](https://docs.helm.sh/using_helm/#using-helm).

First, you have to create a metric index in your splunk instance/cluster, and link it to the HTTP input you want to use.

Then, prepare a values file. You can also check the [examples](examples) for quick start.

Once you have a values file, you can simply install the chart with a release name (optional) by running

```bash
$ helm install --name my-splunk-metrics -f my_values.yaml https://github.com/splunk/splunk-connect-for-kubernetes/releases/download/v1.0.0/splunk-kubernetes-metrics-1.0.0.tgz
```

## Uninstall ##

To uninstall/delete a deployment with name `my-splunk-metrics`:

```bash
$ helm delete --purge my-splunk-metrics
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration ##

The [values.yaml](values.yaml) list all supported configurable parameters for this chart, along with detailed explanation. Read through it to understand how to configure this chart. Also there are some examples in the [examples](examples) directory.

## Components ##

The following table lists all components (i.e. kubernetes objects) of this chart and their responsibilities.

Component | Description | Template
--- | --- | ---
`Deployment` | deploys one pod that runs heapster and fluentd to collect metrics. | [deployment.yaml](templates/deployment.yaml)
`ConfigMap` | contains configuration files for fluentd. | [configmap.yaml](templates/configmap.yaml)
`Secret` | stores credentials like the Splunk HEC token, and SSL certs and keys for HTTPS connection, etc. | [secret.yaml](templates/secret.yaml)
`ServiceAccount` | a service account to run the daemonset. | [serviceaccount.yaml](templates/serviceaccount.yaml)
`ClusterRoleBinding` | binds the system:heapster cluster role to the service account. | [clusterrolebinding.yaml](templates/clusterrolebinding.yaml)

Note: when `rbac.create` is set to `false` (it should be when RBAC is not enabled in the kubernetes cluster), the `ClusterRoleBinding` won't be created.

## License ##

[SPLUNK PRE-RELEASE SOFTWARE LICENSE AGREEMENT](https://www.splunk.com/en_us/legal/splunk-pre-release-software-license-agreement.html)
