import json
import requests
import os
requests.packages.urllib3.disable_warnings()

# Get student ID from environment variables
STUDENT_ID = os.environ.get("STUDENT_ID", "66070000")

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
DEFAULT_HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
DEFAULT_BASICAUTH = ("admin", "cisco")


def _compute_loopback_ip(student_id: str):
    last_three = student_id[-3:]
    x = int(last_three[-3])
    y = int(last_three[-2:])
    return f"172.{x}.{y}.1"


def create(router_ip=None):
    """Create loopback using RESTCONF on the given router_ip (or env value)."""
    router = router_ip or os.environ.get("ROUTER_IP", "10.0.15.61")
    loopback_ip = _compute_loopback_ip(STUDENT_ID)
    api_url = f"https://{router}:443/restconf/data/ietf-interfaces:interfaces/interface=Loopback{STUDENT_ID}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{STUDENT_ID}",
            "description": f"Loopback interface for student {STUDENT_ID}",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": loopback_ip,
                        "netmask": "255.255.255.0"
                    }
                ]
            }
        }
    }

    resp = requests.put(
        api_url,
        data=json.dumps(yangConfig),
        auth=DEFAULT_BASICAUTH,
        headers=DEFAULT_HEADERS,
        verify=False,
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {STUDENT_ID} is created successfully"
    elif resp.status_code == 409:
        print("Interface already exists. Status Code: {}".format(resp.status_code))
        return f"Cannot create: Interface loopback {STUDENT_ID}"
    else:
        print("Error. Status Code: {}".format(resp.status_code))
        return f"Cannot create: Interface loopback {STUDENT_ID}"



def delete(router_ip=None):
    router = router_ip or os.environ.get("ROUTER_IP", "10.0.15.61")
    api_url = f"https://{router}:443/restconf/data/ietf-interfaces:interfaces/interface=Loopback{STUDENT_ID}"

    resp = requests.delete(
        api_url,
        auth=DEFAULT_BASICAUTH,
        headers=DEFAULT_HEADERS,
        verify=False,
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {STUDENT_ID} is deleted successfully"
    elif resp.status_code == 404:
        print("Interface not found. Status Code: {}".format(resp.status_code))
        return f"Cannot delete: Interface loopback {STUDENT_ID}"
    else:
        print("Error. Status Code: {}".format(resp.status_code))
        return f"Cannot delete: Interface loopback {STUDENT_ID}"



def enable(router_ip=None):
    router = router_ip or os.environ.get("ROUTER_IP", "10.0.15.61")
    api_url = f"https://{router}:443/restconf/data/ietf-interfaces:interfaces/interface=Loopback{STUDENT_ID}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{STUDENT_ID}",
            "enabled": True,
        }
    }

    resp = requests.patch(
        api_url,
        data=json.dumps(yangConfig),
        auth=DEFAULT_BASICAUTH,
        headers=DEFAULT_HEADERS,
        verify=False,
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {STUDENT_ID} is enabled successfully"
    elif resp.status_code == 404:
        print("Interface not found. Status Code: {}".format(resp.status_code))
        return f"Cannot enable: Interface loopback {STUDENT_ID}"
    else:
        print("Error. Status Code: {}".format(resp.status_code))
        return f"Cannot enable: Interface loopback {STUDENT_ID}"



def disable(router_ip=None):
    router = router_ip or os.environ.get("ROUTER_IP", "10.0.15.61")
    api_url = f"https://{router}:443/restconf/data/ietf-interfaces:interfaces/interface=Loopback{STUDENT_ID}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{STUDENT_ID}",
            "enabled": False,
        }
    }

    resp = requests.patch(
        api_url,
        data=json.dumps(yangConfig),
        auth=DEFAULT_BASICAUTH,
        headers=DEFAULT_HEADERS,
        verify=False,
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {STUDENT_ID} is shutdowned successfully"
    elif resp.status_code == 404:
        print("Interface not found. Status Code: {}".format(resp.status_code))
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}"
    else:
        print("Error. Status Code: {}".format(resp.status_code))
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}"



def status(router_ip=None):
    router = router_ip or os.environ.get("ROUTER_IP", "10.0.15.61")
    api_url_status = f"https://{router}:443/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback{STUDENT_ID}"

    resp = requests.get(
        api_url_status,
        auth=DEFAULT_BASICAUTH,
        headers=DEFAULT_HEADERS,
        verify=False,
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        iface = response_json.get("ietf-interfaces:interface", {})
        admin_status = iface.get("admin-status")
        oper_status = iface.get("oper-status")
        if admin_status == 'up' and oper_status == 'up':
            return f"Interface loopback {STUDENT_ID} is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return f"Interface loopback {STUDENT_ID} is disabled"
    elif resp.status_code == 404:
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return f"No Interface loopback {STUDENT_ID}"
    else:
        print("Error. Status Code: {}".format(resp.status_code))
        return f"Error checking status of Interface loopback {STUDENT_ID}"

