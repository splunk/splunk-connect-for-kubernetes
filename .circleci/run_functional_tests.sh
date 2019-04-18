#!/usr/bin/env bash
set -e
cd test
sudo pip3 install --upgrade pip
sudo pip3 install -r requirements.txt
#Run pytests
echo "Running functional tests....."
python3 -m pytest \
	--splunkd-url https://$SPLUNK_HEC_HOST:8089 \
	--splunk-user admin \
	--splunk-password $SPLUNK_PASSWORD \
	-p no:warnings