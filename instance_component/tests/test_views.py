import django
import unittest
import json
import botocore
import boto3
import pytest
import os
import logging
logging.basicConfig(level=logging.DEBUG, filename='log_test_output.txt')

from django.test import TestCase, Client
from django.urls import reverse
from instance_component.views import create_instance_list, instanceView
from unittest.mock import patch
from moto import mock_ec2

orig = botocore.client.BaseClient._make_api_call

@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'

# @pytest.fixture(scope='function')
# Create your tests here.
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.instance_url = reverse('instance_view')
    
    def test_my_view(self):
        response = self.client.get(self.instance_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'instanceTemp.html')

    def mock_make_api_call(self, operation_name, kwarg):
        if operation_name == 'DescribeInstances':
            return {'Reservations': [
                {
                            'Instances':[
                                {
                                    'InstanceId': 'i-12345678',
                                    'InstanceType': 't1.micro',
                                    'ImageId': 'ami-1234abcd',
                                    'BlockDeviceMappings': [
                                        {
                                            'Ebs': {
                                            'Status': 'attached',
                                            'VolumeId': '12345',
                                            },
                                        },
                                    ],
                                },
                            ],
                        },
                    
                ],
            }
        elif operation_name == 'DescribeVolumes':
            return {
                'Volumes':[
                    {
                        'Size': 8,
                    },
                ],
            }
        else:
            return []
    def ec2(aws_credentials):
        with mock_ec2():
            yield boto3.client('ec2', 'us-west-1')
    def test_ec2(self):
        with patch('botocore.client.BaseClient._make_api_call', new=self.mock_make_api_call):
            client = boto3.client('ec2')
            ec2_resource = boto3.resource('ec2', region_name='us-west-1')
            my_list = []
            e = client.describe_instances()
            e2 = client.describe_volumes()
            object = e['Reservations'][0]['Instances']
            object2 = e2['Volumes'][0]
            if len(object)==0:
                logging.warning("Add a mock instance!")
            else:
                logging.info("Congratulations, you successfully added a mock instance!")
                self.assertEquals(object[0]['InstanceId'], create_instance_list(instance=e, resource=ec2_resource, list=my_list, code=1)[0]['instanceID'])
                self.assertEquals(object[0]['BlockDeviceMappings'][0]['Ebs']['Status'], create_instance_list(instance=e, resource=ec2_resource, list=my_list, code=1)[0]['Ebs_status'])
                self.assertEquals(object[0]['BlockDeviceMappings'][0]['Ebs']['VolumeId'], create_instance_list(instance=e, resource=ec2_resource, list=my_list, code=1)[0]['Ebs_volume'])
                self.assertEquals(object2['Size'], create_instance_list(instance=e2, resource=ec2_resource, list=my_list, code=2)[0]['Ebs_size'])

                







