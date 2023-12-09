from datetime import datetime
import boto3
import json
import os
import sys

inputticketnumber = os.environ['ticketnumber']
inputaminame = os.environ['ami_name']
inputservername = sys.argv[1]
inputregion = sys.argv[2]


print(f"'{inputticketnumber}' and '{inputaminame}'")

    
def get_instance_id_by_name(inputservername):

    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [inputservername]
            }
        ]
    )
    if response['Reservations']:
            instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']
            return instance_id
    else:
            return None

def create_new_ami(instance_id, newaminame, ami_description):
    
    create_ami_response = ec2_client.create_image(
        InstanceId=instance_id,
        Name=newaminame,
        NoReboot=True,
        Description=ami_description
    )
    return create_ami_response['ImageId']


    
    
ec2_client = boto3.client('ec2',region_name=inputregion)
instance_id = get_instance_id_by_name(inputservername)

if instance_id:
    print(f"Instance ID for '{inputservername}' is: {instance_id}")
    if len(inputaminame) == 0:
        newaminame = inputservername + "_" + inputticketnumber
    else:
        newaminame = inputservername + "_" + inputaminame
    
    ami_description = f'AMI created using Jenkins with {inputticketnumber}'

    image_id = create_new_ami(instance_id, newaminame, ami_description)

    if image_id:
        print(f"AMI created with ID: {image_id}")
    else:
        print("AMI creation failed.")
    

else:
    print(f"No instance found with the name '{inputservername}'")

    
