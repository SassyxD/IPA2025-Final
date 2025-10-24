#######################################################################################
# Yourname: [Student Name]
# Your student ID: [Student ID]
# Your GitHub Repo: https://github.com/SassyxD/IPA2024-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import requests
import json
import time
import os
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
import restconf_final
import netmiko_final
import ansible_final
import netconf_final

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.environ.get("WEBEX_ACCESS_TOKEN")
STUDENT_ID = os.environ.get("STUDENT_ID", "66070000")
ROOM_ID = os.environ.get("WEBEX_ROOM_ID")

# state file to remember selected method (restconf/netconf) per student
STATE_FILE = "state.json"

# allowed router IPs for IPA2025
ALLOWED_ROUTERS = {f"10.0.15.{i}" for i in range(61, 66)}


def _load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Warning: could not save state: {e}")


def _is_ip(s):
    return re.match(r"^\d+\.\d+\.\d+\.\d+$", s) is not None

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = ROOM_ID

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith(f"/{STUDENT_ID}"):
        parts = message.split()
        args = parts[1:]
        responseMessage = "Error: No command or unknown command"
        command = None  # Initialize command variable
        ip = None  # Initialize ip variable

        # load persistent state (method selection)
        state = _load_state()
        method = state.get(STUDENT_ID)

        # if user only sent method selection: "/66070123 restconf"
        if len(args) == 1 and args[0] in ("restconf", "netconf"):
            state[STUDENT_ID] = args[0]
            _save_state(state)
            responseMessage = f"Ok: {args[0].capitalize()}"
            print(responseMessage)
        else:
            # try to extract ip and command from args
            for a in args:
                if _is_ip(a):
                    ip = a
                elif a in ("create", "delete", "enable", "disable", "status", "gigabit_status", "showrun", "motd"):
                    command = a

            # If it's a command that requires method (create/delete/enable/disable/status)
            if command in ("create", "delete", "enable", "disable", "status"):
                if not method:
                    responseMessage = "Error: No method specified"
                else:
                    if not ip:
                        responseMessage = "Error: No IP specified"
                    elif ip not in ALLOWED_ROUTERS:
                        responseMessage = "Error: IP not allowed"
                    else:
                        if method == "restconf":
                            if command == "create":
                                responseMessage = restconf_final.create(router_ip=ip)
                            elif command == "delete":
                                responseMessage = restconf_final.delete(router_ip=ip)
                            elif command == "enable":
                                responseMessage = restconf_final.enable(router_ip=ip)
                            elif command == "disable":
                                responseMessage = restconf_final.disable(router_ip=ip)
                            elif command == "status":
                                responseMessage = restconf_final.status(router_ip=ip)
                        elif method == "netconf":
                            if command == "create":
                                responseMessage = netconf_final.create(router_ip=ip)
                            elif command == "delete":
                                responseMessage = netconf_final.delete(router_ip=ip)
                            elif command == "enable":
                                responseMessage = netconf_final.enable(router_ip=ip)
                            elif command == "disable":
                                responseMessage = netconf_final.disable(router_ip=ip)
                            elif command == "status":
                                responseMessage = netconf_final.status(router_ip=ip)

            # Commands that do not depend on restconf/netconf selection
            elif command == "gigabit_status":
                if not ip:
                    responseMessage = "Error: No IP specified"
                elif ip not in ALLOWED_ROUTERS:
                    responseMessage = "Error: IP not allowed"
                else:
                    # override netmiko target and run
                    netmiko_final.device_ip = ip
                    responseMessage = netmiko_final.gigabit_status()

            elif command == "showrun":
                if not ip:
                    responseMessage = "Error: No IP specified"
                elif ip not in ALLOWED_ROUTERS:
                    responseMessage = "Error: IP not allowed"
                else:
                    # update hosts inventory to point to requested router IP
                    try:
                        hosts_path = os.path.join(os.path.dirname(__file__), "hosts")
                        with open(hosts_path, "r") as f:
                            hosts_txt = f.read()
                        new_hosts = re.sub(r"ansible_host=\d+\.\d+\.\d+\.\d+", f"ansible_host={ip}", hosts_txt)
                        with open(hosts_path, "w") as f:
                            f.write(new_hosts)
                    except Exception as e:
                        print(f"Warning: cannot update hosts file: {e}")
                    responseMessage = ansible_final.showrun()

            elif command == "motd":
                # MOTD: if a message follows 'motd' -> set via Ansible; otherwise read via netmiko
                motd_message = ""
                if 'motd' in args:
                    try:
                        motd_index = args.index('motd')
                        motd_message = ' '.join(args[motd_index+1:]).strip()
                    except Exception:
                        motd_message = ""

                if motd_message:
                    # set MOTD via Ansible
                    if not ip:
                        responseMessage = "Error: No IP specified"
                    elif ip not in ALLOWED_ROUTERS:
                        responseMessage = "Error: IP not allowed"
                    else:
                        result = ansible_final.motd(motd_message, router_ip=ip)
                        if result == 'ok':
                            responseMessage = "Ok: success"
                        else:
                            responseMessage = result
                else:
                    # read MOTD using netmiko
                    if not ip:
                        responseMessage = "Error: No IP specified"
                    elif ip not in ALLOWED_ROUTERS:
                        responseMessage = "Error: IP not allowed"
                    else:
                        netmiko_final.device_ip = ip
                        responseMessage = netmiko_final.read_motd()

            else:
                # No recognized command parsed
                if not args:
                    responseMessage = "Error: No command specified"
                elif not command and not ip:
                    responseMessage = "Error: No command found."
                elif not command:
                    responseMessage = "Error: No command found."
                else:
                    responseMessage = "Error: No command or unknown command"

        print("Resolved response:", responseMessage)
        
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        if command == "showrun" and responseMessage == 'ok':
            # Find the show run file
            import glob
            filename_pattern = f"show_run_{STUDENT_ID}_*.txt"
            matching_files = glob.glob(filename_pattern)
            
            if matching_files:
                filename = matching_files[0]
                fileobject = open(filename, 'rb')
                filetype = "text/plain"
                postData = {
                    "roomId": roomIdToGetMessages,
                    "text": "show running config",
                    "files": (filename, fileobject, filetype),
                }
                postData = MultipartEncoder(postData)
                HTTPHeaders = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": postData.content_type,
                }
            else:
                # If file not found, send error message
                postData = {"roomId": roomIdToGetMessages, "text": "Error: Config file not found"}
                postData = json.dumps(postData)
                HTTPHeaders = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
        # other commands only send text, or no attached file.
        else:
            postData = {"roomId": roomIdToGetMessages, "text": responseMessage}
            postData = json.dumps(postData)

            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
            HTTPHeaders = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}   

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=HTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
