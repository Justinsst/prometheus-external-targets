import socket
import logging
from time import sleep

logger = logging.getLogger(__name__)


def get_ip(hostname, retries, interval):
    retry_count = 1
    while retry_count <= retries:
        try:
            ip = socket.gethostbyname(hostname)
            return ip
        except:
            msg = f"DNS request failed for host: {hostname}. Retrying {str(retry_count)}/{str(retries)}"
            if retry_count >= retries:
                logger.exception(msg)
            else:
                logger.error(msg)    
        sleep(interval)
        retry_count += 1
    return False
        



