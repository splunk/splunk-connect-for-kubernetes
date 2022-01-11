def greater(data, value):
    for name, val in data.items():
        assert val > value, "{} should be greater than {}".format(name, value)


def greater_or_equal(data, value):
    for name, val in data.items():
        assert val >= value, "{} should be greater than or equal to {}".format(
            name, value
        )


def some_should_be_greater(data, val):
    count = 0
    for value in data.values():
        if value <= val:
            count += 1
    assert count < len(
        data
    ), "At least one value should be greater than zero in {}".format(data)


def should_exist(data, value):
    assert len(data) > 0, "No result found"
