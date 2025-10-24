import subprocess
import os

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

