# JMS Tech Social Upgrade — Implementation Plan

> **For Hermes:** Preserve the active V2 publishing path. Do not revive or modify the retired `jms-tech-autoposter` stack.

**Goal:** Turn the existing JMS Tech Support Facebook/Instagram rotation into a varied, local, proof-led publishing system without increasing the four-post-per-week cadence or bypassing the current V2 automation.

## Implementation status — 31 July 2026

**Completed by Hermes**
- Active V2 source, state, scheduler and media contract traced; V2 preflight passes with 42 Tech items.
- Deterministic V2 rotation and two privacy-reviewed camera-install entries staged.
- Five genuine Google-review cards staged with a retained source/provenance record.
- Read-only baseline saved to `/home/josh/kramer-data/reports/jms-tech-social-baseline-2026-07-31.json`; it contains all 31 retrievable Instagram items plus Page/account figures. Facebook post-level Graph readback is currently permission-blocked (`pages_read_engagement`), and is explicitly recorded rather than fabricated.
- Non-destructive post audit saved to `/home/josh/kramer-data/reports/jms-tech-social-post-audit-2026-07-31.json`; no post was hidden, archived, edited or deleted.
- Job-proof lane created at `/home/josh/kramer/state/jms-tech-autoposter/job-proof/` with inbox, approved, rejected, manifest and privacy/consent instructions.
- Facebook website field changed from `http://www.jmstechsupport.com.au/` to `https://jmstechsupport.com.au/` and publicly verified.
- One-shot production-post readback is scheduled for 31 July 2026 at 16:45 Australia/Sydney; a 30-day performance comparison is scheduled for 30 August 2026 at 17:00 Australia/Sydney.

**Reserved for Josh's content-mix decisions**
- The remaining queue composition: new genuine local-job outcomes, direct booking/availability slots, CTA rotation, Reel creative and whether Instagram should remain camera-first or move to a broader service funnel.
- Do not publish, label, or invent those items until Josh supplies/approves the factual asset or queue direction.

**Current verified publisher:**
- Timer: `/home/josh/.config/systemd/user/jms-autoposter-v2-tech.timer`
- Service: `/home/josh/.config/systemd/user/jms-autoposter-v2-tech.service`
- Command: `/home/josh/kramer/bin/jms-autoposter-v2 publish --brand tech`
- Existing rotation: `/home/josh/kramer/state/jms-tech-autoposter/rotation-plan.json`
- Existing state/assets: `/home/josh/kramer/state/jms-tech-autoposter/`

**Architecture:** Keep V2 as the only scheduler and cross-platform publisher. Replace the current all-tip rotation with a 40-slot content calendar that retains useful tips while deliberately introducing real job proof, customer proof, direct booking prompts, and short vertical video. No post goes live outside V2. Every real job asset must be genuine and approved for marketing use.

**Cadence:** Monday 09:15, Wednesday 12:15, Friday 16:30, Sunday 18:30 — Australia/Sydney. No increase in volume.

---

## Phase 1 — Establish the V2 source of truth

### Task 1: Trace V2’s content-selection contract

**Objective:** Identify the exact content file(s) and schema consumed by `jms-autoposter-v2` for brand `tech` before changing calendar data.

**Files to inspect:**
- `/home/josh/kramer/bin/jms-autoposter-v2`
- `/home/josh/kramer/state/jms-tech-autoposter/rotation-plan.json`
- `/home/josh/kramer/state/jms-tech-autoposter/state.json`
- `/home/josh/kramer/state/jms-tech-autoposter/published_hashes.jsonl`

**Actions:**
1. Trace `publish --brand tech` to its content loader.
2. Confirm duplicate detection keys and the current `last_post_date`/per-calendar-day guard.
3. Confirm the directory used for rendered image/video assets.
4. Record the exact V2 output log and service result path.

**Acceptance criteria:** A dry-run or non-publishing inspection identifies the live content source; the old non-V2 state/log paths are not touched.

### Task 2: Take a metrics baseline

**Objective:** Record a starting point that proves whether the change improves the account.

**Metrics:**
- Instagram followers, media count, post-level likes/comments, reach/saves/shares if Meta exposes them.
- Facebook followers, post-level reactions/comments/shares, reach if Meta exposes it.
- Website sessions and completed contact leads attributed to `facebook.com` / `instagram.com` in analytics.

**Output:**
- `/home/josh/kramer-data/reports/jms-tech-social-baseline-2026-07-31.json`

**Acceptance criteria:** Baseline captures the current 226 Instagram followers, 98 Facebook followers, recent post dates, and post engagement. It is read-only collection.

---

## Phase 2 — Replace the tip-only rotation with a deliberate 10-week mix

### Task 3: Build the 40-slot content calendar

**Objective:** Keep four V2 posts a week while guaranteeing varied content categories and preventing rapid repeats.

**Target composition across 40 posts:**
- 20 practical tips (50%)
- 10 genuine local job outcomes (25%)
- 6 review/customer-proof posts (15%)
- 4 direct booking/availability posts (10%)

**Slot pattern each week:**
1. **Monday — job outcome:** a real completed job, before/after, or a short explanation of the fix.
2. **Wednesday — practical tip or 15–30 second vertical Reel.**
3. **Friday — booking/service focus:** computer repairs, Wi-Fi, printers, TV/Chromecast, security cameras, or account recovery. Include one specific CTA.
4. **Sunday — customer proof, FAQ, or a local household-tech scenario.**

**Rules:**
- No tip may recur within 45 days.
- Do not label generic posts as a local job.
- No customer name, address, screen contents, serial number, password, phone number, or identifiable home interior is published without permission.
- Every entry must have `content_type`, `service`, `local_area` where truthful, `CTA`, `asset_path`, and a caption fingerprint.

**Files:**
- Modify the V2 content source identified in Task 1.
- Keep image/video assets beneath the V2 asset directory identified in Task 1.

**Acceptance criteria:** 40 unique entries validate against V2’s existing schema; duplicate detector sees no collision with recently published captions or assets.

### Task 4: Build a real-job evidence intake lane

**Objective:** Make genuine proof posts repeatable rather than waiting for an improvised photo hunt every week.

**Create:**
- `/home/josh/kramer/state/jms-tech-autoposter/job-proof/inbox/`
- `/home/josh/kramer/state/jms-tech-autoposter/job-proof/approved/`
- `/home/josh/kramer/state/jms-tech-autoposter/job-proof/rejected/`
- `/home/josh/kramer/state/jms-tech-autoposter/job-proof/manifest.jsonl`

**Manifest fields:** date, service, suburb (optional), problem, outcome, consent status, source-asset path, redaction required, candidate caption, approval status.

**Workflow:**
1. I inspect each supplied or existing permissible photo/video.
2. I reject anything with private/customer data or missing marketing consent.
3. I crop/redact only where needed and create a platform-safe square post or 9:16 Reel asset.
4. I create the V2 calendar entry. It posts through the normal V2 path.

**Acceptance criteria:** One complete real job post can move from intake to a V2 content slot with no manual publishing or privacy guessing.

---

## Phase 3 — Add video and improve conversion behaviour

### Task 5: Create a reusable short-Reel template

**Objective:** Introduce one clear video post per week without making production ridiculous.

**Format:** 1080×1920, 15–30 seconds, real handset footage or clearly-labelled instructional visuals, subtitles, no Ken Burns effect.

**Template:**
1. First 2 seconds: exact problem — e.g. “Chromecast cannot find the TV?”
2. Next 15 seconds: one safe, demonstrable check.
3. Final 5 seconds: one clear CTA — “Still stuck? JMS Tech comes to you in Yamba, Maclean and the Clarence Valley.”

**Acceptance criteria:** Rendered test asset is visually reviewed before it enters V2. The published post retains its caption on both Facebook and Instagram.

### Task 6: Rewrite CTAs to create replies and qualified DMs

**Objective:** Stop ending every post with the same passive service sentence.

**CTA rotation:**
- “Which room has the worst Wi-Fi in your place?”
- “Has your TV disappeared from Chromecast too?”
- “Message a photo of the error if you are not sure what it means.”
- “Book an on-site fix in Yamba, Maclean or the Clarence Valley.”
- “Need this sorted before the weekend? Send a message.”

**Acceptance criteria:** Every calendar entry has one CTA matched to its content type; no generic CTA is repeated in consecutive posts.

---

## Phase 4 — Repair profile funnel consistency

### Task 7: Align profile links with the actual service funnel

**Objective:** Ensure profile descriptions, website links, and the post CTA take visitors to the appropriate page.

**Verified current state:**
- Instagram bio routes to the security-camera landing page despite a broad service bio.
- Facebook website field uses `http://www.jmstechsupport.com.au/` rather than HTTPS.

**Actions:**
1. Change the Facebook website field to `https://jmstechsupport.com.au/`.
2. Keep Instagram camera-first only if security cameras are the primary conversion campaign. Otherwise set it to the homepage or a purpose-built local service chooser.
3. Verify business name, phone, service areas and URL remain consistent with the website and Google Business Profile.

**Acceptance criteria:** Profile link destination, bio promise, and post CTA tell the same story; links resolve to HTTPS.

---

## Phase 5 — Validate the pipeline and measure after 30 days

### Task 8: V2 dry run and end-to-end validation

**Objective:** Prove the updated rotation does not break posting.

**Steps:**
1. Validate calendar JSON/schema and every referenced asset exists.
2. Run V2 in its available non-publishing/dry-run mode. If V2 has no dry-run mode, use its internal validator without posting.
3. Confirm the once-per-calendar-day guard, duplicate checks, retry-on-failure behaviour, and Telegram error alert remain active.
4. Stage one item and visually inspect its image, crop, caption, and CTA before its scheduled V2 publication.
5. After it publishes, read back both Meta posts and verify the caption exists on each platform.

**Acceptance criteria:** No test content is posted live; first scheduled production post is verified in Facebook and Instagram after publication.

### Task 9: Thirty-day review

**Objective:** Compare outcome rather than declaring victory because the cards look different.

**Compare against the Phase 1 baseline:**
- engagement by content type;
- comments and DMs prompted by CTA type;
- followers;
- website referrals;
- contact form leads/bookings attributed to social;
- whether job proof or video outperforms static tips.

**Decision rule:** Retain the best-performing two job-proof formats and the best Reel format; remove the weak formats. Keep total frequency at four posts per week unless evidence supports a change.

---

## Required inputs that cannot be fabricated

I can handle system changes, content calendar, captions, asset preparation, V2 validation, profile edits, and measurement. Genuine job-proof posts require at least one of:
- existing permissible job photos/video;
- a customer review approved for reuse;
- a factual job summary with no identifying customer information.

No fake “local job” posts. That would be a remarkably stupid way to build a local trust business.
