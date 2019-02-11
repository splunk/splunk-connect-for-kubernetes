import pytest
import time
import os
import logging
import json
from urllib.parse import urlparse
from ..common import check_events_from_splunk


@pytest.mark.parametrize("test_input,expected", [
    ("test_data", 1)
])
def test_splunk_index(setup, test_input, expected):
    '''
    Test that user specified index can successfully index the
    log stream from k8s. If no index is specified, default
    index "circleci_events" will be used.
    '''
    logging.getLogger().info("testing test_splunk_index input={0} \
                 expected={1} event(s)".format(test_input, expected))
    search_query = "index=circleci_events"
    events = check_events_from_splunk(start_time="-34h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(search_query)],
                                      password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                             len(events))
    assert len(events) >= expected


@pytest.mark.parametrize("test_input,expected", [
    ("circleci-k8s-cluster", 1)
])
def test_cluster_name(setup, test_input, expected):
    '''
    Clustername is a configurable parameter, test that user specified cluster-name is attached as a metadata to all the logs
    '''
    logging.getLogger().info("testing test_clusterName input={0} \
                expected={1} event(s)".format(test_input, expected))
    search_query = "index=circleci_events cluster_name=circleci-k8s-cluster | head 1"
    events = check_events_from_splunk(start_time="-24h@h",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  query=["search {0}".format(search_query)],
                                  password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) == expected

@pytest.mark.parametrize("test_input,expected", [
    ("kube:kube-apiserver", 1),
    ("fluentd:monitor-agent", 1),
    ("kube:container:splunk-fluentd-k8s-metrics-agg", 1),
    ("kube:container:splunk-fluentd-k8s-metrics", 1),
    ("kube:container:splunk-fluentd-k8s-logs", 1),
    ("kube:dns-controller", 1),
    ("kube:etcd", 1),
    ("kube:container:splunk-fluentd-k8s-objects", 1),
    ("kube:container:tiller", 1),
    ("kube:kube-controller-manager", 1)
])
def test_sourcetype(setup, test_input, expected):
    '''
    Test that known sourcetypes are present in target index
    '''
    logging.getLogger().info("testing for presence of sourcetype={0} \
                expected={1} event(s)".format(test_input, expected))
    events = check_events_from_splunk(start_time="-24h@h",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  query=["search index=circleci_events sourcetype={0}".format(test_input)],
                                  password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) >= expected

@pytest.mark.parametrize("test_input,expected", [
    ("/var/log/containers/kube-apiserver-ip*", 1),
    ("/var/log/containers/ci*", 1),
    ("namespace:default/pod:ci*", 1),
    ("/var/log/containers/dns-controller*", 1),
    ("/var/log/containers/etcd-server-ip*", 1)
])
def test_source(setup, test_input, expected):
    '''
    Test that known sources are present in target index
    '''
    logging.getLogger().info("testing for presence of sourcetype={0} \
                expected={1} event(s)".format(test_input, expected))
    events = check_events_from_splunk(start_time="-24h@h",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  query=["search index=circleci_events source={0}".format(test_input)],
                                  password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) >= expected

