"""

Remove those pesky AWS default VPCs.

Python Version: 3.7.0
Boto3 Version: 1.7.50

"""

import boto3
from botocore.exceptions import ClientError


def delete_igw(ec2, VpcId):
  """
  Detach and delete the internet gateway
  """

  args = {
    'Filters' : [
      {
        'Name' : 'attachment.vpc-id',
        'Values' : [ VpcId ]
      }
    ]
  }

  try:
    igw = ec2.describe_internet_gateways(**args)['InternetGateways']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if igw:
    igw_id = igw[0]['InternetGatewayId']

    try:
      result = ec2.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=VpcId)
    except ClientError as e:
      print(e.response['Error']['Message'])

    try:
      result = ec2.delete_internet_gateway(InternetGatewayId=igw_id)
    except ClientError as e:
      print(e.response['Error']['Message'])

  return


def delete_subs(ec2, args):
  """
  Delete the subnets
  """

  try:
    subs = ec2.describe_subnets(**args)['Subnets']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if subs:
    for sub in subs:
      sub_id = sub['SubnetId']

      try:
        result = ec2.delete_subnet(SubnetId=sub_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_rtbs(ec2, args):
  """
  Delete the route tables
  """

  try:
    rtbs = ec2.describe_route_tables(**args)['RouteTables']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if rtbs:
    for rtb in rtbs:
      main = 'false'
      for assoc in rtb['Associations']:
        main = assoc['Main']
      if main == True:
        continue
      rtb_id = rtb['RouteTableId']
        
      try:
        result = ec2.delete_route_table(RouteTableId=rtb_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_acls(ec2, args):
  """
  Delete the network access lists (NACLs)
  """

  try:
    acls = ec2.describe_network_acls(**args)['NetworkAcls']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if acls:
    for acl in acls:
      default = acl['IsDefault']
      if default == True:
        continue
      acl_id = acl['NetworkAclId']

      try:
        result = ec2.delete_network_acl(NetworkAclId=acl_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_sgps(ec2, args):
  """
  Delete any security groups
  """

  try:
    sgps = ec2.describe_security_groups(**args)['SecurityGroups']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if sgps:
    for sgp in sgps:
      default = sgp['GroupName']
      if default == 'default':
        continue
      sg_id = sgp['GroupId']

      try:
        result = ec2.delete_security_group(GroupId=sg_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_vpc(ec2, VpcId, region):
  """
  Delete the VPC
  """

  try:
    result = ec2.delete_vpc(VpcId=VpcId)
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    print('VPC {} has been deleted from the {} region.'.format(VpcId, region))

  return


def get_regions(ec2):
  """
  Return all AWS regions
  """

  regions = []

  try:
    aws_regions = ec2.describe_regions()['Regions']
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    for region in aws_regions:
      regions.append(region['RegionName'])

  return regions


def delete_all_default_vpcs_in_all_regions(profile):
  """
  Do the work..

  Order of operation:

  1.) Delete the internet gateway
  2.) Delete subnets
  3.) Delete route tables
  4.) Delete network access lists
  5.) Delete security groups
  6.) Delete the VPC 
  """

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)
  ec2 = session.client('ec2', region_name='us-east-1')

  regions = get_regions(ec2)

  for region in regions:

    ec2 = session.client('ec2', region_name=region)

    try:
      attribs = ec2.describe_account_attributes(AttributeNames=[ 'default-vpc' ])['AccountAttributes']
    except ClientError as e:
      print(e.response['Error']['Message'])
      return

    else:
      VpcId = attribs[0]['AttributeValues'][0]['AttributeValue']

    if VpcId == 'none':
      print('VPC (default) was not found in the {} region.'.format(region))
      continue

    # Are there any existing resources?  Since most resources attach an ENI, let's check..

    args = {
      'Filters' : [
        {
          'Name' : 'vpc-id',
          'Values' : [ VpcId ]
        }
      ]
    }

    try:
      eni = ec2.describe_network_interfaces(**args)['NetworkInterfaces']
    except ClientError as e:
      print(e.response['Error']['Message'])
      return

    if eni:
      print('VPC {} has existing resources in the {} region.'.format(VpcId, region))
      continue

    result = delete_igw(ec2, VpcId)
    result = delete_subs(ec2, args)
    result = delete_rtbs(ec2, args)
    result = delete_acls(ec2, args)
    result = delete_sgps(ec2, args)
    result = delete_vpc(ec2, VpcId, region)

  return




def delete_vpc_and_all_dependencies(profile: str, VpcId: str, region: str):
  """
  Do the work..

  Order of operation:

  1.) Delete the internet gateway
  2.) Delete subnets
  3.) Delete route tables
  4.) Delete network access lists
  5.) Delete security groups
  6.) Delete the VPC 
  """

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)
  
  ec2 = session.client('ec2', profile )

  # regions = get_regions(ec2)


  ec2 = session.client('ec2', region_name=region)

  # # try:
  # #   attribs = ec2.describe_account_attributes(AttributeNames=[ 'default-vpc' ])['AccountAttributes']
  # # except ClientError as e:
  # #   print(e.response['Error']['Message'])
  # #   return

  # # else:
  #   VpcId = attribs[0]['AttributeValues'][0]['AttributeValue']

  # if VpcId == 'none':
  #   print('VPC (default) was not found in the {} region.'.format(region))
  #   continue

  # Are there any existing resources?  Since most resources attach an ENI, let's check..

  args = {
    'Filters' : [
      {
        'Name' : 'vpc-id',
        'Values' : [ VpcId ]
      }
    ]
  }

  try:
    eni = ec2.describe_network_interfaces(**args)['NetworkInterfaces']
    # aws ec2 describe-subnets --filter Name=vpc-id,Values=vpc-0123456789 --query 'Subnets[?MapPublicIpOnLaunch==`false`].SubnetId'
     
    subnets=ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [VpcId]}])['Subnets']
    for subnet in subnets:
      print( f"VpcId [{VpcId}] found subnet [{subnet['SubnetId']}]" )
    
    if not subnets:
      print( f"No subnets found for region [{region}] vpc [{VpcId}], exiting" )
      exit(404)
    
    


  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  # ask user to confirm deletion of all resources
  print('Are you sure you want to delete all resources in the {} region?'.format(region))
  print('This will delete the VPC, subnets, route tables, network access lists, security groups, and internet gateway.')
  print('Type "yes" to continue: ', end='')
  response = input()
  
  if response != 'yes':
    print('Aborting...')
    return
  

  result = delete_igw(ec2, VpcId)
  result = delete_subs(ec2, args)
  result = delete_rtbs(ec2, args)
  result = delete_acls(ec2, args)
  result = delete_sgps(ec2, args)
  result = delete_vpc(ec2, VpcId, region)

  return








if __name__ == "__main__":
  
  import argparse
  
  # accept the profile name as an argument  
  # accept the VpcId as an argument
  # accept the region as an argument
  parser = argparse.ArgumentParser(description='Delete a VPC and all associated network resources')
  parser.add_argument('-p', '--profile', help='AWS profile name', required=True)  
  parser.add_argument('-v', '--vpc_id', help='VPC ID', required=True)
  parser.add_argument('-r', '--region', help='AWS region', required=True)
  args = parser.parse_args()  
  
  # if no profile name is provided, and vpc_id is not provided, print usage and exit
  if not args.profile and not args.vpc_id:
    parser.print_usage()
    sys.exit(1)
  
  
  
  delete_vpc_and_all_dependencies(args.profile, args.vpc_id, args.region)