from pathlib import Path
import pandas as pd
import requests

URL = "https://api.github.com/orgs/python/repos"
PARAMS = {"per_page": 100}
RECORDS_KEY = None

RENAME = {}
KEEP = ["name", "language", "stargazers_count", "forks_count", "open_issues_count", "size", "created_at"]
MUST_HAVE = ["language"]

RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"

def fetch_data():
    """Fetch repository data from the GitHub API."""
    response = requests.get(URL, params=PARAMS, timeout=15)

    response.raise_for_status()
    data = response.json()
    return data

def make_table(data):
    """Convert GitHub data into a pandas DataFrame."""
    df = pd.json_normalize(data)
    return df

def tidy_data(df):
    """Clean and select the required repository columns."""
    df = df.rename(columns=RENAME)
    df = df[KEEP]
    df = df.dropna(subset=MUST_HAVE)
    return df

def save_data(df):
    """Save the cleaned data to a CSV file."""
    RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_FILE, index=False)

def main():
    """Run the GitHub data collection process."""
data = fetch_data()
df = make_table(data)
df = tidy_data(df)
save_data(df)
if __name__ == "__main__":
    main()