{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "splunk-kubernetes-metrics.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "splunk-kubernetes-metrics.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "splunk-kubernetes-metrics.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{/*
The jq filter used to transform Heapster metrics which are formatted in statd format.
Define it as a template here so there we don't need to escape the double quotes `` " ''.
*/}}
{{- define "splunk-kubernetes-metrics.jq_filter" -}}
def extract_labels:
  . as $labels | reduce range(length) as $n ({}; if $n % 2 == 0 then .["label." + $labels[$n]] = $labels[$n + 1] else . end);

def extract_metric:
  if length % 2 == 0
  then (.[:-2] | extract_labels) + {metric: (.[-2] | gsub("/"; ".")), resource_id: .[-1]}
  else (.[:-1] | extract_labels) + {metric: (.[-1] | gsub("/"; "."))}
  end;
  
def extract_container:
  split(".") | {container_type: "pod", node: .[1], namespace: .[3], pod: .[5], container: .[7]} + (.[8:] | extract_metric) | .metric = "container." + .metric | . ;
  
def extract_syscontainer:
  split(".") | {container_type: "sys", node: .[1], container: .[3]} + (.[4:] | extract_metric) | .metric = "container." + .metric | . ;
  
def extract_pod:
  split(".") | {node: .[1], namespace: .[3], pod: .[5]} + (.[6:] | extract_metric) | .metric = "pod." + .metric | . ;
  
def extract_namespace:
  split(".") | {namespace: .[1]} + (.[2:] | extract_metric) | .metric = "namespace." + .metric | . ;
  
def extract_node:
  split(".") | {node: .[1]} + (.[2:] | extract_metric) | .metric = "node." + .metric | . ;
  
def extract_cluster:
  split(".") | .[1:] | extract_metric | .metric = "cluster." + .metric | . ;

def extract:
  if contains(".container.")
  then extract_container
  elif contains(".sys-container.")
  then extract_syscontainer
  elif contains(".pod.")
  then extract_pod
  elif startswith("namespace.")
  then extract_namespace
  elif startswith("node.")
  then extract_node
  elif startswith("cluster.")
  then extract_cluster
  else {}
  end;

 "heapster/namespace:\(env.MY_NAMESPACE)/pod:\(env.MY_POD_NAME)" as $source | .record | to_entries | map({value, source: $source} + (.key | extract)) | .
{{- end -}}
