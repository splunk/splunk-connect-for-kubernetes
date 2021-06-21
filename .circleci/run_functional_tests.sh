#!/usr/bin/env bash
set -e
cd test
#Run pytests
echo "Running functional tests....."
python -m pytest \
	--splunkd-url https://$CI_SPLUNK_HEC_HOST:8089 \
	--splunk-user admin \
	--splunk-password $CI_SPLUNK_PASSWORD \
	-p no:warnings -s
