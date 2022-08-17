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
Create secret to be used.
*/}}
{{- define "splunk-kubernetes-metrics.secret" -}}
{{- if .Values.secret.name -}}
{{- printf "%s" .Values.secret.name -}}
{{- else -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "splunk-kubernetes-metrics.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Get namespace to deploy to.
*/}}
{{- define "splunk-kubernetes-metrics.namespace" -}}
{{- if .Values.namespace -}}
{{- .Values.namespace -}}
{{- else -}}
{{- .Release.Namespace -}}
{{- end -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "splunk-kubernetes-metrics.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "splunk-kubernetes-metrics.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Create the image name
*/}}
{{- define "splunk-kubernetes-metrics.image" -}}
{{- if contains .Values.image.tag "sha256" -}}
{{- printf "%s/%s@%s" .Values.image.registry .Values.image.name .Values.image.tag -}}
{{- else -}}
{{- printf "%s/%s:%s" .Values.image.registry .Values.image.name .Values.image.tag -}}
{{- end -}}
{{- end -}}
{{/*
Create the aggregate image name
*/}}
{{- define "splunk-kubernetes-metrics.imageAgg" -}}
{{- if contains .Values.imageAgg.tag "sha256" -}}
{{- printf "%s/%s@%s" .Values.imageAgg.registry .Values.imageAgg.name .Values.imageAgg.tag -}}
{{- else -}}
{{- printf "%s/%s:%s" .Values.imageAgg.registry .Values.imageAgg.name .Values.imageAgg.tag -}}
{{- end -}}
{{- end -}}

{{/*  evaluate field consume_chunk_on_4xx_errors */}}
{{- define "splunk-kubernetes-metrics.should_consume_chunk_on_4xx_errors" -}}
{{- if ne .Values.splunk.hec.consume_chunk_on_4xx_errors nil -}}
{{- print .Values.splunk.hec.consume_chunk_on_4xx_errors -}}
{{- else if ne .Values.global.splunk.hec.consume_chunk_on_4xx_errors nil -}}
{{- print .Values.global.splunk.hec.consume_chunk_on_4xx_errors -}}
{{- else -}}
{{- print true -}}
{{- end -}}
{{- end -}}
