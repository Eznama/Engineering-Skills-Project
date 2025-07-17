import pandas as pd
from load_logs import load_log
import matplotlib.pyplot as plt

# Load entire log
df = load_log("sample-log.log")

# Set timestamp as index
df = df.set_index("timestamp")

# Count requests per minute
requests_per_min = df.resample("1T").size()

# Show the first 10 values
print(requests_per_min.head(10))

# ─── Plot and Save ────────────────────────────────────────────────────────────

# Plot the traffic over time
requests_per_min.plot()

# Label axes and title
plt.xlabel("Time")
plt.ylabel("Requests per Minute")
plt.title("Web Traffic Over Time")

# Ensure everything fits
plt.tight_layout()

# Save to a PNG file in this folder
plt.savefig("traffic_over_time.png")

# Then display the plot window
plt.show()

# ─── Identify Top IPs and URLs ───────────────────────────────────────────────

# Top 10 IP addresses by request count
top_ips = df["ip"].value_counts().head(10)
print("\nTop 10 IPs by request count:")
print(top_ips)

# Extract just the path (URL) from the request, e.g. "GET /news HTTP/1.1" → "/news"
df["url"] = df["request"].str.split().str[1]

# Top 10 requested URLs
top_urls = df["url"].value_counts().head(10)
print("\nTop 10 URLs by request count:")
print(top_urls)

# ─── Bot vs. Human Classification ────────────────────────────────────────────

# Simple bot pattern: user‑agents containing these keywords
bot_patterns = ["bot", "spider", "crawl"]

# Flag each row as bot if its user_agent contains any of those patterns
df["is_bot_ua"] = df["user_agent"].str.lower().apply(
    lambda ua: any(p in ua for p in bot_patterns)
)

# Compute total requests and bot requests per IP
ip_counts = df.groupby("ip").size().rename("total_reqs")
ip_bot_counts = df[df["is_bot_ua"]].groupby("ip").size().rename("bot_reqs")

# Combine into one DataFrame
ip_summary = pd.concat([ip_counts, ip_bot_counts], axis=1).fillna(0)
ip_summary["bot_frac"] = ip_summary["bot_reqs"] / ip_summary["total_reqs"]

# Compute requests per minute per IP
# First find the time span per IP

# Bring timestamp back as a column
df = df.reset_index()

# Compute first/last timestamp per IP
times = df.groupby("ip")["timestamp"].agg(["min","max"])
times["duration_min"] = (times["max"] - times["min"]).dt.total_seconds() / 60

# Join that duration back onto ip_summary
ip_summary = ip_summary.join(times["duration_min"])

# ---- New filtering step ----
# Drop any IPs whose entire activity spans 0 minutes (to avoid infinite rates)
ip_summary = ip_summary[ip_summary["duration_min"] > 0]
# Optionally, ignore noise from IPs with very few requests
ip_summary = ip_summary[ip_summary["total_reqs"] > 5]

# Now compute requests per minute
ip_summary["reqs_per_min"] = ip_summary["total_reqs"] / ip_summary["duration_min"]

# Show the top 10 suspicious IPs by request rate
print("\nTop 10 IPs by average reqs/min (potential bots):")
print(ip_summary.sort_values("reqs_per_min", ascending=False).head(10))

# Show the top 10 IPs by bot‐UA fraction
print("\nTop 10 IPs by fraction of bot UA strings:")
print(ip_summary.sort_values("bot_frac", ascending=False).head(10))