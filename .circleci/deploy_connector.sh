#!/usr/bin/env bash
set -e
echo "Setup kube client..."
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
sudo apt-get -y install gnupg
sudo mkdir ~/.kube
echo $GPG_KEY | gpg --output config --passphrase-fd 0 --decrypt --batch .circleci/kubeconfig.gpg
sudo mv config ~/.kube/config
#Make sure to check and clean previously failed deployment
echo "Checking if previous deployment exist..."
if [ "`helm ls`" == "" ]; then
   echo "Nothing to clean, ready for deployment"
else
   helm delete --purge $(helm ls --short)
fi
echo "Deploying k8s-connect with latest changes"
helm install --name=ci-$CIRCLE_SHA1 -f .circleci/sck_values.yml helm-artifacts/splunk-connect-for-kubernetes*.tgz
#Todo-need to add test cases and run them before cleaning the deployment
#wait for deployment to finish, sleep longer for metrics-aggr to start sending metrics
sleep 90