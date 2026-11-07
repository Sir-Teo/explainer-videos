# Separate school and health programme effects

World declared PROGRAMME_EFFECT twice: 0.20 for tutoring and later -4.0 for community health workers. Python retained the latter, so the schools generator applied -400 score points rather than the intended +20.

The generator and school targets now use SCHOOL_PROGRAMME_EFFECT = 0.20; the ministry trial uses HEALTH_PROGRAMME_EFFECT = -4.0. Direct consumers in Parts 23, 35 and 42 use the appropriate explicit name. School-dependent computations in Parts 23–28 and 35 are refreshed during their chapter reviews.

A seeded counterfactual test removes tutoring while preserving assignment, pupils and SES, and verifies exactly +20 points for each treated pupil. A separate test protects the -4 mm Hg health effect. Both checks and all 12 existing World checks pass (14 total).

The World source change affects the conservative shared-code fingerprint of every part. Parts 1–18 retain their completed source/visual reviews at their recorded commits, but their current capture fingerprints are being refreshed with the same checks before final integration. Those parts do not use the changed school programme block. Parts 19–22 are also recaptured against the new shared source. No old fingerprint is relabeled as current.

Chinese narration/captions, continuous listening and final bilingual production gates remain open.
