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
yq w -i .circleci/sck_values.yml global.splunk.hec.protocol ${CI_HEC_PROTOCOL:-https}

# Modify docker images to be used
yq w -i .circleci/sck_values.yml splunk-kubernetes-logging.image.name splunk/fluentd-hec
yq w -i .circleci/sck_values.yml splunk-kubernetes-logging.image.tag $FLUENTD_HEC_VERSION

yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.image.name splunk/k8s-metrics
yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.image.tag $K8S_METRICS_VERISION

yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.imageAgg.name splunk/k8s-metrics-aggr
yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.imageAgg.tag $K8S_METRICS_AGGR_VERSION

yq w -i .circleci/sck_values.yml splunk-kubernetes-objects.image.name splunk/kube-objects
yq w -i .circleci/sck_values.yml splunk-kubernetes-objects.image.tag $KUBE_OBJECT_VERSION


# locally build image for triggered functional test
if [ ! -z "$TRIG_PROJECT" ] 
then
    cd /tmp
    TRIG_REPO="$(echo $TRIG_REPO | sed 's/git\@github\.com\:/https\:\/\/github.com\//g')"
    git clone $TRIG_REPO
    cd $TRIG_PROJECT
    git checkout $TRIG_BRANCH
    source docker/build.sh $TRIG_BRANCH
    cd ~/repo
    case $TRIG_PROJECT in
        "fluent-plugin-kubernetes-metrics")
            yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.image.tag $TRIG_BRANCH
            yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.image.pullPolicy IfNotPresent
            ;;
        "fluent-plugin-splunk-hec")
            yq w -i .circleci/sck_values.yml splunk-kubernetes-logging.image.tag $TRIG_BRANCH
            yq w -i .circleci/sck_values.yml splunk-kubernetes-logging.image.pullPolicy IfNotPresent
            ;;
        "fluent-plugin-kubernetes-objects")
            yq w -i .circleci/sck_values.yml splunk-kubernetes-objects.image.tag $TRIG_BRANCH
            yq w -i .circleci/sck_values.yml splunk-kubernetes-objects.image.pullPolicy IfNotPresent
            ;;
        "fluent-plugin-k8s-metrics-agg")
            yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.imageAgg.tag $TRIG_BRANCH
            yq w -i .circleci/sck_values.yml splunk-kubernetes-metrics.imageAgg.pullPolicy IfNotPresent
            ;;
    esac
fi

