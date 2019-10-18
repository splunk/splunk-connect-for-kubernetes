#!/usr/bin/env bash

set -e
source PLUGIN_VERSIONS.sh

# Install yq yaml parser
wget https://github.com/mikefarah/yq/releases/download/2.2.1/yq_linux_amd64
sudo chmod +x yq_linux_amd64
sudo mv yq_linux_amd64 /usr/local/bin/yq

# Modify splunk environment values
yq w -i .circleci/sck_values.yml global.splunk.hec.host $CI_SPLUNK_HEC_HOST
yq w -i .circleci/sck_values.yml global.splunk.hec.token $CI_SPLUNK_HEC_TOKEN
yq w -i .circleci/performance/perf_test_sck_values.yml global.splunk.hec.host $CI_SPLUNK_HEC_HOST_PERF
yq w -i .circleci/performance/perf_test_sck_values.yml global.splunk.hec.token $CI_SPLUNK_HEC_TOKEN_PERF
yq w -i .circleci/sck_values.yml global.splunk.hec.protocol ${CI_HEC_PROTOCOL:-https}

# Modify docker images to be used
yq w -i .circleci/sck_values.yml splunk-kubernetes-logging.image.name splunk/fluentd-hec
yq w -i .circleci/sck_values.yml splunk-kubernetes-logging.image.tag $FLUENTD_HEC_VERSION
yq w -i .circleci/performance/perf_test_sck_values.yml splunk-kubernetes-logging.image.name splunk/fluentd-hec
yq w -i .circleci/performance/perf_test_sck_values.yml splunk-kubernetes-logging.image.tag $FLUENTD_HEC_VERSION

yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.image.name splunk/k8s-metrics
yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.image.tag $K8S_METRICS_VERISION
yq w -i .circleci/performance/perf_test_sck_values.yml splunk-kubernetes-metrics.image.name splunk/k8s-metrics
yq w -i .circleci/performance/perf_test_sck_values.yml splunk-kubernetes-metrics.image.tag $K8S_METRICS_VERISION

yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.imageAgg.name splunk/k8s-metrics-aggr
yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.imageAgg.tag $K8S_METRICS_AGGR_VERSION
yq w -i .circleci/performance/perf_test_sck_values.yml splunk-kubernetes-metrics.imageAgg.name splunk/k8s-metrics-aggr
yq w -i .circleci/performance/perf_test_sck_values.yml splunk-kubernetes-metrics.imageAgg.tag $K8S_METRICS_AGGR_VERSION

yq w -i .circleci/sck_values.yml splunk-kubernetes-objects.image.name splunk/kube-objects
yq w -i .circleci/sck_values.yml splunk-kubernetes-objects.image.tag $KUBE_OBJECT_VERSION
yq w -i .circleci/performance/perf_test_sck_values.yml splunk-kubernetes-objects.image.name splunk/kube-objects
yq w -i .circleci/performance/perf_test_sck_values.yml splunk-kubernetes-objects.image.tag $KUBE_OBJECT_VERSION