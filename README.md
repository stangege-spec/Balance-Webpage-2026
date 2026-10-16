# Balance by Garrett website

The "Feel better" homepage for Balance Fitness / Balance by Garrett and the Bare Min by Garrett products.

It is a plain static site (`index.html` plus `img/`), with no build step.

## Deploy on Vercel

1. In Vercel, choose **Add New → Project** and import this repository.
2. Leave **Framework Preset** as **Other**. Leave the build command and output directory empty.
3. Click **Deploy**.
4. Under **Settings → Domains**, add the new domain.

Every push to `main` redeploys the site.

## Still to wire up

- **Logo:** `img/logo.png` (the header currently loads it from the Wix site).
- **Booking:** the WellnessLiving booking widget, in the "Book a coach" section.
- **Shop:** Stripe payment links for the downloads.
- **App:** App Store and Google Play links.
- **Social:** Instagram and YouTube links.
