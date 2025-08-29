This Project is demo of Serverless architecture ranking instagram influencers based on few predefined metrics such as followers count, average views for last 10 reels, consistency. Since this is a demo project we have used synthetic data but the code can be modified to scrape real time influencer list using instagrapi in python. The following services were explored for this project.  The count will keep changing with the help of lambda function which will be triggered by eventbridge scheduler every 1 hour.

Static frontend (React) on S3 + CloudFront
Public REST API (API Gateway → Lambda) for leaderboard & profiles
Data stored in DynamoDB
Batch jobs on EventBridge to (a) generate demo data, (b) recompute rankings which will trigger lambda
S3 raw bucket (optional) to land JSON snapshots
Lambdas for functions which will be integrated with API Gateway to server Rest API's

Formula for ranking the Influencers
For each influencer, consider the last N reels (e.g., N=10):
followers (F)
recent_avg_views (A) = avg of last N reel views
consistency (C) = 1 − coeff_of_variation(last N) → higher means steadier views
posting_cadence (P) = min(1, reels_in_last_14_days / 10)

score = 100 * ( 
  0.25 * norm(F) +
  0.45 * norm(A) +
  0.20 * C +
  0.10 * P
)

Final Result
<img width="1845" height="966" alt="image" src="https://github.com/user-attachments/assets/311449be-f694-4cf8-84a6-a5778343bc3b" />

