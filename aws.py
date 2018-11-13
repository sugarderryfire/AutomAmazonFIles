# -*- coding: utf-8 -*-

# Boto 3
import boto3
import time
import sys
import paramiko
import base64




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
        client.connect(hostname="54.227.50.10", username="ec2-user", pkey=key)
        print 'running remote command'
        # Execute a command(cmd) after connecting/ssh to an instance
        stdin, stdout, stderr = client.exec_command(command)
        print stdout.read()
        # close the client connection once the job is done
        client.close()
    except Exception, e:
        print e




def terminate_instances(instances):
    #terminate instances in ec2_instances arrן
    for instance in ec2.instances.filter(InstanceIds=ec2_instances):
        print instance
        instance.terminate()


def check_instances():
    reservations = ec2_connection.get_all_reservations(filters={'instance-state-name': 'running'})
    for reservation in reservations:
        for instance in reservation.instances:
	    print(instance.instance_id, instance.instance_type)
	    print instance.ip_address



ec2 = boto3.resource('ec2',region_name='us-east-1')
#execute_command
#config_instances()
#create_instances()
pythonfile='https://1drv.ms/u/s!Aoqg3Te2AhnqabCWJmhRFntkhiA'
comm1='wget -P '
comm1=comm1+pythonfile
execute_command(comm1)
