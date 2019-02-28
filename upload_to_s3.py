import boto3
import threading
import os

s3_cl = boto3.client('s3')
  # SAMPLE
def upload_file(fl_name):
	with open(fl_name, 'rb') as f_obj:
		s3_cl.upload_fileobj(f_obj, 'anilens-assets', f"2019/02/{fl_name}")

fl_names=os.listdir()

for fl in fl_names:
	threading.Thread(target = upload_file, args=(fl,)).start()
