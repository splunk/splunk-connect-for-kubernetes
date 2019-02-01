import pytest
import time
import os
import logging
import json
from urllib.parse import urlparse
from ..common import check_events_from_splunk
from ..common import check_metrics_from_splunk


@pytest.mark.parametrize("test_input,expected", [
    ("test_kube_node_cpu_usage_total", 1)
])
def test_metric_name(setup, test_input, expected):
    '''
    Clustername is a configurable parameter, test that user specified cluster-name is attached as a metadata to all the logs
    '''
    logging.info("testing test_kube_node_cpu_usage_total input={0} \
                expected={1} event(s)".format(test_input, expected))
    logging.getLogger().info("Hey")

    events = check_metrics_from_splunk(start_time="-24h@h",
                                  end_time="now",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  password=setup["splunk_password"],
                                  index="circleci_metrics",
                                  dimension="node",
                                  metric_name="kube.node.cpu.usage.total")
    logging.info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) > 0


