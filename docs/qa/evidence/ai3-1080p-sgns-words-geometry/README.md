# Native 1080p endpoints: SGNS, Words and Geometry

All **113 captured endpoint images** were actually inspected at their native **1920×1080** resolution. No substantive clipping, collision, unreadable critical caption or incorrect displayed result was found. One minor optional Chinese punctuation wrap remains recorded below.

| Scene | EN captures viewed | ZH captures viewed | Recorded runtime outcome |
|---|---:|---:|---|
| SGNS | 23/23 | 22/22 | EN `needs-review`: source changed during render; ZH passed, no warnings |
| Words | 18/18 | 18/18 | Both passed, no warnings |
| Geometry | 16/16 | 16/16 | Both passed, no warnings |

Every target was absent at reconciliation, so no earlier capture was overwritten or relabelled. Six commands ran serially through the cached-only wrapper, with `nice -n 10` and all five recorded numeric-thread environment variables set to one. The wrapper selects 1920×1080, nominal 30fps configuration, skips animations and uses silent placeholders. Commands and exit codes are preserved in [capture-receipt.json.gz](ledgers/capture-receipt.json.gz); the exact wrapper and orchestration source are included. A warning-bearing completed capture is retained as `needs-review`, not converted into a runtime pass.

SGNS checks covered objective and colour roles, history card, measured replay snapshots **0 / 36 / 1,089 / 10,890**, complete derivation and empirical-distribution qualifier, dimension/error panels, omitted-point notes, diagnostic cohort/sample distinction, comparison table and final handoff. The repaired 36- and 1,089-update lists fit at native resolution. Representative captures: [EN 36 updates](images/en-SGNS-006.png), [EN 1,089](images/en-SGNS-007.png), [EN full derivation](images/en-SGNS-013.png), [EN error panels](images/en-SGNS-016.png), [ZH 36](images/zh-SGNS-006.png), [ZH 1,089](images/zh-SGNS-007.png), [ZH full derivation](images/zh-SGNS-012.png).

Words checks covered history cards, the **4.35-million-word** input caption, 300-of-10,000 heatmap, PMI formula and measured examples, smoothed context distribution, dense neighbour columns and similarity bars, rank-threshold qualifiers, analogy labels/arrows and candidate-pool note. Learned English words remain intentionally verbatim in Chinese. Both languages preserve the first-crossing qualification. Representative captures: [EN PMI page](images/en-Words-009.png), [EN neighbour columns](images/en-Words-011.png), [EN analogy](images/en-Words-017.png), [ZH PMI](images/zh-Words-009.png), [ZH neighbours](images/zh-Words-011.png), [ZH analogy](images/zh-Words-017.png).

Geometry checks covered sampled token-ID scope, histogram-window normalization and omitted tails, random-direction scale, raw/centred means, principal-direction bars and ID-colour legend, layer curves, final/peak labels, signed-contribution wording, passage provenance and linear-representation cards. The plot’s measured final/peak layer 12 value **0.94** and layer 6’s dimensions **447, 373, 64**, contributing **64%** of average cosine, match the consumed cache. Representative captures: [EN principal directions](images/en-Geometry-006.png), [EN layers and signed qualifier](images/en-Geometry-010.png), [ZH directions](images/zh-Geometry-006.png), [ZH layers](images/zh-Geometry-010.png).

**Optional polish W1080-01:** the Chinese Words Harris card wraps with a leading comma on its final line: `，意思往往相近`. It remains readable and contained. [Native evidence](images/zh-Words-002.png); the same wrap appears in captures 3 and 4. Parent explicitly retained this in the polish queue; this batch leaves source and captions unchanged. No other substantive native-layout finding was confirmed.

Direct scene SHA256 values, unchanged before capture, after capture and at completion:

| Source | SHA256 |
|---|---|
| `s14_sgns.py` | `bec79fc8bc271484317b002649960bd40eb3d827eb76cbd7a1cf2948541d1673` |
| `s13_words.py` | `97e14f916b8fbd72d5ff1ec35e6ff58a7e4f760e34db3352ae9db7f547036eaf` |
| `s17_geometry.py` | `7d9923cf29cc01dbe96299d569daa7b86abc99fdca9b495c007c18687b481f5a` |

Every consumed JSON/NPZ byte hash and recorded size/mtime signature remained unchanged at completion. Source snapshots, individual frame SHA256 values, native-view timestamps, numerical input hashes, runtime warnings and fingerprints are preserved in the six review ledgers. The only source-bundle overlap during English SGNS capture was the shared caption table: four **Outro-only** footer strings were added (`spectra: separately`, `peak-normalized`, `SGNS: generalized`, `shifted PMI`), with no changed/removed keys. This actual delta is recorded in [completion-review.json.gz](ledgers/completion-review.json.gz). English SGNS retains its conservative warning and stale whole-part fingerprint; the other five fingerprints matched at review completion. Scoped checks do not erase that warning.

The six commands totalled **242.021 seconds**. Their live target folders occupied **33,150,653 bytes**, including TeX assets. Frozen runtime preservation occupied approximately **38.55 MB** before final reporting. Disk free/used snapshots also include concurrent work and are not attributed solely to these six captures. This portable package includes 18 useful native PNGs and compressed ledgers rather than duplicating all 113 images; all originals remain in the frozen runtime capture directories. [manifest.json](manifest.json) records exact original and portable hashes. Verify portable files with `sha256sum -c SHA256SUMS`; inspect a receipt with `gzip -dc ledgers/en-SGNS-review.json.gz`.

These are **native-resolution endpoint captures only**. They do not verify intermediate animation, uninterrupted playback, actual 1080p movie encoding, narrated listening/audio sync, or player/responsive behaviour. Words’ intermediate rank-5/10/25 transitions are outside these captured native endpoints. The earlier [SGNS selected-time motion review](../ai3-sgns-replay-regression/README.md) remains separate evidence at 854×480. No model training, production computation, source/global-caption/STATUS edits, commits or deployment were performed in this batch.
