import json
import boto3

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    print(f'Request payload: {event}')

    # Extract the acct from event
    acct =event['Details']['Parameters']['acct']

    # Print the parsed account number
    print(f'Parsed acct Number: {acct}')


    # DynamoDB table name
    table_name = 'skill_based_routing'

    # Get the DynamoDB table
    table = dynamodb.Table(table_name)

    # Fetch the item by the partition key
    response = table.get_item(
        Key={
            'account_number': acct
        }
    )

    subscription_type = ''
    existing_customer = 'false'
    status_code = 204

    # Extract the item from the response
    item = response.get('Item', None)

    if item:
        print(f'Item found: {item}')
        subscription_type = item['subscription']
        existing_customer = 'true'
        status_code = 200



    print(f'statusCode: {status_code}, existing_customer : {existing_customer}, subscription from db : {subscription_type}')

    # Create the response dictionary
    resp = {
        "existingCustomer": existing_customer,
        "subscription": subscription_type
    }

    # Convert the dictionary to JSON format
    response_body = json.dumps(resp)

    # Return the response
    return {
        'statusCode': status_code,
        'subscription': subscription_type,
        'existingCustomer': existing_customer
    }

