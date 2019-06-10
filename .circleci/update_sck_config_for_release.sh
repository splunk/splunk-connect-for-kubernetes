#!/usr/bin/env bash

set -e
VERSION=`cat VERSION`

# Install yq yaml parser
wget https://github.com/mikefarah/yq/releases/download/2.2.1/yq_linux_amd64
sudo chmod +x yq_linux_amd64
sudo mv yq_linux_amd64 /usr/local/bin/yq

# setup necessary for functional tests
# Modify splunk environment values
yq w -i .circleci/sck_values.yml global.splunk.hec.host $SPLUNK_HEC_HOST
yq w -i .circleci/sck_values.yml global.splunk.hec.token $SPLUNK_HEC_TOKEN

# Pull docker images locally
docker pull splunk/fluentd-hec:1.1.1
docker pull splunk/k8s-metrics:1.1.1
docker pull splunk/k8s-metrics-aggr:1.1.0
docker pull splunk/kube-objects:1.1.0

# Modify docker images to be used
yq w -i .circleci/sck_values.yml splunk-kubernetes-logging.image.name splunk/fluentd-hec:1.1.1
yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.image.name splunk/k8s-metrics:1.1.1
yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.imageAgg.name splunk/k8s-metrics-aggr:1.1.0
yq w -i .circleci/sck_values.yml splunk-kubernetes-objects.image.name splunk/kube-objects:1.1.0
