import pytest
import time
import os
import logging
import json
from urllib.parse import urlparse
from ..common import check_events_from_splunk
from ..common import check_metrics_from_splunk


@pytest.mark.parametrize("metric,dimension", [
    ("kube.pod.cpu.usage.seconds.total", "pod_name"),
    ("kube.node.cpu.usage.total", "node"),
    ("kube.container.cpu.system.seconds.total", "namespace")
])
def test_metric_name(setup, metric, dimension):
    '''
    This test covers one metric from each endpoint that the metrics plugin covers
    '''
    logging.info("testing for presence of metric={0}".format(metric))

    events = check_metrics_from_splunk(start_time="-24h@h",
                                  end_time="now",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  password=setup["splunk_password"],
                                  index="circleci_metrics",
                                  dimension=dimension,
                                  metric_name=metric)
    logging.info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) > 0


