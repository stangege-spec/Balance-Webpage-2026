# Balance by Garrett website

One streamlined page for **balancebygarrett.coach** with four ways to feel better:

1. **The Glendale gym:** personal training ($55 / 25 min, $95 / 55 min) and small group ($160 / month, Mon, Wed, Thu at 9 AM).
2. **Remote health coaching:** Trainerize app, $300 / month.
3. **Bare Min by Garrett app:** free, Balance Plus, Balance Coach, with a QR code to get the app.
4. **Corporate wellness:** free 30-day team pilot, team app license, coached challenge, talks.

Plus a "Bottomless Bucket is back in 2027" note, a testimonial and a free consultation call to action.

It is a plain static site (`index.html`, `img/`, `vercel.json`) with no build step, so it runs on Vercel, Netlify, GitHub Pages or any web host.

## Put it on Vercel

1. Sign in at [vercel.com](https://vercel.com) with GitHub.
2. **Add New → Project**, pick `balance-webpage-2026`, click **Import**.
3. Leave **Framework Preset** as **Other** and the build settings empty. Click **Deploy**.

Every push to `main` redeploys the site.

## Connect balancebygarrett.coach

In the Vercel project, open **Settings → Domains**, add `balancebygarrett.coach`, and also add `www.balancebygarrett.coach` (Vercel offers to redirect one to the other).

The domain is registered at **Namecheap**. In Namecheap, go to **Domain List → Manage** next to balancebygarrett.coach, open **Advanced DNS**, delete the default parking records (the CNAME for `www` and the URL Redirect for `@`), and add the two records Vercel shows you. They usually look like this:

| Type | Host | Value |
|---|---|---|
| A Record | `@` | `76.76.21.21` |
| CNAME Record | `www` | `cname.vercel-dns.com.` |

Use the exact values Vercel shows on the Domains page if they differ. DNS can take from a few minutes up to a day; Vercel adds the HTTPS certificate automatically once it sees the records.

## The QR code

`img/qr-app.svg` and `img/qr-app.png` point to **balancebygarrett.coach/app**. Right now that address opens the Bare Min section of this page (see `vercel.json`). When the app is in the App Store, change the `destination` in `vercel.json` to the store link, and every printed QR code starts sending people there without being reprinted.

## Still to add

- **Logo:** save the Balance by Garrett logo as `img/logo.png` (about 570 × 96). Until then the header tries the logo on the Wix site, then falls back to text.
- **Booking:** a WellnessLiving booking link for the free consultation (now phone and email).
- **App store links** for the "Get the app" buttons, then the `vercel.json` change above.
- **Email list:** the signup form opens an email to Garrett; swap in a Mailchimp or similar form when ready.
