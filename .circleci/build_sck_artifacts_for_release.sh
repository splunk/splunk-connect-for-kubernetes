#!/usr/bin/env bash
set -e
TAG=`cat VERSION`

# Install yq yaml parser
wget https://github.com/mikefarah/yq/releases/download/2.2.1/yq_linux_amd64
sudo chmod +x yq_linux_amd64
sudo mv yq_linux_amd64 /usr/local/bin/yq

yq w -i helm-chart/splunk-kubernetes-logging/values.yaml image.name splunk/fluentd-hec:1.1.1
yq w -i helm-chart/splunk-kubernetes-metrics/values.yaml image.name splunk/k8s-metrics:1.1.1
yq w -i helm-chart/splunk-kubernetes-metrics/values.yaml imageAgg.name splunk/k8s-metrics-aggr:1.1.0
yq w -i helm-chart/splunk-kubernetes-objects/values.yaml image.name splunk/kube-objects:1.1.0

yq w -i helm-chart/splunk-connect-for-kubernetes/Chart.yaml version $VERSION
yq w -i helm-chart/splunk-kubernetes-logging/Chart.yaml version $VERSION
yq w -i helm-chart/splunk-kubernetes-metrics/Chart.yaml version $VERSION
yq w -i helm-chart/splunk-kubernetes-objects/Chart.yaml version $VERSION

yq w -i helm-chart/splunk-connect-for-kubernetes/Chart.yaml appVersion $VERSION
yq w -i helm-chart/splunk-kubernetes-logging/Chart.yaml appVersion $VERSION
yq w -i helm-chart/splunk-kubernetes-metrics/Chart.yaml appVersion $VERSION
yq w -i helm-chart/splunk-kubernetes-objects/Chart.yaml appVersion $VERSION

yq w -i helm-chart/splunk-kubernetes-logging/requirements.yaml dependencies.splunk-kubernetes-logging.version $VERSION
yq w -i helm-chart/splunk-kubernetes-metrics/requirements.yaml dependencies.splunk-kubernetes-metrics.version $VERSION
yq w -i helm-chart/splunk-kubernetes-objects/requirements.yaml dependencies.splunk-kubernetes-objects.version $VERSION

mkdir helm-artifacts-release
if [[ -d "helm-chart/splunk-connect-for-kubernetes/charts" ]]; then
    rm -rf helm-chart/splunk-connect-for-kubernetes/charts
fi
mkdir helm-chart/splunk-connect-for-kubernetes/charts

sub_repos_array=( "helm-chart/splunk-kubernetes-logging"
              "helm-chart/splunk-kubernetes-metrics" "helm-chart/splunk-kubernetes-objects" )
for sub_repo in "${sub_repos_array[@]}"
do
  cp -rp $sub_repo helm-chart/splunk-connect-for-kubernetes/charts
done

repos_array=( "helm-chart/splunk-connect-for-kubernetes" "helm-chart/splunk-kubernetes-logging"
              "helm-chart/splunk-kubernetes-metrics" "helm-chart/splunk-kubernetes-objects" )
for repo in "${repos_array[@]}"
do
  helm package -d helm-artifacts-release $repo
done

rm -rf helm-chart/splunk-connect-for-kubernetes/charts
