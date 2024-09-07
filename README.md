
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



### 2) Launch EC2 Instances and Set Up Load Balancer for default VPC and Subnet
a) Launch EC2 Instances:

Creating two EC2 instances in the specified subnets and attaches them to the specified security group:

-  One instance is launched with the Amazon Linux 2 AMI.
- Another instance is launched with the Ubuntu AMI.

Both instances are launched using the t2.micro instance type.

b) Wait for EC2 Instances to be Running:

- `wait_for_instances_running` function waits for both EC2 instances to transition to the running state.
- The script then uses the `wait` method to wait for the EC2 instances to transition to the running state by passing the list of InstanceIds.
- This method ensures a smooth workflow where the script doesn’t proceed until the necessary infrastructure is properly set up.

c) Creating Application Load Balancer (ALB):

- The ALB is set up across the ap-south-1a,1b and 1c subnets, ensuring availability in different zones.
- It uses the security group for inbound traffic control(SSH and Http).
- Load Balancer ARN is generated and printed.

d) Create Target Group:
- A target group is created where EC2 instances will be registered:

- The target group uses the `HTTP` protocol on port 80.
- Target Group ARN is created and printed.

e) Register EC2 Instances to Target Group:
- The EC2 instances are registered as targets in the created target group.
- Instances are registered with the `register_targets` function.

f) Create Listener for Load Balancer:
- A listener is created to forward traffic from the load balancer to the target group(EC2).
- The listener is configured to handle HTTP traffic on port 80.
- It forwards incoming traffic to the target group containing the EC2 instances.
