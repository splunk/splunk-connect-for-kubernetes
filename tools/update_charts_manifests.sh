#!/usr/bin/env bash
set -e

# execute this script to generate manifests with VERSION and Plugin versions.

TAG=`cat VERSION`
source PLUGIN_VERSIONS.sh

if [ -f "/usr/local/bin/yq" ]; then
    echo "yq already installed"    
else 
    echo "please install yq first"
    exit 1
fi

echo "VERSION $VERSION"
echo "FLUENTD_HEC_VERSION $FLUENTD_HEC_VERSION"
echo "K8S_METRICS_VERISION $K8S_METRICS_VERISION"
echo "K8S_METRICS_AGGR_VERSION $K8S_METRICS_AGGR_VERSION"
echo "KUBE_OBJECT_VERSION $KUBE_OBJECT_VERSION"

echo "Updating Charts' version and default values.yaml"
yq w -i helm-chart/splunk-kubernetes-logging/values.yaml image.name splunk/fluentd-hec:$FLUENTD_HEC_VERSION
yq w -i helm-chart/splunk-kubernetes-metrics/values.yaml image.name splunk/k8s-metrics:$K8S_METRICS_VERISION
yq w -i helm-chart/splunk-kubernetes-metrics/values.yaml imageAgg.name splunk/k8s-metrics-aggr:$K8S_METRICS_AGGR_VERSION
yq w -i helm-chart/splunk-kubernetes-objects/values.yaml image.name splunk/kube-objects:$KUBE_OBJECT_VERSION

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


echo "Updating manifests"
yq w -i manifests/splunk-kubernetes-logging/configMap.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-logging/daemonset.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-logging/daemonset.yaml spec.selector.matchLabels.version $VERSION
yq w -i manifests/splunk-kubernetes-logging/daemonset.yaml spec.template.metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-logging/daemonset.yaml spec.template.spec.containers[0].image splunk/fluentd-hec:$FLUENTD_HEC_VERSION
yq w -i manifests/splunk-kubernetes-logging/secret.yaml metadata.labels.version $VERSION

yq w -i manifests/splunk-kubernetes-metrics/clusterRole.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/clusterRoleAggregator.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/clusterRoleBinding.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/clusterRoleBindingAggregator.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/configMap.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/configMapMetricsAggregator.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/deployment.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/deployment.yaml spec.selector.matchLabels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/deployment.yaml spec.template.metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/deployment.yaml spec.template.spec.containers[0].image splunk/k8s-metrics:$K8S_METRICS_VERISION
yq w -i manifests/splunk-kubernetes-metrics/deploymentMetricsAggregator.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/deploymentMetricsAggregator.yaml spec.selector.matchLabels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/deploymentMetricsAggregator.yaml spec.template.metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/deploymentMetricsAggregator.yaml spec.template.spec.containers[0].image splunk/k8s-metrics-aggr:$K8S_METRICS_AGGR_VERSION
yq w -i manifests/splunk-kubernetes-metrics/secret.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/serviceAccount.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-metrics/clusterRole.yaml dependencies.splunk-kubernetes-metrics.version $VERSION

yq w -i manifests/splunk-kubernetes-objects/clusterRole.yaml dependencies.splunk-kubernetes-objects.version $VERSION
yq w -i manifests/splunk-kubernetes-objects/clusterRoleBinding.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-objects/configMap.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-objects/deployment.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-objects/deployment.yaml spec.selector.matchLabels.version $VERSION
yq w -i manifests/splunk-kubernetes-objects/deployment.yaml spec.template.metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-objects/deployment.yaml spec.template.spec.containers[0].image splunk/k8s-metrics:$KUBE_OBJECT_VERSION
yq w -i manifests/splunk-kubernetes-objects/secret.yaml metadata.labels.version $VERSION
yq w -i manifests/splunk-kubernetes-objects/serviceAccount.yaml metadata.labels.version $VERSION

echo "Manifests and Chart values have been updated locally."