# -*- coding: utf-8 -*-
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import datetime





def handler(event, context):
    dynamodb = boto3.resource("dynamodb", region_name='us-west-2')

    table = dynamodb.Table('order')
    now = datetime.datetime.now()
    timestamp = "{}-{}-{}@{}:{}:{}".format(now.month,now.day,now.year,now.hour,now.minute,now.second)
    try:
        response = table.put_item(
            Item= {
                'orderId': event['order_id'],
                'customerName': event['customer_name'],
                'customerEmail': event['customer_email'],
                'time': timestamp,
                'menuId' : 'pi12'
            }
    )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        table = dynamodb.Table('menu')
        try:
            response = table.get_item(
                 Key={
                    'menuId' : 'pi12'
                    }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            selection = response['Item']['selection']
            i=1
            option = []
            for s in selection:
                option.append(str(i)+". " + str(s))
                i=i+1

            msg = "Hi {}, please choose one of these selection: {} " .format(event['customer_name'], " ".join(option))
    
    return {
             "Message" : msg 
    }
          
           