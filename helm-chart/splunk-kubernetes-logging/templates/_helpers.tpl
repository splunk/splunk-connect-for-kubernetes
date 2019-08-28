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

def extract_container_info:
  (.source | ltrimstr("/var/log/containers/") | split("_")) as $parts
  | ($parts[-1] | split("-")) as $cparts
  | .pod = $parts[0]
  | .namespace = $parts[1]
  | .container_name = ($cparts[:-1] | join("-"))
  | .container_id = ($cparts[-1] | rtrimstr(".log"))
  | .cluster_name = "{{ or .Values.kubernetes.clusterName .Values.global.kubernetes.clusterName | default "cluster_name" }}"
  {{- if .Values.custom_metadata }}
  {{- range .Values.custom_metadata }}
  | .{{ .name }} = "{{ .value }}"
  {{- end }}
  {{- end }}
  | .;

.record | extract_container_info | .sourcetype = (find_sourcetype(.pod; .container_name) // "kube:container:\(.container_name)")
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "splunk-kubernetes-logging.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "splunk-kubernetes-logging.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Create the image name
*/}}
{{- define "splunk-kubernetes-logging.image" -}}
{{- printf "%s/%s:%s" .Values.image.registry .Values.image.name .Values.image.tag -}}
{{- end -}}

{{/*
Converts a path glob to a regular expression.
*/}}
{{- define "splunk-kubernetes-logging.glob_to_regex" -}}
  {{- $str := . -}}
  {{- $str := $str | replace "\\" "\\\\" -}}
  {{- $str := $str | replace "." "\\." -}}
  {{- $str := $str | replace "*" ".*" -}}
  {{- $str := $str | replace "?" "\\?" -}}
  {{- $str := $str | replace "{" "\\{" -}}
  {{- $str := $str | replace "}" "\\}" -}}
  {{- $str := $str | replace "(" "\\(" -}}
  {{- $str := $str | replace ")" "\\)" -}}
  {{- $str := $str | replace "[" "\\[" -}}
  {{- $str := $str | replace "]" "\\]" -}}
  {{- $str := $str | replace "^" "\\^" -}}
  {{- $str := $str | replace "$" "\\$" -}}
  {{- print "^" $str "$" -}}
{{- end }}

{{/*
Generates the jq_transformer query to ensure each record has the appropriate index.
*/}}
{{- define "splunk-kubernetes-logging.index_jq_filter" -}}
  {{- if (or .Values.splunk.hec.indexRouting .Values.global.splunk.hec.indexRouting) -}}
    {{- include "splunk-kubernetes-logging.index_jq_filter_implicit" . -}}
  {{- else -}}
    {{- include "splunk-kubernetes-logging.index_jq_filter_explicit" . -}}
  {{- end -}}
{{- end -}}

{{/*
Generates the jq_transformer query to ensure each record has the appropriate index when routing by namespace.
*/}}
{{- define "splunk-kubernetes-logging.index_jq_filter_implicit" -}}
  {{- $splunkIndexRoutingDefault := or .Values.splunk.hec.indexRoutingDefaultIndex .Values.global.splunk.hec.indexRoutingDefaultIndex "main" -}}
  {{- print ".record | .index = (if .namespace == \"default\" then " ($splunkIndexRoutingDefault | quote) " else .namespace//" ($splunkIndexRoutingDefault | quote) " end)" -}}
{{- end -}}

{{/*
Generates the jq_transformer query to ensure each record has the appropriate index when not routing by namespace.
*/}}
{{- define "splunk-kubernetes-logging.index_jq_filter_explicit" -}}
  {{- $journalPath := or .Values.journalLogPath .Values.global.journalLogPath "/run/log/journal/" -}}
  {{- $splunkHecIndex := (or .Values.splunk.hec.indexName .Values.global.splunk.hec.indexName) -}}
  {{- $logDefsByIndexTag := dict -}}
  {{- range $name, $logDef := .Values.logs -}}
    {{- if (hasKey $logDef "index") -}}
      {{- $index := or $logDef.index $splunkHecIndex -}}
      {{- if (ne $index $splunkHecIndex) -}}
        {{- $sourcetype := or $logDef.sourcetype $name -}}
        {{- $tag := dict "value" "" -}}

        {{- if $logDef.from.pod -}}
          {{- $_ := set $tag "value" "tail.containers.*" -}}
        {{- else if $logDef.from.file -}}
          {{- $_ := set $tag "value" (print "tail.file." $sourcetype) -}}
        {{- else if $logDef.from.journald -}}
          {{- $_ := set $tag "value" (print "journald." $sourcetype) -}}
        {{- else -}}
          {{- print "def TODO_support_log_" $name ": " ($logDef | toJson) "; " -}}
        {{- end }}

        {{- $logDefsByTag := or (pluck $index $logDefsByIndexTag | first) (dict) -}}
        {{- $logDefs := or (pluck $tag.value | first) (list) -}}
        {{- $appendedLogDefs := append $logDefs (and (set $logDef "name" $name)) -}}
        {{- $appendedLogDefsByTag := set $logDefsByTag $tag.value $appendedLogDefs -}}
        {{- $_ := set $logDefsByIndexTag $index $appendedLogDefsByTag -}}
      {{- end }}
    {{- end }}
  {{- end }}

  {{- $isFirstIndex := dict "value" true -}}
  {{- range $index, $logDefsByTag := $logDefsByIndexTag -}}
    {{- if $isFirstIndex.value -}}
      {{- print "if" -}}
      {{- $_ := set $isFirstIndex "value" false -}}
    {{- else -}}
    {{- print " elif" -}}
    {{- end }}
    {{- $isFirstTag := dict "value" true -}}
    {{- range $tag, $logDefs := $logDefsByTag -}}
      {{- if $isFirstTag.value -}}
        {{- print " (" -}}
        {{- $_ := set $isFirstTag "value" false -}}
      {{- else -}}
        {{- print " or (" -}}
      {{- end }}
      {{- print ".tag == " ($tag | quote) " and (" -}}
      {{- $isFirstLogDef := dict "value" true -}}
      {{- range $logDef := $logDefs -}}
        {{- if $isFirstLogDef.value -}}
          {{- print "(" -}}
          {{- $_ := set $isFirstLogDef "value" false -}}
        {{- else -}}
          {{- print " or (" -}}
        {{- end }}
        {{- print ".record.sourcetype == " (or $logDef.sourcetype $logDef.name | quote) -}}

        {{- if $logDef.from.file -}}
          {{- print " and (.record.source | test(" (include "splunk-kubernetes-logging.glob_to_regex" $logDef.from.file.path | quote) "))" -}}
        {{- else if $logDef.from.journald -}}
          {{- print " and .record.source == " (print $journalPath $logDef.from.journald.unit | quote) -}}
        {{- else if $logDef.from.pod -}}
          {{- print " and (.record.pod | startswith(" ($logDef.from.pod | quote) "))" -}}
          {{- if (hasKey $logDef.from "container") -}}
            {{- print " and .record.container == " ($logDef.from.container | quote) -}}
          {{- end }}
        {{- end }}
        {{- print ")" -}}
      {{- end }}
      {{- print "))" -}}
    {{- end }}
    {{- print " then .record | .index = " ($index | quote) -}}
  {{- end }}
  {{- $isAnyIndex := ne 0 (len $logDefsByIndexTag) -}}
  {{- if $isAnyIndex -}}
    {{- print " else " -}}
  {{- end }}
  {{- print ".record | .index = " ($splunkHecIndex | quote) -}}
  {{- if $isAnyIndex -}}
    {{- print " end" -}}
  {{- end }}
{{- end }}
