import os, boto3, time, decimal
from boto3.dynamodb.conditions import Key

TABLE = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def put_item(item): TABLE.put_item(Item=item)

def get_profile(handle):
    res = TABLE.get_item(Key={"PK": f"USER#{handle}", "SK": "PROFILE"})
    return res.get("Item")

def upsert_profile(handle, followers):
    TABLE.put_item(Item={
        "PK": f"USER#{handle}",
        "SK": "PROFILE",
        "handle": handle,
        "followers": int(followers),
        "lastUpdated": int(time.time())
    })

def add_reel(handle, ts, views, likes=0):
    TABLE.put_item(Item={
        "PK": f"USER#{handle}",
        "SK": f"REEL#{ts}",
        "GSI1PK": f"REELS#{handle}",
        "GSI1SK": int(ts),
        "views": int(views),
        "likes": int(likes),
        "ts": int(ts)
    })

def last_n_reels(handle, n=10):
    res = TABLE.query(
        IndexName="GSI1PK-GSI1SK-index",
        KeyConditionExpression=Key("GSI1PK").eq(f"REELS#{handle}")
    )
    items = sorted(res.get("Items", []), key=lambda x: x["ts"], reverse=True)
    return items[:n]

def write_leaderboard(rows):
    # clear & write a compact snapshot: SK=000001,000002 ...
    with TABLE.batch_writer() as bw:
        for i, r in enumerate(rows, start=1):
            bw.put_item(Item={
                "PK": "LEADERBOARD#GLOBAL",
                "SK": f"{i:06d}",
                **r
            })

def read_leaderboard(limit=100):
    res = TABLE.query(
        KeyConditionExpression=Key("PK").eq("LEADERBOARD#GLOBAL"),
        Limit=limit
    )
    return res.get("Items", [])
