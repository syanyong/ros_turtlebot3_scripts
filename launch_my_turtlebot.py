#!/usr/bin/env python
"""
Author: Sarucha Yanyong
Purpose: Remote control turtlebot3
Revision:
1.0  2019-07-10 Baseline
"""

import sys
import subprocess
import os
import paramiko
import socket
import re
import time



def ping(hostname):
    # hostname = "google.com" #example
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        print ("Ping: Destination is UP")
        return True
    else:
        print ("Ping: Destination is Down")
        return False

def send(channel, command=None, live=True, once=False):
    buff = ""
    if command != None:
        channel.send(command + '\n')
    if once:
        return "shutdown"
    while not buff.endswith(":~$ "):
        resp = channel.recv(9999)
        buff += str(resp)
        if live:
            print(str(resp) + "\n")
        # print(buff)
    # print("OUT")
    return buff

def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

def main():
    print("Python version")
    print (sys.version)
    print("Version info.")
    print (sys.version_info)

    # cliend_ip = input("Client IP Address: ").strip()
    master_ip = cliend_ip = None
    # cliend_ip = "192.168.10.207"
    # master_ip = "192.168.10.238"

    if len(sys.argv) >= 2:
        if is_valid_ip(sys.argv[1]) and is_valid_ip(sys.argv[2]):
            master_ip = sys.argv[1]
            cliend_ip = sys.argv[2]
    if master_ip is None and cliend_ip is None:
        master_ip = raw_input("Computer IP Address: ").strip()
        cliend_ip = raw_input("TurtleBot IP Address: ").strip()
    
    print("Connect %s to %s" % (master_ip, cliend_ip))


    if not is_valid_ip(cliend_ip) or not is_valid_ip(master_ip):
        print("Wrong IP Address format.")
        sys.exit(0)


    mode = raw_input("""
    Options
    =========
    [1] Check turtlebot connection.
    [2] Bringup Turtlebot
    [3] Remote shutdown Turtlebot
    [4] Remote restart Turtlebot
    """
    ).strip()
    
    if mode == "1":
        print("Alive." if ping(cliend_ip) else "Lost connection.")

    elif mode == "3":
        if ping(cliend_ip):
            remote = None
            try:
                remote = paramiko.SSHClient()
                remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                remote.connect(cliend_ip, username="pi", password="raspberry")

                channel = remote.invoke_shell()
                send(channel)
                print(send(channel, command="sudo shutdown now", once=True))
                print(send(channel, command="raspberry", once=True))
            except Exception as e:
                print('Connection Failed')
                print(e)
            finally:
                print ("Close")
                if remote:
                    remote.close()

            while ping(cliend_ip):
                print("Shunting down...")
                time.sleep(1)
            print("Robot has been shutdown completely.")

    elif mode == "4":
        if ping(cliend_ip):
            remote = None
            try:
                remote = paramiko.SSHClient()
                remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                remote.connect(cliend_ip, username="pi", password="raspberry")

                channel = remote.invoke_shell()
                send(channel)
                print(send(channel, command="sudo reboot", once=True))
                print(send(channel, command="raspberry", once=True))
            except Exception as e:
                print('Connection Failed')
                print(e)
            finally:
                print ("Close")
                if remote:
                    remote.close()

            while ping(cliend_ip):
                print("Shunting down...")
                time.sleep(1)
            while not ping(cliend_ip):
                print("Booting up...")
                time.sleep(1)
            print("Robot has been reboot completely.")

    elif mode == "2":
        if ping(cliend_ip):
            print(cliend_ip)
            remote = None
            try:
                remote = paramiko.SSHClient()
                remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                remote.connect(cliend_ip, username="pi", password="raspberry")

                channel = remote.invoke_shell()
                send(channel)
                print(send(channel, command="export ROS_MASTER_URI=http://%s:11311" % master_ip))
                print(send(channel, command="export ROS_HOSTNAME=%s" % cliend_ip))
                print(send(channel, command="env | grep \"ROS\""))
                print(send(channel, command="echo $ROS_MASTER_URI"))
                print(send(channel, command="roslaunch turtlebot3_bringup turtlebot3_robot.launch"))
            except Exception as e:
                print('Connection Failed')
                print(e)
            finally:
                print ("Close")
                if remote:
                    remote.close()

if __name__ == "__main__":
    main()
