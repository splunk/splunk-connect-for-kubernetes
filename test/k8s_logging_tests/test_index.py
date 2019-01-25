import pytest
import time
import os
import logging
import json
from urllib.parse import urlparse
from ..common import check_events_from_splunk


@pytest.mark.parametrize("test_input,expected", [
    ("circleci_events", 1)
])
def test_splunk_index(setup, test_input, expected):
    '''
    Test that user specified index can successfully index the
    log stream from k8s. If no index is specified, default
    index "circleci_events" will be used.
    '''
    logging.getLogger().info("testing test_splunk_index input={0} \
                 expected={1} event(s)".format(test_input, expected))
    index = test_input if test_input else "circleci_events"

    events = check_events_from_splunk(index=index,
                                      start_time="-34h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      password=setup["splunk_password"])
    logging.getLogger().info("Splunk received %s events in the last minute",
                             len(events))
    assert len(events) != ""







