import logging
import pytest
import json
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


def greater(test_name, data, value):
    for name, val in data.items():
        if val <= value:
            logger.info(
                "{} metric received by splunk: \n{}".format(
                    test_name["name"], json.dumps(data, indent=2)
                )
            )
            pytest.fail(
                "Metric {} from {} should be greater than {}".format(
                    test_name["name"], name, value
                )
            )


def greater_or_equal(test_name, data, value):
    for name, val in data.items():
        if val < value:
            logger.info(
                "{} metric received by splunk: \n{}".format(
                    test_name["name"], json.dumps(data, indent=2)
                )
            )
            pytest.fail(
                "Metric {} from {} should be greater than or equal to {}".format(
                    test_name["name"], name, value
                )
            )


def some_should_be_greater(test_name, data, val):
    count = 0
    for value in data.values():
        if value > val:
            count += 1
    if len(data) > 0 and count == 0:
        logger.info(
            "{} metric received by splunk: \n{}".format(
                test_name["name"], json.dumps(data, indent=2)
            )
        )
        pytest.fail(
            "For metric {}, at least one value should be greater than {} in {}".format(
                test_name, val, data
            )
        )


def should_exist(test_name, data, value):
    assert len(data) > 0, "Splunk did not received any metric {} with field {}".format(
        test_name["name"], test_name["selector"]
    )
