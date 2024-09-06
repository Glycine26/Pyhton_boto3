# AWS Python SDK - boto3

- boto3 the library used to interact with AWS services from Python code. 

- It provides an object-oriented API as well as low-level access to AWS services, making it a versatile tool for AWS cloud operations.

### 1)  Creates an Amazon VPC, a subnet, and an Internet Gateway 


a) Create VPC: 
- Initializes a VPC with the CIDR block 10.11.0.0/16 and tags it with the name "Server VPC ap-south-1a".

b) Create Subnet: 
- Creates a subnet within the specified availability zone (ap-south-1a) with the CIDR block 10.11.1.0/24.

c) Create Internet Gateway: 
- Generates an Internet Gateway and get it's ID.

d) Attach Internet Gateway: 
- Attaches the Internet Gateway to the created VPC.