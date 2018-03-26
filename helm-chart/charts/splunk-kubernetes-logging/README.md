# Splunk Collector for Kubernetes Logs #

`splunk-kubernetes-logging` is a [Helm](https://github.com/kubernetes/helm) chart that creates a kubernetes daemonset along with other kubernetes objects in a kubernetes cluster to collect the cluster's logs and send them to [splunk](https://www.splunk.com/).

The deamonset created by `splunk-kubernetes-logging` runs [fluentd](https://www.fluentd.org/) with the [Splunk HEC output plugin](https://github.com/splunk/fluent-plugin-splunk-hec) to collect logs and send them via [Splunk HEC](http://docs.splunk.com/Documentation/Splunk/7.0.1/Data/AboutHEC).

It does not only collects logs for applications which are running in the kubernetes cluster, but also the logs for kubernetes itself (i.e. logs from `kubelet`, `apiserver`, etc.). It reads logs from both file system with the [fluentd tail plugin](https://docs.fluentd.org/v1.0/articles/in_tail) and [systemd journal](http://0pointer.de/blog/projects/journalctl.html) with [`fluent-plugin-systemd`](https://github.com/reevoo/fluent-plugin-systemd).

Although it works well by itself, this chart is a part of [`splunk-connector`](https://github.com/splunk/splunk-connector-kubernetes-charts). If you want a full Splunk monnitoring solution for kubernetes, check it out.

## Install ##

See also [Using Helm](https://docs.helm.sh/using_helm/#using-helm).

First, prepare a values file. You can also check the [examples](examples) for quick start.

Once you have a values file, you can simply install the chart with the release name `my-release` (optional) by running

```bash
$ helm install --name my-release -f my_values.yaml stable/splunk-kubernetes-logging
```

## Uninstall ##

To uninstall/delete the my-release deployment:

```bash
$ helm delete --purge my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration ##

The [values.yaml](values.yaml) list all supported configurable parameters for this chart, along with detailed explanation. Read through it to understand how to configure this chart. Also there are some examples in the [examples](examples) directory.

## Components

The following table lists all components (i.e. kubernetes objects) of this chart and their responsibilities.

Component | Description | Template
--- | --- | ---
`Daemonset` | deploys one pod that runs fluentd on each node to collect logs. | [daemonset.yaml](templates/daemonset.yaml)
`ConfigMap` | contains configuration files for fluentd. | [configmap.yaml](templates/configmap.yaml)
`Secret` | stores credentials like the Splunk HEC token, and SSL certs and keys for HTTPS connection, etc. | [secret.yaml](templates/secret.yaml)
