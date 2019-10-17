#!/usr/bin/env bash
set -e
cd test
sudo pip install --upgrade pip
sudo pip install -r requirements.txt
#Run pytests
echo "Running functional tests....."
python3 -m pytest \
	--splunkd-url https://$CI_SPLUNK_HEC_HOST:8089 \
	--splunk-user admin \
	--splunk-password $CI_SPLUNK_PASSWORD \
	-p no:warnings -s
