# October 9, 2026 YouTube rebuild

Published: [Building a Top-Tier Real-Time Trading System](https://youtu.be/EIN-8aFXXR4), grouped in the channel's **Economics & Markets** playlist. Public playback was verified at 1080p with English captions; YouTube's copyright checks found no issues.

All 16 chapters were rendered from source at 1920×1080, 30 fps, H.264 CRF 18. The build uses the original PCM narration, lossless ALAC intermediates, and a final 48 kHz stereo AAC soundtrack with a 384 kb/s encoding target. The finished master measures −16.01 LUFS integrated and −1.43 dBTP. Its duration is 42:50.701, with 778 English caption cues and 16 chapters.

The committed Nasdaq-derived data and original four-core Intel Xeon benchmark results are preserved. Labels and narration identify the original measured machine rather than attributing those benchmarks to the new render workers.

Source revision: `4e3ab0f0acb78c42bec2116b2dd82f3f1d5933b9`.

Build and validation: [GitHub Actions run 37949634931](https://github.com/Sir-Teo/explainer-videos/actions/runs/37949634931). All scenes rendered successfully; the complete video passed decoding, audio synchronization, caption timing, and chapter checks. Contact sheets were reviewed before upload.

```sh
python tools/build.py trading --crf 18 -j 2
python tools/youtube_qa.py trading
```

## YouTube chapter timestamps

```text
0:00 Two o'clock on Fed day
2:49 Part 1: What a market maker does
5:48 Inside the exchange
9:08 Part 2: The feed, byte by byte
11:39 Rebuilding the order book
13:58 Part 3: Why microseconds matter
16:54 The speed of light
19:57 Inside the box: the latency ladder
22:17 The hot path in software
25:52 Hardware: deciding before the packet ends
28:13 Part 4: Fair value
30:49 Quoting: spread, skew, inventory
32:49 Testing on real queues
35:44 Part 5: Risk, and Knight Capital
38:45 Determinism and the research loop
41:01 The whole machine
```
