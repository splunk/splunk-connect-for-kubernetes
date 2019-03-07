import pytest
import time
import os
import logging
import json
from urllib.parse import urlparse
from ..common import check_events_from_splunk
from ..common import check_metrics_from_splunk


@pytest.mark.parametrize("metric", [
    #Aggregator Metrics
    ("kube.container.cpu.limit"),
    ("kube.container.memory.request"),
    ("kube.pod.cpu.limit"),
    ("kube.pod.memory.request"),
    ("kube.namespace.cpu.limit"),
    ("kube.namespace.memory.request"),
    ("kube.cluster.cpu.limit"),
    ("kube.cluster.memory.request"),
    ("kube.node.cpu.capacity"),
    ("kube.node.memory.utilization"),
    #Summary Metrics
    ("kube.node.cpu.usage"),
    ("kube.node.memory.usage"),
    ("kube.node.uptime"),
    ("kube.node.network.rx_bytes"),
    ("kube.node.fs.available_bytes"),
    ("kube.node.imagefs.available_bytes"),
    ("kube.node.runtime.imagefs.maxpid"),
    ("kube.sys-container.cpu.usage"),
    ("kube.sys-container.memory.usage_bytes"),
    ("kube.sys-container.uptime"),
    ("kube.pod.uptime"),
    ("kube.pod.cpu.usage"),
    ("kube.pod.memory.usage_bytes"),
    ("kube.pod.network.rx_bytes"),
    ("kube.pod.ephemeral-storage.available_bytes"),
    ("kube.pod.volume.available_bytes"),
    ("kube.container.uptime"),
    ("kube.container.cpu.usage"),
    ("kube.container.memory.usage_bytes"),
    ("kube.container.rootfs.available_bytes"),
    ("kube.container.logs.used_bytes"),
    #Stats Metrics
    ("kube.node.cpu.cfs.periods"),
    ("kube.node.diskio.io_service_bytes.stats.Read"),
    ("kube.node.filesystem.available"),
    ("kube.node.memory.cache"),
    ("kube.node.tasks_stats.nr_running"),
    ("kube.node.network.*.rx_bytes"),
    #Cadvisor Metrics
    ("kube.container.cpu.load.average.10s"),
    ("kube.container.fs.inodes.free"),
    ("kube.container.last.seen"),
    ("kube.container.memory.usage.bytes"),
    ("kube.container.network.receive.bytes.total"),
    ("kube.container.spec.cpu.period"),
    ("kube.container.tasks.state")
])
def test_metric_name(setup, metric):
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
                                  metric_name=metric)
    logging.info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) > 0
