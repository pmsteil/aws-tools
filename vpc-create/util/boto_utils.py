

import boto3
import sys







def vpcExists( vpc_name ):
    # from ssh import ssh, transport
    ec2 = boto3.resource('ec2')
    # vpc = ec2.Vpc( vpc_name )
    filters = [{'Name':'tag:Name', 'Values':[vpc_name]}]
    vpcs = list(ec2.vpcs.filter(Filters=filters))
    tags = {}
    vpc_id = 0

    for vpc in vpcs:
        client = boto3.client('ec2')
        response = client.describe_vpcs( VpcIds=[ vpc.id ] )

        # response:
        #   {'Vpcs': [{'CidrBlock': '10.0.0.0/20', 'DhcpOptionsId': 'dopt-52d85a2a',
        #    'State': 'available', 'VpcId': 'vpc-009a593301b21e3de', 'OwnerId': '075726826873',
        #    'InstanceTenancy': 'default',
        #    'CidrBlockAssociationSet': [{'AssociationId': 'vpc-cidr-assoc-07ee595682a8d414c', 'CidrBlock': '10.0.0.0/20', 'CidrBlockState': {'State': 'associated'}}], 'IsDefault': False,
        #    'Tags': [{'Key': 'Name', 'Value': 'vpc_create'}]}],
        #    'ResponseMetadata': {'RequestId': '68adf8b2-30b0-4812-838e-b4248d9e777c', 'HTTPStatusCode': 200,
        #    'HTTPHeaders': {'x-amzn-requestid': '68adf8b2-30b0-4812-838e-b4248d9e777c',
        #    'cache-control': 'no-cache, no-store', 'strict-transport-security': 'max-age=31536000;
        #    includeSubDomains', 'content-type': 'text/xml;charset=UTF-8', 'content-length': '1146',
        #    'date': 'Thu, 09 Mar 2023 15:25:05 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}


        # get the VpcId from response
        vpc_id = response["Vpcs"][0]["VpcId"]
        # print( f"response: {response}")
        # for tag in response["Vpcs"][0]["Tags"]:
        #     tags[tag["Key"]] = tag["Value"]
        # print( f"tags: {tags}" )

    return vpc_id

