import boto3

aws_client = boto3.client('ec2',region_name="ap-south-1", aws_access_key_id = "", aws_secret_access_key = "")

vpc_create = aws_client.create_vpc(
    CidrBlock='10.11.0.0/16'
)

vpc_id = vpc_create["Vpc"]["VpcId"]
print(vpc_id)

subnet_create = aws_client.create_subnet(
    AvailabilityZone='ap-south-1a',
    CidrBlock = '10.11.1.0/24',
    VpcId = vpc_id,
)

subnet_id = subnet_create["Subnet"]["SubnetId"]
print("subnet_id")

ig_create = aws_client.create_internet_gateway()
ig_id = ig_create["InternetGateway"]["InternetGatewayId"]
print(ig_id)

response = aws_client.attach_internet_gateway(
    InternetGatewayId = ig_id,
    VpcId = vpc_id,
)
    
print("Internet Gateway Attached successfully")