#!/usr/bin/python
import time
import logging
import subprocess
import yaml


logging.basicConfig(
    format='%(asctime)-15s mod=%(module)s func=%(funcName)s line=%(lineno)d %(message)s',
    level=logging.INFO)

PERF_YAML_FILE = ".circleci/performance/perf_test_sck_values.yml"

# Lookup configurables for datagen - https://github.com/dtregonning/kafka-data-gen
DATAGEN_PERF_CASES = [
    #{
    #    'deployment_name': 'perf-test-datagen',
    #    'namespace': 'default',
    #    'number_of_datagen': 10,
    #    'message_count': 100000,
    #    'message_size': 128,
    #    'eps': 100,
    #    'sleep_duration': 1800
    #},
    #{
    #    'deployment_name': 'perf-test-datagen',
    #    'namespace': 'default',
    #    'number_of_datagen': 10,
    #    'message_count': 100000,
    #    'message_size': 256,
    #   'eps': 100,
    #    'sleep_duration': 1800
    #},
    #{
    #    'deployment_name': 'perf-test-datagen',
    #    'namespace': 'default',
    #    'number_of_datagen': 10,
    #    'message_count': 100000,
    #    'message_size': 512,
    #    'eps': 100,
    #    'sleep_duration': 1800
    #},
    #{
    #    'deployment_name': 'perf-test-datagen',
    #    'namespace': 'default',
    #    'number_of_datagen': 10,
    #   'message_count': 100000,
    #    'message_size': 1024,
    #    'eps': 100,
    #    'sleep_duration': 1800
    # },
    #{
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 50,
    #     'message_count': 100000,
    #     'message_size': 128,
    #     'eps': 100,
    #     'sleep_duration': 1800
    # },
    # {
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 50,
    #     'message_count': 100000,
    #     'message_size': 256,
    #     'eps': 100,
    #     'sleep_duration': 1800
    # },
    # {
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 50,
    #     'message_count': 100000,
    #     'message_size': 512,
    #     'eps': 100,
    #     'sleep_duration': 1800
    # },
    # {
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 50,
    #     'message_count': 100000,
    #     'message_size': 1024,
    #     'eps': 100,
    #     'sleep_duration': 1800
    # }
    # {
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 100,
    #     'message_count': 100000,
    #     'message_size': 128,
    #     'eps': 100,
    #     'sleep_duration': 3600
    # },
    # {
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 100,
    #     'message_count': 100000,
    #     'message_size': 256,
    #     'eps': 100,
    #     'sleep_duration': 3600
    # },
    # {
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 100,
    #     'message_count': 100000,
    #     'message_size': 512,
    #     'eps': 100,
    #     'sleep_duration': 3600
    # },
    # {
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 100,
    #     'message_count': 100000,
    #     'message_size': 1024,
    #     'eps': 100,
    #     'sleep_duration': 3600
    #
    # {
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 100,
    #     'message_count': 225000 ,
    #     'message_size': 1024,
    #     'eps': 250,
    #     'sleep_duration': 3600
    # },
    # {
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 100,
    #     'message_count': 225000 ,
    #     'message_size': 1024,
    #     'eps': 250,
    #     'sleep_duration': 3600
    # },
    # {
    #     'deployment_name': 'perf-test-datagen',
    #     'namespace': 'default',
    #     'number_of_datagen': 100,
    #     'message_count': 225000 ,
    #     'message_size': 1024,
    #     'eps': 250,
    #     'sleep_duration': 3600
    # },
     {
         'deployment_name': 'perf-test-datagen',
         'namespace': 'default',
         'number_of_datagen': 10,
         'message_count': 1000 ,
         'message_size': 1024,
         'eps': 100,
         'sleep_duration': 3600
     }
]

# Lookup configurables for fluent and kubernetes
# 1. Fluentd buffer configurables - https://docs.fluentd.org/v1.0/articles/buffer-section
# 2. Kubernetes limits and requests - https://kubernetes.io/docs/concepts/policy/resource-quotas/
CONNECTOR_PERF_CASES = [
    {
        'buffer_type': 'memory',
        'total_limit_size': '600m',
        'chunk_limit_size': '200m',
        'chunk_limit_records': 512000,
        'flush_interval': '10s',
        'flush_thread_count': 1,
        'overflow_action': 'block',
        'retry_max_times': 3,
        'limits_cpu': '2000m',
        'limits_memory': '2000Mi',
        'requests_cpu': '1000m',
        'requests_memory': '1000Mi',
    },
    # {
    #     'buffer_type': 'memory',
    #     'total_limit_size': '600m',
    #     'chunk_limit_size': '200m',
    #     'chunk_limit_records': 10000,
    #     'flush_interval': '5s',
    #     'flush_thread_count': 1,
    #     'overflow_action': 'block',
    #     'retry_max_times': 3,
    #     'limits_cpu': '2000m',
    #     'limits_memory': '2000Mi',
    #     'requests_cpu': '1000m',
    #     'requests_memory': '1000Mi',
    # },
    # {
    #     'buffer_type': 'memory',
    #     'total_limit_size': '400m',
    #     'chunk_limit_size': '100m',
    #     'chunk_limit_records': 10000,
    #     'flush_interval': '5s',
    #     'flush_thread_count': 1,
    #     'overflow_action': 'block',
    #     'retry_max_times': 3,
    #     'limits_cpu': '2000m',
    #     'limits_memory': '2000Mi',
    #     'requests_cpu': '500m',
    #     'requests_memory': '500Mi',
    # },
    # {
    #     'buffer_type': 'memory',
    #     'total_limit_size': '400m',
    #     'chunk_limit_size': '100m',
    #     'chunk_limit_records': 10000,
    #     'flush_interval': '5s',
    #     'flush_thread_count': 1,
    #     'overflow_action': 'block',
    #     'retry_max_times': 3,
    #     'limits_cpu': '2000m',
    #     'limits_memory': '2000Mi',
    #     'requests_cpu': '1000m',
    #     'requests_memory': '1000Mi',
    # },
    # {
    #     'buffer_type': 'file',
    #     'total_limit_size': '600m',
    #     'chunk_limit_size': '200m',
    #     'chunk_limit_records': 10000,
    #     'flush_interval': '5s',
    #     'flush_thread_count': 1,
    #     'overflow_action': 'block',
    #     'retry_max_times': 3,
    #     'limits_cpu': '2000m',
    #     'limits_memory': '2000Mi',
    #     'requests_cpu': '500m',
    #     'requests_memory': '500Mi',
    # },
]


def read_and_modify_yaml(test_case_connector):
    with open(PERF_YAML_FILE) as yaml_file:
        perf_deploy_yaml = yaml.load(yaml_file)

    # buffer_type
    perf_deploy_yaml["splunk-kubernetes-logging"]["buffer"]["\"@type\""] = test_case_connector['buffer_type']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["buffer"]["\"@type\""] = test_case_connector['buffer_type']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["aggregatorBuffer"]["\"@type\""] = test_case_connector['buffer_type']
    perf_deploy_yaml["splunk-kubernetes-objects"]["buffer"]["\"@type\""] = test_case_connector['buffer_type']
    # total_limit_size
    perf_deploy_yaml["splunk-kubernetes-logging"]["buffer"]["total_limit_size"] = test_case_connector['total_limit_size']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["buffer"]["total_limit_size"] = test_case_connector['total_limit_size']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["aggregatorBuffer"]["total_limit_size"] = test_case_connector['total_limit_size']
    perf_deploy_yaml["splunk-kubernetes-objects"]["buffer"]["total_limit_size"] = test_case_connector['total_limit_size']
    # chunk_limit_size
    perf_deploy_yaml["splunk-kubernetes-logging"]["buffer"]["chunk_limit_size"] = test_case_connector['chunk_limit_size']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["buffer"]["chunk_limit_size"] = test_case_connector['chunk_limit_size']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["aggregatorBuffer"]["chunk_limit_size"] = test_case_connector['chunk_limit_size']
    perf_deploy_yaml["splunk-kubernetes-objects"]["buffer"]["chunk_limit_size"] = test_case_connector['chunk_limit_size']
    # chunk_limit_records
    perf_deploy_yaml["splunk-kubernetes-logging"]["buffer"]["chunk_limit_records"] = test_case_connector['chunk_limit_records']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["buffer"]["chunk_limit_records"] = test_case_connector['chunk_limit_records']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["aggregatorBuffer"]["chunk_limit_records"] = test_case_connector['chunk_limit_records']
    perf_deploy_yaml["splunk-kubernetes-objects"]["buffer"]["chunk_limit_records"] = test_case_connector['chunk_limit_records']
    # flush_interval
    perf_deploy_yaml["splunk-kubernetes-logging"]["buffer"]["flush_interval"] = test_case_connector['flush_interval']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["buffer"]["flush_interval"] = test_case_connector['flush_interval']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["aggregatorBuffer"]["flush_interval"] = test_case_connector['flush_interval']
    perf_deploy_yaml["splunk-kubernetes-objects"]["buffer"]["flush_interval"] = test_case_connector['flush_interval']
    # flush_thread_count
    perf_deploy_yaml["splunk-kubernetes-logging"]["buffer"]["flush_thread_count"] = test_case_connector['flush_thread_count']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["buffer"]["flush_thread_count"] = test_case_connector['flush_thread_count']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["aggregatorBuffer"]["flush_thread_count"] = test_case_connector['flush_thread_count']
    perf_deploy_yaml["splunk-kubernetes-objects"]["buffer"]["flush_thread_count"] = test_case_connector['flush_thread_count']
    # overflow_action
    perf_deploy_yaml["splunk-kubernetes-logging"]["buffer"]["overflow_action"] = test_case_connector['overflow_action']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["buffer"]["overflow_action"] = test_case_connector['overflow_action']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["aggregatorBuffer"]["overflow_action"] = test_case_connector['overflow_action']
    perf_deploy_yaml["splunk-kubernetes-objects"]["buffer"]["overflow_action"] = test_case_connector['overflow_action']
    # retry_max_times
    perf_deploy_yaml["splunk-kubernetes-logging"]["buffer"]["retry_max_times"] = test_case_connector['retry_max_times']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["buffer"]["retry_max_times"] = test_case_connector['retry_max_times']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["aggregatorBuffer"]["retry_max_times"] = test_case_connector['retry_max_times']
    perf_deploy_yaml["splunk-kubernetes-objects"]["buffer"]["retry_max_times"] = test_case_connector['retry_max_times']
    # limits_cpu
    perf_deploy_yaml["splunk-kubernetes-logging"]["resources"]["limits"]["cpu"] = test_case_connector['limits_cpu']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["resources"]["fluent"]["limits"]["cpu"] = test_case_connector['limits_cpu']
    perf_deploy_yaml["splunk-kubernetes-objects"]["resources"]["limits"]["cpu"] = test_case_connector['limits_cpu']
    # limits_memory
    perf_deploy_yaml["splunk-kubernetes-logging"]["resources"]["limits"]["memory"] = test_case_connector['limits_memory']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["resources"]["fluent"]["limits"]["memory"] = test_case_connector['limits_memory']
    perf_deploy_yaml["splunk-kubernetes-objects"]["resources"]["limits"]["memory"] = test_case_connector['limits_memory']
    # requests_cpu
    perf_deploy_yaml["splunk-kubernetes-logging"]["resources"]["requests"]["cpu"] = test_case_connector['requests_cpu']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["resources"]["fluent"]["requests"]["cpu"] = test_case_connector['requests_cpu']
    perf_deploy_yaml["splunk-kubernetes-objects"]["resources"]["requests"]["cpu"] = test_case_connector['requests_cpu']
    # requests_memory
    perf_deploy_yaml["splunk-kubernetes-logging"]["resources"]["requests"]["memory"] = test_case_connector['requests_memory']
    perf_deploy_yaml["splunk-kubernetes-metrics"]["resources"]["fluent"]["requests"]["memory"] = test_case_connector['requests_memory']
    perf_deploy_yaml["splunk-kubernetes-objects"]["resources"]["requests"]["memory"] = test_case_connector['requests_memory']

    with open(PERF_YAML_FILE, "w") as yaml_file:
        yaml.dump(perf_deploy_yaml, yaml_file, default_flow_style=False)


def setup_connector_and_datagen(test_case_datagen, test_case_connector):
    logging.info('Setup connector and datagen')
    read_and_modify_yaml(test_case_connector)
    subprocess.call('.circleci/performance/perf_deploy_sck.sh --deploy', shell=True)
    # "DEPLOYMENT_NAME NAMESPACE NUMBER_OF_REPLICAS MSG_COUNT MSG_SIZE EPS"
    subprocess.call('.circleci/performance/perf_deploy_sck.sh --deploy_data_gen \"{} {} {} {} {} {}\"'.format(
        test_case_datagen['deployment_name'], test_case_datagen['namespace'], test_case_datagen['number_of_datagen'],
        test_case_datagen['message_count'], test_case_datagen['message_size'], test_case_datagen['eps']), shell=True)


def teardown_connector_and_datagen(test_case_datagen, test_case_connector):
    logging.info('Teardown connector and datagen')
    subprocess.call('.circleci/performance/perf_deploy_sck.sh --clean', shell=True)
    # "DEPLOYMENT_NAME NAMESPACE NUMBER_OF_REPLICAS"
    subprocess.call('.circleci/performance/perf_deploy_sck.sh --clean_data_gen \"{} {} {}\"'.format(
        test_case_datagen['deployment_name'], test_case_datagen['namespace'], test_case_datagen['number_of_datagen']),
        shell=True)


def wait_for_connector_do_data_collection_injection(test_case_datagen):
    logging.info('Sleeping for data collection')
    for second in range(int(test_case_datagen['sleep_duration']), 0, -1):
        if(second % 60 == 0):
            logging.info('Sleeping ' + str(second) + '........')
        time.sleep(1)


def _do_perf():
    for test_case_datagen in DATAGEN_PERF_CASES:
        for test_case_connector in CONNECTOR_PERF_CASES:
            logging.info('Executing perf case: {} {}'.format(test_case_datagen, test_case_connector))
            setup_connector_and_datagen(test_case_datagen, test_case_connector)
            wait_for_connector_do_data_collection_injection(test_case_datagen)
            teardown_connector_and_datagen(test_case_datagen, test_case_connector)


def main():
    _do_perf()


if __name__ == '__main__':
    main()