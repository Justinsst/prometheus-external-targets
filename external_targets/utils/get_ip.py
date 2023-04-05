import socket
import logging
from time import sleep
from external_targets.environment import REQUEST_RETRIES, RETRY_REQUEST_INTERVAL


logger = logging.getLogger(__name__)


def get_ip(hostname):
    retries = 0
    while retries < 3:
        try:
            ip = socket.gethostbyname(hostname)
            return ip
        except:
            logger.error(f"DNS request failed for host: {hostname}. Retrying 1/{str(REQUEST_RETRIES)}")    
        sleep(RETRY_REQUEST_INTERVAL)
        retries += 1
    return False
        



