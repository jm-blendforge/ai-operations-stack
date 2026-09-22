# Meta Marketing API — real configurations used (via MCP connector)

## 1. Rolling retargeting audience (website custom audience)
Includes everyone who fired `AddToCart` in the last 14 days; excludes anyone who fires `Purchase`; backfills historical events on creation. Self-maintaining — new cart-adders enter automatically, people age out after 14 days.
```json
{
  "subtype": "WEBSITE", "prefill": true,
  "rule": {
    "inclusions": {"operator":"or","rules":[{"event_sources":[{"type":"pixel","id":"<PIXEL_ID>"}],
      "retention_seconds":1209600,"filter":{"operator":"and","filters":[{"field":"event","operator":"eq","value":"AddToCart"}]},
      "template":"VISITORS_BY_URL"}]},
    "exclusions": {"operator":"or","rules":[{"event_sources":[{"type":"pixel","id":"<PIXEL_ID>"}],
      "retention_seconds":15552000,"filter":{"operator":"and","filters":[{"field":"event","operator":"eq","value":"Purchase"}]},
      "template":"VISITORS_BY_URL"}]}
  }
}
```

## 2. Retargeting ad set inside a CBO campaign with a spend floor
Optimizes for add-to-cart on the pixel; targets only the custom audience; Advantage+ expansion off; `daily_min_spend_target` sets a daily spend floor so campaign budget optimization can't starve a small warm-audience ad set.
```json
{
  "campaign_id": "<CBO_CAMPAIGN_ID>",
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "OFFSITE_CONVERSIONS",
  "promoted_object": {"pixel_id": "<PIXEL_ID>", "custom_event_type": "ADD_TO_CART"},
  "destination_type": "WEBSITE",
  "daily_min_spend_target": <CENTS_PER_DAY>,
  "targeting": {"geo_locations":{"countries":["US"]},
                "custom_audiences":[{"id":"<AUDIENCE_ID>"}],
                "targeting_automation":{"advantage_audience":0}}
}
```

## 3. Diagnosing junk traffic vs. real intent (insights fields)
Ad-level pull that exposed a "lo-fi" blurred creative producing hundreds of clicks and zero carts:
`amount_spent, impressions, clicks, ctr, landing_page_view, omni_add_to_cart, omni_purchase` with `date_preset=maximum`, sorted by spend. Learning-phase status inferred from lifetime `omni_add_to_cart` vs. Meta's ~50-event threshold.

## 4. Go-live pattern
Creatives are immutable, so text/image "edits" are rebuilds. Activation is top-down and non-cascading — campaign → each ad set → each ad — and every edit to a running ad set/creative is a "significant edit" that restarts learning, which is why UX fixes were pushed to the Shopify page side instead.
