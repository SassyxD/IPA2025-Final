from ncclient import manager
import xmltodict
import os

ROUTER_IP = os.environ.get("ROUTER_IP", "10.0.15.61")
STUDENT_ID = os.environ.get("STUDENT_ID", "66070000")

m = manager.connect(
    host=ROUTER_IP,
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

def create():
    last_three = STUDENT_ID[-3:]
    x = int(last_three[-3])
    y = int(last_three[-2:])
    loopback_ip = f"172.{x}.{y}.1"
    
    netconf_config = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback{STUDENT_ID}</name>
                <description>Loopback interface for student {STUDENT_ID}</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                <enabled>true</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{loopback_ip}</ip>
                        <netmask>255.255.255.0</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {STUDENT_ID} is created successfully"
    except Exception as e:
        print(f"Error: {e}")
        return f"Cannot create: Interface loopback {STUDENT_ID}"


def delete():
    netconf_config = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="delete">
                <name>Loopback{STUDENT_ID}</name>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {STUDENT_ID} is deleted successfully"
    except Exception as e:
        print(f"Error: {e}")
        return f"Cannot delete: Interface loopback {STUDENT_ID}"


def enable():
    netconf_config = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback{STUDENT_ID}</name>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {STUDENT_ID} is enabled successfully"
    except Exception as e:
        print(f"Error: {e}")
        return f"Cannot enable: Interface loopback {STUDENT_ID}"


def disable():
    netconf_config = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback{STUDENT_ID}</name>
                <enabled>false</enabled>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {STUDENT_ID} is shutdowned successfully"
    except Exception as e:
        print(f"Error: {e}")
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}"

def netconf_edit_config(netconf_config):
    return m.edit_config(target="running", config=netconf_config)


def status():
    netconf_filter = f"""
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback{STUDENT_ID}</name>
            </interface>
        </interfaces-state>
    </filter>
    """

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        if netconf_reply_dict.get('rpc-reply', {}).get('data', {}).get('interfaces-state', {}).get('interface'):
            # extract admin_status and oper_status from netconf_reply_dict
            interface = netconf_reply_dict['rpc-reply']['data']['interfaces-state']['interface']
            admin_status = interface.get('admin-status', 'down')
            oper_status = interface.get('oper-status', 'down')
            if admin_status == 'up' and oper_status == 'up':
                return f"Interface loopback {STUDENT_ID} is enabled"
            elif admin_status == 'down' and oper_status == 'down':
                return f"Interface loopback {STUDENT_ID} is disabled"
        else: # no operation-state data
            return f"No Interface loopback {STUDENT_ID}"
    except Exception as e:
        print(f"Error: {e}")
        return f"No Interface loopback {STUDENT_ID}"
