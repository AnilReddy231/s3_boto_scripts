import boto3
import botocore.exceptions
from datetime import datetime
import argparse, sys

BUCKET_NAME = 'anilens-assets'
s3 = boto3.resource('s3', verify=False)
date_format = "%Y-%m-%d"

def arg_parse(*args, **kwargs):
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="A utility to restore deleted objects from version enabled S3 Bucket "
    )

    parser.add_argument(
        "-b", "--bucket",
        action='store',
        help="Bucket Name",
        dest='bucket_name'
    )

    parser.add_argument(
        "-k", "--key",
        action='store',
        help="Key Name",
        dest='key_name'
    )

    parser.add_argument(
        "-a", "--after",
        action='store',
        help="After Date",
        dest='after_date',
        default='1900-01-01'
    )

    parser.add_argument(
        "-p", "--prior",
        action='store',
        help="Prior Date",
        dest='prior_date',
        default=datetime.now().strftime("%Y-%m-%d")
    )

    parsed = parser.parse_args()
    main(parsed.bucket_name,parsed.key_name, parsed.after_date,parsed.prior_date)

def main(bucket_name,key_name,after_date,prior_date):
    bucket = s3.Bucket(bucket_name)
    versions = bucket.object_versions.filter(Prefix=key_name)
    after=datetime.strptime(after_date, date_format)
    before=datetime.strptime(prior_date,date_format)

    for version in versions.all():
        if is_delete_marker(version):
            #print(f'Object: {version.object_key} Modified on: {version.last_modified}')
            modified_date=datetime.strptime(version.last_modified.strftime("%Y-%m-%d"), date_format)
            if  after < modified_date < before :
                print(f'Recovering {version.object_key} from {version.last_modified.strftime("%Y-%m-%d")}.')
                version.delete()


def is_delete_marker(version):
    try:
        # note head() is faster than get()
        version.head()
        return False
    except botocore.exceptions.ClientError as e:
        if 'x-amz-delete-marker' in e.response['ResponseMetadata']['HTTPHeaders']:
            return True
        # an older version of the key but not a DeleteMarker
        elif '404' == e.response['Error']['Code']:
            return False


if __name__ == '__main__':
    try:
        sys.exit(arg_parse(*sys.argv))
    except KeyboardInterrupt:
        exit('CTL-C Pressed.')
    except Exception as e:
        exit(f'Unknown Error: {e}')