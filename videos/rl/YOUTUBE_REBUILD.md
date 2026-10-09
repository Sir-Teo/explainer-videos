# October 9, 2026 YouTube rebuild

This edition renders every chapter from source at 1920×1080, 30 fps, H.264 CRF 18. Narration uses the original Kokoro PCM soundtrack, lossless ALAC intermediates, and a final 48 kHz stereo AAC soundtrack at 384 kb/s, mastered to −16 LUFS with a −1.5 dBTP target. Captions and chapter times come from the new renders.

The adder experiments use PyTorch 2.14.1 on Ubuntu 24.04 CPU runners, 8,000 base pretraining steps, and the source's unchanged 120-step RL schedule with three seeds per algorithm. The longer pretraining schedule learns the intended reliable worked-answer strategy: its held-out accuracy is 99.95%, compared with 59.55% for direct answers. The base model's sampled show-work rate is 25.14% and its overall accuracy is 69.74%.

To recompute the adder footage with those settings:

```sh
RL_BASE_STEPS=8000 RL_THREADS=4 python -m videos.rl.compute gauss cloud simplex kl_est base runs tree tilt passk critic scaling dpo
```

Compute `python -m videos.rl.compute mismatch` in a separate environment pinned to PyTorch 2.6.0 and copy its `.cache/rl/mismatch.json` into the rendering checkout. With all caches present, run `python tools/build.py rl --crf 18 -j 2`.

The algorithm comparison below is averaged over three seeds. The original README documents the original experiment edition; this table records the computations used by this rebuild.

| Algorithm | Held-out accuracy | Answers showing work |
|---|---:|---:|
| REINFORCE, per-answer average | 99.07% | 0.07% |
| REINFORCE, constant normalizer | 99.07% | 32.80% |
| RLOO | 99.07% | 42.70% |
| GRPO | 98.90% | 41.47% |
| Dr. GRPO | 99.07% | 51.37% |
| DAPO-style | 99.30% | 50.87% |
| PPO with critic and GAE | 98.40% | 53.40% |

The fixed-pair DPO experiment starts at 68.8% accuracy, peaks at 76.1%, and ends at 12.9%. The final log-probability changes are −5.02 for preferred answers and −9.01 for rejected answers. The narration and charts use these recomputed values.

The Qwen3-0.6B precision experiment uses PyTorch 2.6.0: eight traces sampled together in bfloat16, up to 768 new tokens each, then rescored in bfloat16 and float32. It keeps the original full measurement. Sampler log probabilities are gathered one token at a time to avoid materializing several multi-gigabyte vocabulary tensors; this produces the same selected-token probabilities.

All scene assertions, full video/audio decoding, caption timing, audio/video sync, and export-format checks must pass before publication.
