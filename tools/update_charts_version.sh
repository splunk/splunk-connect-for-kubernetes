#!/usr/bin/env bash
set -e

VERSION=`cat VERSION`

if ! command -v yq &> /dev/null
then
    echo "yq could not be found. Please install yq first"
    exit 1
fi

echo "VERSION $VERSION"
echo "Updating Charts' version"

yq w -i helm-chart/splunk-connect-for-kubernetes/Chart.yaml version $VERSION
yq w -i helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-logging/Chart.yaml version $VERSION
yq w -i helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-metrics/Chart.yaml version $VERSION
yq w -i helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-objects/Chart.yaml version $VERSION

yq w -i helm-chart/splunk-connect-for-kubernetes/Chart.yaml appVersion $VERSION
yq w -i helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-logging/Chart.yaml appVersion $VERSION
yq w -i helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-metrics/Chart.yaml appVersion $VERSION
yq w -i helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-objects/Chart.yaml appVersion $VERSION

yq w -i helm-chart/splunk-connect-for-kubernetes/requirements.yaml dependencies[0].version $VERSION
yq w -i helm-chart/splunk-connect-for-kubernetes/requirements.yaml dependencies[1].version $VERSION
yq w -i helm-chart/splunk-connect-for-kubernetes/requirements.yaml dependencies[2].version $VERSION

