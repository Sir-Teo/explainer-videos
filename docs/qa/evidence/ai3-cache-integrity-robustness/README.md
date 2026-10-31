# Cache sidecar type and transitive-lineage regressions

Two independent source-review findings are repaired. Non-object sidecars and legacy evidence now return
not-current, including JSON null, empty/nonempty arrays, strings, numbers and booleans. Cached-only QA reports
stale data, never runs a producer and leaves malformed sidecars and numerical payloads unchanged.

Power now requires the Letters cache itself to be current, as well as matching its payload hashes. A fixture
changes only the upstream bigram bytes, leaving every Letters/Power payload untouched: both become stale.
Current validation is serialized under the existing nested item locks; no numerical generator changes.

All22 focused cache tests and all238 repository tests pass (2.156seconds and27.567seconds respectively). After
the repair, actual loads of all17 completed items succeeded with producers replaced by fail-on-call functions.
All26 production numerical payload hashes, sizes and modification times still match the preserved pre-upgrade
receipt. No production computation, payload rewrite or sidecar re-attestation was needed.

These checks preserve the original limits: later legacy attestation does not establish historical consumed-input
provenance, and selected-image, rendered, production and listening approval remain separate. The manifest binds
actual logs, frozen validator/tests and the read-only preservation receipt.
