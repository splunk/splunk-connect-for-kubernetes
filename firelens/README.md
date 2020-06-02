# Splunk Connect for AWS ECS and AWS Fargate

Splunk Connect for Kubernetes provides an integration for sending logs to Splunk from AWS ECS and AWS Fargate using [firelens.](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html) <br/>
The fluentd logging component from Splunk Connect for Kubernetes is used to achieve this goal using [Splunk's fluentd HEC plugin.](https://github.com/splunk/fluent-plugin-splunk-hec)

# Enabling Firelens for Splunk Connect for AWS ECS and AWS Fargate

### 1. Configure the fluent.conf file to be used with Splunk's firelens log router container
```
<system>
  log_level info
</system>

<match **>
  @type splunk_hec
  protocol https
  hec_host my-hec-host
  hec_port my-hec-port
  hec_token my-hec-token
  index my-index
  host_key ec2_instance_id
  source_key ecs_cluster
  sourcetype_key ecs_task_definition
  insecure_ssl true
  <fields>
    container_id
    container_name
    ecs_task_arn
    source
  </fields>
  <format>
    @type single_value
    message_key log
    add_newline false
  </format>
</match>
```
The fluent.conf file is used to specify the configuration for [Splunk's HEC REST endpoint.](http://dev.splunk.com/view/event-collector/SP-CAAAE7F) Configure it as follows: <br/>
* `protocol` - The protocol to be used (HTTP/HTTPS)
* `hec_host` - The host exposing Splunk's HEC endpoint
* `hec_token` - The HEC token used for authorizing requests being made to Splunk's HEC endpoint
* `hec_port` - The port configured for use with the above `hec_token`
* `index` - Target Splunk indexes to send data to

Store this `fluent.conf` in an S3 bucket to be used in the next step.

### 2. Configure Splunk's firelens log router container
```json
{
   "essential":true,
   "image":"splunk/fluentd-hec:1.2.0",
   "name":"log_router",
   "firelensConfiguration":{
      "type":"fluentd",
      "options":{
         "config-file-type":"s3",
         "config-file-value":"arn:aws:s3:::my-aws-bucket/fluent.conf"
      }
   }
}
```
Add the above container definition alongside your application container definition. The following options should be configured and updated appropriately:<br/>
* Set the `image` to the relevant Splunk's firelens log router container
* Set the `config-file-value` to the location of your fluent.conf file in s3
* For AWS Fargate the `config-file-type` will be `file` and `config-file-value` is the full path of the configuration file that exists either in the container image or on a volume that is mounted in the container.
* More information for Fargate can be found [on AWS guide for using firelens](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html) 
* For using volumes with Fargate please refer [AWS Fargate Documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_data_volumes.html)


### 3. Configure the application container
In your application container definition add the following log configuration section so that your application can use firelens and Splunk's firelens log router.
```json
"logConfiguration":{
  "logDriver":"awsfirelens"
}
```

### 4. Configure Cloudwatch logs for Splunk's firelens log router container (Optional step/Useful for troubleshooting)
To monitor the logs of Splunk's firelens log router container you can configure a log configuration in Splunk's firelens log router container definition as follows:
```json
"logConfiguration": {
    "logDriver": "awslogs",
    "options": {
      "awslogs-group": "my-log-group",
      "awslogs-region": "my-aws-region",
      "awslogs-stream-prefix": "my-stream-prefix"
    }
}
```
Configure the options for `awslogs-group`, `awslogs-region` and `awslogs-stream-prefix` appropriately. The logDriver can be [awslogs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_awslogs.html) or [awsfirelens.](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html)
This results in a container definition as follows:
```json
{
   "essential":true,
   "image":"splunk/fluentd-hec:1.2.0",
   "name":"log_router",
   "firelensConfiguration":{
      "type":"fluentd",
      "options":{
         "config-file-type":"s3",
         "config-file-value":"arn:aws:s3:::my-aws-bucket/fluent.conf"
      }
   },
   "logConfiguration":{
      "logDriver":"awslogs",
      "options":{
         "awslogs-group":"my-log-group",
         "awslogs-region":"my-aws-region",
         "awslogs-stream-prefix":"my-stream-prefix"
      }
   }
}
```

### 5. Example Task Definition for reference
Following is an example task definition with an nginx web server accessible on port 80. All the logs from this nginx web server will be sent to the Splunk instance configured in the fluent.conf file.
```json
{
   "family":"firelens-ec2-demo-s3",
   "containerDefinitions":[
      {
         "essential":true,
         "image":"splunk/fluentd-hec:1.2.0",
         "name":"log_router",
         "firelensConfiguration":{
            "type":"fluentd",
            "options":{
               "config-file-type":"s3",
               "config-file-value":"arn:aws:s3:::my-aws-bucket/fluent.conf"
            }
         },
         "logConfiguration":{
            "logDriver":"awslogs",
            "options":{
               "awslogs-group":"debug-fluentd",
               "awslogs-region":"us-west-2",
               "awslogs-stream-prefix":"test"
            }
         }
      },
      {
         "essential":true,
         "name":"nginx-example",
         "image":"nginx:1.17",
         "essential":true,
         "portMappings":[
            {
               "hostPort":80,
               "protocol":"tcp",
               "containerPort":80
            }
         ],
         "logConfiguration":{
            "logDriver":"awsfirelens"
         }
      }
   ]
}
```
