install:
	helm install \
	  --set "splunk-kubernetes-objects.splunk.hec.token=14fc1454-b71c-4190-b80b-ef2a1be29bbb" \
	  --set "splunk-kubernetes-objects.splunk.hec.endpoints={https://54.156.204.203:8088}" \
	  --set "splunk-kubernetes-logging.splunk.hec.token=14fc1454-b71c-4190-b80b-ef2a1be29bbb" \
	  --set "splunk-kubernetes-logging.splunk.hec.endpoints={https://54.156.204.203:8088}" \
	  --set "splunk-kubernetes-metrics.splunk.udp.endpoint=54.156.204.203:9995" \
	  .

debug:
	helm install \
	  --set "splunk-kubernetes-objects.splunk.hec.token=14fc1454-b71c-4190-b80b-ef2a1be29bbb" \
	  --set "splunk-kubernetes-objects.splunk.hec.endpoints={https://54.156.204.203:8088}" \
	  --set "splunk-kubernetes-logging.splunk.hec.token=14fc1454-b71c-4190-b80b-ef2a1be29bbb" \
	  --set "splunk-kubernetes-logging.splunk.hec.endpoints={https://54.156.204.203:8088}" \
	  --set "splunk-kubernetes-metrics.splunk.udp.endpoint=54.156.204.203:9995" \
	  --dry-run --debug \
	  .
