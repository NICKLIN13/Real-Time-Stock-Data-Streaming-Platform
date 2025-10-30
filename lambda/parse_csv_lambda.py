import datetime
import json
import boto3
import time
import csv

STREAM_NAME = "new-data-stream"
def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')

    # Set bucket name and file key
    bucket_name = 'raw-stock-price-bucket'
    key = 'AMDprices2021-2022.csv'

    # Get CSV file from S3
    response = s3.get_object(Bucket=bucket_name, Key=key)
    print(response)
    # Split data by lines and extract column names from first row
    data = response['Body'].read().decode('utf-8')
    data = data.split('\n')  # Split data by lines
    data_list = []
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


def get_data(data_dict):
    # Generate data dictionary for Kinesis stream
    return {
        'date' : data_dict['Date'],
        'ticker': 'AMD',
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