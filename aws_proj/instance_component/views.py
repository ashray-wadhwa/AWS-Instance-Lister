from django.http.response import HttpResponse
from django.shortcuts import render
import boto3
import logging
logging.basicConfig(level=logging.DEBUG, filename='log_test_views.txt')


client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2', region_name='us-east-2')
response_instance = client.describe_instances()
response_instance2 = client.describe_volumes()

iam_client = boto3.client('iam') 
iam_response = iam_client.list_users()

# log = open("myprog.log", "a")
# sys.stdout = log

logging.info("-----------------------------------------------------------------")

instance_list = []
def create_instance_list(instance, resource, list):
    if (instance == False):
        logging.warning('No instances on the account!')
    else:
        instance_map = {}
        if 'Reservations' in instance.keys():
            logging.info('Entered describe_instances!')
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
        elif 'Volumes' in instance.keys():
            logging.info('Entered describe_volumes!')
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

create_instance_list(instance=response_instance, resource=ec2_resource, list=instance_list)
create_instance_list(instance=response_instance2, resource=ec2_resource, list=instance_list)

logging.info("-----------------------------------------------------------------")

count_users = []
def create_userinfo(users, count):
    if (users == False):
        logging.warning('No users are linked to this account!')
    else:
        logging.info('Entered list_users!')
        temp_counter = 0
        for x in users['Users']:
            temp_counter = temp_counter+1
            count.append(temp_counter)
    return count

create_userinfo(users=iam_response, count=count_users)
counter = count_users[len(count_users)-1]

logging.info("-----------------------------------------------------------------")


def instanceView(request):
    logging.info("Entered rendering function!")
    return render(request, 'pages/instance_temp.html', {"instances": instance_list, "counter":counter})

logging.info("-----------------------------------------------------------------")
