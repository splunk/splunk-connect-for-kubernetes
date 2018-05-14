connect-chart: logging-chart objects-chart metrics-chart
	@sed -i.bak -E -e 's/^([[:space:]]+repository:[[:space:]]+).+$$/\1local/' helm-chart/splunk-connect-for-kubernetes/requirements.yaml
	@mv helm-chart/splunk-connect-for-kubernetes/requirements.yaml.bak .
	@mkdir -p helm-chart/splunk-connect-for-kubernetes/charts
	@cp build/splunk-kubernetes-*.tgz helm-chart/splunk-connect-for-kubernetes/charts
	@helm package -d build helm-chart/splunk-connect-for-kubernetes
	@mv requirements.yaml.bak helm-chart/splunk-connect-for-kubernetes/requirements.yaml
	@rm -rf helm-chart/splunk-connect-for-kubernetes/charts

logging-chart: build
	@helm package -d build helm-chart/splunk-kubernetes-logging

objects-chart: build
	@helm package -d build helm-chart/splunk-kubernetes-objects

metrics-chart: build
	@helm package -d build helm-chart/splunk-kubernetes-metrics

build:
	@mkdir -p build

.PHONY: manifests
manifests: connect-chart
	@helm template \
	   --set global.splunk.hec.host=MY-SPLUNK-HOST \
	   --set global.splunk.hec.token=MY-SPLUNK-TOKEN \
	   --set global.splunk.hec.insecureSSL=true \
	   --set splunk-kubernetes-objects.kubernetes.insecureSSL=true \
	   $$(ls build/splunk-connect-for-kubernetes-*.tgz) \
	   | ruby tools/gen_manifest.rb manifests

cleanup:
	@rm -rf build
