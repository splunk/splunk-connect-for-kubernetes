#!/usr/bin/env bash
set -e
echo "Pushing SCK artifacts to s3..."
aws s3 cp helm-artifacts/splunk-kubernetes-logging*.tgz s3://k8s-ci-artifacts/
aws s3 cp helm-artifacts/splunk-kubernetes-metrics*.tgz s3://k8s-ci-artifacts/
aws s3 cp helm-artifacts/splunk-kubernetes-objects*.tgz s3://k8s-ci-artifacts/
aws s3 cp helm-artifacts/splunk-connect-for-kubernetes*.tgz s3://k8s-ci-artifacts/
