"""Full canonical text-LM QA presentation; consumes accepted results, never computes them."""
from __future__ import annotations

import math
import os
import re
import textwrap

import manimpango
import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import LM_COLORS, TEXT_C, load

# Nominal tokenizer pieces, actual model head, and preserved original update schedule.
LM_SPECS = {
    "bytes256": ("bytes", 256, 256, 1000),
    "bpe1024": ("bpe", 1024, 1025, 835),
    "unigram1024": ("unigram", 1024, 1025, 835),
    "bpe4096": ("bpe", 4096, 4097, 504),
    "unigram4096": ("unigram", 4096, 4097, 504),
}

# Exact static narration pairs are also registered narrowly in narration_zh.json.
NARRATION = {
    "card": (
        "Chapter four. What a token is worth. We compare five original tokenizer configurations at three seeds each. These are newly completed QA candidates, not recovered historical results. The original training schedules are preserved. Their measured work and revised compute estimates differ, so this is a descriptive comparison, not an equal-compute race.",
        "第4章。一个词元值多少。我们比较五种原始分词配置，每种运行三个种子。这些是新完成的QA候选，并非恢复出的历史结果。原始训练步数保持不变，但实测工作量和重新核算的计算量估计并不相同。因此这里只作描述性比较，不是等计算量竞赛。"),
    "units": (
        "Bits per token uses different units for different tokenizers. For a common text suffix, add the negative log probabilities along each tokenizer's canonical token path, then divide by the exact number of Unicode characters in that suffix. Dividing both numerator and denominator by the same number of scored tokens gives bits per token divided by characters per scored token. This is one token path, not a marginal likelihood summed over every possible tokenization.",
        "不同分词器的每词元比特数使用不同单位。对于共同的文本后缀，沿各分词器的规范词元路径累加负对数概率，再除以后缀中精确的Unicode字符数。分子分母同时除以相同的计分词元数，就得到每词元比特数除以每计分词元的字符数。这里只计一条词元路径，不是对所有可能切法求和后的边际似然。"),
    "targets": (
        "The scored passage suffix is identical across all five tokenizers. A shared prefix ends at a token boundary for every encoding and at a strict UTF-8 boundary. That prefix conditions the predictions but is excluded from the score. These rows show the actual number of scored tokens at seed zero. The numerical conversion uses the four-thousand-and-ninety-six-piece BPE model and exactly this same suffix.",
        "五种分词器计分的段落后缀完全相同。共同前缀的终点既是每种编码的词元边界，也是严格的UTF-8边界。前缀用于提供预测条件，但不计入分数。表中列出种子零实际计分的词元数。数值换算使用4096片段的BPE模型，而且始终使用同一个后缀。"),
    "schedule": (
        "The Transformer body has three layers, width ninety-six and a context of one hundred and twenty-eight tokens. Embeddings, output heads and total parameter counts differ. Subword heads contain one additional unknown-token class beyond their nominal pieces. The unknown counts here describe the encoded full training corpus, not how many unknown targets were encountered during the sampled updates. Original lossy training encodings are preserved.",
        "Transformer主体有三层，宽度为九十六，上下文为一百二十八个词元。但嵌入、输出头和总参数量不同。子词模型的输出头比名义片段数多一个未知词元类别。这里的未知计数描述编码后的完整训练语料，不是在抽样更新中实际遇到的未知目标次数。原始有损训练编码保持不变。"),
    "work": (
        "Completed updates determine the number of training target tokens. We also tally the original source bytes covered by the sampled target windows, counting repeated exposures again. This is neither a unique-coverage count nor a passage-density estimate of characters read. CPU and wall times are measured around the training loop and include validation and checkpoint overhead. Each entry shows the three-seed mean and recorded range.",
        "已完成的更新次数决定训练目标词元数。我们还按实际抽样目标窗口累计其覆盖的原文源字节，重复接触的内容重复计数。这既不是不重复覆盖量，也不是用段落词元密度推算的字符阅读量。CPU时间和墙钟时间在训练循环外测量，包含验证和检查点开销。各项显示三个种子的均值和实际范围。"),
    "compute": (
        "These are estimates of matrix operations, not measured hardware FLOPs or CPU seconds. The triangular and dense attention conventions give different estimates while keeping the same completed original update schedules. They exclude normalization, rotary position operations, softmax, optimizer work, validation and kernel overhead. The displayed cost per token comes directly from the accepted estimator, not from dividing a reference budget by rounded steps.",
        "这些是矩阵运算量的估计，不是实测硬件FLOP，也不是CPU秒数。在保持原始已完成训练步数不变时，三角注意力和稠密注意力两种口径给出不同估计。它们不包含归一化、旋转位置运算、softmax、优化器、验证和内核开销。每词元代价直接来自通过验收的估计器，而不是参考预算除以取整步数。"),
    "curves": (
        "All fifteen learning curves are shown, including every recorded finite validation point. The horizontal axis uses the triangular matrix-operation estimate. The vertical axis is a diagnostic proxy: sampled validation bits per token divided by the validation corpus's average characters per token. The windows differ across tokenizers. These curves are not exact common-suffix character scores, and their range is chosen from all displayed data rather than clipping high values.",
        "这里画出全部十五条学习曲线，包括每一个记录下来的有限验证点。横轴使用三角矩阵运算量估计。纵轴只是诊断性近似：抽样验证每词元比特数，再除以验证语料的平均每词元字符数。不同分词器使用的窗口不同。这些曲线不是共同后缀的精确每字符分数，坐标范围来自全部显示数据，不截掉较高的数值。"),
    "scores": (
        "Final scores use exact common suffixes for both the passage and the full validation text. Every row shows the mean and observed minimum to maximum over seeds zero, one and two. A lower recorded score describes this cohort and these runs. Three-seed ranges are not confidence intervals or a significance test. Different vocabulary sizes, initializations, sampled windows and compute prevent an isolated causal claim about the tokenizer.",
        "最终分数分别使用段落和完整验证文本的精确共同后缀。每行显示种子零、一、二的均值和实际最小至最大值。较低的记录分数只描述这组文本与这些训练。三个种子的范围不是置信区间，也不是显著性检验。词表大小、初始化、抽样窗口和计算量均不同，不能据此单独归因于分词器。"),
    "why": (
        "Tokenization changes the sequence length, the text represented in a fixed token window, the model's embedding and output size, and the distribution of training targets. Those effects interact. These original-schedule runs do not isolate them. The separately studied lossless UTF-8 fallback candidate is outside these fifteen canonical cases. Keep the measured outcomes, diagnostic proxies and scientific limitations together.",
        "分词改变序列长度、固定词元窗口中所表示的文本、模型嵌入与输出头大小，以及训练目标的分布。这些作用彼此影响。按原始步数完成的这些训练没有把它们逐一分离。另行研究的无损UTF-8回退候选不属于这里十五个规范案例。实测结果、诊断性近似和科学限制需要一起看。"),
    "sample_bytes": (
        "This byte-model example uses seed zero at temperature zero point eight. The prompt is the model's first eight passage tokens; the displayed generated text is a continuation only, appended once. The excerpt is illustrative, not a generation-quality benchmark. Byte output is decoded as UTF-8 with replacement, so a replacement character is a decoding result, not the model's unknown-token class.",
        "这个字节模型例子使用种子零，温度为零点八。提示是该模型在段落开头的八个词元；显示的生成文本仅为续写，只接在提示后一次。这个摘录仅作示例，不是生成质量基准。字节输出按UTF-8解码并允许替换字符，因此替换字符是解码结果，不是模型的未知词元类别。"),
    "sample_bpe": (
        "This BPE example also uses seed zero and temperature zero point eight, but eight BPE prompt tokens cover different text from eight byte tokens. The prompts are not matched. Subword output uses the original decoder, which displays an unknown class as a question mark. Prompt and continuation are shown separately so the prompt cannot be duplicated. Truncated excerpts are marked, while the accepted output remains unchanged.",
        "这个BPE例子同样使用种子零和零点八的温度，但八个BPE提示词元覆盖的文本与八个字节词元不同，提示并不匹配。子词输出保留原始解码器，用问号显示未知类别。提示与续写分开显示，避免重复提示。截短的摘录会标明，而通过验收的原始输出保持不变。"),
}


def accepted_lm_data(data=None):
    """Explicit QA provider only: this namespace has no canonical training producer.

    Missing providers fail instead of regenerating original ``lms`` dependencies.
    The render harness must bind this key to the independently accepted summary.
    """
    d = load("lms_qa_original_schedule") if data is None else data
    if not isinstance(d, dict) or d.get("numerical_acceptance", {}).get("status") != "passed":
        raise ValueError("Bits requires an independently accepted full canonical summary")

    def integer(v, name, minimum=0):
        if isinstance(v, bool) or not isinstance(v, (int, np.integer)) or v < minimum:
            raise ValueError(f"{name}: invalid integer")
        return int(v)

    def number(v, name, positive=False):
        if isinstance(v, bool) or not isinstance(v, (int, float, np.number)) or not math.isfinite(float(v)):
            raise ValueError(f"{name}: nonfinite/non-numeric value")
        if float(v) < 0 or (positive and float(v) <= 0):
            raise ValueError(f"{name}: invalid sign")
        return float(v)

    def finite_tree(v):
        if isinstance(v, dict):
            for item in v.values():
                finite_tree(item)
        elif isinstance(v, (list, tuple)):
            for item in v:
                finite_tree(item)
        elif isinstance(v, (int, float, np.number)) and not isinstance(v, bool):
            if not math.isfinite(float(v)):
                raise ValueError("Bits summary contains a nonfinite numeric value")

    finite_tree(d)
    prefixes = d["common_prefix"]
    for split in ("passage", "valid"):
        p = prefixes[split]
        integer(p["bytes"], split + " prefix bytes", 1)
        integer(p["characters"], split + " prefix characters", 1)
        integer(p["suffix_characters"], split + " suffix characters", 1)
        if p["characters"] > p["bytes"] or not re.fullmatch(r"[0-9a-f]{64}", p["suffix_sha256"]):
            raise ValueError("Invalid shared suffix identity")
    rows = d["runs"]
    expected = {f"{encoding}_s{s}" for encoding in LM_SPECS for s in range(3)}
    if not isinstance(rows, list) or len(rows) != 15 or {r["name"] for r in rows} != expected:
        raise ValueError("Bits requires exactly five canonical encodings × three seeds")
    for r in rows:
        encoding, seed_text = r["name"].rsplit("_s", 1)
        seed = int(seed_text)
        kind, size, vocab, steps = LM_SPECS[encoding]
        cfg = r["cfg"]
        expected_cfg = dict(encoding=encoding, kind=kind, size=size, vocab=vocab, steps=steps, seed=seed)
        if any(cfg.get(k) != v for k, v in expected_cfg.items()):
            raise ValueError(f"{r['name']}: encoding/head/schedule mismatch")
        for key in ("size", "vocab", "steps", "seed"):
            integer(cfg[key], "configuration " + key)
        if integer(r["seed"], "seed") != seed or integer(r["vocab"], "vocab", 1) != vocab:
            raise ValueError("Run identity differs from configuration")
        if integer(r["executed_steps"], "executed steps", 1) != steps:
            raise ValueError("Bits refuses an incomplete original schedule")
        if integer(r["training_tokens"], "training targets", 1) != steps * 16 * 128:
            raise ValueError("Training-target count differs from completed updates")
        for key in ("total_params", "training_target_source_bytes"):
            integer(r[key], key, 1)
        if r["total_params"] != {256: 381600, 1025: 529248, 4097: 1119072}[vocab]:
            raise ValueError("Parameter count differs from the original model shape")
        integer(r["unknown_training_corpus_tokens"], "encoded corpus UNKs")
        for key in ("train_cpu_seconds", "train_wall_seconds", "estimated_triangular_flops", "estimated_dense_flops"):
            number(r[key], key, positive=True)
        per = number(r["flops"]["triangular_per_token"], "triangular FLOPs/token", positive=True)
        if not math.isclose(r["estimated_triangular_flops"], per * r["training_tokens"], rel_tol=1e-12):
            raise ValueError("Compute estimate differs from actual completed target count")
        if r["estimated_dense_flops"] < r["estimated_triangular_flops"]:
            raise ValueError("Dense estimate is smaller than triangular estimate")
        for key in ("common_passage_bpc", "common_valid_bpc", "passage_common_bits_per_scored_token"):
            number(r[key], key)
        m = integer(r["passage_common_scored_tokens"], "scored passage tokens", 1)
        cpt = number(r["passage_common_characters_per_scored_token"], "scored-token density", positive=True)
        if not math.isclose(cpt, prefixes["passage"]["suffix_characters"] / m, rel_tol=1e-12):
            raise ValueError("Unit conversion uses a different character/token cohort")
        if not math.isclose(r["passage_common_bits_per_scored_token"] / cpt, r["common_passage_bpc"], rel_tol=1e-10, abs_tol=1e-12):
            raise ValueError("BPT/CPT differs from exact common-suffix BPC")
        c = r["sampled_validation_curve"]
        if not isinstance(c, list) or not c or c[-1]["executed_steps"] != steps:
            raise ValueError("Missing full-horizon validation diagnostic")
        previous = 0
        for point in c:
            s = integer(point["executed_steps"], "validation update", 1)
            if not previous < s <= steps:
                raise ValueError("Validation update order/range is invalid")
            previous = s
            number(point["token_nll"], "sampled token NLL")
            number(point["original_mean_density_valid_bpc"], "sampled density proxy")
        if r["sample_semantics"] != "continuation-only":
            raise ValueError("Generated sample must explicitly exclude its prompt")
        if r["sample_decoding"] != "UTF8 replacement for bytes; original question-mark UNK decoder for subwords":
            raise ValueError("Unexpected sample decoding convention")
        if r["sample_seed"] != seed or not math.isclose(number(r["sample_temperature"], "temperature", positive=True), .8):
            raise ValueError("Unexpected generation settings")
        for key, length in (("sample_prompt_ids", 8), ("sample_generated_ids", 200 if kind == "bytes" else 60)):
            ids = r[key]
            if not isinstance(ids, list) or len(ids) != length or any(integer(v, key) >= vocab for v in ids):
                raise ValueError("Sample token IDs differ from original generation contract")
        if not all(isinstance(r[k], str) for k in ("sample_prompt", "sample_generated")):
            raise ValueError("Sample text is missing")
    # Columns described as one value per encoding must truly be identical across seeds.
    for encoding in LM_SPECS:
        group = [r for r in rows if r["cfg"]["encoding"] == encoding]
        for key in ("total_params", "unknown_training_corpus_tokens", "training_tokens", "estimated_triangular_flops", "estimated_dense_flops", "passage_common_scored_tokens"):
            if len({r[key] for r in group}) != 1:
                raise ValueError(f"{encoding}: {key} differs across seeds")
        if len({r["flops"]["triangular_per_token"] for r in group}) != 1:
            raise ValueError("Per-token estimator differs across identical model shapes")
    return d


def lm_stats():
    d = accepted_lm_data()
    return d, list(LM_SPECS), {n: np.array([r["common_passage_bpc"] for r in sorted(
        (r for r in d["runs"] if r["cfg"]["encoding"] == n), key=lambda r: r["seed"])]) for n in LM_SPECS}


class Bits(VoiceoverScene):
    """Five sections, split into bounded, bilingual panels for native QA witnesses."""

    def construct(self):
        self.d = accepted_lm_data()
        self.groups = {n: sorted([r for r in self.d["runs"] if r["cfg"]["encoding"] == n], key=lambda r: r["seed"])
                       for n in LM_SPECS}
        self.language = os.environ.get("EXPLAINER_LANG", "en")
        if self.language not in ("en", "zh"):
            raise ValueError("Bits supports en/zh only")
        self.font = "Noto Sans CJK SC" if self.language == "zh" else "DejaVu Sans"
        if not {self.font, "DejaVu Sans Mono"}.issubset(set(manimpango.list_fonts())):
            raise RuntimeError("Required Bits display font is unavailable")
        self.camera.background_color = "#0D1117"
        self.card()
        self.units()
        self.race()
        self.replay()
        self.why()

    def tr(self, en, zh):
        return zh if self.language == "zh" else en

    def t(self, en, zh=None, size=24, color=WHITE, width=12.7, bold=False, mono=False):
        out = data_text(self.tr(en, en if zh is None else zh),
                        font="DejaVu Sans Mono" if mono else self.font, font_size=size,
                        color=color, weight=BOLD if bold else NORMAL, line_spacing=1.1)
        if out.width > width:
            out.scale_to_fit_width(width)
        return out

    def name(self, encoding):
        kind, size, _, _ = LM_SPECS[encoding]
        return self.tr("Bytes" if kind == "bytes" else f"{'BPE' if kind == 'bpe' else 'Unigram'} {size:,}",
                       "字节" if kind == "bytes" else f"{'BPE' if kind == 'bpe' else '一元模型'} {size:,}")

    def table(self, headers, rows, widths, row_height=.65, size=22):
        total = sum(widths)
        if total > 12.7 + 1e-9:
            raise ValueError("Bits table exceeds its panel")
        centers, left = [], -total / 2
        for width in widths:
            centers.append(left + width / 2)
            left += width
        header_cells = VGroup(*[
            self.t(en, zh, size=19, color=GREY_A, width=widths[j] - .16, bold=True)
            for j, (en, zh) in enumerate(headers)
        ])
        data_rows = [VGroup(*[
            self.t(str(value), size=size, color=LM_COLORS[encoding] if j == 0 else WHITE,
                   width=widths[j] - .16)
            for j, value in enumerate(values)
        ]) for encoding, values in rows]
        # Measure after column-width fitting: multiline means/ranges can be taller
        # than the old fixed pitch. Keep the same clear gap between every row.
        header_height = max(cell.height for cell in header_cells)
        cell_height = max(cell.height for row in data_rows for cell in row)
        padding = .18
        pitch = max(row_height, cell_height + padding)
        divider_y = -header_height / 2 - padding
        first_y = divider_y - padding - cell_height / 2
        for j, cell in enumerate(header_cells):
            cell.move_to([centers[j], 0, 0])
        group = VGroup(header_cells, Line([-total / 2, divider_y, 0],
                                          [total / 2, divider_y, 0], color=GREY_D))
        for i, row in enumerate(data_rows):
            for j, cell in enumerate(row):
                cell.move_to([centers[j], first_y - i * pitch, 0])
            group.add(row)
        return group

    def panel(self, title_en, title_zh, content, narration, footer_en, footer_zh):
        banner = self.t("ORIGINAL-SCHEDULE QA · 15 runs · unequal compute", "原始步数 QA · 15 次训练 · 计算量不同",
                        size=16, color=GREY_B).to_edge(UP, buff=.18)
        title = self.t(title_en, title_zh, size=34, bold=True).next_to(banner, DOWN, buff=.16)
        rule = Line(LEFT * 6.45, RIGHT * 6.45, color=GREY_D).next_to(title, DOWN, buff=.16)
        footer = self.t(footer_en, footer_zh, size=18, color=GREY_A).to_edge(DOWN, buff=.2)
        # Preserve a dedicated content rectangle; do not let a long label move adjacent columns.
        if content.width > 12.7:
            content.scale_to_fit_width(12.7)
        if content.height > 5.2:
            content.scale_to_fit_height(5.2)
        content.move_to([0, -.15, 0])
        group = VGroup(banner, title, rule, content, footer)
        with self.voiceover(NARRATION[narration][0]):
            self.play(FadeIn(group), run_time=.6)
        self.wait(.6)
        self.clear_scene(run_time=.4)

    @staticmethod
    def summary(values, scale=1, decimals=3):
        v = np.asarray(values, float) / scale
        return f"{v.mean():,.{decimals}f}\n[{v.min():,.{decimals}f}, {v.max():,.{decimals}f}]"

    def card(self):
        body = VGroup(
            self.t("4 · What a token is worth", "4 · 一个词元值多少", size=43, bold=True),
            self.t("Five canonical encodings × seeds 0, 1, 2", "五种规范编码 × 种子 0、1、2", size=28),
            self.t("New original-recipe candidates; historical outputs are not recovered.", "新完成的原始配方候选；不是恢复的历史输出。", size=23, color=GREY_A),
            self.t("Same body shape; different heads, parameters, windows and compute.", "主体形状相同；输出头、参数、窗口和计算量不同。", size=23, color=GREY_A),
        ).arrange(DOWN, buff=.5)
        self.panel("Comparing different token units", "比较不同的词元单位", body, "card",
                   "Descriptive outcomes; no equal-compute, superiority or isolated-causal claim.",
                   "描述性结果；不宣称等计算量、优越性或单独的因果作用。")

    def units(self):
        r = self.groups["bpe4096"][0]
        body = VGroup(
            self.t("BPC = canonical-token-path total bits / exact suffix characters", "BPC = 规范词元路径的总比特数 / 后缀精确字符数", size=28),
            self.t("BPT = total bits / scored tokens", "BPT = 总比特数 / 计分词元数", size=27, color=C.BITS),
            self.t("CPT = exact suffix characters / scored tokens", "CPT = 后缀精确字符数 / 计分词元数", size=27, color=TEXT_C),
            self.t("BPC = BPT / CPT", size=36, color=C.BITS, bold=True),
            self.t("One canonical token path, conditional on the common prefix.\nNot a sum over every possible tokenization.",
                   "在共同前缀条件下，只计一条规范词元路径。\n不对所有可能的分词切法求和。", size=23, color=GREY_A),
        ).arrange(DOWN, buff=.32)
        self.panel("Use the same scored suffix and denominator", "使用相同的计分后缀和分母", body, "units",
                   "Unicode characters are counted exactly; the conditioning prefix is excluded.",
                   "Unicode 字符数精确计数；条件前缀不计分。")
        p = self.d["common_prefix"]["passage"]
        rows = [(n, [self.name(n), f"{g[0]['passage_common_scored_tokens']:,}",
                     f"{g[0]['passage_common_characters_per_scored_token']:.6f}"])
                for n, g in self.groups.items()]
        table = self.table([("Encoding", "编码"), ("Scored tokens · seed 0", "计分词元 · 种子 0"),
                            ("Characters / scored token", "字符 / 计分词元")], rows, [3.5, 4.4, 4.4], row_height=.53)
        conversion = self.t(
            f"BPE 4,096 · seed 0: {r['passage_common_bits_per_scored_token']:.6f} / "
            f"{r['passage_common_characters_per_scored_token']:.6f} ≈ {r['common_passage_bpc']:.6f} BPC",
            f"BPE 4,096 · 种子 0：{r['passage_common_bits_per_scored_token']:.6f} / "
            f"{r['passage_common_characters_per_scored_token']:.6f} ≈ {r['common_passage_bpc']:.6f} BPC", size=24, color=C.BITS)
        definition = self.t(f"Passage prefix: {p['bytes']} bytes / {p['characters']} Unicode characters; "
                            f"scored suffix: {p['suffix_characters']:,} characters.",
                            f"段落前缀：{p['bytes']} 字节 / {p['characters']} 个 Unicode 字符；"
                            f"计分后缀：{p['suffix_characters']:,} 个字符。", size=21, color=GREY_A)
        self.panel("One text suffix, different token counts", "同一个文本后缀，不同的词元数",
                   VGroup(table, conversion, definition).arrange(DOWN, buff=.28), "targets",
                   "The numerical ratio uses the same scored tokens and characters; displayed decimals are rounded.",
                   "数值比值使用同一组计分词元和字符；显示的小数经过四舍五入。")

    def race(self):
        rows = []
        for n, g in self.groups.items():
            r = g[0]
            rows.append((n, [self.name(n), f"{r['cfg']['size']:,}", f"{r['vocab']:,}",
                             f"{r['total_params']:,}", f"{r['executed_steps']:,}",
                             f"{r['unknown_training_corpus_tokens']:,}"]))
        table = self.table([("Encoding", "编码"), ("Nominal\npieces", "名义\n片段数"),
                            ("Actual head\nclasses", "实际输出\n类别数"), ("Parameters", "参数量"),
                            ("Updates", "更新次数"), ("Encoded training-corpus\nUNK tokens", "编码后训练语料中的\nUNK 词元数")],
                           rows, [2.7, 1.25, 1.65, 2.05, 1.35, 3.65], size=21)
        body = VGroup(table, self.t("Body: 3 layers · width 96 · 128-token context · batch 16\n"
                                    "Subwords: nominal pieces + one UNK output; original lossy training encoding retained.",
                                    "主体：3 层 · 宽度 96 · 128 词元上下文 · 批量 16\n"
                                    "子词：名义片段数 + 一个 UNK 输出；保留原始有损训练编码。", size=22, color=GREY_A)).arrange(DOWN, buff=.35)
        self.panel("Original schedules and actual model sizes", "原始训练步数与实际模型大小", body, "schedule",
                   "Each row applies to all three seeds. Corpus UNKs are not sampled-update exposures.",
                   "每行适用于三个种子。语料 UNK 数不是抽样更新中的接触次数。")
        rows = [(n, [self.name(n), f"{g[0]['training_tokens'] / 1e6:.6f}",
                     self.summary([r['training_target_source_bytes'] for r in g], 1e6, 6),
                     self.summary([r['train_cpu_seconds'] for r in g], decimals=2),
                     self.summary([r['train_wall_seconds'] for r in g], decimals=2)]) for n, g in self.groups.items()]
        table = self.table([("Encoding", "编码"), ("Target tokens\nmillions", "目标词元\n百万"),
                            ("Target-source bytes · M\nmean [min, max]", "目标源字节 · 百万\n均值 [最小, 最大]"),
                            ("CPU seconds\nmean [min, max]", "CPU 秒\n均值 [最小, 最大]"),
                            ("Wall seconds\nmean [min, max]", "墙钟秒\n均值 [最小, 最大]")],
                           rows, [2.5, 1.8, 3.3, 2.5, 2.5], row_height=.75, size=21)
        self.panel("Measured completed work · all three seeds", "实测已完成工作量 · 三个种子", table, "work",
                   "Repeated target-source bytes count again; loop times include validation/checkpoint overhead.",
                   "重复的目标源字节重复计数；循环时间包含验证和检查点开销。")
        rows = [(n, [self.name(n), f"{g[0]['flops']['triangular_per_token'] / 1e6:.6f}",
                     f"{g[0]['estimated_triangular_flops'] / 1e9:,.2f}",
                     f"{g[0]['estimated_dense_flops'] / 1e9:,.2f}"]) for n, g in self.groups.items()]
        table = self.table([("Encoding", "编码"), ("Triangular / token\nMFLOP estimate", "三角口径 / 词元\n百万 FLOP 估计"),
                            ("Triangular total\nGFLOP estimate", "三角口径总量\n十亿 FLOP 估计"),
                            ("Dense total\nGFLOP estimate", "稠密口径总量\n十亿 FLOP 估计")], rows, [2.8, 3.3, 3.3, 3.2])
        note = self.t("Matrix estimates only: exclude norm, rotary, softmax, optimizer,\nvalidation and kernel costs. Not measured hardware FLOPs or CPU time.",
                      "只估计矩阵运算：不含归一化、旋转位置、softmax、优化器、\n验证和内核代价。不是实测硬件 FLOP，也不是 CPU 时间。", size=22, color=GREY_A)
        self.panel("Compute estimates · original schedules unchanged", "计算量估计 · 原始步数不变",
                   VGroup(table, note).arrange(DOWN, buff=.38), "compute",
                   "Per-run estimates are identical across seeds within an encoding; budgets differ across encodings.",
                   "同一编码内每个种子的估计相同；不同编码的计算预算不同。")

    @staticmethod
    def nice_step(span):
        raw = span / 4
        base = 10 ** math.floor(math.log10(raw))
        return next(m * base for m in (1, 2, 2.5, 5, 10) if m * base >= raw)

    def learning_chart(self):
        datasets = []
        for n, g in self.groups.items():
            for r in g:
                c = r["sampled_validation_curve"]
                x = np.array([p["executed_steps"] * 16 * 128 * r["flops"]["triangular_per_token"] / 1e12 for p in c])
                y = np.array([p["original_mean_density_valid_bpc"] for p in c])
                datasets.append((n, r["seed"], x, y))
        xmax = max(float(x.max()) for _, _, x, _ in datasets)
        ymin = min(float(y.min()) for _, _, _, y in datasets)
        ymax = max(float(y.max()) for _, _, _, y in datasets)
        sx = self.nice_step(xmax * 1.04)
        sy = self.nice_step(max(ymax - ymin, .2) * 1.12)
        xhi = math.ceil(xmax * 1.04 / sx) * sx
        ylo = max(0, math.floor((ymin - .06 * max(ymax - ymin, .2)) / sy) * sy)
        yhi = math.ceil((ymax + .06 * max(ymax - ymin, .2)) / sy) * sy
        ax = Axes(x_range=[0, xhi, sx], y_range=[ylo, yhi, sy], x_length=10.8, y_length=3.25,
                  tips=False, axis_config={"include_ticks": False, "stroke_color": GREY_C})
        plot = VGroup(ax)
        for x in np.arange(0, xhi + sx * .01, sx):
            plot.add(self.t(f"{x:g}", size=19).next_to(ax.c2p(x, ylo), DOWN, buff=.12))
        for y in np.arange(ylo, yhi + sy * .01, sy):
            plot.add(self.t(f"{y:g}", size=19).next_to(ax.c2p(0, y), LEFT, buff=.12))
        for n, seed, x, y in datasets:
            # Keep every accepted sample; no y cap, point deletion, smoothing or invented initial point.
            path = VMobject(color=LM_COLORS[n], stroke_width=(3.1, 2.3, 1.8)[seed], fill_opacity=0)
            path.set_points_as_corners([ax.c2p(float(xx), float(yy)) for xx, yy in zip(x, y)])
            if seed == 1:
                path = DashedVMobject(path, num_dashes=34, dashed_ratio=.65)
            elif seed == 2:
                path.set_stroke(opacity=.65, family=True)
            # Apply after dash/stroke styling too: no child may fill the implicit
            # closing edge between the final and initial learning-curve samples.
            path.set_fill(opacity=0, family=True)
            plot.add(path)
        xlabel = self.t("Triangular matrix-operation estimate · TFLOP", "三角矩阵运算量估计 · 万亿 FLOP", size=20).next_to(ax, DOWN, buff=.48)
        ylabel = self.t("Sampled validation bits/token ÷ corpus characters/token · approximate BPC",
                        "抽样验证每词元比特数 ÷ 语料平均每词元字符数 · 近似 BPC", size=20).next_to(ax, UP, buff=.16)
        plot.add(xlabel, ylabel)
        legend = VGroup(*[self.t(self.name(n), size=20, color=LM_COLORS[n]) for n in self.groups]).arrange(RIGHT, buff=.35)
        styles = self.t("Seeds 0 / 1 / 2: solid / dashed / thin translucent; 15 lines.",
                        "种子 0 / 1 / 2：实线 / 虚线 / 细半透明线；共 15 条。", size=18, color=GREY_A)
        return VGroup(legend, plot, styles).arrange(DOWN, buff=.22)

    def replay(self):
        self.panel("Learning curves are sampled diagnostics", "学习曲线是抽样诊断", self.learning_chart(), "curves",
                   "Tokenizer-specific windows; approximate density normalization. Exact common-suffix scores follow.",
                   "窗口随分词器而异；密度归一化只是近似。下一页为精确共同后缀分数。")
        rows = [(n, [self.name(n), self.summary([r['common_passage_bpc'] for r in g], decimals=6),
                     self.summary([r['common_valid_bpc'] for r in g], decimals=6)]) for n, g in self.groups.items()]
        table = self.table([("Encoding", "编码"), ("Passage BPC\nmean [min, max]", "段落 BPC\n均值 [最小, 最大]"),
                            ("Full validation BPC\nmean [min, max]", "完整验证 BPC\n均值 [最小, 最大]")],
                           rows, [3.1, 4.8, 4.8], row_height=.7, size=23)
        definitions = []
        for split, en, zh in (("passage", "Passage", "段落"), ("valid", "Validation", "验证集")):
            p = self.d["common_prefix"][split]
            definitions.append(self.t(f"{en}: prefix {p['bytes']} bytes / {p['characters']} characters; "
                                      f"scored suffix {p['suffix_characters']:,} Unicode characters.",
                                      f"{zh}：前缀 {p['bytes']} 字节 / {p['characters']} 字符；"
                                      f"计分后缀 {p['suffix_characters']:,} 个 Unicode 字符。", size=19, color=GREY_A))
        body = VGroup(table, VGroup(*definitions).arrange(DOWN, buff=.12)).arrange(DOWN, buff=.3)
        self.panel("Exact suffix scores · recorded three-seed ranges", "精确后缀分数 · 三个种子的实际范围", body, "scores",
                   "Canonical-path NLL / (ln 2 × exact suffix characters). Ranges are not confidence intervals.",
                   "规范路径 NLL /（ln 2 × 后缀精确字符数）。实际范围不是置信区间。")

    @staticmethod
    def excerpt(value, limit, columns=72):
        # Escaped controls are explicit; never silently normalize the accepted sample's whitespace.
        value = value.replace("\r", "[CR]").replace("\t", "[TAB]")
        truncated = len(value) > limit
        value = value[:limit]
        lines = []
        for line in value.split("\n"):
            lines.extend(textwrap.wrap(line, width=columns, replace_whitespace=False,
                                       drop_whitespace=False, break_long_words=True, break_on_hyphens=False) or [""])
        return "\n".join(lines) + ("\n[excerpt truncated]" if truncated else "")

    def why(self):
        body = VGroup(
            self.t("Tokenization changes several things together", "分词同时改变多个因素", size=29, bold=True),
            self.t("Sequence length and text represented by 128 tokens", "序列长度，以及 128 个词元表示的文本", size=25),
            self.t("Embedding/head size, parameters and matrix cost", "嵌入与输出头大小、参数量和矩阵代价", size=25),
            self.t("Target frequencies, UNK handling and sampled windows", "目标频率、UNK 处理和抽样窗口", size=25),
            self.t("These original-schedule runs do not isolate those effects.\nThe extra UTF-8 fallback experiment is outside the canonical 15.",
                   "这些按原始步数完成的训练没有把各作用分离。\n额外的 UTF-8 回退实验不属于这 15 个规范案例。", size=23, color=GREY_A),
        ).arrange(DOWN, buff=.35)
        self.panel("Interpret the comparison within its scope", "在实验范围内解释比较", body, "why",
                   "Recorded outcomes do not establish superiority or an isolated tokenizer effect.",
                   "记录的结果不证明优越性，也不能单独归因于分词器。")
        for encoding, narration in (("bytes256", "sample_bytes"), ("bpe4096", "sample_bpe")):
            r = self.groups[encoding][0]
            prompt = self.t(self.excerpt(r["sample_prompt"], 180), size=23, mono=True, width=12.0)
            generated = self.t(self.excerpt(r["sample_generated"], 220), size=23, mono=True, width=12.0)
            body = VGroup(
                self.t("Prompt · this tokenizer's first 8 passage tokens", "提示 · 该分词器在段落开头的 8 个词元", size=23, color=LM_COLORS[encoding]),
                prompt,
                self.t("Generated continuation only · prompt not repeated", "仅生成的续写 · 不重复提示", size=23, color=LM_COLORS[encoding]),
                generated,
                self.t("Byte decoder: UTF-8 replacement. Subword decoder: '?' for UNK.\n"
                       "Prompts differ across tokenizers; excerpts are illustrative, not a quality benchmark.",
                       "字节解码：UTF-8 替换字符。子词解码：用 '?' 表示 UNK。\n"
                       "各分词器的提示不同；摘录仅作示例，不是质量基准。", size=20, color=GREY_A),
            ).arrange(DOWN, aligned_edge=LEFT, buff=.24)
            self.panel(self.name(encoding) + " · seed 0 · temperature 0.8",
                       self.name(encoding) + " · 种子 0 · 温度 0.8", body, narration,
                       "Accepted output is preserved; [excerpt truncated] marks display truncation; [CR]/[TAB] escape controls.",
                       "保留通过验收的输出；[excerpt truncated] 标记显示截短；[CR]/[TAB] 转义控制字符。")
