#!/usr/bin/env bash
set -e

export VERSION=`cat VERSION`

if ! command -v yq &> /dev/null
then
    echo "yq could not be found. Please install yq first"
    echo "for MacOS, brew install yq"
    exit 1
fi

echo "VERSION $VERSION"
echo "Updating Charts' version"

yq e -i '.version = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/Chart.yaml 
yq e -i '.version = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-logging/Chart.yaml
yq e -i '.version = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-metrics/Chart.yaml
yq e -i '.version = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-objects/Chart.yaml

yq e -i '.appVersion = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/Chart.yaml
yq e -i '.appVersion = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-logging/Chart.yaml
yq e -i '.appVersion = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-metrics/Chart.yaml
yq e -i '.appVersion = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-objects/Chart.yaml

yq e -i '.dependencies[0].version = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/requirements.yaml
yq e -i '.dependencies[1].version = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/requirements.yaml
yq e -i '.dependencies[2].version = env(VERSION)' helm-chart/splunk-connect-for-kubernetes/requirements.yaml

