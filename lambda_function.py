import boto3
import csv
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    sns = boto3.client('sns')

    # Extract bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    # Initialize variables
    table_name = 'music-festival-table'
    topic_arn = 'arn:aws:sns:us-east-2:741448922277:Music-Festival-Setup-SNS'

    try:
        # Get the CSV file from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        content = response['Body'].read().decode('utf-8')

        # Parse CSV content
        csv_file = io.StringIO(content)
        reader = csv.DictReader(csv_file)

        # Reference the DynamoDB table
        table = dynamodb.Table(table_name)

        # Batch write to DynamoDB
        with table.batch_writer() as batch:
            for row in reader:
                performer = row['Performer']
                stage = row['Stage']
                date = row['Date']
                start_time = row['Start']
                end_time = row['End']
                date_start_time = f"{date}#{start_time}"

                item = {
                    'Performer': performer,
                    'DateStartTime': date_start_time,
                    'Stage': stage,
                    'Date': date,
                    'StartTime': start_time,
                    'EndTime': end_time,
                }
                batch.put_item(Item=item)

        # Send success notification
        message = f"Successfully processed file '{object_key}' and inserted records into DynamoDB."
        sns.publish(TopicArn=topic_arn, Message=message, Subject='Lambda Execution Successful')

    except Exception as e:
        # Send failure notification
        message = f"Error processing file '{object_key}': {str(e)}"
        sns.publish(TopicArn=topic_arn, Message=message, Subject='Lambda Execution Failed')
        raise e
