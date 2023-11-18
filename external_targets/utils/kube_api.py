import functools
import logging
from kubernetes import client, config

logger = logging.getLogger(__name__)


def cluster_config(func):
    @functools.wraps
    def wrapper(*args, **kwargs):
        if kwargs["kubeconfig"]:
            kubeconfig = kwargs["kubeconfig"]
            try:
                config.load_kube_config(kubeconfig)
            except config.config_exception.ConfigException:
                raise RuntimeError(
                    f"Unable to load specified kubeconfig file: {kubeconfig}"
                )
        else:
            try:
                config.load_incluster_config()
            except config.config_exception.ConfigException:
                raise RuntimeError("Unable to load in-cluster kube config")
        result = func(*args, **kwargs)
        return result

    return wrapper


@cluster_config
def apply_endpoint(
    manifest: dict, namespace: str, kubeconfig: str = None
) -> bool:
    v1 = client.CoreV1Api()
    # Attmept to create the resource first.
    try:
        v1.create_namespaced_endpoints(namespace=namespace, body=manifest)
        return True
    except client.ApiException as e:
        if e.reason == "Conflict":
            logger.info(
                f"{manifest['kind']} resource "
                f'"{manifest["metadata"]["name"]}" already exists. Trying '
                "replace instead."
            )
        else:
            logger.exception(
                f"Failed to create {manifest['metadata']['name']} "
                f"{manifest['kind']}. Trying replace instead."
            )
    # Try replacing the resource if creation fails.
    try:
        v1.replace_namespaced_endpoints(
            name=manifest["metadata"]["name"],
            namespace=namespace,
            body=manifest,
        )
        logging.info(
            f'{manifest["kind"]} resource "{manifest["metadata"]["name"]}" '
            "was replaced."
        )
        return True
    except client.ApiException:
        logger.error(
            f"Failed to replace Endpoint resource "
            f"{manifest['metadata']['name']}."
        )
        raise


@cluster_config
def delete_endpoint(
    manifest: dict, namespace: str, kubeconfig: str = None
) -> bool:
    v1 = client.CoreV1Api()
    try:
        v1.delete_namespaced_endpoints(
            name=manifest["metadata"]["name"],
            namespace=namespace,
        )
        logging.info(
            f"{manifest['kind']} resource with name "
            f"{manifest['metadata']['name']} was deleted."
        )
        return True
    except client.ApiException:
        logger.warning(
            f"Failed to delete Endpoint resource {manifest['metadata']['name']}. "
            "It may not exist."
        )
    return False
