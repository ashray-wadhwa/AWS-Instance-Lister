from django.http.response import HttpResponse
from django.shortcuts import render
import boto3
ec2 = boto3.client('ec2')
ec2Resource = boto3.resource('ec2', region_name='us-east-2')
client1 = boto3.client('iam') 
# client2 = boto3.client('organizations')
responseInstance = ec2.describe_instances()
instanceList = []
instanceMap = {}
tempValue = ""
sizeList = []
print("-----------------------------------------------------------------")
if (len(responseInstance['Reservations']) == 0):
    print("No instances")
else:
    print(responseInstance)
    for r in responseInstance['Reservations']:
        volumeCounter=0
        for i in r['Instances']:
            instanceMap["instanceID"]=i['InstanceId']
            tempValue = i['InstanceId']
            ec2Instance = ec2Resource.Instance(tempValue)
            volumes = ec2Instance.volumes.all()
            for volume in volumes:
                instanceMap["Ebs_size"]=volume.size
            for j in i['BlockDeviceMappings']:
                instanceMap["Ebs_volume"]=j['Ebs']['VolumeId']
                instanceMap["Ebs_status"]=j['Ebs']['Status']

            instanceList.append(instanceMap.copy())
            instanceMap.clear()
            volumeCounter=volumeCounter+1

            # instanceList.append(i['State']['Name'])
            # i['InstanceId']
            # i['State']['Name']

            # ['Ebs']['VolumeId']
            # ['Ebs']['Status']
            
    
print("-----------------------------------------------------------------")

response = client1.list_users()
counter1 = 0
for x in response['Users']:
    counter1 = counter1+1

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
    return render(request, 'instanceTemp.html', {"instances": instanceList, "counter1":counter1})
    # , "types": typeList
    # , "sizeList":sizeList