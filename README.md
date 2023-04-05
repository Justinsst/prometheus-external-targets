# External-targets

Allow prometheus targets outside a cluster to be scraped by hostname instead of IP address (i.e., manually creating an endpoint resource).

## Getting Started

This project requires Python 3.8, and uses [Poetry to manage dependencies][poetry-proj].

To get started after cloning the project:

* Install Poetry locally:
  * `pip install --user poetry`
* Install the dependencies:
  * `poetry install`
* Enter the virtualenv to interact with the setup:
  * `poetry shell`
* Run the tool locally:
  * `external-targets -k <your kubeconfig>`
* Install as helm chart:
  * `helm -n <namespace> install external-targets-test ./helm/external-targets/ -f values.yaml`
  * Example values file: 
    ```
    # Number of seconds to wait before performing DNS requests. 
    refreshInterval: 30

    # List of hosts to scrape
    externalTargets:
    - my-scrape-target.example

    serviceMonitor:
    # The label to apply to the servicemonitor resource so it gets picked up by the prometheus operator. 
    serviceMonitorSelectorLabel:
        release: prometheus
    metricsPath: "/metrics/"
    
    # The port for the metrics endpoint for all hosts.
    service:
        metricsPort: "9100"
    ``` 

[poetry-proj]: https://python-poetry.org/
