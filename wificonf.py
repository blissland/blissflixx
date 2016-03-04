#!/usr/bin/python3
#===============================================================
#Simple Python3 prog to display current IP Address and to allow
# users to enter wifi details and update the file:-
#   /etc/wpa_supplicant/wpa_supplicant.conf
#SteveDee 
#Feb 2016
#----------------------------------------------------------------
import os
import time

#extract IP Address from ifconfig
TheIP = "blank"
os.system("ifconfig > /home/pi/blissflixx/ifconfig.txt")
f_ipaddr = open('/home/pi/blissflixx/ifconfig.txt', 'r')
inet_details = f_ipaddr.read()
index=inet_details.find("inet addr:")
offset = len("inet addr:")
#I assume there are no more than 3 "inet addr" entries in ifconfig
if index < 0:
    print("\n>>>>>>>>>>>>>>  Hmmm, can't find an IP address!\n")
else:
    testip = inet_details[index+offset:index+25]
    index_sp =  testip.find(" ")
    testip=testip[0:index_sp]
    if testip != "127.0.0.1":        #exclude loopback
        TheIP = testip
    else:
        testip=inet_details[index+offset:len(inet_details)]
        index=testip.find("inet addr:")
        if index < 0:
            print("\n>>>>>>>>>>>>  Hmmm, can't find an IP address!\n")
        else:
            testip=testip[index+offset:index+25]
            index_sp = testip.find(" ")
            TheIP =testip[0:index_sp]

if TheIP != "blank":
    print("\n*********************************************************************************\n")
    print("\nPoint the browser on your remote tablet/laptop/phone to http://"+TheIP+"\n")
    print("\n*********************************************************************************\n\n")

os.system("iwconfig > /home/pi/blissflixx/iwconfig.txt")
time.sleep(5)
f_wireless = open('/home/pi/blissflixx/iwconfig.txt', 'r')
wifi_details = f_wireless.read()
index = wifi_details.find("Bit Rate")
if index > -1:
    rate = wifi_details[index:index + 17]
    print ("\n Wifi " + rate + "\n")

print ("\n If you need to re-configure BlissFlixx to suit your wifi...\n")
print ("   ... please attached a keyboard to your Pi & enter the wifi/router SSID\n")

#re-configure wifi
varSSID = input("SSID: ")
varPASS = input("Please enter wifi password: ")
print (varSSID,' ',varPASS,'\n')
os.system('wpa_passphrase ' + '"' +varSSID + '"' +" " + '"' + varPASS + '"' + ' > /home/pi/a_pytest')
f_template = open('/home/pi/blissflixx/wpa_template', 'r')
f_wifi = open('/home/pi/a_pytest', 'r')
wpa_details = f_template.read() + '\n\n' + f_wifi.read()
print (wpa_details)
f_wpasupp = open('/home/pi/a_pytest', 'w')
f_wpasupp.write(wpa_details)
f_wpasupp.close()
f_wifi.close()
f_template.close()
os.system('sudo mv /home/pi/a_pytest /etc/wpa_supplicant/wpa_supplicant.conf')
print ("...I just need to re-boot the Pi so that changes can take affect...this may take a minute or two to stop all processes...")
time.sleep(5)
os.system('sudo shutdown now -r')
