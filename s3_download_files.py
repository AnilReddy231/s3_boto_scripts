import os
import boto3
import logging

BUCKET_NAME='anilens-assets'
BUCKET_PATH='2018/08'

def get_files(bucket_name, prefix):
# Create a boto3 client that doesn't require credentials
    s3_cl = boto3.client('s3')
    # Loop through the bucket and download files
    logging.info(f"Bucket : {bucket_name} prefix: {prefix} ")
    s3_files=[bucket['Key'] for bucket in s3_cl.list_objects(Bucket=BUCKET_NAME,Prefix=BUCKET_PATH)['Contents']]
    for s3_fl in s3_files:
        logging.info(f"Downloading {s3_fl}")
        # create filepath if it doesn't exist
        folder, filename = os.path.split(s3_fl)
        if not os.path.exists('./' + folder):
            logging.info(f'Creating local directory ./ {folder}')
            os.makedirs('./' + folder)
        s3_cl.download_file(Bucket=BUCKET_NAME,Key=s3_fl, Filename=f'./{s3_fl}')

def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    get_files(BUCKET_NAME, BUCKET_PATH)
   
if __name__ == "__main__":
    main()