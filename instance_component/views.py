from django.http.response import HttpResponse
from django.shortcuts import render
import sys
import boto3
ec2 = boto3.client('ec2')
ec2_resource = boto3.resource('ec2', region_name='us-east-2')
iam_client = boto3.client('iam') 
# client2 = boto3.client('organizations')
response_instance = ec2.describe_instances()
instance_list = []
instance_map = {}
temp_value = ""
log = open("myprog.log", "a")
sys.stdout = log
print("-----------------------------------------------------------------")
if (len(response_instance['Reservations']) == 0):
    print("No instances")
else:
    print(response_instance)
    for r in response_instance['Reservations']:
        volume_counter=0
        for i in r['Instances']:
            instance_map["instanceID"]=i['InstanceId']
            temp_value = i['InstanceId']
            ec2Instance = ec2_resource.Instance(temp_value)
            volumes = ec2Instance.volumes.all()
            for volume in volumes:
                instance_map["Ebs_size"]=volume.size
            for j in i['BlockDeviceMappings']:
                instance_map["Ebs_volume"]=j['Ebs']['VolumeId']
                instance_map["Ebs_status"]=j['Ebs']['Status']

            instance_list.append(instance_map.copy())
            instance_map.clear()
            volume_counter=volume_counter+1

            # instanceList.append(i['State']['Name'])
            # i['InstanceId']
            # i['State']['Name']

            # ['Ebs']['VolumeId']
            # ['Ebs']['Status']
            
    
print("-----------------------------------------------------------------")

response = iam_client.list_users()
counter = 0
for x in response['Users']:
    counter = counter+1

# response2 = client2.describe_organization()
# counter2 = 0
# for x in response2['Organization']:
#     print(x['Arn'])

# print(ec2.describe_iam_instance_profile_associations(Filters=[
#             {
#                 'Name': 'instance-id',
#                 'Values': ['i-0763b55c052098e49']
#             }
#         ]))
# print(ec2.describe_instance_attribute(Attribute='userData', InstanceId='i-0763b55c052098e49'))

#ALSO ADD PLATFORM

# from django.http import HttpResponse
# Create your views here.
def instanceView(request):
    # return HttpResponse('hello, this is instanceView')
    return render(request, 'instanceTemp.html', {"instances": instance_list, "counter":counter})
    # , "types": typeList
    # , "sizeList":sizeList