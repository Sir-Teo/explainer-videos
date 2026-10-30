# AI, Built — Part 23: Every Sense Is a Token

Part 23 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). How text, sound and pictures become sequences of tokens, how the codes are
learned, how speech is recognized and synthesized, and how pictures and words are matched, from Bell Labs' Audrey
(1952) to the omni models of 2026. A hook, sixteen chapters and an outro, about 55 minutes, in English and Chinese.
Every model in it is trained or run on the CPU that renders the video; every number comes from `compute.py` or a cited
source.

## Outline

* **Hook: one sequence.** Text, a picture and a voice (a held-out Kokoro voice's log-mel spectrogram) become one
  stream of tokens; the questions of the part; objectives.
* **1. How we got here.** Four threads on one time axis: listening (Audrey 1952, time warping, HMMs, CTC, deep
  acoustic models, Deep Speech, wav2vec 2.0, Whisper), speaking (the Voder 1939, formant synthesis, unit selection,
  WaveNet, Tacotron, VALL-E, Qwen3-TTS), text (Shannon's letters, Gage's byte pairs 1994, WordPiece, BPE for
  translation, SentencePiece, byte-level BPE, entropy patches) and pictures (captioning, VQ-VAE, CLIP, Flamingo,
  LLaVA, early fusion), meeting in GPT-4o, Moshi and the Qwen omni models.
* **2. Merges as compression.** Words run out (word types in two million characters of the novels; the share of the
  passage's words never seen); characters make sequences long. Gage's algorithm and Sennrich, Haddow & Birch's BPE,
  replayed on a phrase; why it compresses (a merge found n times saves n symbols; L_k = L_0 − Σ n_i; greedy); the
  length of the text against the number of merges; one sentence at 0 to 8,000 merges; WordPiece's
  likelihood rule and its first merges; vocabulary sizes of GPT-2, Llama 3, GPT-4o, Gemma 3.
* **3. A probability for every cut.** Kudo's unigram language model: P(x) = Σ over cuts Π p(pieces); the lattice of a
  word, the forward algorithm, Viterbi, expected counts; training by EM and pruning, replayed (bits per character as
  the vocabulary shrinks); BPE and the unigram model side by side; sampled cuts (subword regularization);
  SentencePiece.
* **4. What a token is worth.** Bits per character = bits per token / characters per token, derived; five tokenizers
  (bytes; BPE and unigram at 1,024 and 4,096 pieces), the same small transformer (explainer.lm.pocket), the same FLOPs,
  three seeds: learning curves against compute, bits per character on the scoreboard's passage with the spread; why
  vocabulary size trades text per FLOP against the output layer; samples from two of the models.
* **5. Bytes and patches.** Tokenizer failure modes; UTF-8 and GPT-2's byte-level BPE; the series' own byte-level
  BPE (explainer/ai/novels.py) on the passage; ByT5, MegaByte, the Byte Latent Transformer; our byte model's next-byte
  entropy along a line of the passage, a threshold, the patches; the share of surprise on a patch's first byte against
  BPE's token starts, at equal average length.
* **6. Learning a codebook.** k-means codebooks of 4 × 4 letter patches; the straight-through estimator, the codebook
  and commitment losses (VQ-VAE); dead codes; a VQ autoencoder trained three ways (plain, EMA, EMA with data
  initialization and dead-code restarts), three seeds: codes in use through training, the usage histogram, perplexity
  and error.
* **7. Codes without a codebook.** FSQ (bound, round, a fixed grid of Π L_i codes), LFQ (signs, 2^d codes, the entropy
  term); all five quantizers at 256 codes, three seeds; residual stages against one codebook at equal bits.
* **8. Sampling sound.** Aliasing derived (cos(2π(f + k f_s)n/f_s) = cos(2πfn/f_s); evenness), the sampling theorem;
  tones sampled at 8 kHz and their measured spectral peaks; the folding curve; speech decimated with and without a
  filter; the STFT, Slaney's mel filters, Whisper's log-mel front end, our implementation checked against transformers'.
* **9. Neural codecs.** From PCM to SoundStream and EnCodec (residual VQ, quantizer dropout); our codec, a small
  cousin that codes Whisper's log-mel picture instead of the wave (a strided convolution to 50 frames a second, 8
  stages × 256 codes, quantizer dropout, EMA codebooks with restarts; turning the picture back into sound would need a
  vocoder, the expensive part), trained on Kokoro speech, its training replayed on a held-out voice; spectrograms and
  Whisper's word error rate, reading the rebuilt pictures directly, at 400 to 3,200 bits a second, two seeds; semantic and acoustic tokens (AudioLM, Mimi, Qwen3-TTS's tokenizer); our stages' perplexities.
* **10. From Audrey to hidden Markov models.** Audrey (Davis, Biddulph & Balashek 1952); a template recognizer of
  our own (one Kokoro voice's digits) on the same voice and eleven others; dynamic time warping (Vintsyuk 1968; Sakoe &
  Chiba 1978) with an alignment path; templates from ten voices on two new ones; HMMs with Gaussian mixtures, the noisy
  channel argmax P(sound|W)P(W); 2012's deep acoustic models.
* **11. Connectionist temporal classification.** The alignment problem; the blank and the collapse map; p(y|x) as a
  sum over paths; the forward recursion on 2L+1 states, derived (Part 7's forward algorithm); a small CTC recognizer
  (seven convolutions, dilated, 20 ms frames) trained on Kokoro digit strings, three seeds, its posteriors replayed through
  training; the lattice's posterior occupancy and best path from the trained network, its total checked against
  PyTorch's CTC loss; word error rates on held-out and training voices; Deep Speech, RNN-T, attention.
* **12. Listening at scale.** wav2vec 2.0 and Whisper; Whisper base.en on the held-out voices: its input, its token
  stream, its word error rates on sentences and digit strings against our CTC model, its mistakes; large-v3, turbo,
  Qwen3-ASR, and how this series' narration is checked and aligned (tools/tts_server.py).
* **13. Speaking.** The source–filter model and formants, the Voder, Klatt, unit selection, HMM synthesis; WaveNet
  (an autoregressive model of samples, μ-law, dilated causal convolutions); Tacotron 2; VALL-E (codec tokens, a
  3-second prompt); Qwen3-TTS, the narrator: its tokenizer (12.5 Hz, 16 codebooks of 2,048, semantic + acoustic), its
  multi-token prediction, and the clip it clones its voice from as its own codes (through `.venv-tts`; skipped
  gracefully without it).
* **14. Matching pictures and words.** Captioning and CLIP; our letters-and-captions model; InfoNCE as a lower bound on
  the mutual information, derived from the optimal critic (Part 24 derives it another way); the estimate against log N
  at batch sizes 16, 64, 256; training replayed; zero-shot retrieval of captions never seen in training; SigLIP's
  sigmoid loss against CLIP's softmax at three batch sizes, equal pairs, three seeds.
* **15. Models that see.** Flamingo, BLIP-2, LLaVA (connectors); resolution (our CLIP reading shrunken letters) and
  Qwen2-VL's dynamic resolution (token counts from the published rule); M-RoPE position ids, computed; Qwen2.5-VL and
  Qwen3-VL; early fusion (Chameleon, Qwen3.5).
* **16. Every sense at once.** Cascades and GPT-4o; full duplex (Moshi: two streams, the inner monologue); Thinker and
  Talker (Qwen2.5-Omni, Qwen3-Omni, Qwen3.5-Omni), PersonaPlex; tokens a second for each sense.
* **Outro.** Recap tiles from this part's results, where it comes back, six problems, next time (Part 24),
  references.

## Running it

```
python tools/make.py ai23                         # compute, then the narrated cut in English and Chinese
python -m videos.ai.ai23.compute                  # just the numbers (Part 1's novels, Part 21's letters)
python -m videos.ai.ai23.compute --force codec    # recompute one item
AI23_SCALE=0.05 python -m videos.ai.ai23.compute  # a smoke test of every code path, into .cache/ai23_quick/
python tools/build.py ai23 -q l                   # a 480p preview
```

The computation takes about two and a half hours on a busy 4-core machine, on one torch thread (`AI23_THREADS`). It
is seeded throughout and resumable: synthesized speech is saved voice by voice (`.cache/ai23/speech/`), the language
models checkpoint every 100 steps and the codec every 500, and every item made of several runs saves each run as it
finishes. It needs Kokoro-82M (a dependency of the repo; the eleven extra voices, about 0.5 MB each, download on first
use) and Whisper base.en (about 290 MB, downloaded by `transformers` on first use). The narrator's codes need
`.venv-tts` with `qwen_tts` and the Qwen3-TTS-12Hz-1.7B-Base model in the Hugging Face cache; without them the item
records that they are missing and the chapter says so. `AI23_NARRATOR_GENERATE=0` skips having the narrator speak a
new sentence (the slowest step on a CPU, about ten minutes).

## Results on this machine

(filled in from `.cache/ai23/`; see the report at the end of the computation)

## References

**Books.** D. Jurafsky & J. H. Martin, *Speech and Language Processing*, 3rd ed. draft (tokenization, ASR, TTS);
L. Rabiner & B.-H. Juang, *Fundamentals of Speech Recognition* (1993); P. Taylor, *Text-to-Speech Synthesis* (2009).

**Text.** P. Gage, "A New Algorithm for Data Compression", *C Users Journal* (1994); M. Schuster & K. Nakajima,
"Japanese and Korean Voice Search" (ICASSP 2012); R. Sennrich, B. Haddow & A. Birch, "Neural Machine Translation of
Rare Words with Subword Units" (ACL 2016); T. Kudo, "Subword Regularization" (ACL 2018); T. Kudo & J. Richardson,
"SentencePiece" (EMNLP 2018); A. Radford et al., "Language Models are Unsupervised Multitask Learners" (GPT-2, 2019);
L. Xue et al., "ByT5" (2021); L. Yu et al., "MegaByte" (2023); A. Pagnoni et al., "Byte Latent Transformer: Patches
Scale Better Than Tokens" (arXiv 2412.09871, 2024); Llama 3 (Meta, 2024), Gemma 3 (Google, 2025) vocabulary sizes from
their reports.

**Codebooks.** A. van den Oord, O. Vinyals & K. Kavukcuoglu, "Neural Discrete Representation Learning" (VQ-VAE, 2017);
A. Razavi, A. van den Oord & O. Vinyals, VQ-VAE-2 (2019); F. Mentzer, D. Minnen, E. Agustsson & M. Tschannen, "Finite
Scalar Quantization" (2023); L. Yu et al., "Language Model Beats Diffusion: Tokenizer is Key to Visual Generation"
(MAGVIT-v2, LFQ, 2023).

**Sound.** H. Nyquist (1928); C. E. Shannon, "Communication in the Presence of Noise" (1949); N. Zeghidour et al.,
"SoundStream" (2021); A. Défossez et al., "High Fidelity Neural Audio Compression" (EnCodec, 2022); Z. Borsos et al.,
"AudioLM" (2022); A. Défossez et al., "Moshi: a speech-text foundation model for real-time dialogue" (arXiv 2410.00037,
2024; Mimi: 24 kHz, 12.5 Hz, 8 codebooks of 2,048, 1.1 kbps, WavLM distilled into the first; 160/200 ms).

**Recognition.** K. H. Davis, R. Biddulph & S. Balashek, "Automatic Recognition of Spoken Digits", *JASA* 24, 637
(1952); T. Vintsyuk (1968); H. Sakoe & S. Chiba (1978); J. Baker, "The DRAGON System" (1975); F. Jelinek (1976);
L. Rabiner, "A Tutorial on Hidden Markov Models" (1989); G. Hinton et al., "Deep Neural Networks for Acoustic Modeling
in Speech Recognition" (2012); A. Graves, S. Fernández, F. Gomez & J. Schmidhuber, "Connectionist Temporal
Classification" (ICML 2006); A. Hannun et al., "Deep Speech" (2014); A. Baevski et al., "wav2vec 2.0" (2020);
A. Radford et al., "Robust Speech Recognition via Large-Scale Weak Supervision" (Whisper, 2022); Qwen Team, "Qwen3-ASR
Technical Report" (arXiv 2601.21337, 2026).

**Synthesis.** H. Dudley, the Voder (1939); D. Klatt, "Software for a Cascade/Parallel Formant Synthesizer" (1980);
A. Hunt & A. Black, "Unit Selection in a Concatenative Speech Synthesis System" (1996); A. van den Oord et al.,
"WaveNet" (2016); J. Shen et al., "Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions"
(Tacotron 2, 2017); C. Wang et al., "Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers" (VALL-E,
2023); Qwen Team, "Qwen3-TTS Technical Report" (arXiv 2601.15621, 2026: 12.5 Hz, 16 codebooks of 2,048, WavLM-taught
semantic codebook, MTP, 97/101 ms first packet, over 5 million hours, 10 languages); G. E. Peterson & H. L. Barney
(1952), the formants drawn.

**Pictures and words.** O. Vinyals et al., "Show and Tell" (2015); A. Radford et al., "Learning Transferable Visual
Models From Natural Language Supervision" (CLIP, 2021); X. Zhai et al., "Sigmoid Loss for Language Image
Pre-Training" (SigLIP, 2023); M. Tschannen et al., SigLIP 2 (2025); J.-B. Alayrac et al., "Flamingo" (2022); J. Li et
al., "BLIP-2" (2023); H. Liu, C. Li, Q. Wu & Y. J. Lee, "Visual Instruction Tuning" (LLaVA, 2023); P. Wang et al.,
"Qwen2-VL" (2024; dynamic resolution: transformers' `smart_resize`, copied); Qwen Team, Qwen2.5-VL (2025), Qwen3-VL
(arXiv 2511.21631, 2025); Chameleon Team, "Chameleon" (2024); Qwen3.5-397B-A17B model card (February 2026).

**Omni.** OpenAI, "Hello GPT-4o" (May 2024: 232 ms minimum, 320 ms average audio response); OpenAI, "Introducing
gpt-realtime" (August 2025); Qwen Team, Qwen2.5-Omni (2025), "Qwen3-Omni Technical Report" (arXiv 2509.17765, 2025:
Thinker–Talker MoE, 234 ms, 119/19/10 languages, Apache 2.0; the Talker no longer reads the Thinker's text
representations), "Qwen3.5-Omni Technical Report" (arXiv 2604.15804, 2026); R. Roy et al., "PersonaPlex" (arXiv
2602.06053, 2026).

## Problems

1. Show that a BPE merge of a pair found n times (without overlaps) shortens the text by exactly n symbols. In
   "aaaa", how often does the pair (a, a) occur, and how many merges does it allow?
2. One model pays 9.6 bits per token with 3.2 characters a token; another pays 2.9 bits per byte on plain bytes.
   Which is better per character? Show that per-character perplexity is per-token perplexity to the power
   1/(characters per token).
3. How many codes do FSQ levels (8, 5, 5, 5) give, and how many bits? What bitrate do 8 residual stages of 1,024 codes
   give at 75 frames a second?
4. Show that cos(2πft) and cos(2π(f_s − f)t) agree at every t = n/f_s. Sampled at 16 kHz, where does a 9 kHz tone
   appear?
5. List every path of T = 3 frames over {a, b, ∅} that collapses to "ab", and check the count with the forward
   recursion. Why must every path for "aa" contain a blank?
6. Show that f*(x, y) = log p(y | x)/p(y) minimizes InfoNCE, and that log N − L ≤ log N for any critic. How much
   information can a batch of 256 certify?

## Solutions

**1.** Replacing one occurrence of (a, b) by the single symbol ab turns two symbols into one, so n separate occurrences
save n symbols. In "aaaa" the pair (a, a) sits at three overlapping positions, but merging left to right gives
"aa aa": two merges, saving two symbols, not three. That is why `learn_bpe` here records the actual savings next to the
(overlapping) pair counts it ranks by, and checks that the merged text's length equals L₀ minus the savings.

**2.** The first: 9.6 / 3.2 = 3.0 bits per character. The second: on ASCII text a byte is a character, so 2.9 bits
per character; it is better. Perplexity per character is 2^(bits per character) = 2^(bits per token / characters per
token) = (2^(bits per token))^(1/characters per token).

**3.** 8 · 5 · 5 · 5 = 1,000 codes, log₂ 1000 ≈ 9.97 bits. 8 stages × log₂ 1024 = 10 bits × 75 frames/s = 6,000
bits/s: EnCodec's 6 kbps setting.

**4.** At t = n/f_s, cos(2π(f_s − f)n/f_s) = cos(2πn − 2πfn/f_s) = cos(2πfn/f_s), by periodicity and evenness. At
16 kHz the Nyquist frequency is 8 kHz, and 9 kHz folds to 16 − 9 = 7 kHz.

**5.** aab, abb, ∅ab, a∅b, ab∅: five paths. With all probabilities 1 the recursion counts paths: on the states
(∅, a, ∅, b, ∅), α₁ = (1, 1, 0, 0, 0); α₂ = (1, 2, 1, 1, 0) (b may be reached from a, skipping the blank, since b ≠ a);
α₃(b) = α₂(b) + α₂(∅) + α₂(a) = 1 + 1 + 2 = 4 and α₃(final ∅) = α₂(final ∅) + α₂(b) = 0 + 1 = 1; total 5. For "aa",
two adjacent a's merge into one, so the skip from the first a to the second is forbidden: every path passes through
the blank between them.

**6.** The loss is the cross-entropy of guessing which of the N captions is the partner. Given x and the N captions,
the true posterior that slot k holds the partner is p(y_k | x) Π_{j≠k} p(y_j) divided by its sum over k, that is,
[p(y_k | x)/p(y_k)] / Σ_l [p(y_l | x)/p(y_l)], a softmax of f* = log p(y | x)/p(y) (plus anything depending on x
alone). A cross-entropy is smallest at the true posterior, so f* is optimal for every N. A cross-entropy of a discrete
guess is never negative, so log N − L ≤ log N. With N = 256 the most it can certify is log 256 ≈ 5.55 nats = 8 bits.

## 习题

1. 证明：一个出现n次（互不重叠）的字节对，合并一次能让文本恰好缩短n个符号。在“aaaa”里，字节对(a, a)出现几次？能合并几次？
2. 一个模型每个词元花9.6比特，平均每个词元3.2个字符；另一个直接读字节，每字节2.9比特。按每字符算哪个更好？证明每字符困惑度等于每词元困惑度的（1/每词元字符数）次方。
3. FSQ的等级取(8, 5, 5, 5)，一共有多少个码，几比特？8级残差量化、每级1024个码、每秒75帧，码率是多少？
4. 证明cos(2πft)和cos(2π(f_s − f)t)在每个t = n/f_s上取值相同。以16 kHz采样时，9 kHz的音调会出现在哪里？
5. 列出在{a, b, ∅}上长为T = 3、折叠后得到“ab”的所有路径，并用前向递推核对数目。为什么“aa”的每条路径都必须经过一个空白符？
6. 证明f*(x, y) = log p(y | x)/p(y)使InfoNCE最小，并证明对任何打分函数都有log N − L ≤ log N。一个256的批次最多能证实多少信息？

## 解答

**1.** 把一次(a, b)换成一个符号ab，两个符号变成一个，所以n次互不重叠的出现省下n个符号。“aaaa”里(a, a)出现在三个互相重叠的位置，但从左到右合并得到“aa aa”：两次合并，省两个符号，而不是三个。所以这里的`learn_bpe`在用来排序的（含重叠的）字节对计数旁边，还记下实际省下的符号数，并核对合并后的文本长度正好等于L₀减去省下的总数。

**2.** 第一个：9.6 / 3.2 = 每字符3.0比特。第二个：ASCII文本里一个字节就是一个字符，所以每字符2.9比特，它更好。每字符困惑度是2的（每字符比特数）次方，等于2的（每词元比特数 / 每词元字符数）次方，也就是每词元困惑度的（1/每词元字符数）次方。

**3.** 8 · 5 · 5 · 5 = 1000个码，log₂ 1000 ≈ 9.97比特。8级 × log₂ 1024 = 10比特，乘以每秒75帧，是每秒6000比特：正是EnCodec的6 kbps档。

**4.** 在t = n/f_s处，cos(2π(f_s − f)n/f_s) = cos(2πn − 2πfn/f_s) = cos(2πfn/f_s)，用到余弦的周期性和偶性。16 kHz采样的奈奎斯特频率是8 kHz，9 kHz会折叠到16 − 9 = 7 kHz。

**5.** aab，abb，∅ab，a∅b，ab∅：共五条。把所有概率都取1，递推就在数路径：在状态(∅, a, ∅, b, ∅)上，α₁ = (1, 1, 0, 0, 0)；α₂ = (1, 2, 1, 1, 0)（b可以跳过空白、直接从a到达，因为b ≠ a）；α₃(b) = α₂(b) + α₂(∅) + α₂(a) = 1 + 1 + 2 = 4，α₃(末尾∅) = α₂(末尾∅) + α₂(b) = 0 + 1 = 1；合计5。对“aa”，相邻的两个a会合并成一个，所以不允许从第一个a跳到第二个a：每条路径都要经过它们之间的空白符。

**6.** 这个损失是猜N个说明里哪一个是配对的交叉熵。给定x和N个说明，第k个位置是配对的真实后验概率，正比于p(y_k | x) Π_{j≠k} p(y_j)，即[p(y_k | x)/p(y_k)] / Σ_l [p(y_l | x)/p(y_l)]，正是f* = log p(y | x)/p(y)（再加任何只依赖x的项）的softmax。交叉熵在真实后验处最小，所以f*对任何N都是最优的。离散猜测的交叉熵永远不为负，所以log N − L ≤ log N。N = 256时，最多能证实log 256 ≈ 5.55奈特，即8比特。

## Glossary (new terms in this part)

| English | 中文 |
|---|---|
| byte-pair encoding (BPE), merge | 字节对编码（BPE），合并 |
| word type, out-of-vocabulary word | 词型，未登录词 |
| WordPiece | WordPiece |
| unigram language model (tokenizer) | 一元语言模型（分词器） |
| cut (segmentation) of a word, lattice | 切分，格（网格） |
| subword regularization, SentencePiece | 子词正则化，SentencePiece |
| byte-level BPE, UTF-8 | 字节级BPE，UTF-8 |
| tokenizer-free model, patch, entropy patching | 无分词器模型，块，按熵分块 |
| Byte Latent Transformer (BLT) | 字节潜变量Transformer（BLT） |
| codebook, dead code, codebook collapse | 码本，死码，码本坍缩 |
| straight-through estimator, stop-gradient | 直通估计器，停止梯度 |
| codebook loss, commitment loss | 码本损失，承诺损失 |
| exponential moving average (EMA) codebook | 指数移动平均（EMA）码本 |
| dead-code restart | 死码重启 |
| finite scalar quantization (FSQ) | 有限标量量化（FSQ） |
| lookup-free quantization (LFQ), entropy term | 免查表量化（LFQ），熵项 |
| residual vector quantization (RVQ), stage | 残差向量量化（RVQ），级 |
| quantizer dropout | 量化器丢弃 |
| sampling rate, Nyquist frequency, sampling theorem | 采样率，奈奎斯特频率，采样定理 |
| aliasing, anti-aliasing filter, decimation | 混叠，抗混叠滤波器，抽取（降采样） |
| short-time Fourier transform (STFT), spectrogram | 短时傅里叶变换（STFT），频谱图 |
| mel scale, mel filterbank, log-mel spectrogram | 梅尔刻度，梅尔滤波器组，对数梅尔频谱 |
| neural audio codec, bitrate (kbps) | 神经音频编解码器，码率（kbps） |
| semantic tokens, acoustic tokens | 语义词元，声学词元 |
| template matching, dynamic time warping (DTW) | 模板匹配，动态时间规整（DTW） |
| acoustic model, Gaussian mixture | 声学模型，高斯混合 |
| word error rate (WER) | 词错误率（WER） |
| connectionist temporal classification (CTC), blank | 连接时序分类（CTC），空白符 |
| collapse map, alignment, posterior occupancy | 折叠映射，对齐，后验占有率 |
| RNN transducer, listen-attend-spell | RNN转录器，听-注意-拼写 |
| weak supervision | 弱监督 |
| forced aligner | 强制对齐器 |
| source–filter model, formant | 源-滤波器模型，共振峰 |
| formant synthesis, unit selection, statistical parametric synthesis | 共振峰合成，单元选择，统计参数合成 |
| vocoder, μ-law | 声码器，μ律 |
| dilated causal convolution | 扩张因果卷积 |
| codec language model, voice cloning | 编解码器语言模型，声音克隆 |
| multi-token prediction (MTP), first-packet latency | 多词元预测（MTP），首包延迟 |
| critic, density ratio | 打分函数（评判函数），密度比 |
| zero-shot retrieval | 零样本检索 |
| sigmoid loss (SigLIP) | sigmoid损失（SigLIP） |
| vision-language model, connector, Perceiver resampler, Q-Former | 视觉语言模型，连接器，感知重采样器，Q-Former |
| dynamic resolution, M-RoPE | 动态分辨率，多模态旋转位置编码（M-RoPE） |
| early fusion | 早期融合 |
| cascade, full duplex, inner monologue | 级联，全双工，内心独白 |
| Thinker, Talker | 思考者（Thinker），说话者（Talker） |
