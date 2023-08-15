from datetime import datetime
import boto3
import json
import os
inputticketnumber = os.environ['ticketnumber']
inputaminame = os.environ['ami_name']



print(f"'{inputticketnumber}' and '{inputaminame}'")

with open('serverlists.txt', 'r') as file:
    servernames = [line.strip() for line in file]
    
def get_instance_id_by_name(instance_name):

    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [instance_name]
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
        Description=ami_description
    )
    return create_ami_response['ImageId']


        
for instance_name in servernames:

    region_lookup = {
        "USEA":"us-east-1",
        "USWE":"us-west-2",
        "CACE":"ca-central-1",
        "EUWE":"eu-west-1",
        "EUCE":"eu-central-1",
        "APSP":"ap-southeast-1",
        "APAU":"ap-southeast-2"
    }
    aws_region  = region_lookup[instance_name[:4]]
    print(f"'{aws_region}'")
    
    ec2_client = boto3.client('ec2',region_name=aws_region)

    instance_id = get_instance_id_by_name(instance_name)
    if instance_id:
        print(f"Instance ID for '{instance_name}' is: {instance_id}")
        If not inputaminame:
            newaminame = instance_name + inputticketnumber
        else
            newaminame = instance_name + inputaminame
        
        ami_description = f'AMI created using Jenkins with {inputticketnumber}'
    
        image_id = create_new_ami(instance_id, newaminame, ami_description)
    
        if image_id:
            print(f"AMI created with ID: {image_id}")
        else:
            print("AMI creation failed.")
        

    else:
        print(f"No instance found with the name '{instance_name}'")

    
