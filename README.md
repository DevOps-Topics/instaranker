Influencer Leaderboard (Serverless Demo)

This project is a serverless architecture demo that ranks Instagram influencers based on a set of predefined metrics such as followers, average reel views, and posting consistency.
Currently, the leaderboard uses synthetic demo data, but the code can easily be extended to scrape real influencer data using instagrapi in Python.

Architecture Overview
Frontend: React app hosted on S3 + CloudFront
Backend: REST API via API Gateway → Lambda
Database: DynamoDB for influencer data
Batch Jobs: EventBridge scheduled jobs every hour to:
  Generate demo data
  Recompute influencer rankings
Optional: Raw data snapshots stored in S3
Lambdas: Functions integrated with API Gateway to serve REST APIs

Formula for ranking the Influencers
For each influencer, we consider the last N reels (N=10 by default):
Followers (F)
Recent Average Views (A) = average views across last N reels
Consistency (C) = 1 − coeff_of_variation(last N) → higher = steadier views
Posting Cadence (P) = min(1, reels_in_last_14_days / 10)
score = 100 * ( 
  0.25 * norm(F) +
  0.45 * norm(A) +
  0.20 * C +
  0.10 * P
)

Real-time influencer ranking (updates every hour via Lambda + EventBridge)
Synthetic data for demo purposes (plug-and-play with real data via Instagrapi)
Serverless, pay-per-use design with AWS Lambda, DynamoDB & API Gateway

Static leaderboard frontend served via S3 + CloudFront

Final Result
<img width="1845" height="966" alt="image" src="https://github.com/user-attachments/assets/311449be-f694-4cf8-84a6-a5778343bc3b" />

  The result is really worth the effort, Happy clouding

