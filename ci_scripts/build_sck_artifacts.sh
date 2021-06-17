#!/usr/bin/env bash
set -e
VERSION=$(cat VERSION)
TAG="$VERSION-${GITHUB_SHA}"

function replace_generic_version() {
  file="$1"
  _line=$(awk '/version:/{print NR;exit}' $file)
  replacement="version: $TAG"
  # Escape backslash, forward slash and ampersand for use as a sed replacement.
  replacement_escaped=$(echo "$replacement" | sed -e 's/[\/&]/\\&/g')
  sed -i "${_line}s/.*/$replacement_escaped/" "$file"
}

repos_array=("helm-chart/splunk-connect-for-kubernetes" "helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-logging"
  "helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-metrics" "helm-chart/splunk-connect-for-kubernetes/charts/splunk-kubernetes-objects")

for repo in "${repos_array[@]}"; do
  filename="${repo}/Chart.yaml"
  replace_generic_version $filename
done

mkdir helm-artifacts

for repo in "${repos_array[@]}"; do
  helm package -d helm-artifacts $repo
done
