# -*- coding: utf-8 -*-

# Boto 3
import boto3
import time
import sys
import paramiko
import base64
import os
import random
import subprocess



#hostIP="54.152.202.91"
runningInstances=[]
regionList=["us-east-1","us-east-2","us-west-1","us-west-2","eu-west-2","ap-southeast-2","ap-northeast-1","eu-central-1"]
imageList=["ami-0ac019f4fcb7cb7e6","ami-0f65671a86f061fcd","ami-063aa838bd7631e0b","ami-0bbe6b35405ecebdb","ami-0b0a60c0a2bd40612","ami-07a3bd4944eb120a0","ami-07ad4b1c3af1ea214","ami-0bdf93799014acdc4"]
chosenImage=""


def config_instances():
    outfile = open('ec2keyInstance4.pem','w')
    key_pair = ec2.create_key_pair(KeyName='ec2keyInstance4')
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)


def create_instances():
    #create instances.
    ec2_instances = ec2.create_instances(ImageId="ami-0ac019f4fcb7cb7e6",MinCount=1,MaxCount=1,KeyName="ec2keyInstance4")
    time.sleep(10)
    return ec2_instances



def execute_command(hostIP):
    key = paramiko.RSAKey.from_private_key_file('ec2keyInstance4.pem')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect/ssh to an instance
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=hostIP, username="ubuntu", pkey=key)
        execute(client,'wget https://github.com/sugarderryfire/AutomAmazonFIles/blob/master/geckodriver?raw=true')
	execute(client,'mv geckodriver\?raw\=true geckodriver')
        execute(client,'wget https://raw.githubusercontent.com/sugarderryfire/AutomAmazonFIles/master/Automain.py')
        execute(client,'sudo apt -y install python')
        execute(client,'sudo apt update')
        execute(client,'sudo apt -y install python-pip')
	execute(client,'sudo pip install selenium')
	execute(client,'sudo pip install xlrd')
	execute(client,'sudo pip install pandas')
	execute(client,'sudo pip install openpyxl')
	execute(client,'sudo pip install stem')
	execute(client,'sudo pip install splinter')
	execute(client,'sudo apt -y install xvfb')
	#execute(client,'export DISPLAY=:99')
        # close the client connection once the job is done
   	client.close()
    except Exception, e:
        print e


def execute_command2(hostIP):
    key = paramiko.RSAKey.from_private_key_file('ec2keyInstance4.pem')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect/ssh to an instance
    try:
	time.sleep(5)
	print 'second stage'
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=hostIP, username="ubuntu", pkey=key)
	execute(client,'sudo cp geckodriver /usr/local/bin/geckodriver')
	execute(client,'sudo chmod +x /usr/local/bin/geckodriver')
	execute(client,'sudo apt-get -y install firefox')
        # close the client connection once the job is done
   	client.close()
    except Exception, e:
        print e



def execute_command3(hostIP):
    mandatoryCommand="cat scr.sh | ssh -o StrictHostKeyChecking=no -i ec2keyInstance4.pem ubuntu@"
    mandatoryCommand=mandatoryCommand+hostIP
#    mandatoryCommand=mandatoryCommand+ " |"
    #mandatoryCommand=mandatoryCommand + " && exit"
    key = paramiko.RSAKey.from_private_key_file('ec2keyInstance4.pem')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect/ssh to an instance
    try:
	time.sleep(5)
	print 'third stage'
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=hostIP, username="ubuntu", pkey=key)
	execute(client,'sudo apt -y install xvfb')
#	execute(client,comm1)
        #execute(client,comm2)
	mandatoryCommand=mandatoryCommand+" &"
	os.system(mandatoryCommand)
	#execute(client,mandatoryCommand)
	#returned_output = subprocess.check_output(mandatoryCommand)	
	print 'test1v'
	#execute(client,'python Automain.py blockchain block.chain.technology')
        # close the client connection once the job is done
   	client.close()
    except Exception, e:
        print e




def execute(client,command):
    try:
        print 'running remote command'
        # Execute a command(cmd) after connecting/ssh to an instance
        stdin, stdout, stderr = client.exec_command(command)
        print stdout.read()
    except Exception, e:
        print e
	




def terminate_instances():
    print 'terminate'
    #terminate instances in ec2_instances arrן
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
	instance.terminate()
	print instance.public_ip_address



def get_instances():
    # Boto 3
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    instancesList=[]
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
	instancesList.append(instance.public_ip_address)
	print(instance.id, instance.instance_type,instance.public_ip_address)
    return instancesList


def get_first_instance():
    # Boto 3
    # Use the filter() method of the instances collection to retrieve
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
	return instance.public_ip_address

    

def get_currentRegion():
    global chosenImage
    listLen=len(regionList)
    chosenIndex=random.randint(0,listLen-1)
    chosenImage=imageList[chosenIndex]
    return regionList[chosenIndex]


def get_random(min1,max1):
    chosenNumber=random.randint(min1-1,max1-1)
    return chosenNumber


ec2 = boto3.resource('ec2',region_name="us-east-1")

#execute_command
#config_instances()
while(True):
    create_instances()
    time.sleep(100)
    #get_instances()
    hostIP=str(get_first_instance())
    print hostIP
    execute_command(hostIP)
    execute_command2(hostIP)
    execute_command3(hostIP)
    print 'test'
    time.sleep(400)
    #time.sleep(get_random(360,500))
    terminate_instances()
    time.sleep(100)
#sys.exit(0)
#time.sleep(get_random(300,400))
