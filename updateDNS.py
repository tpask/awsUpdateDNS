#!/bin/python
import boto3
import requests, os

#note: zoneId and hostedZone are redacted
zoneId = '/hostedzone/xxxx'
hostedZone = 'xxxx'

hostName = os.environ.get('ENV_MIGHT_EXIST')

def updateDNS (ip, hostName):
  client = boto3.client('route53')
  boto3.set_stream_logger('botocore')
  response = client.change_resource_record_sets(
    HostedZoneId=zoneId,
    ChangeBatch={
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': hostName,
                    'ResourceRecords': [ { 'Value': ip} ],
                    'Type': 'A',
                    'TTL': 300
                }
            }
        ]
    }
  )

# get public IP address
r = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4')
ip = r.text

# get hostname
hostName = os.environ.get('HOSTNAME')
hostName = "%s.%s" %(hostName, hostedZone)
print  ip, hostName

resp = updateDNS(ip, hostName)

