import pytest
import time
import os
import logging
import json
from urllib.parse import urlparse
from ..common import check_events_from_splunk
from ..common import collect_metric_from_splunk
from test.k8s_metrics_tests.metric_data.aggregated import (
    container_limit_request,
    aggregated_metrics,
)


@pytest.fixture(scope="session")
def index_metrics():
    index_metrics = (
        os.environ["CI_INDEX_METRICS"]
        if os.environ.get("CI_INDEX_METRICS")
        else "ci_metrics"
    )
    return index_metrics


@pytest.mark.parametrize(
    "aggregated_metric",
    aggregated_metrics,
    ids=[metric["name"] for metric in aggregated_metrics],
)
def test_metric_name_on_metrics_aggregator(setup, aggregated_metric, index_metrics):
    events = collect_metric_from_splunk(
        aggregated_metric["name"],
        index_metrics,
        aggregated_metric["selector"],
        url=setup["splunkd_url"],
        user=setup["splunk_user"],
        password=setup["splunk_password"],
    )
    for assert_func, value in aggregated_metric["assertions"]:
        assert_func(events, value)


def test_container_limit_and_requests(setup, index_metrics):
    containers = [
        "splunk-fluentd-k8s-metrics-agg",
        "splunk-fluentd-k8s-metrics",
        "splunk-fluentd-k8s-logs",
        "splunk-fluentd-k8s-objects",
    ]
    selector = "name"

    for resource in ["cpu", "memory"]:
        for metric in ["limit", "request"]:
            logging.info(
                "testing {} metric".format(f"kube.container.{resource}.{metric}")
            )
            events = collect_metric_from_splunk(
                f"kube.container.{resource}.{metric}",
                index_metrics,
                selector,
                url=setup["splunkd_url"],
                user=setup["splunk_user"],
                password=setup["splunk_password"],
                func="avg",
            )
            actual_data = container_limit_request[resource][metric]
            for container_name in containers:
                assert events[container_name] == actual_data[container_name]


def test_pod_and_cluster_limit_and_requests(setup, index_metrics):
    containers = [
        "splunk-fluentd-k8s-metrics-agg",
        "splunk-fluentd-k8s-metrics",
        "splunk-fluentd-k8s-logs",
        "splunk-fluentd-k8s-objects",
    ]
    pods = [
        "splunk-kubernetes-metrics-agg",
        "splunk-kubernetes-metrics",
        "splunk-kubernetes-logging",
        "splunk-kubernetes-objects",
    ]
    selector = "name"
    for resource in ["cpu", "memory"]:
        for metric in ["limit", "request"]:
            logging.info("testing {} metric".format(f"kube.pod.{resource}.{metric}"))
            events = collect_metric_from_splunk(
                f"kube.pod.{resource}.{metric}",
                index_metrics,
                selector,
                url=setup["splunkd_url"],
                user=setup["splunk_user"],
                password=setup["splunk_password"],
                func="avg",
            )
            actual_data = container_limit_request[resource][metric]
            total = 0
            count = 0
            for pod_name, value in events.items():
                total += value
                for container, pod in zip(containers, pods):
                    if pod in pod_name:
                        count += 1
                        assert value == actual_data[container]
                        break
            logging.info(
                "testing {} metric".format(f"kube.cluster.{resource}.{metric}")
            )
            # count should number of logging deamonset + number of metrics deamonset + one metric-aggr pod + one object deamonset
            assert count == 2 * setup["nodes_count"] + 2
            events = collect_metric_from_splunk(
                f"kube.cluster.{resource}.{metric}",
                index_metrics,
                "cluster_name",
                url=setup["splunkd_url"],
                user=setup["splunk_user"],
                password=setup["splunk_password"],
                func="avg",
            )
            assert list(events.values())[0] == total


def test_namespace_limit_and_requests(setup, index_metrics):
    selector = "name"
    nodes = setup["nodes_count"]
    for resource in ["cpu", "memory"]:
        for metric in ["limit", "request"]:
            logging.info(
                "testing {} metric".format(f"kube.namespace.{resource}.{metric}")
            )
            events = collect_metric_from_splunk(
                f"kube.namespace.{resource}.{metric}",
                index_metrics,
                selector,
                url=setup["splunkd_url"],
                user=setup["splunk_user"],
                password=setup["splunk_password"],
                func="avg",
            )
            actual_data = container_limit_request[resource][metric]
            assert (
                events["default"]
                == (
                    actual_data["splunk-fluentd-k8s-logs"]
                    + actual_data["splunk-fluentd-k8s-metrics"]
                )
                * nodes
                + actual_data["splunk-fluentd-k8s-objects"]
                + actual_data["splunk-fluentd-k8s-metrics-agg"]
            )
