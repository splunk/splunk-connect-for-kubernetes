import pytest
import sys
import os
import logging
from urllib.parse import urlparse
from ..common import check_events_from_splunk, collect_metric_from_splunk
from ..common import check_metrics_from_splunk
from test.k8s_metrics_tests.metric_data.summary import summary_metrics
from test.k8s_metrics_tests.metric_data.cAdvisor import cAdvisor_metrics
from test.k8s_metrics_tests.metric_data.stats import stats_metrics


is_stats_endpoint_enabled = None
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
    "stats_metric",
    stats_metrics,
    ids=[metric["name"] for metric in stats_metrics],
)
def test_metric_from_stats(setup, stats_metric, index_metrics):
    """
    This test covers one metric from each endpoint that the metrics plugin covers
    """
    global is_stats_endpoint_enabled
    if is_stats_endpoint_enabled is None:
        index_event = (
            os.environ["CI_INDEX_EVENT"]
            if os.environ.get("CI_INDEX_EVENT")
            else "ci_events"
        )
        query = f"| search index= {index_event} \"'/stats' endpoint is not available. It has been deprecated since k8s v1.15, disabled since v1.18, and removed in v1.21 and onwards\""
        result = check_events_from_splunk(
            query=query,
            url=setup["splunkd_url"],
            user=setup["splunk_user"],
            password=setup["splunk_password"],
        )
        is_stats_endpoint_enabled = len(result) == 0
        if not is_stats_endpoint_enabled:
            logger.info("Skipping tests from stats metrics")

    if not is_stats_endpoint_enabled:
        pytest.skip("Stats endpoint is not available")
    events = collect_metric_from_splunk(
        stats_metric["name"],
        index_metrics,
        stats_metric["selector"],
        url=setup["splunkd_url"],
        user=setup["splunk_user"],
        password=setup["splunk_password"],
    )
    for assert_func, value in stats_metric["assertions"]:
        assert_func(stats_metric, events, value)


@pytest.mark.parametrize(
    "summary_metric",
    summary_metrics,
    ids=[metric["name"] for metric in summary_metrics],
)
def test_metric_from_summary(setup, summary_metric, index_metrics):
    """
    This test covers one metric from each endpoint that the metrics plugin covers
    """
    events = collect_metric_from_splunk(
        summary_metric["name"],
        index_metrics,
        summary_metric["selector"],
        url=setup["splunkd_url"],
        user=setup["splunk_user"],
        password=setup["splunk_password"],
    )
    for assert_func, value in summary_metric["assertions"]:
        assert_func(summary_metric, events, value)


@pytest.mark.parametrize(
    "cAdvisor_metric",
    cAdvisor_metrics,
    ids=[metric["name"] for metric in cAdvisor_metrics],
)
def test_metric_from_cAdvisor(setup, cAdvisor_metric, index_metrics):
    """
    This test covers one metric from each endpoint that the metrics plugin covers
    """
    events = collect_metric_from_splunk(
        cAdvisor_metric["name"],
        index_metrics,
        cAdvisor_metric["selector"],
        url=setup["splunkd_url"],
        user=setup["splunk_user"],
        password=setup["splunk_password"],
    )
    for assert_func, value in cAdvisor_metric["assertions"]:
        assert_func(cAdvisor_metric, events, value)
