import json
import pytest
import sys
import os
import logging
from urllib.parse import urlparse
from ..common import check_events_from_splunk
from ..common import collect_metric_from_splunk
from test.k8s_metrics_tests.metric_data.aggregated import (
    container_limit_request,
    aggregated_metrics,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


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
        assert_func(aggregated_metric, events, value)


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
            logger.info(
                "testing {} metric".format(f"kube.container.{resource}.{metric}")
            )
            events = collect_metric_from_splunk(
                f"kube.container.{resource}.{metric}",
                index_metrics,
                selector,
                url=setup["splunkd_url"],
                user=setup["splunk_user"],
                password=setup["splunk_password"],
                func="latest",
            )
            actual_data = container_limit_request[resource][metric]
            for container_name in containers:
                if events[container_name] != actual_data[container_name]:
                    logger.info(
                        "{} metric received by splunk: \n{}".format(
                            f"kube.container.{resource}.{metric}",
                            json.dumps(events, indent=2),
                        )
                    )
                    pytest.fail(
                        f"Received invalid kube.container.{resource}.{metric} metric for container {container_name}"
                    )


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
            logger.info("testing {}".format(f"kube.pod.{resource}.{metric}"))
            events = collect_metric_from_splunk(
                f"kube.pod.{resource}.{metric}",
                index_metrics,
                selector,
                url=setup["splunkd_url"],
                user=setup["splunk_user"],
                password=setup["splunk_password"],
                func="latest",
            )

            actual_data = container_limit_request[resource][metric]
            # Total holds cluster limit/request
            total = 0
            # Count
            count = 0
            for pod_name, value in events.items():
                total += value
                for container, pod in zip(containers, pods):
                    if pod in pod_name:
                        count += 1
                        if value != actual_data[container]:
                            logger.info(
                                "{} metric received by splunk: \n{}".format(
                                    f"kube.pod.{resource}.{metric}",
                                    json.dumps(events, indent=2),
                                )
                            )
                            pytest.fail()
                        break
            logger.info("testing {}".format(f"kube.cluster.{resource}.{metric}"))

            assert (
                count == 2 * setup["nodes_count"] + 2
            ), f"count should be equal to number of logging deamonset + number of metrics deamonset + one metric-aggr pod + one object deamonset. Make sure correct node count is provided."
            events = collect_metric_from_splunk(
                f"kube.cluster.{resource}.{metric}",
                index_metrics,
                "cluster_name",
                url=setup["splunkd_url"],
                user=setup["splunk_user"],
                password=setup["splunk_password"],
                func="latest",
            )
            logger.info(
                "{} metric received by splunk: {}".format(
                    f"kube.cluster.{resource}.{metric}", json.dumps(events, indent=2)
                )
            )
            assert list(events.values())[0] == total


def test_namespace_limit_and_requests(setup, index_metrics):
    selector = "name"
    nodes = setup["nodes_count"]
    for resource in ["cpu", "memory"]:
        for metric in ["limit", "request"]:
            logger.info(
                "testing {} metric".format(f"kube.namespace.{resource}.{metric}")
            )
            events = collect_metric_from_splunk(
                f"kube.namespace.{resource}.{metric}",
                index_metrics,
                selector,
                url=setup["splunkd_url"],
                user=setup["splunk_user"],
                password=setup["splunk_password"],
                func="latest",
            )
            logger.info(
                "Splunk received {} events for metric {}".format(
                    events, f"kube.namespace.{resource}.{metric}"
                )
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

def test_multi_container_pod_limit_and_request(setup, index_metrics):
    selector = "name"
    for resource in ["cpu", "memory"]:
        for metric in ["limit", "request"]:
            logger.info(
                "testing {} metric".format(f"kube.container.{resource}.{metric} for multi-container pods")
            )
            container_events = collect_metric_from_splunk(
                f"kube.container.{resource}.{metric}",
                index_metrics,
                selector,
                url=setup["splunkd_url"],
                user=setup["splunk_user"],
                password=setup["splunk_password"],
                func="latest",
            )
            if not "pod-wo-index-wo-ns-index-dup" in container_events:
                pytest.fail("pod 'pod-wo-index-wo-ns-index-dup' not found" )

            assert container_events["pod-wo-index-wo-ns-index"] == 50
            assert container_events["pod-wo-index-wo-ns-index-dup"] == 50
            
            pod_events = collect_metric_from_splunk(
                f"kube.pod.{resource}.{metric}",
                index_metrics,
                selector,
                url=setup["splunkd_url"],
                user=setup["splunk_user"],
                password=setup["splunk_password"],
                func="latest",
            )

            for pod_name, metric_value in pod_events.items():
                if "pod-wo-index-wo-ns-index" in pod_name:
                    assert metric_value == 100, f"{resource}.{metric} of pod '{pod_name}' should be 100"
