#!/usr/bin/env python3
"""From100Quid auto-poster.

Reads queue.json, posts the first due unposted item to X, marks it posted.
Designed to run on a GitHub Actions cron — no human in the loop.
Veto mechanism: edit/delete any queue item before its `not_before` time.

Secrets required (repo Settings → Secrets → Actions):
    X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from requests_oauthlib import OAuth1Session

QUEUE = Path(__file__).parent / "queue.json"
POST_URL = "https://api.twitter.com/2/tweets"


def main() -> None:
    items = json.loads(QUEUE.read_text())
    now = datetime.now(timezone.utc)
    due = [i for i in items
           if not i.get("posted")
           and datetime.fromisoformat(i["not_before"]) <= now]
    if not due:
        print("Nothing due.")
        return
    item = due[0]

    if len(item["text"]) > 280:
        sys.exit(f"Item {item['id']} is {len(item['text'])} chars — fix the queue.")

    session = OAuth1Session(
        os.environ["X_API_KEY"],
        client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_SECRET"],
    )
    payload = {"text": item["text"]}
    if item.get("reply_to_last_posted"):
        last = [i for i in items if i.get("posted") and i.get("tweet_id")]
        if last:
            payload["reply"] = {"in_reply_to_tweet_id": last[-1]["tweet_id"]}

    r = session.post(POST_URL, json=payload)
    if r.status_code not in (200, 201):
        sys.exit(f"Post failed: {r.status_code} {r.text}")

    item["posted"] = True
    item["posted_at"] = now.isoformat(timespec="seconds")
    item["tweet_id"] = r.json().get("data", {}).get("id")
    QUEUE.write_text(json.dumps(items, indent=2, ensure_ascii=False))
    print(f"Posted {item['id']}: {item['text'][:60]}…")


if __name__ == "__main__":
    main()
