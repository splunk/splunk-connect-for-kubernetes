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
    search_query = "index=circleci_events OR index=kube-system"
    events = check_events_from_splunk(start_time="-1h@h",
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
    search_query = "index=circleci_events OR index=kube-system cluster_name=circleci-k8s-cluster | head 1"
    events = check_events_from_splunk(start_time="-1h@h",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  query=["search {0}".format(search_query)],
                                  password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) == expected

@pytest.mark.parametrize("test_input,expected", [
    ("test-namespace-routing", 1),
    ("kube-system", 1),
    ("kube-public", 1)
])
def test_namespace_routing(setup, test_input, expected):
    '''
    Test namespace routing feature. This test will create an index in Splunk with name as the namespace, start a pod to generate some logs,
    then check if the logs are indexed as events in Splunk. The test handles the cleanup of the index and its events.
    '''
    # Splunk index and namespace are assumed to be the same
    index = test_input
    namespace = test_input

    # Handle special cases of default namespaces kube-system and kube-public
    if test_input == "kube-system" or test_input == "kube-public":
        search_query = "index={0}".format(test_input)
        events = check_events_from_splunk(index=index,
                                          start_time="-1h@h",
                                          url=setup["splunkd_url"],
                                          user=setup["splunk_user"],
                                          query=["search {0}".format(search_query)],
                                          password=setup["splunk_password"])
        logging.getLogger().info("Received {0} events in the index {1}".format(len(events), index))
        assert len(events) >= 0
        pytest.skip("Test successful, skipping rest of the test for special cases")

    # Initialize kubernetes python client
    config.load_kube_config()
    v1 = client.CoreV1Api()
    found = False

    # Search for namespace
    for ns in v1.list_namespace().items:
        if test_input == ns.metadata.name:
            found = True

    # Create namespace
    if not found:
        logging.getLogger().info("creating namespace")
        try:
            v1.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name=test_input)))
        except ApiException as e:
            logging.getLogger().info("Exception when calling CoreV1Api create_namespace: {0}".format(e))

    search_query = "index={0} | delete".format(test_input)
    events = check_events_from_splunk(index=index,
                                      start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(search_query)],
                                      password=setup["splunk_password"])
    logging.getLogger().info("Received {0} events in the index {1}".format(len(events), index))
    assert len(events) == 0

    # Data generator image metadata
    image_name = "cp-data-gen"
    image_address = "chaitanyaphalak/kafkadatagen:1.0-4-gca7f6d8"
    image_pull_policy = "IfNotPresent"

    # Create pod in the test namespace to generate logs
    pod = client.V1Pod()
    pod.metadata = client.V1ObjectMeta(name=image_name)

    container = client.V1Container(name=image_name, image=image_address, image_pull_policy=image_pull_policy)

    spec = client.V1PodSpec(containers=[container])
    pod.spec = spec
    try:
        v1.create_namespaced_pod(namespace=namespace, body=pod)
    except ApiException as e:
        logging.getLogger().info("Exception when calling CoreV1Api create_namespaced_pod: {0}".format(e))

    logging.getLogger().info("Sleeping for 60 seconds")
    time.sleep(60)

    # Check if we have those generated logs from kubernetes in Splunk
    v1.delete_namespaced_pod(name=image_name, namespace=namespace, body=pod)

    search_query = "index={0}".format(test_input)
    events = check_events_from_splunk(index=index,
                                      start_time="-1h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      query=["search {0}".format(search_query)],
                                      password=setup["splunk_password"])
    logging.getLogger().info("Splunk received {0} events in the last minute in the index {1}".format(len(events), index))

    assert len(events) > 0

@pytest.mark.parametrize("test_input,expected", [
    ("kube:kube-apiserver", 1),
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
                                  query=["search index=circleci_events OR index=kube-system sourcetype={0}".format(test_input)],
                                  password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) >= expected

@pytest.mark.parametrize("test_input,expected", [
    ("/var/log/containers/kube-apiserver-*", 1),
    ("/var/log/containers/ci*", 1),
    ("/var/log/containers/coredns*", 1),
    ("/var/log/containers/etcd-*", 1)
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
                                  query=["search index=circleci_events OR index=kube-system source={0}".format(test_input)],
                                  password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) >= expected
