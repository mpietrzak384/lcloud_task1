#!/usr/bin/env python

# -*- coding: utf8 -*-"



import boto3

from botocore.client import ClientError

import requests

import subprocess

import os

# Collecting information about EC2 instance from AWS service

user_data = 'http://169.254.169.254/latest/user-data'

meta_data = 'http://169.254.169.254/latest/meta-data'

ec2InsDatafile = 'ec2InsDatafile'

ec2_params = {
    'Instance ID': 'instance-id',
    'Public IP': 'public-ipv4',
    'Private IP': 'local-ipv4',
    'Security Groups': 'security-groups',
}

try:

    fh = open(ec2InsDatafile, 'w')

except:

    print('Error while opening file for write')

for param, value in ec2_params.items():

    try:

        responce = requests.get(meta_data +'/' + value)

    except:

        print("Error while making request")

    if isinstance(responce.text,list):

        print(responce.text +': is list')

        data = ' '.joint(responce.text)

    else:

        data = param +":"+responce.text

    try:

          fh.write(data+'\r\n')

    except:

        print('Error during writing to file')
        print(data)

#Getting  OS related if from system files

os_vers = "grep '^VERSION=' /etc/os-release |cut -d'=' -f2"
os_name = "grep '^NAME' /etc/os-release |cut -d'=' -f2"
os_name_val ='OS NAME: '+ os.popen(os_name).read().rstrip()
os_vers_val ='OS VERSION: '+ os.popen(os_vers).read().rstrip()
os_usrs = "grep -E '/bin/(bash|sh)$' /etc/passwd | awk -F: '{print $1}' | xargs echo"
os_usrs_val = 'Login able users: ' + os.popen(os_usrs).read().strip()

try:
    fh.write('Operating System: ' + os_name_val + ' ' + os_vers_val + '\r\n')

    fh.write(os_usrs_val+'\r\n')

except:

    print("Error during write to file")
    fh.close()

# Upload file to s3 storage

s3_bucket_name = 'applicant-task'
s3_key_prefix = 'r5d4/'

s3_conn = boto3.client('s3')


try:

    with open(ec2InsDatafile, 'r') as fh:
        
        response=requests.get(meta_data +'/' + 'instance-id')

        s3_conn.put_object(

            Bucket=s3_bucket_name,

            Key=s3_key_prefix + 'system_info' + response.text  + '.txt',

            Body=fh.read()

        )

    print(s3_key_prefix + 'system_info' + response.text + '.txt')

    print("File has been uploaded into " + s3_bucket_name + " S3 bucket with instance_id key.")

except ClientError as e:
   print("Are you sure the destination bucket exist? Check it.")
   print("Error details:", e)
