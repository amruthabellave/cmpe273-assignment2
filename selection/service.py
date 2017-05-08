# -*- coding: utf-8 -*-
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


def get_from_menu(op,num):
    dynamodb = boto3.resource("dynamodb", region_name='us-west-2')
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
        l1 = response['Item'][op]
        if op=='selection' :
            val = l1[num-1]
        elif op=='size' :
            size_list = l1.keys()
            val = size_list[num-1]

        return val


def handler(event, context):
    dynamodb = boto3.resource("dynamodb", region_name='us-west-2')

    table = dynamodb.Table('order')
    try:
        response = table.get_item(
            Key= {
                'orderId': event['orderId']            
            }
    )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if response['Item'].has_key('selection'): ## This means that the customer has selected the type of pizza, the size option must be provided
           size = get_from_menu("size",int(event['input']))
           t1 = dynamodb.Table('menu')
           try:
                response = t1.get_item(
                    Key={
                        'menuId' : 'pi12'
                    }
                )
           except ClientError as e:
                print(e.response['Error']['Message'])
           else:
                size_map = response['Item']['size']
                price = size_map.get(size)
                r = table.update_item(
                    Key = {
                        'orderId': event['orderId'] 
                        },
                    UpdateExpression="set size = :r1, price = :r2, orderStatus= :r3",
                    ExpressionAttributeValues={
                        ':r1': size ,
                        ':r2': price,
                        ':r3': 'processing'
                        }
                    )
                msg = "Your order costs ${}. We will email you when the order is ready. Thank you! " .format(price)
    
                return {
                    "Message" : msg 
                }
        else: ## provide the sellection option
            sel = get_from_menu("selection",int(event['input']))
            print sel
            r = table.update_item(
                Key = {
                    'orderId': event['orderId'] 
                },
                UpdateExpression="set selection = :r",
                ExpressionAttributeValues={
                    ':r': sel }
            )
        
            t1 = dynamodb.Table('menu')
            try:
                response = t1.get_item(
                    Key={
                        'menuId' : 'pi12'
                    }
                )
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                size_map = response['Item']['size']
                size_list = size_map.keys()
                i=1
                option = []
                for s in size_list:
                    option.append(str(i)+". " + str(s))
                    i=i+1
                msg = "Which size do you want?: {} " .format(" ".join(option))
    
                return {
                    "Message" : msg 
                }
                
            