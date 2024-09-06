import boto3

#Intializing ec2&load balancer client
ec2_client = boto3.client("ec2", region_name="ap-south-1", aws_access_key_id= "", aws_secret_access_key="")
elb_client = boto3.client("elbv2", region_name="ap-south-1", aws_access_key_id="", aws_secret_access_key="")

# VPC ID, subnet IDs, and security group ID
vpc_id = ""
subnet_id = ""
# if multiple subnets: subnet_ids = ['', ''] 
security_group_id = " "

# Amazon Linux 2 AMI ID
amazon_linux_ami_id = 'ami-0abcdef1234567890'  # Replace with your Amazon Linux AMI ID

# Ubuntu AMI ID
ubuntu_ami_id = 'ami-0abcdef1234567890'  # Replace with your Ubuntu AMI ID

# creating ec2 in vpc 
instance1 = ec2_client.run_instance(
    ImageId = amazon_linux_ami_id,
    InstanceType = "t2-micro",
    KeyName = "" #key pair name
    MinCount = 1,
    MaxCount = 1,
    SubnetId = subnet_id,
    SecurityGroupId = security_group_id
    #if Sg is multiple : SecurityGroupIds=[sg_id]
)

instance2 = ec2_client.run_instance(
    ImageId = ubuntu_ami_id,
    InstanceType = "t2-micro",
    KeyName = "" #key pair name
    MinCount = 1,
    MaxCount = 1,
    SubnetId = subnet_id,
    SecurityGroupId = security_group_id
    #if Sg is multiple : SecurityGroupIds=[sg_id]
)

instance1_Id = instance1["Instance"]
instance2_Id = instance2["Instance"]

print(f"Instance Id's : Instance1 : {instance1_Id}, Instance2 : {instance2_Id}")

#Create Apllication load balancer
