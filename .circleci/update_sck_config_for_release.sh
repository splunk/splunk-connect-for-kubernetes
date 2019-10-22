#!/usr/bin/env bash

set -e
VERSION=`cat VERSION`

source PLUGIN_VERSIONS.sh

# Install yq yaml parser
wget https://github.com/mikefarah/yq/releases/download/2.2.1/yq_linux_amd64
sudo chmod +x yq_linux_amd64
sudo mv yq_linux_amd64 /usr/local/bin/yq

# setup necessary for functional tests
# Modify splunk environment values
yq w -i .circleci/sck_values.yml global.splunk.hec.host $CI_SPLUNK_HEC_HOST
yq w -i .circleci/sck_values.yml global.splunk.hec.token $CI_SPLUNK_HEC_TOKEN

# Pull docker images locally
docker pull splunk/fluentd-hec:$FLUENTD_HEC_VERSION
docker pull splunk/k8s-metrics:$K8S_METRICS_VERISION
docker pull splunk/k8s-metrics-aggr:$K8S_METRICS_AGGR_VERSION
docker pull splunk/kube-objects:$KUBE_OBJECT_VERSION

# Modify docker images to be used
yq w -i .circleci/sck_values.yml splunk-kubernetes-logging.image.name splunk/fluentd-hec:$FLUENTD_HEC_VERSION
yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.image.name splunk/k8s-metrics:$K8S_METRICS_VERISION
yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.imageAgg.name splunk/k8s-metrics-aggr:$K8S_METRICS_AGGR_VERSION
yq w -i .circleci/sck_values.yml splunk-kubernetes-objects.image.name splunk/kube-objects:$KUBE_OBJECT_VERSION
