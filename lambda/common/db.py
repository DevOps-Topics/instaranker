import statistics, math
from decimal import Decimal


def coeff_var(nums):
    if not nums:
        return Decimal("0")
    mean = sum(nums) / len(nums)
    if mean == 0:
        return Decimal("0")
    sd = statistics.pstdev(nums)
    return Decimal(str(sd / mean))


def normalize(values):
    """Return a function that maps values into [0,1] as Decimal"""
    if not values:
        return lambda x: Decimal("0")
    lo, hi = min(values), max(values)
    if hi == lo:
        return lambda x: Decimal("0.5")
    return lambda x: (Decimal(str(x - lo)) / Decimal(str(hi - lo)))


def compute_scores(profiles, reels_map, N=10):
    rows = []
    for h, prof in profiles.items():
        reels = reels_map.get(h, [])
        lastN = reels[:N]

        views = [r["views"] for r in lastN]
        avg_views = (sum(views) / len(views)) if views else 0
        C = Decimal("1") - coeff_var(views) if views else Decimal("0")

        # cadence: reels in last 14 days / 10 (capped)
        recent_count = sum(
            1 for r in lastN if (lastN and (lastN[0]["ts"] - r["ts"]) <= 14 * 24 * 3600)
        )
        P = min(1.0, recent_count / 10.0)

        rows.append({
            "handle": h,
            "followers": Decimal(str(prof.get("followers", 0) or 0)),
            "recent_avg_views": Decimal(str(avg_views)),
            "consistency": C,
            "posting_cadence": Decimal(str(P)),
        })

    # normalize F & A
    normF = normalize([r["followers"] for r in rows])
    normA = normalize([r["recent_avg_views"] for r in rows])

    # final score
    for r in rows:
        score = (
            Decimal("0.25") * normF(r["followers"]) +
            Decimal("0.45") * normA(r["recent_avg_views"]) +
            Decimal("0.20") * r["consistency"] +
            Decimal("0.10") * r["posting_cadence"]
        )
        r["score"] = (score * Decimal("100")).quantize(Decimal("0.0001"))  # optional rounding

    rows.sort(key=lambda x: x["score"], reverse=True)
    return rows

