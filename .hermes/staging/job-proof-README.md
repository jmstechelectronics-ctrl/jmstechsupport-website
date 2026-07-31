# JMS Tech job-proof intake

A proof post begins here. Do not place customer photos or video directly into the V2 rotation.

## Folders

- `inbox/` — unreviewed supplied asset; never published.
- `approved/` — privacy-checked asset with an approved manifest record; eligible for V2 staging.
- `rejected/` — asset retained only if needed for record-keeping; manifest records why it cannot be used.
- `manifest.jsonl` — one JSON object per submitted asset, including approval status.

## Required manifest object

```json
{
  "submitted_at": "2026-07-31T00:00:00Z",
  "service": "security camera installation",
  "suburb": "Yamba",
  "problem": "Customer requested camera coverage for an entry point.",
  "outcome": "Camera installed and setup completed.",
  "consent_status": "approved_for_social",
  "source_asset_path": "job-proof/inbox/example.jpg",
  "redaction_required": false,
  "candidate_caption": "",
  "approval_status": "approved",
  "reviewed_at": "2026-07-31T00:00:00Z",
  "review_notes": "No faces, address, plates, screens, serials or security-sensitive detail visible."
}
```

## Hard stop rules

Reject or redact any asset showing a face, house number, address, vehicle plate, customer screen, login, serial number, password, access-control detail, alarm-panel code, or unconfirmed marketing permission.

A factual job summary without identifying details may be used only after the same manifest approval.
