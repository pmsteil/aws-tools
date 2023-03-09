

import boto3
import os
import sys
from util.boto_utils import *

# VPC Lab
# vpc-lab	10.0.0.0/24	254
# vpc-lab Public Subnet	10.0.0.0/28	16	Enable auto-assign public IPv4 address
# vpc-lab Internet GW	10.0.8.0/28		attach to vpc-lab  vpc
# vpc-lab public route			"attach to vpc
# edit route table and add route for 0.0.0.0/0 to IGW
# associate route to public subnet"

# vpc	10.0.0.0/20	4096
# subnet1	10.0.1.0/24	256
# subnet2	10.0.2.0/24	256
# subnet3	10.0.3.0/24	256
# ... subnet 16	10.0.15.0/24	256



# from ssh import ssh, transport
ec2 = boto3.resource('ec2')

# get vpc_name, vpc_subnets from command line
vpc_name = sys.argv[1]
vpc_subnets = sys.argv[2]


# if the vpc doesn't exist, create it
if vpc_id := vpcExists( vpc_name ):
    vpc = ec2.Vpc( vpc_id )
    print( f"Found existing vpc [{vpc_name}]... " )
else:
    print( f"creating vpc [{vpc_name}]...")
    try:
        vpc = ec2.create_vpc(CidrBlock='10.0.0.0/20' )
    except Exception as e:
            if "maximum number of VPCs has been reached" in str(e):
                print( "Maximum number of VPCs has been reached... please delete a VPC... bailing..." )
                exit(1)

    # add tag to VPC
    vpc.create_tags(Tags=[{"Key": "Name", "Value": f"{vpc_name}"}])

    vpc.wait_until_available()
    print( f"vpc [{vpc_name}] created!")



# enable public dns hostname so that we can SSH into it later
print( f"Enabling public dns hostname for vpc [{vpc_name}]")
ec2Client = boto3.client('ec2')
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )


print( "Creating public subnet...")
# create public subnet and associate it with route table
public_subnet = ec2.create_subnet(CidrBlock='10.0.0.0/24', VpcId=vpc.id)

exit(1)


# create an internet gateway and attach it to VPC
internetgateway = ec2.create_internet_gateway()
# attach internet gateway to VPC
vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)


# create a public route table and a public route
routetable = vpc.create_route_table()
route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)

routetable.associate_with_subnet(SubnetId=public_subnet.id)

# Create a security group and allow SSH inbound rule through the VPC
securitygroup = ec2.create_security_group(GroupName='sg_public', Description='Allow public traffic', VpcId=vpc.id)

# add ssh ingress from internet
securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)






# create a file to store the key locally
outfile = open('ec2-keypair.pem', 'w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)
# chmod 400 ec2-keypair.pem
os.chmod('ec2-keypair.pem', 0o400)



# Create a linux instance in the subnet
instance = ec2.create_instances(
 ImageId='ami-0de53d8956e8dcf80',
 InstanceType='t2.micro',
 MaxCount=1,
 MinCount=1,
 NetworkInterfaces=[{
 'SubnetId': subnet.id,
 'DeviceIndex': 0,
 'AssociatePublicIpAddress': True,
 'Groups': [securitygroup.group_id]
 }],
 KeyName='ec2-keypair')

instance.wait_until_running()

instance_description = instance.describe()

print( f"Instance ID: {instance_description['Instances'][0]['InstanceId']}" )
print( f"Instance IP: {instance_description['Instances'][0]['PublicIpAddress']}")

instance_ip = instance_description['Instances'][0]['PublicIpAddress']

# ssh into the instance_ip
# ssh.connect( instance_ip, 'ec2-user', 'ec2-keypair.pem' )




