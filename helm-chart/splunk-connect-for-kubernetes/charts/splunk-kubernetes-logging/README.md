# Splunk Collect for Kubernetes Logs #

`splunk-kubernetes-logging` is a [Helm](https://github.com/kubernetes/helm) chart that creates a kubernetes daemonset along with other kubernetes objects in a kubernetes cluster to collect the cluster's logs and send them to [splunk](https://www.splunk.com/).

The deamonset runs [fluentd](https://www.fluentd.org/) with the [Splunk HEC output plugin](https://github.com/splunk/fluent-plugin-splunk-hec) to collect logs and send them over [Splunk HEC](http://docs.splunk.com/Documentation/Splunk/7.1.0/Data/AboutHEC).

It does not only collects logs for applications which are running in the kubernetes cluster, but also the logs for kubernetes itself (i.e. logs from `kubelet`, `apiserver`, etc.). It reads logs from both file system with the [fluentd tail plugin](https://docs.fluentd.org/v1.0/articles/in_tail) and [systemd journal](http://0pointer.de/blog/projects/journalctl.html) with [`fluent-plugin-systemd`](https://github.com/reevoo/fluent-plugin-systemd).

Although it works well by itself, this chart is a part of [`splunk-connect-for-kubernetes`](https://github.com/splunk/splunk-connect-for-kubernetes). If you want a full Splunk monitoring solution for kubernetes, check it out.

## Install ##

See also [Using Helm](https://docs.helm.sh/using_helm/#using-helm).

First, prepare a values file. You can also check the [examples](examples) for quick start.

Once you have a values file, you can simply install the chart with a release name (optional) by running

Helm 2
```bash
$ helm install --name my-splunk-logging -f my_values.yaml https://github.com/splunk/splunk-connect-for-kubernetes/releases/download/1.4.5/splunk-kubernetes-logging-1.4.5.tgz
```

Helm 3
```bash
$ helm install my-splunk-logging -f my_values.yaml https://github.com/splunk/splunk-connect-for-kubernetes/releases/download/1.4.5/splunk-kubernetes-logging-1.4.5.tgz
```
## Uninstall ##

To uninstall/delete a deployment with name `my-splunk-logging`:

Helm 2
```bash
$ helm delete --purge my-splunk-logging
```

Helm 3
```bash
$ helm delete my-splunk-logging
```
The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration ##

The [values.yaml](values.yaml) list all supported configurable parameters for this chart, along with detailed explanation. Read through it to understand how to configure this chart. Also there are some examples in the [examples](examples) directory.

### About Logs ###

With the default settings, it assumes that logs for `kubelet` and `docker` are available in journald logs, and all other Kubernetes system components are running as containers. If that's not your case, you should set the `logs` in your Values file.

The default journald directory is `/run/log/journal`, if that's not your case, you need to set `journalLogPath` in your Values file.

Container logs (except the Kubernetes system components) will be indexed in Splunk with `sourcetype` set to `kube:container:<container_name>`, you can define `sourcetype` for each container in `logs` too.


## Components ##

The following table lists all components (i.e. kubernetes objects) of this chart and their responsibilities.

Component | Description | Template
--- | --- | ---
`Daemonset` | deploys one pod that runs fluentd on each node to collect logs. | [daemonset.yaml](templates/daemonset.yaml)
`ConfigMap` | contains configuration files for fluentd. | [configMap.yaml](templates/configMap.yaml)
`Secret` | stores credentials like the Splunk HEC token, and SSL certs and keys for HTTPS connection, etc. | [secret.yaml](templates/secret.yaml)

## License ##

See [LICENSE.md](LICENSE.md).
