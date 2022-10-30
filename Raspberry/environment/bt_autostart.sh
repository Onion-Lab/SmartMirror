#!/bin/bash
bluetoothctl <<EOF
power on
discoverable on
pairable on
EOF
sudo rfcomm release 0
sudo rfcomm watch hci0 &
