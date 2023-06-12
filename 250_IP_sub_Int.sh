#!/bin/bash

# Define Network Interface
INTERFACE="enp0s31f6"

# Define IP base
IPBASE="192.168.60."

# Define subnet mask
NETMASK="255.255.255.0"

# Loop over the range
for i in {2..253}
do
    # Calculate the IP
    IP="$IPBASE$i"
    
    # Use ifconfig to add the IP to the NIC
    sudo ifconfig $INTERFACE:$i $IP netmask $NETMASK up

    # Output the command for logging purposes
    echo "Bound $IP to $INTERFACE:$i"
done

# Echo finished
echo "Finished binding IPs to $INTERFACE"

