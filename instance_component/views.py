from django.http.response import HttpResponse
from django.shortcuts import render
import sys
import boto3
import logging
logging.basicConfig(level=logging.DEBUG, filename='log_test_views.txt')

ec2 = boto3.client('ec2')
ec2_resource = boto3.resource('ec2', region_name='us-east-2')
iam_client = boto3.client('iam') 
# client2 = boto3.client('organizations')
response_instance = ec2.describe_instances()
response_instance2 = ec2.describe_volumes()
instance_list = []
# log = open("myprog.log", "a")
# sys.stdout = log

logging.info("-----------------------------------------------------------------")

def create_instance_list(instance, resource, list, code):
    if (instance == False):
        logging.warning('No instances on the account!')
    else:
        instance_map = {}
        # print(response_instance)
        if(code == 1):
            logging.info('Entered decribe_instances!')
            for r in instance['Reservations']:
                volume_counter=0
                for i in r['Instances']:
                    instance_map["instanceID"]=i['InstanceId']
                    for j in i['BlockDeviceMappings']:
                        instance_map["Ebs_volume"]=j['Ebs']['VolumeId']
                        instance_map["Ebs_status"]=j['Ebs']['Status']
                    list.append(instance_map.copy())
                    instance_map.clear()
                    volume_counter=volume_counter+1
        elif(code == 2):
            logging.info('Entered decribe_volumes!')
            my_count=0
            for r in instance['Volumes']:
                if(len(list) != 0):
                    list[my_count]["Ebs_size"]=r['Size']
                else:
                    list.append({
                        "Ebs_size": r['Size']
                    })
            my_count += 1
    return list

logging.info("-----------------------------------------------------------------")

create_instance_list(instance=response_instance, resource=ec2_resource, list=instance_list, code=1)
create_instance_list(instance=response_instance2, resource=ec2_resource, list=instance_list, code=2)

response = iam_client.list_users()
counter = 0
for x in response['Users']:
    counter = counter+1

# from django.http import HttpResponse
# Create your views here.
def instanceView(request):
    # return HttpResponse('hello, this is instanceView')
    logging.info("Entered rendering function!")
    return render(request, 'instanceTemp.html', {"instances": instance_list, "counter":counter})
    # , "types": typeList
    # , "sizeList":sizeList