# Balance by Garrett website

One streamlined page for **balancebygarrett.com** with four ways to feel better:

1. **The Glendale gym:** personal training ($55 / 25 min, $95 / 55 min) and small group ($160 / month, Mon, Wed, Thu at 9 AM).
2. **Remote health coaching:** Trainerize app, $100 / month.
3. **Bare Min by Garrett app:** free, Balance Plus, Balance Coach, with a QR code to get the app.
4. **Corporate wellness:** free 30-day team pilot, team app license, coached challenge, talks.

Plus a "Bottomless Bucket is back in 2027" note, a testimonial and a free movement screen call to action.

It is a plain static site (`index.html`, `img/`, `vercel.json`) with no build step, so it runs on Vercel, Netlify, GitHub Pages or any web host.

## Put it on Vercel

1. Sign in at [vercel.com](https://vercel.com) with GitHub.
2. **Add New → Project**, pick `balance-webpage-2026`, click **Import**.
3. Leave **Framework Preset** as **Other** and the build settings empty. Click **Deploy**.

Every push to `main` redeploys the site.

## Connect balancebygarrett.com

In the Vercel project, open **Settings → Domains**, add `balancebygarrett.com`, and also add `www.balancebygarrett.com` (Vercel offers to redirect one to the other).

- **If you bought the domain through Vercel:** nothing else to do. It connects on its own.
- **If the domain is at another registrar** (GoDaddy, Google/Squarespace, Namecheap, Wix and so on), add the two records Vercel shows you in that registrar's DNS settings. They usually look like this:

| Type | Name | Value |
|---|---|---|
| A | `@` | `76.76.21.21` |
| CNAME | `www` | `cname.vercel-dns.com` |

Use the exact values Vercel shows on the Domains page if they differ. DNS can take from a few minutes up to a day; Vercel adds the HTTPS certificate automatically once it sees the records.

## The QR code

`img/qr-app.svg` and `img/qr-app.png` point to **balancebygarrett.com/app**. Right now that address opens the Bare Min section of this page (see `vercel.json`). When the app is in the App Store, change the `destination` in `vercel.json` to the store link, and every printed QR code starts sending people there without being reprinted.

## Still to add

- **Logo:** save the Balance by Garrett logo as `img/logo.png` (about 570 × 96). Until then the header tries the logo on the Wix site, then falls back to text.
- **Booking:** a WellnessLiving booking link for the free movement screen (now phone and email).
- **App store links** for the "Get the app" buttons, then the `vercel.json` change above.
- **Email list:** the signup form opens an email to Garrett; swap in a Mailchimp or similar form when ready.
