This file is for documentation purposes only. It contains which selector field used in each test



| Metric type | selector for stats | selector for summary | selector for cAdvisor | selector for aggregated |
| ----------- | ------------------ | -------------------- | --------------------- | ----------------------- |
| container   | -                  | container-name       | container_name        | name                    |
| pod         | -                  | pod-name             | pod_name              | name                    |
| node        | node               | node                 | -                     | node                    |
| namespace   | -                  | -                    | -                     | name                    |
| cluster     | -                  | -                    | -                     | name                    |

Selector field suggest unique identifier field for given metric. 
Here, `"-"` means the given type of metric doesn't exist in metric source(i.e stats/summary/cAdvisor)

For example, `kube.container.uptime` summary metric suggest container uptime. Each containers will have different uptime. So, we can group all `kube.container.uptime` by container's name. Summary scrapper will set the container's name as `container-name`. For this metric, since it is container metric and it's coming from summary api, the selector field will be `container-name`. 

Test will search following query in splunk for example test: `| mstats max(kube.container.cpu.uptime) where index=<index> by container-name`

