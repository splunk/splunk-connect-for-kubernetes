
# Prerequsite
* Python version must be > 3.x

# Testing Instructions
0. (Optional) Use a virtual environment for the test  
    `virtualenv --python=python3.6 venv`  
    `source venv/bin/activate`
1. Install the dependencies  
    `pip install -r requirements.txt`  
2. Start the test with the required options configured  
    `python -m pytest <options>`  

    **Options are:**  
    --splunkd-url
    * Description: splunkd url used to send test data to. Eg: https://localhost:8089  
    * Default: https://localhost:8089

    --splunk-user
    * Description: splunk username  
    * Default: admin

    --splunk-password
    * Description: splunk user password  
    * Default: changeme

# How metric tests works
Test collects test data from metric_data, each data contains metric name, field selector for metric and list of asserions.

Generic search query used in metric tests: `| mstats max(<metric-name>) where index=<index-name> by <selector field>`

All selector fields are listed in [selector.md](https://github.com/splunk/splunk-connect-for-kubernetes/blob/develop/test/k8s_metrics_tests/metric_data/selector.md)