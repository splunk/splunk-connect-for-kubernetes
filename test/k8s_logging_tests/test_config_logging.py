import pytest
import time
import os
import logging
import json
import sys
from urllib.parse import urlparse
from ..common import check_events_from_splunk, create_index_in_splunk, delete_index_in_splunk
from kubernetes import client, config
from kubernetes.client.rest import ApiException

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


@pytest.mark.parametrize("test_input,expected", [
    ("test_data", 1)
])
def test_splunk_index(setup, test_input, expected):
    '''
    Test that user specified index can successfully index the
    log stream from k8s. If no index is specified, default
    index "ci_events" will be used.
    '''
    logger.info("testing test_splunk_index input={0} expected={1} event(s)".format(
        test_input, expected))
    index_logging = os.environ["CI_INDEX_EVENTS"] if os.environ.get("CI_INDEX_EVENTS") else "ci_events"
    search_query = "index=" + index_logging
    events = check_events_from_splunk(start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected


@pytest.mark.parametrize("test_input,expected", [
    ("ci-k8s-cluster", 1)
])
def test_cluster_name(setup, test_input, expected):
    '''
    Test that user specified cluster-name is attached as a metadata to all the logs
    '''
    logger.info("testing test_clusterName input={0} expected={1} event(s)".format(
        test_input, expected))
    index_logging = os.environ["CI_INDEX_EVENTS"] if os.environ.get("CI_INDEX_EVENTS") else "ci_events"
    search_query = "index=" + index_logging + " cluster_name::" + test_input
    events = check_events_from_splunk(start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected


@pytest.mark.parametrize("label,index,expected", [
    ("pod-w-index-wo-ns-index", "pod-anno", 1),
    ("pod-wo-index-w-ns-index", "ns-anno", 1),
    ("pod-w-index-w-ns-index", "pod-anno", 1)
])
def test_label_collection(setup, label, index, expected):
    '''
    Test that user specified labels is attached as a metadata to all the logs
    '''
    logger.info("testing label_app label={0} index={1} expected={2} event(s)".format(
        label, index, expected))
    search_query = "index=" + index + " label_app::" + label
    events = check_events_from_splunk(start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected


@pytest.mark.parametrize("container_name,index,expected", [
    ("pod-w-index-w-ns-index", "pod-anno", 1),
    ("pod-wo-index-w-ns-index", "ns-anno", 1),
    ("pod-w-index-wo-ns-index", "pod-anno", 1),
    ("pod-wo-index-wo-ns-index", os.environ["CI_INDEX_EVENTS"]
     if os.environ.get("CI_INDEX_EVENTS") else "ci_events", 1),
])
def test_annotation_routing(setup, container_name, index, expected):
    '''
    Test annotation routing feature. it tests different combinations of 
    namespace annotations and pod annotations.
    '''
    logger.info("testing test_annotation_routing pod={0} index={1} expected={2} event(s)".format(
        container_name, index, expected))
    search_query = "index=" + index + " container_name::" + container_name
    events = check_events_from_splunk(start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected


@pytest.mark.parametrize("container_name,expected", [
    ("pod-w-index-w-ns-exclude", 0),
    ("pod-w-exclude-wo-ns-exclude", 0)
])
def test_annotation_excluding(setup, container_name, expected):
    '''
    Test annotation excluding feature. 
    '''
    logger.info("testing test_annotation_excluding pod={0} expected={1} event(s)".format(
        container_name, expected))
    search_query = "index=*" + " container_name::" + container_name
    events = check_events_from_splunk(start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("kube:kube-apiserver", 1),
    ("kube:container:etcd", 1),
    ("kube:kube-controller-manager", 1),
    ("kube:container:splunk-fluentd-k8s-metrics-agg", 1),
    ("kube:container:splunk-fluentd-k8s-metrics", 1),
    ("kube:container:splunk-fluentd-k8s-logs", 1),
    ("kube:container:splunk-fluentd-k8s-objects", 1),
    ("empty_sourcetype", 0)
])
def test_sourcetype(setup, test_input, expected):
    '''
    Test that known sourcetypes are present in target index
    '''
    logger.info("testing for presence of sourcetype={0} expected={1} event(s)".format(
        test_input, expected))
    index_logging = os.environ["CI_INDEX_EVENTS"] if os.environ.get("CI_INDEX_EVENTS") else "ci_events"
    source_type = ' sourcetype=""' if test_input == "empty_sourcetype" else ' sourcetype=' + test_input
    search_query = "index=" + index_logging + source_type
    events = check_events_from_splunk(start_time="-24h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected if test_input != "empty_sourcetype" else len(
        events) == expected


@pytest.mark.parametrize("sourcetype,index,expected", [
    ("kube:container:pod-wo-index-w-ns-index", "ns-anno", 1),
    ("sourcetype-anno", "pod-anno", 1)
])
def test_annotation_sourcetype(setup, sourcetype, index, expected):
    '''
    Test annotation for sourcetype properly overwrites it when set
    '''
    logger.info("testing for annotation sourcetype of {0} index={1} expected={2} event(s)".format(
        sourcetype, index, expected))
    search_query = "index=" + index + ' sourcetype=' + sourcetype
    events = check_events_from_splunk(start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected


@pytest.mark.parametrize("test_input,expected", [
    ("/var/log/containers/kube-apiserver-*", 1),
    ("/var/log/containers/ci*", 1),
    ("/var/log/containers/coredns*", 1),
    ("/var/log/containers/etcd-*", 1),
    ("empty_source", 0)
])
def test_source(setup, test_input, expected):
    '''
    Test that known sources are present in target index
    '''
    logger.info("testing for presence of source={0} expected={1} event(s)".format(
        test_input, expected))
    index_logging = os.environ["CI_INDEX_EVENTS"] if os.environ.get("CI_INDEX_EVENTS") else "ci_events"
    source = ' source=""' if test_input == "empty_source" else ' source=' + test_input
    search_query = "index=" + index_logging + ' OR index="kube-system"' + source
    events = check_events_from_splunk(start_time="-24h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected if test_input != "empty_source" else len(
        events) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("dummy_host", 1),
    ("empty_host", 0)
])
def test_host(setup, test_input, expected):
    '''
    Test that known hosts are present in target index
    '''
    logger.info("testing for presence of host={0} expected={1} event(s)".format(
        test_input, expected))
    index_logging = os.environ["CI_INDEX_EVENTS"] if os.environ.get("CI_INDEX_EVENTS") else "ci_events"
    host = ' host!=""' if test_input == "dummy_host" else ' host=""'
    search_query = "index=" + index_logging + host
    events = check_events_from_splunk(start_time="-24h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected


@pytest.mark.parametrize("test_input,expected", [
    ("pod", 1),
    ("namespace", 1),
    ("container_name", 1),
    ("container_id", 1)
])
def test_default_fields(setup, test_input, expected):
    '''
    Test that default fields are attached as a metadata to all the logs
    '''
    logger.info("testing test_clusterName input={0} expected={1} event(s)".format(
        test_input, expected))
    index_logging = os.environ["CI_INDEX_EVENTS"] if os.environ.get("CI_INDEX_EVENTS") else "ci_events"
    search_query = "index=" + index_logging + " " + test_input + "::*"
    events = check_events_from_splunk(start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected


@pytest.mark.parametrize("field,value,expected", [
    ("customfield1", "customvalue1", 1),
    ("customfield2", "customvalue2", 1)
])
def test_custom_metadata_fields(setup, field,value, expected):
    '''
    Test user provided custom metadata fields are ingested with log
    '''
    logger.info("testing custom metadata field={0} value={1} expected={2} event(s)".format(
        field,value, expected))
    index_logging = os.environ["CI_INDEX_EVENTS"] if os.environ.get("CI_INDEX_EVENTS") else "ci_events"
    search_query = "index=" + index_logging + " " + field + "::" + value
    events = check_events_from_splunk(start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected



@pytest.mark.parametrize("label,index,value,expected", [
    ("pod-w-index-wo-ns-index", "pod-anno", "pod-value-2", 1),
    ("pod-wo-index-w-ns-index", "ns-anno", "ns-value", 1),
    ("pod-w-index-w-ns-index", "pod-anno", "pod-value-1", 1)
])
def test_custom_metadata_fields_annotations(setup, label, index, value, expected):

    '''
    Test that user specified labels are resolved from the user specified annotations and attached as a metadata
    to all the logs
    '''
    logger.info("testing custom metadata annotation label={0} value={1} expected={2} event(s)".format(
        label, value, expected))
    search_query = "index=" + index + " label_app::" + label + " custom_field::" + value

    events = check_events_from_splunk(start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(
                                          search_query)],
                                      password=setup["splunk_password"])
    logger.info("Splunk received %s events in the last minute",
                len(events))
    assert len(events) >= expected
