import datetime, oss2, os, sys
from dotenv import load_dotenv

load_dotenv()

access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')
endpoint = os.getenv('OSS_ENDPOINT')
auth = oss2.Auth(access_key_id, access_key_secret)
service = oss2.Service(auth, endpoint)
print('\n'.join(info.name for info in oss2.BucketIterator(service)))
def upload_bucket(bucket_name, file_path):
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    bucket_name = bucket_name
    local_file_name = file_path.split('/')[-1]
    upload_file_path = file_path
    try:
    # Create bucket
        bucket.create_bucket()
        # Upload the file
        with open(upload_file_path, "rb") as data:
            bucket.put_object(local_file_name, data, progress_callback=percentage)
        print(datetime.datetime.now(), 'Finished uploading')

    except Exception as ex:
        print('Exception:')
        print(ex)
    

# Determine whether a bucket exists
def does_bucket_exist(bucket):
    try:
        bucket.get_bucket_info()
    except oss2.exceptions.NoSuchBucket:
        return False
    except:
        raise
    return True

# Progress bar for download/upload operations.
# consumed_bytes specifies the size of data that has been downloaded/uploaded.
# total_bytes specifies the total size of the object that you want to download/uploaed.
def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()

# List all buckets
def list_bucket():
    print('\n'.join(info.name for info in oss2.BucketIterator(service)))

# List all objects in a bucket
def list_object(bucket_name):
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    for obj in oss2.ObjectIterator(bucket):
        print(obj.key)

# Delete object
# Specify the full path of the object that you want to delete. Do not include the bucket name in the full path.
def delete_object(path, bucket_name):
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    bucket.delete_object(path)

# Download an object from a bucket
def download_object(object_path, local_path, bucket_name):
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    bucket.get_object_to_file(object_path, local_path)