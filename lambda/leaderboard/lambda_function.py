import json, os, boto3
from common.db import read_leaderboard
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # cast cleanly: int if no decimal part, else float
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}
    limit = int(params.get("limit", "100"))
    data = read_leaderboard(limit)
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json", "access-control-allow-origin": "*"},
        "body": json.dumps({"items": data}, cls=DecimalEncoder)
    }
