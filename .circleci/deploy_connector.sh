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
helm install ci-sck -f .circleci/sck_values.yml helm-artifacts/splunk-connect-for-kubernetes*.tgz
#wait for deployment to finish
until kubectl get pod | grep Running | [[ $(wc -l) == 4 ]]; do
   sleep 1;
done