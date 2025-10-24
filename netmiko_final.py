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

