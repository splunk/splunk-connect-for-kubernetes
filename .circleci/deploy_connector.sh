#!/usr/bin/env bash
set -e
#Update helm server version
helm init --force-upgrade
# Wait for helm to be ready 
until kubectl get pod --all-namespaces | grep tiller | grep -q "1\/1"; do
   sleep 1;
done 
#Make sure to check and clean previously failed deployment
echo "Checking if previous deployment exist..."
if [ "`helm ls`" == "" ]; then
   echo "Nothing to clean, ready for deployment"
else
   helm delete --purge $(helm ls --short)
fi
echo "Deploying k8s-connect with latest changes"
helm install --name=ci-$CIRCLE_SHA1 -f .circleci/sck_values.yml helm-artifacts/splunk-connect-for-kubernetes*.tgz
#wait for deployment to finish
until kubectl get pod | grep Running | [[ $(wc -l) == 4 ]]; do
   sleep 1;
done