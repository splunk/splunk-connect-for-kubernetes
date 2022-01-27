from test.k8s_metrics_tests.metric_data.helper import (
    greater,
    greater_or_equal,
    should_exist,
    some_should_be_greater,
)

cAdvisor_metrics = [
    {
        "name": "kube.container.cpu.load.average.10s",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.cpu.system.seconds.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.cpu.usage.seconds.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.cpu.user.seconds.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.fs.inodes.free",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.inodes.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.fs.io.current",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.io.time.seconds.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.io.time.weighted.seconds.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.limit.bytes",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.fs.read.seconds.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.reads.bytes.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.reads.merged.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.reads.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.sector.reads.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.sector.writes.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.usage.bytes",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.fs.write.seconds.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.writes.bytes.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.writes.merged.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.fs.writes.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.last.seen",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.memory.cache",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.memory.failcnt",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.memory.failures.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.memory.max.usage.bytes",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.memory.rss",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.memory.swap",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.memory.usage.bytes",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.memory.working.set.bytes",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.pod.network.receive.bytes.total",
        "selector": "pod_name",
        "assertions": [[should_exist, None], [some_should_be_greater, 0]],
    },
    {
        "name": "kube.pod.network.receive.errors.total",
        "selector": "pod_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.pod.network.receive.packets.dropped.total",
        "selector": "pod_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.pod.network.receive.packets.total",
        "selector": "pod_name",
        "assertions": [[should_exist, None], [some_should_be_greater, 0]],
    },
    {
        "name": "kube.container.network.tcp.usage.total",
        "selector": "container_name",
        "assertions": [[greater_or_equal, 0]],
    },
    {
        "name": "kube.pod.network.transmit.bytes.total",
        "selector": "pod_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.pod.network.transmit.errors.total",
        "selector": "pod_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.pod.network.transmit.packets.dropped.total",
        "selector": "pod_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.pod.network.transmit.packets.total",
        "selector": "pod_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.network.udp.usage.total",
        "selector": "container_name",
        "assertions": [[greater_or_equal, 0]],
    },
    {
        "name": "kube.container.spec.cpu.period",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.spec.cpu.shares",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.spec.memory.limit.bytes",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.spec.memory.reservation.limit.bytes",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.spec.memory.swap.limit.bytes",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.start.time.seconds",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
    {
        "name": "kube.container.tasks.state",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
    },
    {
        "name": "kube.container.cpu.cfs.throttled.seconds.total",
        "selector": "container_name",
        "assertions": [[should_exist, None], [greater, 0]],
    },
]
