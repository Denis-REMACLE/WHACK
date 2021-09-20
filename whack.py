#!/usr/bin/env python3
import os
from random import randint

def get_interfaces():
    
    # Get the list of equipments from /sys/classe/net
    print("\nGetting interfaces list ...\n")   
    availableIfaces = [str(i) for i in os.listdir("/sys/class/net")]

    choices = {}
    # Processing the interfaces into a readable dictionnary
    # And print the interfaces to the user
    for i in range(len(availableIfaces)):
        print("[%i] : %s" %(i, availableIfaces[i]))
        choices[str(i)] = str(availableIfaces[i])

    # Ask user for prefered interface
    userChoice = input("\nPlease choose an interface to use : ")

    # Check if the choice is good
    while userChoice not in choices:
        print("\nThis is not quite right !")
        userChoice = input("\nPlease choose an interface to use : ")

    # Get only the prefered interface to keep track of
    interface = choices[userChoice]
    print("\nYou chose : "+interface)
    return interface

def get_target(interface):
    
    print("\nGetting nearby AP list ...\n")
    os.system("iw dev "+interface+" scan\
                | grep \"SSID:\"\
                | rev \
                | cut -d \":\" -f1 \
                | rev \
                | sed '/^*/d' > interfaces.tmp")
    
    choices = {}
    number = 0
    with open("interfaces.tmp", "r") as accessPoints:
        for accessPoint in accessPoints:
            print("[%i] : %s" %(number, accessPoint.strip("\n")))
            choices[str(number)] = accessPoint.strip("\n")
            number+=1
    
    userChoice = input("\nPlease choose the AP you want to target : ")
    while userChoice not in choices:
        print("\nThis is not quite right !")
        userChoice = input("\nPlease choose the AP you want to target : ")
    
    os.system("rm interfaces.tmp")
    target = choices[userChoice]
    print("\nYou chose : "+target)
    return target

if __name__ == "__main__":
    
    # Check for root privileges
    if os.geteuid()!=0:
        print("You need sudo for that")
        exit()

    # Print a banner
    f = open("banner/banner_%d.txt" % randint(0, 5), 'r')
    f.read()
    f.close()
    interface = get_interfaces()
    target = get_target(interface)
