import re
import pandas as pd

# 1) Build a regex that matches one log line and captures the key fields.
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)\s+'           # IP address
    r'(?P<ident1>\S+)\s+'       # first “-” field
    r'(?P<country>\S+)\s+'      # country code (e.g. NO, SE, FR)
    r'(?P<ident2>\S+)\s+'       # second “-” field
    r'\[(?P<timestamp>[^\]]+)\]\s+'      # timestamp, inside [ ]
    r'"(?P<request>[^"]*)"\s+'  # request line, inside " "
    r'(?P<status>\d{3})\s+'     # HTTP status code
    r'(?P<size>\S+)\s+'         # response size
    r'"(?P<referrer>[^"]*)"\s+' # referrer, inside " "
    r'"(?P<user_agent>[^"]*)"'  # user‑agent, inside " "
)

def load_log(path: str) -> pd.DataFrame:
    """
    Read the log file line by line, apply the regex to extract fields,
    and return a pandas DataFrame.
    """
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            m = LOG_PATTERN.match(line)
            if not m:
                # If a line doesn’t match, skip it or print a warning
                print("Skipping malformed line:", line)
                continue
            rows.append(m.groupdict())

    df = pd.DataFrame(rows)

    # Convert types
    df['timestamp'] = pd.to_datetime(
        df['timestamp'], 
        format='%d/%m/%Y:%H:%M:%S'
    )
    df['status'] = df['status'].astype(int)
    # size can be “-” if no bytes sent; convert those to zero
    df['size'] = df['size'].replace('-', '0').astype(int)

    return df

if __name__ == "__main__":
    df = load_log("sample-log.log")
    print(df.head())
    print("\nDataFrame shape:", df.shape)