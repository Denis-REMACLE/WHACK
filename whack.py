#!/usr/bin/env python3
import os
from random import randint
import re

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
    
    print("\nGetting nearby AP list ...\n")
    os.system("iw dev "+interface+" scan | awk -f scan.awk > interfaces.tmp")
    
    choices = {}
    number = 0
    with open("interfaces.tmp", "r") as accessPoints:
        for accessPoint in accessPoints:
            print("[%i] : %s" %(number, accessPoint.strip("\n")))
            choices[str(number)] = accessPoint.strip("\n")
            number+=1
    
    userChoice = str(input("\nPlease choose the AP you want to target : "))
    while userChoice not in choices:
        print("\nThis is not quite right !")
        userChoice = str(input("\nPlease choose the AP you want to target : "))
    
    os.system("rm interfaces.tmp")

    target = choices[userChoice].split()
    print("\nYou chose : "+target)
    return target

if __name__ == "__main__":
    
    # Check for root privileges
    if os.geteuid()!=0:
        print("You need sudo for that")
        exit()

    # Print a banner
    os.system("cat banner/banner_%d.txt" % randint(0, 5))
    interface = get_interfaces()
    target = get_target(interface)