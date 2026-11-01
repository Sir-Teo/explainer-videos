# Byte-preserving silent QA storage recovery

On1November2026 at2026-11-01T05:45:49.043823+00:00, 180 inactive Part1–5 silent-motion WAV files had their aligned zero-byte interior ranges converted to sparse filesystem holes. Physical allocation decreased by **1,644,777,472bytes**; free disk was observed at1,337,757,696before and2,982,375,424after, while unrelated QA jobs continued.

No file was deleted or re-encoded. Every affected file retained its complete SHA256, byte length, inode, device, mode and originalmtime (restored explicitly); filesystemctime changes are recorded rather than represented as unchanged. The full candidate range was read and proved zero before each hole-punch operation, then the complete file was rehashed. Header/tail bytes outside that range were preserved. No candidate was observed open or mapped by visible processes. All306 protected numerical/trained/corpus and Part6cache signatures retained exact hash/size/mtime/mode/inode/device.

Only old `renders/qa/series/ai1` through`ai5` `*_motion` WAV files were eligible. Active Part6renders, generated speech, models, raw input, unique images, movies and original evidence paths were retained. Sparse allocation still reads as the identical original bytes. This is filesystem capacity recovery, not a new silence/audio-quality/listening approval.

The initial private checker failed before any mutation because it assumed a mapping instead of a list for the protection inventory; its log is retained. The corrected run completed with exact-byte assertions. No disk threshold was lowered, credential changed or access restriction bypassed.
