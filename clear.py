# -*- mode: python3 -*-
from backend import s3

print("Clearing bucket")
s3.clear_bucket()
print("Done")
