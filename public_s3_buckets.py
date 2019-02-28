# coding: utf-8
import boto3
import os
from collections import defaultdict

if os.path.exists(os.path.join(os.environ['HOME'], ".aws", "credentials")) or os.path.exists(os.path.join(os.environ['HOME'], ".aws", "config")):
    profile_name = input("Enter your AWS profile name [default]: ") or "default"
    session = boto3.Session(profile_name=profile_name)
    s3_resource = session.resource("s3")
    s3_client = s3_resource.meta.client
else:
    access_key = inout("Enter your AWS access key ID: ")
    secret_key = input("Enter your AWS secret key: ")
    s3_resource = boto3.resource("s3", aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key)
    s3_client = s3_resource.meta.client

HAVE = {
    "READ": "readable",
    "WRITE": "writable",
    "READ_ACP": "readable permissions",
    "WRITE_ACP": "writeable permissions",
    "FULL_CONTROL": "Full Control"
}
GROUPS = {
    "http://acs.amazonaws.com/groups/global/AllUsers": "Everyone",
    "http://acs.amazonaws.com/groups/global/AuthenticatedUsers": "Authenticated AWS users"
}

def check_acl(acl):
    """
    Checks if the Access Control List is public.
    """
    public_grants = defaultdict()
    for grant in acl.grants:
        grantee = grant["Grantee"]
        if grantee["Type"] == "Group" and grantee["URI"] in GROUPS:
            public_grants['users']=grantee["URI"]
            public_grants['permission']=grant['Permission']
    indicator = True if public_grants else False
    return indicator, public_grants

for bucket in s3_resource.buckets.all():
    bkt_name=bucket.name
    acl = bucket.Acl()
    public, grants = check_acl(acl)
    if public:
        print(f"Bucket:{bkt_name} has {HAVE[grants['permission']]} for {GROUPS[grants['users']]}")