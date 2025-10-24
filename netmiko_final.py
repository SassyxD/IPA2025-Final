from netmiko import ConnectHandler
from pprint import pprint
import os

device_ip = os.environ.get("ROUTER_IP", "10.0.15.61")
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        interface_status = []
        for status in result:
            if "GigabitEthernet" in status["interface"]:
                interface_status.append(f"{status['interface']} {status['status']}")
                if status["status"] == "up":
                    up += 1
                elif status["status"] == "down":
                    down += 1
                elif status["status"] == "administratively down":
                    admin_down += 1
        ans = f"{', '.join(interface_status)} -> {up} up, {down} down, {admin_down} administratively down"
        pprint(ans)
        return ans


def read_motd():
    """Return configured MOTD banner using netmiko. If none, return error string."""
    try:
        with ConnectHandler(**device_params) as ssh:
            # show running-config and filter banner motd line
            output = ssh.send_command("show running-config | include banner motd")
            if not output or "banner motd" not in output:
                return "Error: No MOTD Configured"
            # expect something like: banner motd ^Authorized users only! Managed by 66070123^
            # extract between first ^ and last ^
            m = output.strip()
            # find the first caret ^ occurrence
            if '^' in m:
                parts = m.split('^')
                if len(parts) >= 2 and parts[1].strip():
                    return parts[1].strip()
            # fallback: return full line
            return m
    except Exception as e:
        print(f"Error reading MOTD via netmiko: {e}")
        return "Error: No MOTD Configured"

