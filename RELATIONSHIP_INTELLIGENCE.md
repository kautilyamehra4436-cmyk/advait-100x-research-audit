# Advait Owner-Aligned Relationship Intelligence

## Purpose
The Relationship Intelligence module adapts opportunity ranking to an explicit owner profile. The default profile prioritizes useful relationships, verified needs, phone-first execution, zero spend, and owner control. The owner profile is configuration, not an inferred personality model: update it only from explicit owner instructions.

## Current scope
- Categorizes opportunity descriptions into a transparent work taxonomy.
- Leaves ambiguous or unmatched work as `unknown`.
- Reports frequency by category, top work types, unknown work, ranked opportunities, and suggested next focus.
- Scores opportunities using owner fit, verified need, usefulness, feasibility, and relationship value.
- Requires a source and evidence before assigning a priority score.
- Enforces an avoid-list and validates score weights and rating ranges.

## Defense and privacy
- Offline analysis only; this module does not crawl websites or contact people.
- No automatic messages, public posts, bids, contracts, payment requests, withdrawals, or transfers.
- Do not place phone numbers, email addresses, credentials, bank details, or sensitive personal data in opportunity records. Store source references and minimal evidence descriptions.
- Unknown work is retained for owner review; ambiguous classification is not guessed.
- Scores are explainable ranking signals, not permission to act.
- Owner approval remains mandatory for outreach, work acceptance, pricing, contracts, spending, and financial actions.

## Run tests
```sh
python -m unittest -v tests.test_relationship_intelligence
```

## Example integration
Collect opportunity records from an authorized source, then call `build_opportunity_report(items, owner_profile)`. The report is suitable for a CEO board input. This module itself does not provide a live data feed; an authorized discovery adapter and evidence store are separate pending components.

## Owner profile
`DEFAULT_OWNER_PROFILE` is the starting template. Explicit owner choices may change priority categories and weights. Never infer sensitive traits or silently rewrite the profile based on a single interaction.
