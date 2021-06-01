from boto3 import client

s3 = client("s3")

default_bucket = "eyedentity"


def get_images(bucket=default_bucket):
    objects = s3.list_objects(Bucket=bucket).get("Contents")
    if not objects:
        return dict()

    def get_last_modified(obj):
        return int(obj["LastModified"].strftime("%s"))

    return [obj["Key"] for obj in sorted(objects, key=get_last_modified, reverse=True)]


def upload_image(file, key, bucket=default_bucket):
    return s3.upload_file(file, bucket, key, ExtraArgs={"ACL": "public-read"})


def clear_bucket(bucket=default_bucket):
    response = s3.list_objects_v2(Bucket=bucket).get("Contents")
    if response:
        for item in response:
            s3.delete_object(Bucket=bucket, Key=item["Key"])


class ObjectList(object):
    def __init__(self, bucket=default_bucket):
        self.bucket = bucket
        self.objects = list()
        self.update()

    def update(self):
        # print("Updating ObjectList")
        self.objects = get_images(bucket=self.bucket)

    def return_objects(self):
        return self.objects
