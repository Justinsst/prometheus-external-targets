import argparse
import logging
import os
import yaml
from time import sleep
from .utils import kube_api
from .utils.get_ip import get_ip
from .environment import *


def main():
    log_format = '%(asctime)-15s %(funcName)s:%(levelname)s %(message)s'
    logging.basicConfig(level=LOGLEVEL, format=log_format)

    kubeconfig = parse_args().kubeconfig
    body = yaml.safe_load(os.environ['BASE_ENDPOINT_MANIFEST'])
    target_hostnames = os.environ['TARGETS']

    while True:
        endpoint_addresses = []
        for hostname in target_hostnames.splitlines():
            logging.info(f'Getting IP for hostname "{hostname}".')
            ip = get_ip(hostname, REQUEST_RETRIES, RETRY_REQUEST_INTERVAL)
            if not ip:
                raise RuntimeError(f"DNS lookup failed for host {hostname}")
            entry = {'ip': ip}
            logging.info(f'Got IP {ip} for hostname "{hostname}".')
            endpoint_addresses.append(entry)
        body['subsets'][0]['addresses'] = endpoint_addresses
        logging.debug(f"New endpoint manifest: {body}")
        try:
            kube_api.apply_endpoint(body, NAMESPACE, kubeconfig=kubeconfig)
            logging.info(f"Successfully updated Endpoint resource.")
        except RuntimeError:
            logging.exception()
        logging.info(f"Waiting for {REFRESH_INTERVAL} seconds before next refresh.")
        sleep(REFRESH_INTERVAL)


def parse_args():
    parser = argparse.ArgumentParser(usage='%(prog)s -k <kubeconfig>')
    parser.add_argument("-k", "--kubeconfig",
                        help="Path to the cluster's kubeconfig. If not specified, \
                              the in-cluster config is used (source namespace is assumed \
                              to be on the current cluster).")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()