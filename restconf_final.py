import json
import requests
import os
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
# Get student ID and router IP from environment variables
STUDENT_ID = os.environ.get("STUDENT_ID", "66070000")
ROUTER_IP = os.environ.get("ROUTER_IP", "10.0.15.61")

# Calculate IP address from student ID (last 3 digits)
last_three = STUDENT_ID[-3:]
x = int(last_three[-3])
y = int(last_three[-2:])
LOOPBACK_IP = f"172.{x}.{y}.1"

api_url = f"https://{ROUTER_IP}:443/restconf/data/ietf-interfaces:interfaces/interface=Loopback{STUDENT_ID}"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")


def create():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{STUDENT_ID}",
            "description": f"Loopback interface for student {STUDENT_ID}",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": LOOPBACK_IP,
                        "netmask": "255.255.255.0"
                    }
                ]
            }
        }
    }

    resp = requests.put(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {STUDENT_ID} is created successfully"
    elif(resp.status_code == 409):
        print('Interface already exists. Status Code: {}'.format(resp.status_code))
        return f"Cannot create: Interface loopback {STUDENT_ID}"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Cannot create: Interface loopback {STUDENT_ID}"



def delete():
    resp = requests.delete(
        api_url, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {STUDENT_ID} is deleted successfully"
    elif(resp.status_code == 404):
        print('Interface not found. Status Code: {}'.format(resp.status_code))
        return f"Cannot delete: Interface loopback {STUDENT_ID}"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Cannot delete: Interface loopback {STUDENT_ID}"



def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{STUDENT_ID}",
            "enabled": True
        }
    }

    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {STUDENT_ID} is enabled successfully"
    elif(resp.status_code == 404):
        print('Interface not found. Status Code: {}'.format(resp.status_code))
        return f"Cannot enable: Interface loopback {STUDENT_ID}"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Cannot enable: Interface loopback {STUDENT_ID}"



def disable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{STUDENT_ID}",
            "enabled": False
        }
    }

    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {STUDENT_ID} is shutdowned successfully"
    elif(resp.status_code == 404):
        print('Interface not found. Status Code: {}'.format(resp.status_code))
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}"



def status():
    api_url_status = f"https://{ROUTER_IP}:443/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback{STUDENT_ID}"

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return f"Interface loopback {STUDENT_ID} is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return f"Interface loopback {STUDENT_ID} is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return f"No Interface loopback {STUDENT_ID}"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Error checking status of Interface loopback {STUDENT_ID}"

