# Webex Usage Guide for IPA2025-Final

## Prerequisites

1. **Environment Variables** - Set these before running:
```bash
export WEBEX_ACCESS_TOKEN="your_webex_bot_token_here"
export WEBEX_ROOM_ID="your_webex_room_id_here"
export STUDENT_ID="66070123"  # Replace with your student ID
```

2. **Activate Virtual Environment**:
```bash
source .venv/bin/activate
```

3. **Network Access**:
   - Must be on KMITl network or VPN to access routers (10.0.15.61-65)
   - Routers must have NETCONF (port 830) and RESTCONF (port 443) enabled

## Running the Bot

```bash
source .venv/bin/activate
python3 ipa2024_final.py
```

The bot will continuously poll for new messages in the Webex room.

## Supported Commands

### 1. Method Selection (Restconf/Netconf)
First, select which method to use for loopback interface commands:

```
/66070123 restconf
```
Response: `Ok: Restconf`

```
/66070123 netconf
```
Response: `Ok: Netconf`

### 2. Loopback Interface Commands

All these commands require **method selection first** and must specify **router IP**:

**Create Interface:**
```
/66070123 10.0.15.61 create
```
Response: `Interface loopback 66070123 is created successfully using Restconf` (or Netconf)

**Delete Interface:**
```
/66070123 10.0.15.61 delete
```
Response: `Interface loopback 66070123 is deleted successfully using Netconf`

**Enable Interface:**
```
/66070123 10.0.15.61 enable
```
Response: `Interface loopback 66070123 is enabled successfully using Restconf`

**Disable Interface:**
```
/66070123 10.0.15.61 disable
```
Response: `Interface loopback 66070123 is shutdowned successfully using Netconf`

**Check Status:**
```
/66070123 10.0.15.61 status
```
Response: 
- `Interface loopback 66070123 is enabled` (if up)
- `Interface loopback 66070123 is disabled` (if down)
- `No Interface loopback 66070123` (if doesn't exist)

### 3. GigabitEthernet Status (Netmiko)

Check status of all GigabitEthernet interfaces:

```
/66070123 10.0.15.61 gigabit_status
```
Response example:
```
GigabitEthernet1 up, GigabitEthernet2 up, GigabitEthernet3 down, GigabitEthernet4 administratively down -> 2 up, 1 down, 1 administratively down
```

### 4. Show Running Config (Ansible)

Save and retrieve running configuration:

```
/66070123 10.0.15.61 showrun
```
Response: Sends file `show_run_66070123_CSR1KV-Pod1-1.txt` attached to Webex message

### 5. MOTD Banner Configuration

**Set MOTD (using Ansible):**
```
/66070123 10.0.15.61 motd Authorized users only! Managed by 66070123
```
Response: `Ok: success`

**Read MOTD (using Netmiko):**
```
/66070123 10.0.15.61 motd
```
Response: `Authorized users only! Managed by 66070123`
or `Error: No MOTD Configured` if none set

## Error Messages

The bot provides clear error messages:

- `Error: No method specified` - You need to select restconf or netconf first
- `Error: No IP specified` - Command requires router IP (10.0.15.61-65)
- `Error: IP not allowed` - IP must be in range 10.0.15.61-65
- `Error: No command specified` - No valid command found in message
- `Cannot create: Interface loopback XXX` - Interface already exists
- `Cannot delete: Interface loopback XXX` - Interface doesn't exist
- `Error: Ansible` - Ansible playbook failed

## Example Workflow

```
# 1. Select method
/66070123 restconf
> Ok: Restconf

# 2. Create loopback interface
/66070123 10.0.15.61 create
> Interface loopback 66070123 is created successfully using Restconf

# 3. Check status
/66070123 10.0.15.61 status
> Interface loopback 66070123 is enabled

# 4. Set MOTD
/66070123 10.0.15.61 motd Welcome to Router 1
> Ok: success

# 5. Read MOTD
/66070123 10.0.15.61 motd
> Welcome to Router 1

# 6. Check GigabitEthernet interfaces
/66070123 10.0.15.61 gigabit_status
> GigabitEthernet1 up, GigabitEthernet2 up, GigabitEthernet3 down, GigabitEthernet4 administratively down -> 2 up, 1 down, 1 administratively down

# 7. Get running config
/66070123 10.0.15.61 showrun
> (File attachment: show_run_66070123_CSR1KV-Pod1-1.txt)

# 8. Switch to different router
/66070123 10.0.15.62 create
> Interface loopback 66070123 is created successfully using Restconf

# 9. Switch to Netconf method
/66070123 netconf
> Ok: Netconf

# 10. Now commands use Netconf
/66070123 10.0.15.63 create
> Interface loopback 66070123 is created successfully using Netconf
```

## Notes

- **Order matters**: For loopback commands, you must select a method (restconf/netconf) before running create/delete/enable/disable/status
- **IP is required**: All commands except method selection require a router IP
- **Method is persistent**: Once you select restconf or netconf, it stays selected until you change it
- **Multiple routers**: You can target different routers (10.0.15.61-65) without changing method
- **MOTD and gigabit_status**: These don't require method selection (they use Ansible/Netmiko directly)

## Troubleshooting

**Bot not responding:**
- Check WEBEX_ACCESS_TOKEN and WEBEX_ROOM_ID are set correctly
- Verify bot has access to the room
- Check network connectivity

**Cannot connect to router:**
- Verify you're on KMITl network or VPN
- Check router IP is in allowed range (10.0.15.61-65)
- Verify router has NETCONF/RESTCONF enabled
- Check credentials (admin/cisco)

**Ansible errors:**
- Ensure cisco.ios collection is installed: `ansible-galaxy collection install cisco.ios`
- Check hosts file has correct ansible_host IP
- Verify SSH connectivity to router

**Import errors:**
- Activate virtual environment: `source .venv/bin/activate`
- Reinstall packages: `pip install -r requirements.txt`
