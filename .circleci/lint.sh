#!/usr/bin/env bash
set -e

# chart template linting
wget https://github.com/helm/chart-testing/releases/download/v2.3.3/chart-testing_2.3.3_linux_amd64.tar.gz
tar -xvf chart-testing_2.3.3_linux_amd64.tar.gz
sudo chmod +x ct
sudo mv ct /usr/local/bin/ct

# lint helm charts
echo "Linting charts"
helm lint helm-chart/*
echo "Linting charts with CI values"
helm lint --values .circleci/sck_values.yml helm-chart/*
cd .circleci
echo "Linting charts ct lint tool"
ct lint helm-chart/*
