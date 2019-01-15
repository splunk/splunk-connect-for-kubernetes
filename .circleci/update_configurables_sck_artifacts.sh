#!/bin/bash
set -e
# Install yq yaml parser
wget https://github.com/mikefarah/yq/releases/download/2.2.1/yq_linux_amd64
sudo chmod +x yq_linux_amd64
sudo mv yq_linux_amd64 /usr/local/bin/yq

# Modify splunk environment values
yq w -i .circleci/sck_values.yaml global.splunk.hec.host $SPLUNK_HOST
yq w -i .circleci/sck_values.yaml global.splunk.hec.token $SPLUNK_TOKEN
yq w -i .circleci/sck_values.yaml splunk-kubernetes-logging.splunk.hec.indexName $SPLUNK_INDEX_LOGGING
yq w -i .circleci/sck_values.yaml splunk-kubernetes-metrics.splunk.hec.indexName $SPLUNK_INDEX_METRICS
yq w -i .circleci/sck_values.yaml splunk-kubernetes-objects.splunk.hec.indexName $SPLUNK_INDEX_OBJECTS

# Modify docker images to be used
image_name=$(echo "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/k8s-ci-logging:latest")
yq w -i .circleci/sck_values.yaml splunk-kubernetes-logging.image.name $image_name
image_name=$(echo "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/k8s-ci-metrics:latest")
yq w -i .circleci/sck_values.yaml splunk-kubernetes-metrics.image.name $image_name
image_name=$(echo "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/k8s-ci-metrics-agg:latest")
yq w -i .circleci/sck_values.yaml splunk-kubernetes-metrics.imageAgg.name $image_name
image_name=$(echo "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/k8s-ci-objects:latest")
yq w -i .circleci/sck_values.yaml splunk-kubernetes-objects.image.name $image_name
