#!/usr/bin/env python3
import sys
print("Python version", end="")
print (sys.version)
print("Version info.", end="")
print (sys.version_info)

import subprocess
import os
import paramiko


def ping(hostname):
    # hostname = "google.com" #example
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        print ("Destination is UP")
        return True
    else:
        print ("Destination is Down")
        return False

def send(channel, command=None, live=True):
    buff = ""
    if command != None:
        channel.send(command + '\n')
    while not buff.endswith(":~$ '"):
        resp = channel.recv(9999)
        buff += str(resp)
        if live:
            print(str(resp) + "\n")
        # print(buff, buff[-5:])
    return buff

def main():
    # cliend_ip = input("Client IP Address: ").strip()
    cliend_ip = "192.168.10.207"
    master_ip = "192.168.10.238"
    if ping(cliend_ip):
        print(cliend_ip)
        remote = None
        try:
            remote = paramiko.SSHClient()
            remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            remote.connect(cliend_ip, username="pi", password="raspberry")

            channel = remote.invoke_shell()
            send(channel)
            # print(send(channel, command="env"))
            print(send(channel, command="export ROS_MASTER_URI=http://%s:11311" % master_ip))
            print(send(channel, command="export ROS_HOSTNAME=%s" % cliend_ip))
            print(send(channel, command="env | grep \"ROS\""))
            print(send(channel, command="echo $ROS_MASTER_URI"))
            print(send(channel, command="roslaunch turtlebot3_bringup turtlebot3_robot.launch"))

            # buff = ""
            # while not buff.endswith(":~$ '"):
            #     resp = channel.recv(9999)
            #     buff += str(resp)
            #     # print(buff, buff[-5:])

            # channel.send("env" + '\n')
            # buff = ''
            # while True:
            #     resp = channel.recv(9999)
            #     buff += str(resp)
            #     print(buff)

            # print("END")
            # command = 
            # """
            # ROS_ETC_DIR=/opt/ros/kinetic/etc/ros
            # ROS_ROOT=/opt/ros/kinetic/share/ros
            # ROS_MASTER_URI=http://172.20.10.4:11311
            # ROS_VERSION=1
            # ROS_PACKAGE_PATH=/home/pi/catkin_ws/src:/opt/ros/kinetic/share
            # ROSLISP_PACKAGE_DIRECTORIES=/home/pi/catkin_ws/devel/share/common-lisp
            # ROS_HOSTNAME=172.20.10.2
            # ROS_DISTRO=kinetic

            # """

            # stdin,stdout,stderr=remote.exec_command("~/.profile")
            # outlines=stdout.readlines()
            # resp=''.join(outlines)
            # print(resp)

            # stdin,stdout,stderr=remote.exec_command("source ./pamiko.sh")
            # outlines=stdout.readlines()
            # resp=''.join(outlines)
            # print(resp)
            
            # stdin,stdout,stderr=remote.exec_command("env")
            # outlines=stdout.readlines()
            # resp=''.join(outlines)
            # print(resp)
            # # print ("you are login Sir")
            # remote.exec_command('echo "" > /home/pi/test.txt')
            # session = remote.invoke_shell()
            # session.send("enable\n")

            # print('started...')
            # stdin, stdout, stderr = remote.exec_command('cat ~/.bashrc', get_pty=False)

            # for line in iter(stdout.readline, ""):
            #     print(line, end="<")
            # print('finished.')

            # pre_cmd = "source ~/.bashrc;"
            # stdin, stdout, stderr = remote.exec_command("ls", get_pty=True)

            # # for line in iter(stdout.readline, ""):
            # #     print(line, end="<")
            # # print('finished.')
            # chan=remote.invoke_shell()
            # chan.send('echo $PATH\n')
            # print (chan.recv(1024))
        except Exception as e:
            print('Connection Failed')
            print(e)
        finally:
            print ("Close")
            if remote:
                remote.close()
        # remote.exec_command('ls -l')
        # stdin, stdout, stderr = remote.exec_command('ls -l')
        # print (stdout)
        # stdin.write("echo > '/home/pi/james.txt'")
        # stdin.flush()

if __name__ == "__main__":
    main()
