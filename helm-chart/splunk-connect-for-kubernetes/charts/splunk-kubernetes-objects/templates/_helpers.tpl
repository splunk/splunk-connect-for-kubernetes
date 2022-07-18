{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "splunk-kubernetes-objects.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "splunk-kubernetes-objects.fullname" -}}
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
{{- define "splunk-kubernetes-objects.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Get namespace to deploy to.
*/}}
{{- define "splunk-kubernetes-objects.namespace" -}}
{{- if .Values.namespace -}}
{{- .Values.namespace -}}
{{- else -}}
{{- .Release.Namespace -}}
{{- end -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "splunk-kubernetes-objects.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "splunk-kubernetes-objects.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Create secret to be used.
*/}}
{{- define "splunk-kubernetes-objects.secret" -}}
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
{{- define "splunk-kubernetes-objects.convert-memory" -}}
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
Create the image name
*/}}
{{- define "splunk-kubernetes-objects.image" -}}
{{- if contains .Values.image.tag "sha256" -}}
{{- printf "%s/%s@%s" .Values.image.registry .Values.image.name .Values.image.tag -}}
{{- else -}}
{{- printf "%s/%s:%s" .Values.image.registry .Values.image.name .Values.image.tag -}}
{{- end -}}
{{- end -}}

{{/*  evaluate field consume_chunk_on_4xx_errors */}}
{{- define "splunk-kubernetes-objects.should_consume_chunk_on_4xx_errors" -}}
{{- if ne .Values.splunk.hec.consume_chunk_on_4xx_errors nil -}}
{{- print .Values.splunk.hec.consume_chunk_on_4xx_errors -}}
{{- else if ne .Values.global.splunk.hec.consume_chunk_on_4xx_errors nil -}}
{{- print .Values.global.splunk.hec.consume_chunk_on_4xx_errors -}}
{{- else -}}
{{- print true -}}
{{- end -}}
{{- end -}}
