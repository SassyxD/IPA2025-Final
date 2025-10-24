import subprocess
import os
import re

def showrun():
    """
    ใช้ Ansible playbook เพื่อสำรองการตั้งค่าจาก router
    ใช้งานได้บน Ubuntu/Linux เท่านั้น
    """
    try:
        # รัน Ansible playbook
        result = subprocess.run(
            ['ansible-playbook', 'playbook.yaml'],
            capture_output=True,
            text=True,
            env=os.environ.copy()
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            return 'ok'
        else:
            return 'Error: Ansible'
    except FileNotFoundError:
        print("Error: ansible-playbook not found.")
        print("Please install Ansible on Ubuntu:")
        print("  sudo apt install ansible")
        return 'Error: Ansible not installed'
    except Exception as e:
        print(f"Error running ansible playbook: {e}")
        return 'Error: Ansible'


def motd(message, router_ip=None):
    """Run an Ansible playbook to configure MOTD banner using environment variable MOTD.
    Returns 'ok' on success or an error string on failure.
    """
    try:
        # update hosts file to point to router_ip if provided
        if router_ip:
            try:
                hosts_path = os.path.join(os.path.dirname(__file__), "hosts")
                with open(hosts_path, "r") as f:
                    hosts_txt = f.read()
                new_hosts = re.sub(r"ansible_host=\d+\.\d+\.\d+\.\d+", f"ansible_host={router_ip}", hosts_txt)
                with open(hosts_path, "w") as f:
                    f.write(new_hosts)
            except Exception as e:
                print(f"Warning: cannot update hosts file for motd: {e}")

        env = os.environ.copy()
        env["MOTD"] = message

        result = subprocess.run(
            ['ansible-playbook', 'playbook_motd.yaml'],
            capture_output=True,
            text=True,
            env=env
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            return 'ok'
        else:
            return 'Error: Ansible'
    except FileNotFoundError:
        print("Error: ansible-playbook not found.")
        return 'Error: Ansible not installed'
    except Exception as e:
        print(f"Error running ansible playbook for MOTD: {e}")
        return 'Error: Ansible'

