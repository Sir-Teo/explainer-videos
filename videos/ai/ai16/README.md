# AI, Built — Part 16: Every Sense Is a Token

Part 16 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). How text,
pictures and sound become tokens for one model, and how pictures and words are matched. A hook and five chapters:

* **One sequence.** Text, a picture and a voice turned into one stream of tokens.
* **Cutting text into tokens.** Byte-pair encoding learned on two million characters of the novels: the first
  merges; one sentence at 0, 500, 2,000 and 8,000 merges; characters per token on the passage.
* **Codebooks.** 4 × 4 patches of letter pictures quantized by codebooks of 16, 64 and 256 codes (k-means); residual
  quantization in four stages of 16; finite scalar quantization.
* **Sound as tokens.** A synthesized voice saying five vowels (pulses through Peterson and Barney's formants); its
  spectrogram; the frames as residual-quantized codes, and the spectrogram rebuilt from them.
* **Matching senses.** A small contrastive model pairing letter pictures with captions such as "bold serif A",
  trained with CLIP's softmax loss and SigLIP's sigmoid loss.
* **One model, every sense.** A thinker and a talker (Qwen's omni models); full-duplex speech (Moshi).
* **Recap**, where it comes back, Part 17's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai16.compute          # needs Part 1's books
python tools/build.py ai16                # English
python tools/build.py ai16 --lang zh      # Chinese
```

References: Gage (1994); Sennrich, Haddow & Birch (2016); van den Oord et al., VQ-VAE (2017); Mentzer et al., FSQ
(2023); Zeghidour et al., SoundStream (2021); Défossez et al., EnCodec (2022) and Moshi (2024); Radford et al., CLIP
(2021); Zhai et al., SigLIP (2023); Peterson & Barney (1952); Qwen Team, Qwen2.5-Omni and Qwen3-Omni (2025).
