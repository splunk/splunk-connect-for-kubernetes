include PLUGIN_VERSIONS.sh
export $(shell sed 's/=.*//' PLUGIN_VERSIONS.sh)

create-dir:
	@mkdir -p build

main-chart: create-dir
	@helm package -d build helm-chart/splunk-connect-for-kubernetes

logging-chart: create-dir
	@helm package -d build helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-logging

objects-chart: create-dir
	@helm package -d build helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-objects

metrics-chart: create-dir
	@helm package -d build helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-metrics

all-charts: create-dir
	@helm package -d build helm-chart/splunk-connect-for-kubernetes
	@helm package -d build helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-logging
	@helm package -d build helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-objects
	@helm package -d build helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-metrics

build: all-charts

.PHONY: manifests
manifests: main-chart
	@./tools/update_charts_version.sh
	@helm template \
	   --set global.splunk.hec.host=MY-SPLUNK-HOST \
	   --set global.splunk.hec.token=MY-SPLUNK-TOKEN \
	   --set global.splunk.hec.insecureSSL=true \
	   --set splunk-kubernetes-logging.fullnameOverride="splunk-kubernetes-logging" \
	   --set splunk-kubernetes-metrics.fullnameOverride="splunk-kubernetes-metrics" \
	   --set splunk-kubernetes-objects.fullnameOverride="splunk-kubernetes-objects" \
	   --set splunk-kubernetes-objects.kubernetes.insecureSSL=true \
	   --set splunk-kubernetes-objects.image.tag=$(KUBE_OBJECT_VERSION) \
	   --set splunk-kubernetes-logging.image.tag=$(FLUENTD_HEC_VERSION) \
	   --set splunk-kubernetes-metrics.image.tag=$(K8S_METRICS_VERISION) \
	   --set splunk-kubernetes-metrics.imageAgg.tag=$(K8S_METRICS_AGGR_VERSION) \
	   --set splunk-kubernetes-logging.podSecurityPolicy.create=true \
	   --set splunk-kubernetes-metrics.podSecurityPolicy.create=true \
	   --set splunk-kubernetes-objects.podSecurityPolicy.create=true \
	   $$(ls build/splunk-connect-for-kubernetes-*.tgz) \
	   | ruby tools/gen_manifest.rb manifests

cleanup:
	@rm -rf build
