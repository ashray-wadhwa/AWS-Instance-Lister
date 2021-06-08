from django.http.response import HttpResponse
from django.shortcuts import render
import boto3
ec2 = boto3.client('ec2')
responseInstance = ec2.describe_instances()
instanceList = []
print("-----------------------------------------------------------------")
if (len(responseInstance['Reservations']) == 0):
    print("No instances")
else:
    print(responseInstance)
    for r in responseInstance['Reservations']:
        for i in r['Instances']:
            instanceList.append(i['InstanceId'])
            instanceList.append(i['State'])
print("-----------------------------------------------------------------")

#ALSO ADD PLATFORM

# from django.http import HttpResponse
# Create your views here.
def instanceView(request):
    # return HttpResponse('hello, this is instanceView')
    return render(request, 'instanceTemp.html', {"instances": instanceList})
    # , "types": typeList