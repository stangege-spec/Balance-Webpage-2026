# Balance by Garrett website

The homepage for **balancebygarrett.coach**, hosted on GitHub Pages from `main` (root). It is a plain static site with no build step: `index.html`, `img/`, `js/` and `data/`.

## What's on the page

1. **Four ways to feel better:** the Glendale gym ($55 / 25 min, $95 / 55 min, small group $160 / month), remote coaching ($300 / month), the Bare Min tools, and corporate wellness.
2. **Shop**, with each product in its own band:
   - the **Bare Min by Garrett app** (sample Today screen, App Store and Google Play buttons, QR code);
   - the **workbook** on Amazon;
   - the eight **Grow workshops** (4 weeks each) and the complete set on Gumroad.
3. **Google reviews**, **blog posts** from livebalancefit.com, **social links**, Garrett's bio and the free consultation call to action.

## Changing a link

Every outside link (Amazon, App Store, Google Play, each Gumroad product, socials, Google profile) is in **`js/links.js`**. Paste the new URL between the quotes and commit. A buy button with an empty link reads "Coming soon"; a social button with an empty link is hidden.

## Blog and reviews update on their own

The **Update blog and reviews** action (`.github/workflows/feeds.yml`) runs every 6 hours. It reads the livebalancefit.com blog feed and Google reviews, saves them to `data/blog.json` and `data/reviews.json`, and the page shows the newest posts and reviews. Run it any time from the **Actions** tab with **Run workflow**.

The blog works with no setup. Google reviews need a free Google Places API key:

1. In [Google Cloud Console](https://console.cloud.google.com/), create a project, enable **Places API (New)**, and under **APIs & Services → Credentials** create an **API key** (restrict it to Places API).
2. In this repo, open **Settings → Secrets and variables → Actions → New repository secret**, name it `GOOGLE_PLACES_API_KEY`, and paste the key.
3. Run the action once. It finds the gym by its name and address. If it picks the wrong listing, add a repository **variable** `GOOGLE_PLACE_ID` with the right Place ID.

Google gives at most 5 recent reviews; the site shows the 4 and 5 star ones that have text, plus the overall rating and a link to all reviews.

## The QR code

`img/qr-app.svg` and `img/qr-app.png` point to **balancebygarrett.coach/app**, which forwards to the app section (`app/index.html`). When the app is in the stores, change that page's forward to the store link and every printed QR code follows.

## Still to add

- **Logo:** save the Balance by Garrett logo as `img/logo.png` (about 570 × 96). Until then the header uses the logo from the Wix site.
- **Workbook cover:** `img/workbook-cover.jpg` is a stand-in; replace it with the Amazon cover (2:3, about 600 × 900).
- **Links** still empty in `js/links.js`: App Store, Google Play, each Grow module's own Gumroad page, YouTube and other socials, and the Google profile.
- **Booking:** a WellnessLiving booking link for the free consultation (now phone and email).
