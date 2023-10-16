# Prometheus-external-targets

Allow a [Kubernetes Prometheus instance][kube-prometheus-stack] to scrape targets external to the cluster by hostname instead of IP address.

This Helm chart allows you to define a list of hostnames to scrape and the IP address in the Endpoint resource object will be updated dynamically via a DNS lookup. This avoids having to manually create an Endpoint resource with a list of IP addresses.

## Getting Started

This project requires Python 3.8, and uses [Poetry to manage dependencies][poetry-proj].

To get started after cloning the project:

* Install Poetry locally:
  * `pip install --user poetry`
* Install the dependencies:
  * `poetry install`
* Enter the virtualenv to interact with the setup:
  * `poetry shell`

## Install as Helm chart:

You should create new Helm releases for groups of hosts (i.e., grouped by function). 

For example, if you have a list of database hosts to monitor, you can create a Helm release dedicated to those hosts (say you name it `external-db-hosts`). If you need to add another database host you'd update the values of that release, but if you wanted to monitor a cluster of VM servers you'd create a ***new*** Helm release with an applicable name.

```
# Install the chart on your cluster of choice.
helm -n <namespace> install external-db-hosts ./helm/prometheus-external-targets -f values.yaml
```
Example values file: 
```
# Number of seconds to wait before refreshing the list of IPs. 
refreshInterval: 30

# Number of times to retry after failed DNS request for each given hostname.
maxDnsRetries: 3

# Number of seconds to wait between retried DNS requests.
retryRequestInterval: 5

# List of hosts to scrape
externalTargets:
- my-scrape-target.example

serviceMonitor:
  metricsPath: "/metrics"
  # The label to apply to the servicemonitor resource so it gets picked up by the prometheus operator. 
  serviceMonitorSelectorLabel:
    release: prometheus

# The port for the metrics endpoint for all hosts.
service:
    metricsPort: "9100"
``` 

[kube-prometheus-stack]: https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

[poetry-proj]: https://python-poetry.org/
