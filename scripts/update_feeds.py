#!/usr/bin/env python3
"""Refresh data/blog.json from the livebalancefit.com blog feed and
data/reviews.json from Google (Places API). Run by .github/workflows/feeds.yml.

Standard library only. Each feed is independent: if one fails or is not set up,
its JSON file is left as it was, so the site keeps showing the last good copy.

Environment:
  GOOGLE_PLACES_API_KEY  required for reviews (repo secret)
  GOOGLE_PLACE_ID        optional; found by searching GOOGLE_PLACE_QUERY when unset
  GOOGLE_PLACE_QUERY     optional; defaults to the Glendale gym's name and address
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED = "https://www.livebalancefit.com/blog-feed.xml"
UA = "BalanceByGarrettSite/1.0 (+https://balancebygarrett.coach)"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url, headers=None, data=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def write_if_changed(path, payload, compare_keys):
    """Write JSON only when the content (not just the timestamp) changed."""
    old = {}
    if path.exists():
        try:
            old = json.loads(path.read_text())
        except ValueError:
            pass
    if all(old.get(k) == payload.get(k) for k in compare_keys):
        print(f"{path.name}: no change")
        return
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"{path.name}: updated")


def bigger_wix_image(url):
    # Wix feed images are small thumbnails; ask Wix for a 640x400 crop instead.
    m = re.match(r"(https://static\.wixstatic\.com/media/[^/]+?\.(\w+))", url or "")
    if not m:
        return url or ""
    return f"{m.group(1)}/v1/fill/w_640,h_400,al_c,q_80/file.{m.group(2)}"


def summary(html, limit=170):
    text = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html or ""))).strip()
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "…"


def update_blog():
    root = ET.fromstring(get(FEED))
    posts = []
    for item in root.iter("item"):
        enc = item.find("enclosure")
        date = item.findtext("pubDate") or ""
        try:
            date = parsedate_to_datetime(date).date().isoformat()
        except (TypeError, ValueError):
            date = ""
        posts.append({
            "title": (item.findtext("title") or "").strip(),
            "link": (item.findtext("link") or "").strip(),
            "date": date,
            "image": bigger_wix_image(enc.get("url") if enc is not None else ""),
            "summary": summary(item.findtext("description")),
        })
    posts = [p for p in posts if p["title"] and p["link"]]
    posts.sort(key=lambda p: p["date"], reverse=True)
    if not posts:
        raise RuntimeError("feed had no posts")
    write_if_changed(ROOT / "data/blog.json",
                     {"source": FEED, "updated": NOW, "posts": posts[:6]}, ["posts"])


def places(path, key, fields, body=None):
    headers = {"X-Goog-Api-Key": key, "X-Goog-FieldMask": fields}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    return json.loads(get("https://places.googleapis.com/v1/" + path, headers, data))


def update_reviews():
    key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not key:
        print("reviews: skipped (add the GOOGLE_PLACES_API_KEY secret to turn on)")
        return
    place_id = os.environ.get("GOOGLE_PLACE_ID")
    if not place_id:
        query = os.environ.get("GOOGLE_PLACE_QUERY") or \
            "Balance Fitness, 4170 N Port Washington Rd, Glendale, WI 53212"
        found = places("places:searchText", key, "places.id,places.displayName",
                       {"textQuery": query}).get("places", [])
        if not found:
            raise RuntimeError(f"no Google place found for {query!r}")
        place_id = found[0]["id"]
        print(f"reviews: using place {found[0].get('displayName', {}).get('text')} ({place_id})")
    p = places("places/" + urllib.parse.quote(place_id), key,
               "rating,userRatingCount,googleMapsUri,reviews")
    reviews = []
    for r in p.get("reviews", []):
        text = (r.get("text") or r.get("originalText") or {}).get("text", "").strip()
        if not text or (r.get("rating") or 0) < 4:
            continue
        who = r.get("authorAttribution", {})
        reviews.append({
            "author": who.get("displayName", "Google user"),
            "photo": who.get("photoUri", ""),
            "rating": r.get("rating"),
            "when": r.get("relativePublishTimeDescription", ""),
            "text": text,
        })
    write_if_changed(ROOT / "data/reviews.json", {
        "updated": NOW,
        "rating": p.get("rating"),
        "count": p.get("userRatingCount"),
        "url": p.get("googleMapsUri", ""),
        "reviews": reviews,
    }, ["rating", "count", "url", "reviews"])


if __name__ == "__main__":
    failed = False
    for job in (update_blog, update_reviews):
        try:
            job()
        except Exception as e:  # keep the other feed going, report at the end
            failed = True
            print(f"{job.__name__} failed: {e}", file=sys.stderr)
    sys.exit(1 if failed else 0)
