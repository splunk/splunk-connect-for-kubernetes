#!/usr/bin/env bash
set -e

#Make sure to check and clean previously failed deployment
echo "Checking if previous deployment exist..."
if [ "`helm ls --short`" == "" ]; then
   echo "Nothing to clean, ready for deployment"
else
   helm delete $(helm ls --short)
fi
echo "Deploying k8s-connect with latest changes"
helm install ci-sck --set global.splunk.hec.token=$CI_SPLUNK_HEC_TOKEN \
--set global.splunk.hec.host=$CI_SPLUNK_HOST \
--set kubelet.serviceMonitor.https=true \
-f ci_scripts/sck_values.yml helm-artifacts/splunk-connect-for-kubernetes*.tgz
#wait for deployment to finish
# 2 logging, 2 metrics, 1 aggregator, 1 object 
until kubectl get pod | grep Running | [[ $(wc -l) == 7 ]]; do
   sleep 5;
done