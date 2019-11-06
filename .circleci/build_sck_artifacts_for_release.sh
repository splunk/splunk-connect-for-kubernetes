#!/usr/bin/env bash
set -e
VERSION=`cat VERSION`

source PLUGIN_VERSIONS.sh

# Install yq yaml parser
wget https://github.com/mikefarah/yq/releases/download/2.2.1/yq_linux_amd64
sudo chmod +x yq_linux_amd64
sudo mv yq_linux_amd64 /usr/local/bin/yq

# Before release, "make manifests" call should have been run. 
# then there are nothing else to change. but keeping them here just in case 
yq w -i helm-chart/splunk-kubernetes-logging/values.yaml image.tag $FLUENTD_HEC_VERSION
yq w -i helm-chart/splunk-kubernetes-metrics/values.yaml image.tag $K8S_METRICS_VERISION
yq w -i helm-chart/splunk-kubernetes-metrics/values.yaml imageAgg.tag $K8S_METRICS_AGGR_VERSION
yq w -i helm-chart/splunk-kubernetes-objects/values.yaml image.tag $KUBE_OBJECT_VERSION

yq w -i helm-chart/splunk-connect-for-kubernetes/Chart.yaml version $VERSION
yq w -i helm-chart/splunk-kubernetes-logging/Chart.yaml version $VERSION
yq w -i helm-chart/splunk-kubernetes-metrics/Chart.yaml version $VERSION
yq w -i helm-chart/splunk-kubernetes-objects/Chart.yaml version $VERSION

yq w -i helm-chart/splunk-connect-for-kubernetes/Chart.yaml appVersion $VERSION
yq w -i helm-chart/splunk-kubernetes-logging/Chart.yaml appVersion $VERSION
yq w -i helm-chart/splunk-kubernetes-metrics/Chart.yaml appVersion $VERSION
yq w -i helm-chart/splunk-kubernetes-objects/Chart.yaml appVersion $VERSION

yq w -i helm-chart/splunk-connect-for-kubernetes/requirements.yaml dependencies[0].version $VERSION
yq w -i helm-chart/splunk-connect-for-kubernetes/requirements.yaml dependencies[1].version $VERSION
yq w -i helm-chart/splunk-connect-for-kubernetes/requirements.yaml dependencies[2].version $VERSION

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
