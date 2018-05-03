# Splunk Connect for Kubernetes #

Splunk Connect for Kubernetes (the connector) is a set of Kubernetes objects which once deployed in to a Kubernetes cluster, it collects data from the cluster, and sends the data to a Splunk indexer or a Splunk indexer cluster. The connector utilizes Fluentd and Heapster to collect data. Data it collects include: logs, objects, and metrics.

The connector is provided as a Helm chart, so that it can be installed easily using the Helm command line tool. Please see [the README file](./helm-chart/README.md) for the details.

For people who do not use Helm, a set of manifests manifests
