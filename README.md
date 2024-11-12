# Music Festival Lineup Service

## Overview

This service processes CSV files uploaded to an S3 bucket, parses the data using AWS Lambda, stores it in a DynamoDB table, and sends notifications via SNS upon completion.

## AWS Services

- **AWS S3**: Stores the uploaded CSV files.
- **AWS Lambda**: Processes the CSV files upon upload.
- **Amazon DynamoDB**: Stores the parsed performance data.
- **Amazon SNS**: Sends notifications about the success or failure of the processing.

## DynamoDB Schema Design

- **Table Name**: `music-festival-table`
- **Primary Key**:
  - **Partition Key**: `Performer` (String)
  - **Sort Key**: `DateStartTime` (String) - a concatenation of `Date` and `StartTime`
- **Attributes**:
  - `Performer`: Name of the performer
  - `DateStartTime`: Combination of date and start time (e.g., `"2025-07-12#8:00"`)
  - `Stage`: Stage name
  - `Date`: Performance date
  - `StartTime`: Start time of the performance
  - `EndTime`: End time of the performance

### Design Rationale

- **Efficient Querying**:
  - **By Performer**: Retrieve all performances by a specific performer.
  - **By Stage and Time**: List all performances on a specific stage within a time range.
  - **By Date and Time**: Fetch performances within a given date and time range.


## Cost and Scalability Analysis
- **Data Volume**:
  - Every 100 lines of CSV data ≈ **5 KB**
  - **1,000 records/day** ≈ 50 KB/day
  - **10,000 records/day** ≈ 500 KB/day
  - **100,000 records/day** ≈ 5 MB/day

### AWS Lambda

- **Cost Factors**:
  - **Number of Requests**: Based on the number of files uploaded.
  - **Duration of Execution**: Billed in 1 ms increments.
- **Scalability**:
  - Automatically scales to handle concurrent executions.
- **Cost Optimization**:
  - Write efficient code to minimize execution time.
  - Allocate appropriate memory to optimize performance and cost.

### Amazon DynamoDB

- **Pricing Models**:
  - **On-Demand Capacity Mode**: Pay per request; ideal for variable or unpredictable workloads.
  - **Provisioned Capacity Mode**: Specify read/write capacity units; cost-effective for steady workloads.
- **Cost Estimates**:
  - **Storage Costs**: Minimal due to small data size.
  - **Read/Write Costs**: Dependent on the number of read/write requests.
- **Scalability**:
  - Seamlessly scales to accommodate large volumes of data with low latency.

### Cost-Efficient Strategies

- **Optimize Lambda Execution**: Efficient code reduces execution time and cost.
- **S3 Lifecycle Policies**: Implement policies to archive or delete old files, reducing storage costs.

## Security Considerations

- **IAM Roles and Policies**:
  - **Lambda Execution Role**: Grants least-privilege permissions to access S3, DynamoDB, and SNS.
  - **Resource-Specific Access**: Permissions are restricted to specific resources using ARNs.
- **Access Control**:
  - **S3 Bucket Policies**: Restrict who can upload files to the bucket.
  - **SNS Topic Policies**: Limit who can publish to and subscribe from the topic.

## Deployment Instructions

1. **Deploy AWS Resources**:
   - Use the provided CloudFormation template to set up the infrastructure, which includes:
     - S3 bucket
     - Lambda function
     - DynamoDB table
     - SNS topic
     - IAM roles and permissions
2. **Lambda Function**:
   - The function code is embedded in the CloudFormation template.
3. **Configuration**:
   - Environment variables (`TABLE_NAME` and `TOPIC_ARN`) are set automatically via the template.
4. **Testing**:
   - Upload a test CSV file to the S3 bucket named `music-festival-lineup`.
   - Verify that:
     - Data is stored correctly in the DynamoDB table `music-festival-table`.
     - A notification is received via SNS indicating success or failure.

## Conclusion

This service is production ready providing a scalable, cost-effective solution for processing music festival performance data, with an optimized DynamoDB schema that supports efficient querying by performer, stage, and time range.
