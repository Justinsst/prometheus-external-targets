from kubernetes import client, config
import logging

logger = logging.getLogger(__name__)


def cluster_config(func):
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
def apply_endpoint(manifest, namespace, kubeconfig=None):
    v1 = client.CoreV1Api()
    try:
        v1.create_namespaced_endpoints(namespace=namespace, body=manifest)
        return True
    except client.ApiException as e:
        if e.reason == "Conflict":
            logger.info(
                f"Failed to create {manifest['metadata']['name']} "
                f"{manifest['kind']}, resource already exists. "
                "Trying replace instead."
            )
        else:
            logger.exception(
                f"Failed to create {manifest['metadata']['name']} "
                f"{manifest['kind']}. Trying replace instead."
            )

    try:
        v1.replace_namespaced_endpoints(
            name=manifest["metadata"]["name"],
            namespace=namespace,
            body=manifest,
        )
        logging.info(
            f"{manifest['kind']} resource with name "
            f"{manifest['metadata']['name']} was replaced."
        )
        return True
    except client.ApiException:
        logger.exception("")
        raise RuntimeError(
            f"Failed to replace Endpoint resource "
            f"{manifest['metadata']['name']}."
        )


@cluster_config
def delete_endpoint(manifest, namespace, kubeconfig=None):
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
