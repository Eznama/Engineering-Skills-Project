## Findings & Verification
# Top IP Addresses by Total Requests

Findings:
45.133.1.2 – 5,400 requests

45.133.1.1 – 5,400 requests

35.185.0.156 – 3,600 requests

Verify:
print(df["ip"].value_counts().head(10))

This counts and sorts requests per IP.

# Top IPs by Average Requests per Minute (Potential Bots)

Findings:
35.185.0.156 → 3,600 reqs over ~30 min ⇒ ~120 req/min

45.133.1.1 → 5,400 reqs over ~60 min ⇒ ~90 req/min

45.133.1.2 → 5,400 reqs over ~60 min ⇒ ~90 req/min

Verify:
df2 = df.reset_index()

times = df2.groupby("ip")["timestamp"].agg(["min","max"])

times["mins"] = (times["max"]-times["min"]).dt.total_seconds()/60

counts = df2["ip"].value_counts()

rate = (counts / times["mins"])[counts.index]

print(rate.head(10))

Calculates duration per IP and divides total reqs by minutes.


# Bot‑Like Activity by User‑Agent String

Findings:
No high‑volume IPs had UAs with “bot”, “spider” or “crawl”

A few 10.0.0.* IPs flagged but sent very few reqs

Verify:
df["is_bot"] = df["user_agent"].str.lower().str.contains("bot|spider|crawl")

print(df.groupby("ip")["is_bot"].mean().sort_values(ascending=False).head(10))

Flags keywords, computes fraction of bot‑like requests.

## Assumptions
Complete traffic record: I assumed the provided log file includes every website visit during the problem window, so nothing important is missing.

Accurate timestamps: I assumed the clocks that stamped each log entry are correct and synced, so the order and timing of events truly reflect what happened.

Isolated workspace: I ran my Python code in its own virtual environment (venv) so installing packages for this project won’t interfere with other software on my computer.

## Solutions and Costs
Slow down fast visitors (Rate‑limiting)

What it is: Tell your server “only let each visitor make X requests per second,” so scripts can’t overwork it.

Cost: $0 (built into most web servers)

Block the worst offenders (IP blacklisting)

What it is: Identify the IP addresses causing the most traffic and outright deny them access.

Cost: $0 (just add a few lines to your server settings)

Offload static files to a free CDN

What it is: Serve images, CSS, and JS from a Content Delivery Network (like Cloudflare’s free plan) 
instead of your own servers.

Cost: $0 (free tier available)