import time, boto3
from boto3.dynamodb.conditions import Key
from common.db import TABLE, write_leaderboard, last_n_reels
from common.ranking import compute_scores

def lambda_handler(event, context):
    # scan profiles
    profiles = {}
    scan_kwargs = { "FilterExpression": "begins_with(PK, :p) AND SK = :s",
                    "ExpressionAttributeValues": {":p":"USER#", ":s":"PROFILE"} }
    resp = TABLE.scan(**scan_kwargs)
    for item in resp.get("Items", []):
        profiles[item["handle"]] = item

    # gather reels
    reels_map = {h: last_n_reels(h, 50) for h in profiles.keys()}

    # compute & write
    rows = compute_scores(profiles, reels_map, N=10)
    with_ranks = [{**r, "rank": i+1} for i, r in enumerate(rows)]
    write_leaderboard(with_ranks[:2000])
    return {"statusCode": 200, "body": f"recomputed {len(with_ranks)}"}
