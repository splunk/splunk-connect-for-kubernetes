import pytest
import time
import os
import logging
import json
from urllib.parse import urlparse
from ..common import check_events_from_splunk, create_index_in_splunk, delete_index_in_splunk
from kubernetes import client, config
from kubernetes.client.rest import ApiException

@pytest.mark.parametrize("test_input,expected", [
    ("pods", 1),
    ("namespaces", 1),
    ("nodes", 1),
    ("events", 1)
])
def test_k8s_objects(setup, test_input, expected):
    '''
    Test that user specified index can successfully index the
    objects stream from k8s.
    '''
    logging.getLogger().info("testing test_splunk_index input={0} \
                 expected={1} event(s)".format(test_input, expected))
    index_objects = os.environ["CI_INDEX_OBJECTS"] if os.environ.get("CI_INDEX_OBJECTS") else "ci_objects"
    search_query = "index=" + index_objects
    events = check_events_from_splunk(start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(search_query)],
                                      password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                             len(events))
    assert len(events) >= expected

@pytest.mark.parametrize("test_input,expected", [
    ("kube:objects:events", 1),
    ("kube:objects:pods", 1),
    ("kube:objects:namespaces", 1),
    ("kube:objects:nodes", 1),
    ("empty_sourcetype", 0)
])
def test_k8s_objects_sourcetype(setup, test_input, expected):
    '''
    Test that known sourcetypes are present in target index
    '''
    logging.getLogger().info("testing for presence of sourcetype={0} \
                expected={1} event(s)".format(test_input, expected))
    index_objects = os.environ["CI_INDEX_OBJECTS"] if os.environ.get("CI_INDEX_OBJECTS") else "ci_objects"
    source_type = ' sourcetype=""' if test_input == "empty_sourcetype" else ' sourcetype=' + test_input
    search_query = "index=" + index_objects + source_type
    events = check_events_from_splunk(start_time="-24h@h",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  query=["search {0}".format(search_query)],
                                  password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) >= expected if test_input != "empty_sourcetype" else len(events) == expected

@pytest.mark.parametrize("test_input,expected", [
    ("dummy_host", 1),
    ("empty_host", 0)
])
def test_k8s_objects_host(setup, test_input, expected):
    '''
    Test that known hosts are present in target index
    '''
    logging.getLogger().info("testing for presence of host={0} \
                expected={1} event(s)".format(test_input, expected))
    index_objects = os.environ["CI_INDEX_OBJECTS"] if os.environ.get("CI_INDEX_OBJECTS") else "ci_objects"
    host = ' host!=""' if test_input == "dummy_host" else ' host=""'
    search_query = "index=" + index_objects + host
    events = check_events_from_splunk(start_time="-24h@h",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  query=["search {0}".format(search_query)],
                                  password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) >= expected


@pytest.mark.parametrize("test_input,expected", [
    ("dummy_source", 1),
    ("empty_source", 0)
])
def test_k8s_objects_source(setup, test_input, expected):
    '''
    Test that known sources are present in target index
    '''
    logging.getLogger().info("testing for presence of source={0} \
                expected={1} event(s)".format(test_input, expected))
    index_objects = os.environ["CI_INDEX_OBJECTS"] if os.environ.get("CI_INDEX_OBJECTS") else "ci_objects"
    source = ' source!=""' if test_input == "dummy_source" else ' source=""'
    search_query = "index=" + index_objects + source
    events = check_events_from_splunk(start_time="-24h@h",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  query=["search {0}".format(search_query)],
                                  password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) >= expected if test_input != "empty_source" else len(events) == expected

@pytest.mark.parametrize("test_input,expected", [
    ("ci-k8s-cluster-objects", 1)
])
def test_cluster_name(setup, test_input, expected):
    '''
    Test that user specified cluster-name is attached as a metadata to all the objects
    '''
    logging.getLogger().info("testing for presence of cluster_name input={0} \
                expected={1} event(s)".format(test_input, expected))
    index_objects = os.environ["CI_INDEX_OBJECTS"] if os.environ.get("CI_INDEX_OBJECTS") else "ci_objects"
    search_query = "index=" + index_objects + " cluster_name::" + test_input
    events = check_events_from_splunk(start_time="-1h@h",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  query=["search {0}".format(search_query)],
                                  password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) >= expected
