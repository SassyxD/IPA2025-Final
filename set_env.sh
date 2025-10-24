#!/bin/bash

# IPA2024-Final Environment Variables Setup Script for Ubuntu/Linux

# Webex Teams Configuration
export WEBEX_ACCESS_TOKEN="ODc4Zjk4MmMtODUxYS00NzljLTk5MDQtNDhlMGQ4YzM0NGUyZDJmMjMyYjYtNWVi_PS65_e37c9b35-5d15-4275-8997-b5c6f91a842d"
export WEBEX_ROOM_ID="Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vYmQwODczMTAtNmMyNi0xMWYwLWE1MWMtNzkzZDM2ZjZjM2Zm"

# Student Configuration
export STUDENT_ID="66070061"

# Router Configuration
export ROUTER_IP="10.0.15.61"

echo "Environment variables set successfully!"
echo "Token: ${WEBEX_ACCESS_TOKEN:0:30}..."
echo "Room ID: ${WEBEX_ROOM_ID:0:30}..."
echo "Student ID: $STUDENT_ID"
echo "Router IP: $ROUTER_IP"
