# Systems Assessment & Build-vs-Buy — How I Do It, With the Receipts

The recurring engagement: come into a business, survey the systems and the needs, decide what to buy off the shelf versus build, and sequence it so the foundation holds before automation and AI go on top. Below is the method as I actually practice it, followed by the real decisions it produced across three businesses.

---

## The method (extracted from the work, not a textbook)

**1. Inventory the landscape before touching anything.**
Every platform, license, integration, batch job, and manual workaround — including what's already paid for and idle. The freight-brokerage engagement's Phase 1 is exactly this: full Salesforce org audit (batch jobs, Flows, data health, permissions), Accounting Seed audit, API discovery, and a written list of every integration gap and manual workaround in use. At Blackforge it was a full storefront and stack walkthrough before any fix.

**2. Find what's owned but underused first.**
The cheapest capability is the one already licensed. Bank Direct Connect was included in the accounting license; Sales Engagement cadences were free on the Salesforce edition; carrier compliance monitoring was already configured but only in manual mode. Activating idle capability beats buying new capability every time.

**3. Pin the constraints that decide the answer.**
Plan tiers, license add-ons, data thresholds, governance rules. Einstein lead scoring needs 1,000+ converted leads and an add-on — so rule-based scoring first. Live carrier shipping rates need Shopify's Advanced plan — so flat rates. Salesforce now requires admin-approved Connected Apps — so that's a Phase 1 task, not a surprise in Phase 3. Constraints are found up front or they become rework.

**4. Buy-vs-build decision rule, in order:**
- **Pre-built connector first** (vendor-built and maintained — configuration, not development).
- **Configure over code** (Flows, rules, native features).
- **Build a thin custom layer only for business-specific logic** the platform can't express.
- **Enterprise middleware only at scale** — MuleSoft-class iPaaS is a Phase 4 question, not a Phase 1 default.
- **Don't switch platforms to solve a problem the current one can solve** — evaluated Klaviyo for reviews and kept Judge.me, because the requirement was a shareable link, not a new platform.

**5. Sequence: stabilize → fix & activate → integrate & automate → scale with AI.**
Automation on an unstable foundation just automates the mess. AI on thin data returns noise. Each phase has a deliverable before the next starts.

---

## Real decisions — what was considered, what was chosen, why

| Decision | Options weighed | Chose | Why |
|---|---|---|---|
| Carrier-payment platform integration (brokerage) | Pre-built Revenova↔E-Pay connector · custom Flow/Apex build · MuleSoft | **Pre-built connector**, Flow/Apex only for brokerage-specific logic, MuleSoft deferred to Phase 4 | Vendor-built and maintained; configuration not development; lowest risk and fastest go-live |
| Lead scoring (brokerage) | Einstein AI scoring · rule-based Flow scoring | **Rule-based first, Einstein at Phase 3–4** | Einstein needs 1,000+ converted leads and an add-on license; no data yet to train it |
| Load visibility (brokerage) | MacroPoint · project44 · TextLocate · Trucker Tools | **MacroPoint primary, TextLocate for app-resistant carriers, others layered by mode** | All pre-built on the TMS; chosen by fit — broker-focused vs. multi-modal vs. SMS-only |
| Bank reconciliation (brokerage) | New integration · Bank Direct Connect | **Bank Direct Connect** | Already included in the accounting license — activate, don't buy |
| Prospecting data (brokerage) | ZoomInfo · UpLead · Freight Genie · LeadSend | **Tiered by budget and fit**; UpLead as the cost-effective entry | Same Salesforce integration, 95% accuracy, a fraction of the cost at startup scale |
| Outreach cadences (brokerage) | Third-party sequencing tool · native Sales Engagement | **Native Sales Engagement** | Included free on the edition already licensed |
| Reviews platform (Blackforge) | Migrate to Klaviyo Reviews · keep Judge.me | **Keep Judge.me** | The need was a shareable review link, which Judge.me already had; migrating would cost money and delay collection |
| Review-reward automation (Blackforge) | Judge.me paid tier · manual Shopify discount code | **Manual code** | Small volume didn't justify a monthly tier to automate a few dozen sends |
| Shipping rates (Blackforge) | Live UPS/FedEx carrier rates · flat rates | **Flat rates** | Live third-party rates require the Advanced plan and would price out $15–30 items; flat rates were correct for the catalog |
| Ad creative delivery (Blackforge) | Dynamic catalog ads · hand-curated creative | **Curated** | Dynamic format auto-pulled off-brand images; control mattered more than automation |
| Social content production (Blackforge) | Scheduler SaaS · in-house agent pipeline | **Built the agent pipeline** | Needed editing, brand-voice captioning, and an approval gate — no off-the-shelf tool did all three |
| Email automation ownership (Blackforge) | Shopify Flow · Klaviyo · both | **One owner per trigger** — Klaviyo for cart/checkout/welcome, Shopify Flow for the rest | Both were firing; customers were double-emailed; consolidation, not a new tool |
| Marketplace channel (Blackforge) | Bulk manual listings linking out · Facebook Shop with website checkout | **Shop with website checkout** as the engine, a few manual listings on top | Bulk linked listings violate platform policy and have no API; the Shop is compliant and syncs the whole catalog |
| Bilingual site experience (HealthBlendRX) | Rebuild the site in two languages · thin GTM injection layer | **Built a thin GTM layer** | Delivered two language-native experiences without a rebuild; survives SPA re-renders |
| Telehealth platform (HealthBlendRX) | Stay on incumbent · migrate | **Migrate**, against a written non-negotiable requirements list | Requirements (native-language physicians, separate branded experiences, pharmacy failover, own payment processor, e-prescribing, data ownership, SLA) drove vendor selection, not sales pitches |
| CRM & automation stack (HealthBlendRX) | Custom build · off-the-shelf stack | **Close CRM + Zapier + GTM** | Proven tools wired together; effort went into workflow design and fixing a duplicate-trigger bug, not into reinventing a CRM |

---

## Assessment artifacts (available in the repo / on request)
- **Brokerage Phase 1 "Stabilize & Assess" checklist** — org audit, accounting audit, integration-gap inventory, API discovery, ICP definition, Connected App registration. (`freight-brokerage-ai-strategy/`)
- **Blackforge stack audit → decision log** — shipping profiles, email automation ownership, ad-format diagnosis, review platform evaluation. (`README.md`, `code/`)
- **HealthBlendRX platform requirements list** — the non-negotiables used to evaluate and select the telehealth platform.

---

## What a hiring manager should take from this
The pattern is the same regardless of stack: inventory first, activate what's already owned, pin the constraints, buy before build, build thin, defer enterprise middleware, and sequence stability before automation before AI. It's been applied to a Salesforce/TMS enterprise stack, a Shopify commerce stack, and a WordPress/CRM telehealth stack — and the decisions above are the evidence, not the claim.
