import json
import boto3
from boto3 import client as boto3_client
import uuid
import time, datetime


# Adds data to Kinesis stream, also clears s3 output data folders beforehand.
# stream name, folder names and s3 file path
STREAM_NAME = "new-data-stream"
bucket_name = 'd-bucket'
folder_names= ['part_a','part_b','part_c']
def lambda_handler(event, context):
    for name in folder_names:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.objects.filter(Prefix=name+'/').delete()
    time.sleep(10)
    data = json.loads(event['body']).splitlines()  # Split data by lines
    print(data)
    columns = data[0].split(',')  # Extract column names from first row
    kinesis_client = boto3.client('kinesis', region_name='us-east-1')
    # Iterate over rows and generate data for Kinesis stream
    for row in data[1:]:
        row_data = row.split(',')  # Split row data by comma
        if len(row_data)<len(columns):
            continue
        data_dict = dict(zip(columns, row_data))
        generate(STREAM_NAME, kinesis_client, data_dict)
        time.sleep(0.01)
    # Return response    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
#this allows for part B window to not carry over between runs
def get_data(data_dict):
        # Generate data dictionary for Kinesis stream
    return {
        'date' : data_dict['Date'],
        'ticker': data_dict['Ticker'],
        'open_price' : data_dict['Open'],
        'high' : data_dict['High'],
        'low' : data_dict['Low'],
        'close_price' : data_dict['Close'],
        'adjclose' : data_dict['Adj Close'],
        'volume' : data_dict['Volume'],
        'event_time': datetime.datetime.now().isoformat(),
    }

def generate(stream_name, kinesis_client, data):
    # Put record to Kinesis stream
    kinesis_client.put_record(
        StreamName=stream_name,
        PartitionKey="partitionkey",
        Data=json.dumps(get_data(data))
    )