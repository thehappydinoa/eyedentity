from boto3 import client

s3 = client("s3")


def get_images(bucket="eyedentity"):
    objects = s3.list_objects(Bucket=bucket).get("Contents")
    if not objects:
        return dict()
    return [key["Key"] for key in objects]


def upload_image(data, key, bucket="eyedentity"):
    return s3.upload_fileobj(data, bucket, key)
