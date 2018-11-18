# -*- coding: utf-8 -*-

# Boto 3
import boto3
import time
import sys
import paramiko
import base64
import os


hostIP="54.152.202.91"
runningInstances=[]
regionLIst=["us-east-1","us-east-2","us-west-1","us-west-2","eu-west-2","ap-southeast-2","ap-northeast-1","eu-central-1"]


def config_instances():
    outfile = open('ec2keyInstance4.pem','w')
    key_pair = ec2.create_key_pair(KeyName='ec2keyInstance4')
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)


def create_instances():
    #create instances.
    ec2_instances = ec2.create_instances(ImageId='ami-013be31976ca2c322',MinCount=1,MaxCount=1,KeyName="ec2keyInstance4")
    time.sleep(10)

    """
    for instance in ec2_instances:
        while instance.state != "running":
            print '...instance is {state}'.format(state=instance.state)
            sys.stdout.flush()
            time.sleep(5)
    """
    return ec2_instances



def execute_command(command):
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


def execute_command2():
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



def execute_command3():
    key = paramiko.RSAKey.from_private_key_file('ec2keyInstance4.pem')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    comm1='yes "" | /usr/bin/Xvfb :99 -ac -screen 0 1024x768x8'
    comm2='export DISPLAY=:99'
    # Connect/ssh to an instance
    try:
	time.sleep(5)
	print 'third stage'
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=hostIP, username="ubuntu", pkey=key)
	execute(client,'sudo apt -y install xvfb')
#	execute(client,comm1)
        #execute(client,comm2)
	os.system('cat scr.sh | ssh -i ec2keyInstance4.pem ubuntu@54.152.202.91')
	#execute(client,'python Automain.py blockchain block.chain.technology')
        # close the client connection once the job is done
   	client.close()
    except Exception, e:
        print e

def execute_command4():
    key = paramiko.RSAKey.from_private_key_file('ec2keyInstance4.pem')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    comm1='/usr/bin/Xvfb :99 -ac -screen 0 1024x768x8 & export DISPLAY=:99 & python Automain.py blockchain block.chain.technology'
    comm2='yes "" | export DISPLAY=:99'
    # Connect/ssh to an instance
    try:
	time.sleep(5)
	print 'fourth stage'
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=hostIP, username="ubuntu", pkey=key)
	#execute(client,comm2)
	execute(client,'python Automain.py blockchain block.chain.technology')
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
	




def terminate_instances(instances):
    #terminate instances in ec2_instances arrן
    for instance in ec2.instances.filter(InstanceIds=ec2_instances):
        print instance
        instance.terminate()



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



def check_instances():
    runningInstances=[]
    reservations = ec2_connection.get_all_reservations(filters={'instance-state-name': 'running'})
    for reservation in reservations:
        for instance in reservation.instances:
	    print(instance.instance_id, instance.instance_type)
	    runningInstances.append(instance.ip_address)
	    print instance.ip_address



ec2 = boto3.resource('ec2',region_name='us-east-1')
get_instances()
#execute_command
#config_instances()
#create_instances()
time.sleep(60)
#execute_command()
#execute_command2()
#execute_command3()
