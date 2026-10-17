# Chinese edition of *AI, Built* (人工智能，从零搭建)

Translations live in `videos/ai/aiN/narration_zh.json`, keyed by the English line; check them with
`python tools/translate_narration.py aiN --check`.

- Spoken Mandarin, short sentences; same content and order as the English.
- Keep every `<bookmark mark='x'/>`, in order, before the words it times.
- Full-width punctuation; numbers as digits (4.08 比特, 2260万); Latin letters stay Latin (p, q, H(p), KL, GPT-2).
- Spoken math: 以2为底的对数, p分之1, q减去p帽, 对所有x求和, 至多, 当且仅当.
- Model and product names stay as they are (GPT-2, Qwen3, gzip, xz, bzip2); book titles in 《》 with the English
  title on first mention where it helps (《傲慢与偏见》, 《马耳他之鹰》).
- On-screen text lives in `videos/ai/ai_text_zh.json` (exact `strings`, `phrases` inside `\text{}`, regex
  `patterns`); `python tools/collect_text.py --check aiN` lists what is still English, `--lang zh aiN` dry-runs the
  Chinese build. Text the models read or wrote (the passage, Shannon's sentence, generated samples, tokens) stays in
  English: it is data. Draw such words with `data_text(...)` (from `explainer.ai`), never `Text(...)`: a bare `Text` of a word that happens to be in the table ("yes", "noise", "next") would be translated.

## Glossary

| English | 中文 |
|---|---|
| Claude Shannon | 克劳德·香农 (香农) |
| the guessing game | 猜字游戏 |
| information theory | 信息论 |
| probability distribution | 概率分布 |
| conditional probability | 条件概率 |
| the chain rule | 链式法则 |
| context | 上下文 |
| surprise (surprisal) | 意外度（惊奇度） |
| bit / nat | 比特 / 奈特 |
| entropy | 熵 |
| conditional entropy | 条件熵 |
| redundancy | 冗余 |
| Jensen's inequality | 詹森不等式 |
| concave | 凹函数（向下弯） |
| code, codeword | 编码，码字 |
| fixed-length code | 定长编码 |
| prefix-free code | 无前缀码（前缀码） |
| Kraft's inequality | 克拉夫特不等式 |
| Huffman code | 霍夫曼编码 |
| source coding theorem | 信源编码定理 |
| cross-entropy | 交叉熵 |
| Kullback–Leibler divergence (KL) | KL散度（库尔巴克–莱布勒散度） |
| Gibbs' inequality | 吉布斯不等式 |
| mutual information | 互信息 |
| mode-covering / mode-seeking | 覆盖所有峰 / 只盯一个峰 |
| arithmetic coding | 算术编码 |
| compression, compressor | 压缩，压缩器 |
| counting model (n-gram) | 计数模型（n元模型） |
| smoothing (add-α) | 平滑（加α平滑） |
| overfitting, generalization | 过拟合，泛化 |
| maximum likelihood | 最大似然 |
| likelihood | 似然 |
| logit | logit（打分） |
| softmax | softmax |
| gradient, gradient descent | 梯度，梯度下降 |
| learning rate | 学习率 |
| loss | 损失 |
| token | 词元（token） |
| language model | 语言模型 |
| parameters | 参数 |
| scoreboard | 记分牌 |
| bits per character | 每字符比特数 |
| the passage | 测试段落 |
| power law | 幂律 |
| vector, cosine similarity | 向量，余弦相似度 |
| *The Maltese Falcon* | 《马耳他之鹰》 |
| Project Gutenberg | 古登堡计划 |
