from boto3 import client

s3 = client("s3")


def get_images(bucket="eyedentity"):
    objects = s3.list_objects(Bucket=bucket).get("Contents")
    if not objects:
        return dict()
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    return [obj['Key'] for obj in sorted(objects, key=get_last_modified, reverse=True)]


def upload_image(file, key, bucket="eyedentity"):
    return s3.upload_file(file, bucket, key, ExtraArgs={'ACL': 'public-read'})


def clear_bucket(bucket="eyedentity"):
    response = s3.list_objects_v2(Bucket=bucket).get("Contents")
    if response:
        for item in response:
            s3.delete_object(Bucket=bucket, Key=item['Key'])
