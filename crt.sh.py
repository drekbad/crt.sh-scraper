#!/usr/bin/env python3

import argparse
import json
import sys
import time
import urllib.request
import urllib.error

def fetch_crtsh(domain: str, max_retries: int = 5) -> list | None:
    """Fetch certificate data from crt.sh with retries."""
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; crt-subdomain-tool/1.0)"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw)
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            print(f"Attempt {attempt+1}/{max_retries} failed: {e}", file=sys.stderr)
            if attempt < max_retries - 1:
                sleep = 2 ** attempt
                print(f"Retrying in {sleep} seconds...", file=sys.stderr)
                time.sleep(sleep)
    
    print("Failed to retrieve data after all retries.", file=sys.stderr)
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Pull unique subdomains from crt.sh (Certificate Transparency logs)"
    )
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g. example.com)")
    parser.add_argument("-o", "--outfile", help="Output file (optional; prints to stdout if omitted)")
    args = parser.parse_args()

    domain = args.domain.strip().lower()

    print(f"Searching crt.sh for subdomains of {domain}...", file=sys.stderr)

    data = fetch_crtsh(domain)
    if not data:
        print("No results returned (site may be rate-limiting or temporarily down).", file=sys.stderr)
        sys.exit(1)

    subdomains = set()
    for entry in data:
        if "name_value" not in entry:
            continue
        # name_value can contain multiple names separated by newlines
        for name in entry["name_value"].splitlines():
            name = name.strip().lower()
            if (name and
                not name.startswith("*.") and          # drop wildcards
                name.endswith("." + domain) and       # must be a subdomain of the target
                name != domain):                      # exclude the apex domain itself
                subdomains.add(name)

    if not subdomains:
        print("No (non-wildcard) subdomains found.", file=sys.stderr)
        sys.exit(0)

    sorted_subs = sorted(subdomains)

    if args.outfile:
        with open(args.outfile, "w") as f:
            f.write("\n".join(sorted_subs) + "\n")
        print(f"Done → {len(sorted_subs)} unique subdomains written to {args.outfile}")
    else:
        print("\n".join(sorted_subs))
        print(f"\nDone → {len(sorted_subs)} unique subdomains found.")


if __name__ == "__main__":
    main()
