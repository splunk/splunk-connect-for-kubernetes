# Splunk Collect for Kubernetes Objects #

`splunk-kubernetes-objects` is a [Helm](https://github.com/kubernetes/helm) chart that creates a kubernetes deployment along with other kubernetes objects in a kubernetes cluster to collect the cluster's objects and send them to [splunk](https://www.splunk.com/).

The deployment runs [fluentd](https://www.fluentd.org/) with the [kubernetes objects input plugin](https://github.com/splunk/fluent-plugin-kubernetes-objects) and the [Splunk HEC output plugin](https://github.com/splunk/fluent-plugin-splunk-hec) to collect objects and send them via [Splunk HEC](http://docs.splunk.com/Documentation/Splunk/7.1.0/Data/AboutHEC).

For more details on how object data are collected, check the [README](https://github.com/splunk/fluent-plugin-kubernetes-objects/blob/main/README.md) of the kubernetes objects input plugin.

Although it works well by itself, this chart is a part of [`splunk-connect-for-kubernetes`](https://github.com/splunk/splunk-connect-for-kubernetes). If you want a full Splunk monitoring solution for kubernetes, check it out.

## Install ##

See also [Using Helm](https://docs.helm.sh/using_helm/#using-helm).

First, prepare a values file. You can also check the [examples](examples) for quick start.

Once you have a values file, you can simply install the chart with a release name (optional) by running

Helm 2
```bash
$ helm install --name my-splunk-objects -f my_values.yaml https://github.com/splunk/splunk-connect-for-kubernetes/releases/download/1.4.3/splunk-kubernetes-objects-1.4.3.tgz
```

Helm 3
```bash
$ helm install my-splunk-objects -f my_values.yaml https://github.com/splunk/splunk-connect-for-kubernetes/releases/download/1.4.3/splunk-kubernetes-objects-1.4.3.tgz
```

## Uninstall ##

To uninstall/delete a deployment with name `my-splunk-objects`:

Helm 2
```bash
$ helm delete --purge my-splunk-objects
```

Helm 3
```bash
$ helm delete my-splunk-objects
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration ##

The [values.yaml](values.yaml) list all supported configurable parameters for this chart, along with detailed explanation. Read through it to understand how to configure this chart. Also there are some examples in the [examples](examples) directory.

## Components

The following table lists all components (i.e. kubernetes objects) of this chart and their responsibilities.

Component | Description | Template
--- | --- | ---
`Deployment` | creates a pod that runs fluentd to collect kubernetes objects. | [deployment.yaml](templates/deployment.yaml)
`ConfigMap` | contains configuration files for fluentd. | [configmap.yaml](templates/configmap.yaml)
`Secret` | stores credentials like the Splunk HEC token, and SSL certs and keys for HTTPS connection, etc. | [secret.yaml](templates/secret.yaml)
`ServiceAccount` | a service account for the deployment. | [serviceaccount.yaml](templates/serviceaccount.yaml)
`ClusterRole` | defines permissions needed for the service account. | [clusterrole.yaml](templates/clusterrole.yaml)
`ClusterRoleBinding` | binds the cluster role to the service account. | [clusterrolebinding.yaml](templates/clusterrolebinding.yaml)

Note: when `rbac.create` is set to `false` (it should be when RBAC is not enabled in the kubernetes cluster), the `ClusterRole` and `ClusterRoleBinding` won't be created.

## License ##

See [LICENSE.md](LICENSE.md).
