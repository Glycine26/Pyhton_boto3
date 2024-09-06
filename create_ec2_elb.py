import boto3

#Intializing ec2&load balancer client
ec2_client = boto3.client("ec2", region_name="ap-south-1", aws_access_key_id= " ", aws_secret_access_key=" ")
elb_client = boto3.client("elbv2", region_name="ap-south-1", aws_access_key_id=" ", aws_secret_access_key=" ")

# VPC ID, subnet IDs, and security group ID
vpc_id = "vpc-0aba37ec0a923db88"
subnet_ids = ['subnet-00fae3dadb5b5c0df','subnet-0ba636c9d622d3e2d','subnet-0decd62512b8ee41b']
# if single subnet: subnet_ids = [''] 
security_group_id = "sg-05f87f7f3db143430"

# Amazon Linux 2 AMI ID
amazon_linux_ami_id = 'ami-020562d2cd769c81b'  # Replace with your Amazon Linux AMI ID

# Ubuntu AMI ID
ubuntu_ami_id = 'ami-05932268453c05d23'  # Replace with your Ubuntu AMI ID

# creating ec2 in vpc
# Create EC2 instances with Amazon Linux 2 
instance1 = ec2_client.run_instances(
    ImageId = amazon_linux_ami_id,
    InstanceType = "t2.micro",
    KeyName = "web_host_key", #key pair name
    MinCount = 1,
    MaxCount = 1,
    SubnetId = subnet_ids[1],
    SecurityGroupIds = [security_group_id]
    #if Sg is multiple : SecurityGroupIds=[sg_id]
)

# Create EC2 instances with Ubuntu
instance2 = ec2_client.run_instances(
    ImageId = ubuntu_ami_id,
    InstanceType = "t2.micro",
    KeyName = "web_host_key", #key pair name
    MinCount = 1,
    MaxCount = 1,
    SubnetId = subnet_ids[2],
    SecurityGroupIds = [security_group_id]
    #if Sg is multiple : SecurityGroupIds=[sg_id]
)

instance1_Id = [instance['InstanceId'] for instance in instance1['Instances']]
instance2_Id = [instance['InstanceId'] for instance in instance2['Instances']]

print(f"Instance Id's : Instance1 : {instance1_Id}, Instance2 : {instance2_Id}")
# print(f"Amazon Linux instances: {[instance.id for instance in instance1]}")
# print(f"Ubuntu instances: {[instance.id for instance in instance2]}")

# Wait for instances to be running
def wait_for_instances_running(instance_ids):
    print("Waiting for instances to be in the running state...")
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=instance_ids)
    print("All instances are running.")

wait_for_instances_running(instance1_Id + instance2_Id)

#Create Apllication load balancer
lb_create = elb_client.create_load_balancer(
    Name = "Website-load-balancer",
    Subnets = subnet_ids,
    SecurityGroups = [security_group_id],
    Scheme = "internet-facing",
    Type = "application",
    IpAddressType= "ipv4"
)
elb_arn = lb_create["LoadBalancers"][0]["LoadBalancerArn"]
print(f"Load Balancer ARN: {elb_arn}")

# Create a Target group.
target_group_response = elb_client.create_target_group(
    Name = "web-target-group",
    Protocol = "HTTP",
    Port=80,
    VpcId=vpc_id,
    TargetType="instance"
)

target_group_arn = target_group_response["TargetGroups"][0]["TargetGroupArn"]
print(f"Target Group ARN: {target_group_arn}")

#Register the EC2 instances with the target group
elb_client.register_targets(
    TargetGroupArn=target_group_arn,
    Targets=[{'Id': instance}for instance in instance1_Id + instance2_Id]
)
print('EC2 instances registered with target group successfully')

# Create a listener for the load balancer
#Listener is associated with LB and is responsible for handling incoming traffic and forward them to target group
elb_client.create_listener(
    LoadBalancerArn=elb_arn,
    Protocol='HTTP',
    Port=80,
    DefaultActions=[{
        'Type': 'forward',
        'TargetGroupArn' : target_group_arn
    }]
)
print("Listener created for load balancer successfully")