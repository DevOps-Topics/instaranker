import json
from common.db import get_profile

def lambda_handler(event, context):
    handle = event["pathParameters"]["handle"]
    prof = get_profile(handle)
    if not prof:
        return {"statusCode": 404, "body": "Not found"}
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json", "access-control-allow-origin": "*"},
        "body": json.dumps(prof)
    }
