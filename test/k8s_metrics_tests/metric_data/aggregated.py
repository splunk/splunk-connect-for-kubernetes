from test.k8s_metrics_tests.metric_data.helper import (
    greater,
    greater_or_equal,
    should_exist,
)


container_memory_limit = {
    "splunk-fluentd-k8s-logs": 0,
    "splunk-fluentd-k8s-objects": 0,
    "splunk-fluentd-k8s-metrics": 300,
    "splunk-fluentd-k8s-metrics-agg": 300,
}
container_memory_request = {
    "splunk-fluentd-k8s-logs": 200,
    "splunk-fluentd-k8s-objects": 200,
    "splunk-fluentd-k8s-metrics": 300,
    "splunk-fluentd-k8s-metrics-agg": 300,
}
container_cpu_limit = {
    "splunk-fluentd-k8s-logs": 0,
    "splunk-fluentd-k8s-objects": 0,
    "splunk-fluentd-k8s-metrics": 200,
    "splunk-fluentd-k8s-metrics-agg": 200,
}
container_cpu_request = {
    "splunk-fluentd-k8s-logs": 100,
    "splunk-fluentd-k8s-objects": 100,
    "splunk-fluentd-k8s-metrics": 200,
    "splunk-fluentd-k8s-metrics-agg": 200,
}

container_limit_request = {
    "cpu": {
        "limit": container_cpu_limit,
        "request": container_cpu_request,
    },
    "memory": {"limit": container_memory_limit, "request": container_memory_request},
}

aggregated_metrics = [
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.container.cpu.limit",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.container.cpu.request",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.container.memory.limit",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.container.memory.request",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.pod.cpu.limit",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.pod.cpu.request",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.pod.memory.limit",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.pod.memory.request",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.namespace.cpu.limit",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.namespace.cpu.request",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.namespace.memory.limit",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.namespace.memory.request",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.cluster.cpu.limit",
        "selector": "cluster_name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.cluster.cpu.request",
        "selector": "cluster_name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.cluster.memory.limit",
        "selector": "cluster_name",
    },
    {
        "assertions": [[should_exist, None], [greater_or_equal, 0]],
        "name": "kube.cluster.memory.request",
        "selector": "cluster_name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.capacity",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.allocatable",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.capacity",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.allocatable",
        "selector": "node",
    },
    # Will be resolved after next release
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.reservation",
        "selector": "node",
    },
    # Will be resolved after next release
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.cpu.utilization",
        "selector": "node",
    },
    # Will be resolved after next release
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.reservation",
        "selector": "node",
    },
    # Will be resolved after next release
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.node.memory.utilization",
        "selector": "node",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.namespace.cpu.usage",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.namespace.memory.usage",
        "selector": "name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.cluster.cpu.usage",
        "selector": "cluster_name",
    },
    {
        "assertions": [[should_exist, None], [greater, 0]],
        "name": "kube.cluster.memory.usage",
        "selector": "cluster_name",
    },
]
