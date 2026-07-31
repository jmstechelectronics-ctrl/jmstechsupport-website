# JMS Web Design — assessment

**Assessed:** 31 July 2026, Australia/Sydney  
**Scope:** live site, conversion path, Search Console, public-facing social profile configuration, Instagram content sample, and publisher health.  
**Initial assessment changes:** none. Implementation updates are recorded below.

> **Implementation update — 31 July 2026:** The assessment’s pricing, homepage-load and Facebook Page URL items have been actioned and deployed in commit `81ffc3f`. Active V2 publisher discovery is complete; portfolio-preview posts and current-price captions are staged into V2 without publishing. Instagram’s website control remains mobile-app-only.

## Executive assessment

The site is credible, clear and technically accessible, but it has two immediate commercial-consistency failures: **pricing contradicts itself in structured data and terms**, and **the observed social publishing path is not operationally attributable**. Performance is also too slow for a paid acquisition landing page.

The homepage visual design is strong: the mobile hero is readable, the offer is prominent, the CTA is obvious, and the pricing shown to visitors is straightforward. The basic lead path is wired: FormSubmit points to the thank-you page, the honeypot is present, and `fbq` is loaded on both pages. A real submission was deliberately not made, because it would contaminate the production lead inbox.

## Evidence

### Live site and conversion

- Live homepage title: `JMS Web Design | Websites for Tradies & Small Businesses Australia`.
- Live mobile hero visibly presents `Still using Facebook as your website?`, `$349 once, $29 a month`, and the primary `Send your Facebook page` CTA.
- The form has name, email, optional phone, Facebook/profile link and business-description inputs; it submits to FormSubmit and sends successful submissions to `/thanks.html`.
- Form protection is configured with `_captcha=false` plus FormSubmit's `_honey` honeypot.
- Meta Pixel `1537482598109576` is present and `fbq` resolves as a function on the live homepage and thank-you page. The thank-you page contains the Lead event source.
- Direct production lead-event verification was not performed: a fake submission would create a real email and contaminate the lead stream.

### Performance and search

A Lighthouse mobile run on the live home page produced:

| Category | Score |
|---|---:|
| Performance | 43/100 |
| Accessibility | 100/100 |
| Best practices | 100/100 |
| SEO | 92/100 |

Measured diagnostics: FCP **3.1 s**, LCP **6.9 s**, total blocking time **1,450 ms**, CLS **0**. Lighthouse estimated at least **55 KiB** responsive-image savings. Treat this as a representative single synthetic run, not a field-data verdict.

Search Console is verified and accessible under `sc-domain:jmswebdesign.com.au`, but its overview currently shows **“Processing data, please check again in a day or so”** for performance, indexing and experience. There is no current Search Console traffic or query baseline to report.

A fresh web search indexes the branded home page. The site was not returned in the first five results for either `website design for tradies Australia` or `websites for tradies Australia`; established niche competitors occupied those results.

### Social baseline

Current direct Meta readback:

| Surface | Evidence |
|---|---|
| Facebook Page | 12 followers; website field is `http://jmswebdesign.com.au/` |
| Instagram | `@jmswebdesign.com.au`, 282 followers, 1,092 following, 39 feed items |
| Latest content sample | 39 images, zero videos/reels in the returned sample; mean 4.77 likes, 0 comments |
| Approximate like rate | 1.69% of current followers per post |

The last ten Instagram posts are mostly broad vertical templates: mechanics, cafés, creators, cleaners, allied health, painters and beauty businesses. A mechanic post was repeated within eight days. The content is active — the newest item was published 30 July — but it is not demonstrating the work or process behind a real JMS Web customer build.

Facebook post-level collection is blocked by current token permissions (`pages_read_engagement` / Page Public Content Access). No Facebook engagement numbers were invented.

### Publishing operations

The legacy `jms-web-autoposter` systemd timer is disabled and has no next trigger. Its journal has no recent executions; its last known log is 28 June. Its state/log history also records Facebook and Instagram failures, including cases reported as `Posted!` after an Instagram 400 response. That is not an acceptable source of truth.

Despite this, Instagram posts continued through 30 July. Therefore a different production path is publishing current content. It has not yet been identified, so there is no reliable answer to **what posts where, when, and whether both platforms succeeded**.

The separate `JMS Web Autoposter Watchdog` scheduled job is enabled for 17:30 daily, but its most recent run is marked `error` and it delivers locally rather than to Josh. A watchdog that errors silently is decorative plumbing.

## Prioritised actions

### P0 — decide one current offer, then make it true everywhere — completed

Visitor-facing pricing is `$349 once + $29/month` in `index.html:1183`, but JSON-LD still says `$469 upfront + $49/month` in `index.html:815` and `index.html:824`. `terms.html:84` also retains the old $469/$49 Full Setup terms.

Josh confirmed the authoritative offer is **$349 once + $29/month**. Homepage pricing, JSON-LD pricing and terms were aligned and deployed in commit `81ffc3f`. The active V2 caption inventory now appends the same offer and its six-month minimum term.

### P0 — identify and restore ownership of the active social publisher — completed

Do not turn on the disabled legacy timer merely because it exists. That would risk duplicate publishing and reviving a known partial-failure path.

The active publisher is `jms-autoposter-v2-web.timer`, running `/home/josh/kramer/bin/jms-autoposter-v2 publish --brand web` daily at 17:00 with up to three hours of random delay. Its 30 July Mechanic post completed on both Facebook and Instagram. The legacy `jms-web-autoposter*` units are not the live publisher and remain disabled.

The V2 Web rotation now has 14 verified items: the existing approved ads, four portfolio-preview creatives (A360 Disability Solutions, JMS Tech Support, LeadDrop and ClawGauge), and no unsupported NDIS provider-count card. Every current caption appends the authoritative offer and minimum term. Each local and public media path passed an image-content check. The next eligible V2 Web item is Pet; nothing has been manually published.

### P1 — improve paid-landing-page speed — first pass completed

A simulated **6.9 s LCP** is too slow for an acquisition page. The first pass removed an unused Google Font stylesheet/preconnect sequence and lazy-loaded the three non-essential hero mockups. Local Lighthouse moved from **43 to 53 performance**, FCP from **3.1 s to 1.3 s**, and LCP from **6.9 s to 5.4 s**. TBT remained high and requires a separate third-party-script review; Meta/Google attribution was retained rather than amputated for a vanity score.

### P1 — bring social profile links to canonical HTTPS — Facebook completed

The Facebook Page website field now reads `https://jmswebdesign.com.au/` and was read back through the Graph API. Instagram still displays the HTTP destination publicly; the available browser session is signed out and Instagram’s Graph API does not expose a profile-website update. It needs the authenticated Instagram profile session, not a fake workaround.

### P1 — use social proof from real website outcomes

The feed is visually consistent but generic: all returned media are static images and there are no observed comments. Keep a useful vertical rotation, but add real build proof: client-approved before/after presence, screen recordings, launch walkthroughs, short client outcomes, and direct offer/booking posts. Avoid claiming outcomes that are not evidenced.

### P2 — clarify target-market hierarchy

The hero says tradies and small businesses, while the current social feed mixes creators, cafés, NDIS, beauty and trades. This is viable only if deliberate. Pick one hierarchy for acquisition: a primary segment, secondary segments, and content allocation. Otherwise every post tells a different buyer that the service is “for them,” which is the marketing equivalent of shouting into a paddock.

### P2 — repair small messaging inconsistencies

The website uses first-person copy at `index.html:1010` (`I’ll handle the website side`) despite the surrounding JMS Web voice using `we/us`. The footer links use the expected Facebook and Instagram handles; the public Page API currently resolves to its numeric URL rather than a vanity link, which should be checked when profiles are next reviewed.

## What was deliberately not changed

- No website copy, price, schema, terms, social profile, ad, post, queue, timer or service was edited.
- No fake FormSubmit lead was submitted.
- No disabled social publisher was started.
- No Facebook/Instagram item was deleted, hidden, edited or posted.
