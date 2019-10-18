#!/usr/bin/env bash
set -e
pyenv global 3.6.5
cd test
sudo pip install --upgrade pip
sudo pip install -r requirements.txt
#Run pytests
echo "Running functional tests....."
python -m pytest \
	--splunkd-url https://$CI_SPLUNK_HEC_HOST:8089 \
	--splunk-user admin \
	--splunk-password $CI_SPLUNK_PASSWORD \
	-p no:warnings -s
