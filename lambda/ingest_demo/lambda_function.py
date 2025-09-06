import os, time, random
from common.db import upsert_profile, add_reel

INFLUENCERS = [
    ("ananya.style", 120000),
    ("rahul.tech",   80000),
    ("desi.foodie",  150000),
    ("fit.mehul",    60000),
    ("travel_ria",   90000),
    ("irfansview", 200000),
    ("foodie.raj", 70000),
    ("fashionista", 180000),
    ("traveler", 50000),
    ("foodie.raj", 90000),
]

def lambda_handler(event, context):
    now = int(time.time())
    print(f"Lambda triggered at {now}, event = {event}")
    for handle, followers in INFLUENCERS:
        # slight drift in followers
        followers = int(followers * (1 + random.uniform(-0.001, 0.003)))
        upsert_profile(handle, followers)
        print(f"Updated profile: {handle}, followers={followers}")
        # add 0–2 new reels with various popularity/volatility
        for _ in range(random.choice([0,1,2])):
            base = followers * random.uniform(0.05, 0.3)
            noise = random.gauss(0, base*0.15)
            views = max(100, int(base + noise))
            add_reel(handle, now - random.randint(0, 3600*6), views, likes=int(views*0.05))
    return {"statusCode": 200, "body": "ok"}
