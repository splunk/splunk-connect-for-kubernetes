{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "splunk-kubernetes-logging.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "splunk-kubernetes-logging.fullname" -}}
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
{{- define "splunk-kubernetes-logging.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Get namespace to deploy to.
*/}}
{{- define "splunk-kubernetes-logging.namespace" -}}
{{- if .Values.namespace -}}
{{- .Values.namespace -}}
{{- else -}}
{{- .Release.Namespace -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "splunk-kubernetes-logging.secret" -}}
{{- if .Values.secret.name -}}
{{- printf "%s" .Values.secret.name -}}
{{- else -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{/*
Convert memory value from resources.limit to fluentd buffer.
Rules:
* fluentd does not support *i units
* fluentd does not support E and P
*/}}
{{- define "splunk-kubernetes-logging.convert-memory" -}}
{{- $mem := lower . -}}
{{- if hasSuffix "p" $mem -}}
{{- printf "%sT" (trimSuffix "p" $mem | atoi | mul 1000 | toString) -}}
{{- else if hasSuffix "pi" $mem -}}
{{- printf "%sT" (trimSuffix "pi" $mem | atoi | mul 1024 | toString) -}}
{{- else if hasSuffix "e" $mem -}}
{{- printf "%sT" (trimSuffix "e" $mem | atoi | mul 1000 1000 | toString) -}}
{{- else if hasSuffix "ei" $mem -}}
{{- printf "%sT" (trimSuffix "ei" $mem | atoi | mul 1024 1024 | toString) -}}
{{- else if hasSuffix "ti" $mem -}}
{{- printf "%sT" (1000 | div (trimSuffix "ti" $mem | atoi | mul 1024) | toString) -}}
{{- else if hasSuffix "gi" $mem -}}
{{- printf "%sG" (1000 | div (trimSuffix "gi" $mem | atoi | mul 1024) | toString) -}}
{{- else if hasSuffix "mi" $mem -}}
{{- printf "%sM" (1000 | div (trimSuffix "mi" $mem | atoi | mul 1024) | toString) -}}
{{- else if hasSuffix "ki" $mem -}}
{{- printf "%sK" (1000 | div (trimSuffix "ki" $mem | atoi | mul 1024) | toString) -}}
{{- else -}}
{{- $mem -}}
{{- end -}}
{{- end -}}


{{/*
The jq filter used to generate source and sourcetype for container logs.
Define it as a template here so there we don't need to escape the double quotes `` " ''.
To find the sourcetype, it cannot use map here, because the `pod` extracted from source
is not exact the pod name. That's why we generated all those `if-elif-then` here.
*/}}
{{- define "splunk-kubernetes-logging.container_jq_filter" -}}
{{- $logs := dict "list" list }}
{{- range $name, $logDef := .Values.logs }}
{{- if (and $logDef.from.pod $logDef.sourcetype) }}
{{- set $logs "list" (append $logs.list (dict "name" $name "from" $logDef.from "sourcetype" $logDef.sourcetype)) | and nil }}
{{- end }}
{{- end -}}
def find_sourcetype(pod; container_name):
{{- with first $logs.list }}
container_name + "/" + pod |
if startswith({{ list (or .from.container .name) .from.pod | join "/" | quote }}) then {{ .sourcetype | quote }}
{{- end }}
{{- range rest $logs.list }}
elif startswith({{ list (or .from.container .name) .from.pod | join "/" | quote }}) then {{ .sourcetype | quote }}
{{- end }}
else empty
end;

def set_index(value):
if value == "default"
then
{{- $index := or .Values.splunk.hec.indexRoutingDefaultIndex .Values.global.splunk.hec.indexRoutingDefaultIndex | default "main" | quote }}
{{- printf " %s" $index -}}
else value
end;

def extract_container_info:
  (.source | ltrimstr("/var/log/containers/") | split("_")) as $parts
  | ($parts[-1] | split("-")) as $cparts
  | .pod = $parts[0]
  | .namespace = $parts[1]
  | .index = set_index($parts[1])
  | .container_name = ($cparts[:-1] | join("-"))
  | .container_id = ($cparts[-1] | rtrimstr(".log"))
  | .cluster_name = "{{ or .Values.kubernetes.clusterName .Values.global.kubernetes.clusterName | default "cluster_name" }}"
  {{- if .Values.customMetadata }}
  {{- range .Values.customMetadata }}
  | .{{ .name }} = "{{ .value }}"
  {{- end }}
  {{- end }}
  | .;

.record | extract_container_info | .sourcetype = (find_sourcetype(.pod; .container_name) // "kube:container:\(.container_name)")
{{- end -}}


{{- define "splunk-kubernetes-logging.set_sourcetype" -}}
{{- $logs := dict "list" list }}
{{- range $name, $logDef := .Values.logs }}
{{- if (and $logDef.from.pod $logDef.sourcetype) }}
{{- set $logs "list" (append $logs.list (dict "name" $name "from" $logDef.from "sourcetype" $logDef.sourcetype)) | and nil }}
{{- end }}
{{- end -}}
def find_sourcetype(pod; container_name):
{{- with first $logs.list }}
container_name + "/" + pod |
if startswith({{ list (or .from.container .name) .from.pod | join "/" | quote }}) then {{ .sourcetype | quote }}
{{- end }}
{{- range rest $logs.list }}
elif startswith({{ list (or .from.container .name) .from.pod | join "/" | quote }}) then {{ .sourcetype | quote }}
{{- end }}
else empty
end;

.record | .sourcetype = (find_sourcetype(.pod; .container_name) // "kube:container:\(.container_name)")
{{- end -}}


{{/*
Create the name of the service account to use
*/}}
{{- define "splunk-kubernetes-logging.serviceAccountName" -}}
    {{ default (include "splunk-kubernetes-logging.fullname" .) .Values.serviceAccount.name }}
{{- end -}}
Create the image name
*/}}
{{- define "splunk-kubernetes-logging.image" -}}
{{- if contains .Values.image.tag "sha256" -}}
{{- printf "%s/%s@%s" .Values.image.registry .Values.image.name .Values.image.tag -}}
{{- else -}}
{{- printf "%s/%s:%s" .Values.image.registry .Values.image.name .Values.image.tag -}}
{{- end -}}
{{- end -}}

{{/*  evaluate field consume_chunk_on_4xx_errors */}}
{{- define "splunk-kubernetes-logging.should_consume_chunk_on_4xx_errors" -}}
{{- if ne .Values.splunk.hec.consume_chunk_on_4xx_errors nil -}}
{{- print .Values.splunk.hec.consume_chunk_on_4xx_errors -}}
{{- else if ne .Values.global.splunk.hec.consume_chunk_on_4xx_errors nil -}}
{{- print .Values.global.splunk.hec.consume_chunk_on_4xx_errors -}}
{{- else -}}
{{- print true -}}
{{- end -}}
{{- end -}}
