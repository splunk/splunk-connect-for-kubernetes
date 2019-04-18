#!/usr/bin/env bash
set -e
TAG="1.1.0.Alpha-${CIRCLE_SHA1}"

function replace_generic_version ()
{
  file="$1"
  _line=`awk '/version:/{print NR;exit}' $file`
  replacement="version: $TAG"
  # Escape backslash, forward slash and ampersand for use as a sed replacement.
  replacement_escaped=$( echo "$replacement" | sed -e 's/[\/&]/\\&/g' )
  sed -i "${_line}s/.*/$replacement_escaped/" "$file"
}

repos_array=( "helm-chart/splunk-connect-for-kubernetes" "helm-chart/splunk-kubernetes-logging"
              "helm-chart/splunk-kubernetes-metrics" "helm-chart/splunk-kubernetes-objects" )
sub_repos_array=( "helm-chart/splunk-kubernetes-logging"
              "helm-chart/splunk-kubernetes-metrics" "helm-chart/splunk-kubernetes-objects" )

for repo in "${repos_array[@]}"
do
  filename="${repo}/Chart.yaml"
  replace_generic_version $filename
done

mkdir helm-artifacts
mkdir helm-chart/splunk-connect-for-kubernetes/charts

for sub_repo in "${sub_repos_array[@]}"
do
  cp -rp $sub_repo helm-chart/splunk-connect-for-kubernetes/charts
done

for repo in "${repos_array[@]}"
do
  helm package -d helm-artifacts $repo
done

rm -rf helm-chart/splunk-connect-for-kubernetes/charts
