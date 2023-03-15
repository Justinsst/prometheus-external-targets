import argparse
import logging
import socket
import os
import yaml
from time import sleep
from utils import kube_api
from environment import LOGLEVEL, NAMESPACE, REFRESH_INTERVAL


def main():
    log_format = '%(asctime)-15s %(funcName)s:%(levelname)s %(message)s'
    logging.basicConfig(level=LOGLEVEL, format=log_format)

    kubeconfig = parse_args().kubeconfig
    body = yaml.safe_load(os.environ.get('BASE_ENDPOINT_MANIFEST'))
    target_hostnames = os.environ.get('TARGETS')

    while True:
        endpoint_addresses = []
        for hostname in target_hostnames.splitlines():
            entry = {'ip': socket.gethostbyname(hostname)}
            endpoint_addresses.append(entry)
        body['subsets'][0]['addresses'] = endpoint_addresses
        logging.debug(f"New endpoint manifest: {body}")
        kube_api.apply_endpoint(body, NAMESPACE, kubeconfig=kubeconfig)
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