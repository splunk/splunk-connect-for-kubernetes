from test.k8s_metrics_tests.metric_data.helper import (
    greater,
    greater_or_equal,
    should_exist,
)

summary_metrics = [
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.uptime",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.usage_rate",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.usage",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.available_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.usage_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.rss_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.memory.page_faults",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.memory.major_page_faults",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.network.rx_bytes",
        "selector": "node",
    },
    {
        "assertions": [[greater_or_equal, 0]],
        "name": "kube.node.network.rx_errors",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.network.tx_bytes",
        "selector": "node",
    },
    {
        "assertions": [[greater_or_equal, 0]],
        "name": "kube.node.network.tx_errors",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.fs.available_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.fs.capacity_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.fs.used_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.fs.inodes_free",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.fs.inodes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.fs.inodes_used",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.imagefs.available_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.imagefs.capacity_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.imagefs.used_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.imagefs.inodes_free",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.imagefs.inodes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.imagefs.inodes_used",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.runtime.imagefs.maxpid",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.runtime.imagefs.curproc",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.uptime",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.usage",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.available_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.usage_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.rss_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.rss_bytes",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.memory.page_faults",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.node.memory.major_page_faults",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.uptime",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.cpu.usage_rate",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.cpu.usage",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.memory.available_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.memory.usage_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.memory.rss_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.pod.memory.page_faults",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.pod.memory.major_page_faults",
        "selector": "pod-name",
    },
    {
        "assertions": [[greater_or_equal, 0]],
        "name": "kube.pod.network.rx_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[greater_or_equal, 0]],
        "name": "kube.pod.network.rx_errors",
        "selector": "pod-name",
    },
    {
        "assertions": [[greater_or_equal, 0]],
        "name": "kube.pod.network.tx_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[greater_or_equal, 0]],
        "name": "kube.pod.network.tx_errors",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.ephemeral-storage.available_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.ephemeral-storage.capacity_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.ephemeral-storage.used_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.ephemeral-storage.inodes_free",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.ephemeral-storage.inodes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.ephemeral-storage.inodes_used",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.volume.available_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.volume.capacity_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.volume.used_bytes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.volume.inodes_free",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.volume.inodes",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.pod.volume.inodes_used",
        "selector": "pod-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.uptime",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.cpu.usage_rate",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.cpu.usage",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.memory.available_bytes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.memory.usage_bytes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.memory.rss_bytes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.container.memory.page_faults",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.container.memory.major_page_faults",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.memory.working_set_bytes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.rootfs.available_bytes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.rootfs.capacity_bytes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.container.rootfs.used_bytes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.rootfs.inodes_free",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.rootfs.inodes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.rootfs.inodes_used",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.logs.available_bytes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.logs.capacity_bytes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.logs.used_bytes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.logs.inodes_free",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.logs.inodes",
        "selector": "container-name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.container.logs.inodes_used",
        "selector": "container-name",
    },
]
