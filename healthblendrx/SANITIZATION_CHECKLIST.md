# What to add — and what to strip — before anything from HealthBlendRX goes in this repo

Healthcare context: treat this as PHI-adjacent. When in doubt, describe it instead of pasting it.

## ADD (sanitized)
- [ ] `code/gtm_bilingual_injection.js` — the GTM tag. STRIP: GTM container ID (GTM-XXXX), tag IDs, Contentsquare tag ID, any hardcoded URLs to admin/checkout endpoints. KEEP: the MutationObserver + pushState logic, selectors, the EN/ES copy map (business copy is fine).
- [ ] `code/zapier_workflows.md` — one line per zap: **Trigger → Action(s)**. e.g. "Site form submission → create Close lead → apply lifecycle tag → enqueue SMS." STRIP: zap IDs, webhook URLs, API keys, field values, any sample records.
- [ ] `code/close_crm_workflow_fix.md` — the duplicate-trigger fix as before/after logic (which stage was on the trigger, why it re-fired, the exit condition added). STRIP: lead names, emails, phone numbers, any real record.
- [ ] `code/pptx_deck_builder.py` — the python-pptx generator. STRIP: the business-plan text, financials, and slide content; leave the structure/functions with placeholder content.

## NEVER ADD
- Patient or lead data of any kind — names, emails, phones, conditions, prescriptions, visit notes.
- Credentials, API keys, webhook URLs, OAuth tokens, container/pixel/tag IDs.
- Vendor names for the telehealth platform, pharmacy, or any contract/pricing/SLA detail. Say "telehealth platform" / "pharmacy partner."
- Financials, equity structure, cap table, or partner names.
- Anything from a system you don't solely control without a heads-up to your co-founders.

## FINAL CHECK before committing
grep the folder for: `@`, `GTM-`, `http`, `key`, `token`, `secret`, phone patterns, and any real first/last name. If it hits, fix it or leave it out.
