#!/usr/bin/env python3
from os import geteuid, system, listdir
from random import randint

def get_interfaces():
    
    # Get the list of equipments from /sys/classe/net
    print("\nGetting interfaces list ...\n")   
    availableIfaces = [str(i) for i in listdir("/sys/class/net")]

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
        userChoice = input("\nThis is not quite right !\nPlease choose an interface to use : ")

    # Get only the prefered interface to keep track of
    interface = choices[userChoice]
    print("\nYou chose : "+interface)
    return interface

def get_target(interface):
    
    print("\nGetting nearby AP list ...\n")
    system("iw dev "+interface+" scan | grep \"SSID:\" | rev | cut -d \":\" -f1 | rev | sed '/^*/d' > interfaces.tmp")
    
    choices = {}
    number = 0
    with open("interfaces.tmp", "r") as accessPoints:
        for accessPoint in accessPoints:
            print("[%i] : %s" %(number, accessPoint.strip("\n")))
            choices[str(number)] = accessPoint.strip("\n")
            number+=1
    
    userChoice = input("\nPlease choose the AP you want to target : ")
    while userChoice not in choices:
        userChoice = input("\nThis is not quite right !\nPlease choose the AP you want to target : ")
    
    system("rm interfaces.tmp")
    target = choices[userChoice]
    print("\nYou chose : "+target)
    return target

if __name__ == "__main__":
    
    # Check for root privileges
    if geteuid()!=0:
        print("You need sudo for that")
        exit()

    # Print a banner
    system("cat banner_%d.txt" % randint(0, 5))
    interface = get_interfaces()
    target = get_target(interface)
