from test.k8s_metrics_tests.metric_data.helper import (
    greater,
    greater_or_equal,
    should_exist,
    some_should_be_greater,
)


stats_metrics = [
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.cfs.periods",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.cpu.cfs.throttled_periods",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.cpu.cfs.throttled_time",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.usage.total",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.usage.user",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.usage.system",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.cpu.load_average",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.diskio.*.stats.Async",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.diskio.*.stats.Read",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.diskio.*.Sync",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.diskio.*.stats.Total",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.diskio.*.stats.Write",
        "selector": "node",
    },
    {
        "assertions": [[greater_or_equal, 0]],
        "name": "kube.node.diskio.*.minor",
        "selector": "node",
    },
    {
        "assertions": [[greater_or_equal, 0]],
        "name": "kube.node.diskio.*.major",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.filesystem.available",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.base_usage",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.filesystem.capacity",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.filesystem.inodes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.filesystem.inodes_free",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.io_in_progress",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.io_time",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.read_time",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.reads_completed",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.reads_merged",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.sectors_read",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.sectors_written",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.filesystem.usage",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.weighted_io_time",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.write_time",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.writes_completed",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.filesystem.writes_merged",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.cache",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.container_data.pgfault",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.memory.container_data.pgmajfault",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.memory.failcnt",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.hierarchical_data.pgfault",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.memory.hierarchical_data.pgmajfault",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.max_usage",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.rss",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.memory.swap",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.usage",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.working_set",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.tasks_stats.nr_io_wait",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.tasks_stats.nr_running",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.tasks_stats.nr_sleeping",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.tasks_stats.nr_stopped",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.tasks_stats.nr_uninterruptible",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [some_should_be_greater, 0]],
        "name": "kube.node.network.*.rx_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.network.*.rx_dropped",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.network.*.rx_errors",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [some_should_be_greater, 0]],
        "name": "kube.node.network.*.rx_packets",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [some_should_be_greater, 0]],
        "name": "kube.node.network.*.tx_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.network.*.tx_dropped",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.network.*.tx_errors",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [some_should_be_greater, 0]],
        "name": "kube.node.network.*.tx_packets",
        "selector": "node",
    },
]
