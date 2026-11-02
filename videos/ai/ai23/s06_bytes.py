from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import MONO, PART, SURP_C, TEXT_C, load, token_chips

PATCH_C = C.CONTEXT


def byte_label(value: int) -> str:
    """Display a byte, without interpreting individual UTF-8 bytes as characters."""
    return "·" if value == 32 else chr(value) if 33 <= value <= 126 else f"{value:02x}"


def patch_data():
    """Require explicit corrected-presentation inputs; never repair legacy caches.

    The preserved original producer does not meet this contract. A verified QA
    provider must supply the independently reviewed corrected-boundary product.
    """
    # No producer owns this key: missing accepted QA input must fail before
    # the legacy cache loader can train a byte model on first use.
    p = load("patches_qa_corrected_boundary")
    required = {
        "candidate": "corrected_boundary",
        "mean_length_numerator": "full source bytes",
        "mean_length_denominator": "number of patches, including initial patch",
    }
    for key, expected in required.items():
        if str(p.get(key, "")) != expected:
            raise ValueError(f"Bytes QA requires {key}={expected!r}; legacy patch inputs are refused")
    if int(p["source_bytes"]) != int(p["n_bytes"]) + 1:
        raise ValueError("Expected exactly one unscored source byte")
    n = len(str(p["example"]).encode("utf-8"))
    H, S = (np.asarray(p[key], float) for key in ("example_H", "example_S"))
    if n < 2 or H.shape != (n,) or S.shape != (n,):
        raise ValueError("Patch-example scores must align exactly with its UTF-8 bytes")
    if not (np.isnan(H[0]) and np.isnan(S[0])):
        raise ValueError("The corrected global-zero example must start with an unscored byte")
    if not (np.isfinite(H[1:]).all() and np.isfinite(S[1:]).all()):
        raise ValueError("Every remaining example byte must have finite entropy and surprise")
    if np.asarray(p["example_bpe"]).shape != (n,):
        raise ValueError("BPE boundaries must align with the same example bytes")
    start = float(p["bpe_start_share"])
    if not np.isfinite(start) or not 0 <= start <= 1:
        raise ValueError("A measured scored-byte BPE start share is required")
    return p


def byte_cells(text: str, cell=0.36, color=GREY_B):
    bs = text.encode("utf-8")
    g = VGroup()
    for b in bs:
        sq = Square(cell, stroke_color=color, stroke_width=1.2, fill_color=color, fill_opacity=0.12)
        g.add(VGroup(sq, data_text(f"{b:02x}", font=MONO, font_size=13, color=WHITE).move_to(sq)))
    return g.arrange(RIGHT, buff=0.03)


class Bytes(VoiceoverScene):
    def construct(self):
        self.card()
        self.bytelevel()
        self.free()
        self.entropy()
        self.measure()

    def card(self):
        card = chapter_card(5, r"Bytes and patches", r"Could a model do without a tokenizer?", lit=(2019,), part=PART)
        with self.voiceover("Chapter five. Bytes and patches."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def bytelevel(self):
        b = load("bpe")
        words = ["cat", "café", "naïve"]
        rows = VGroup()
        for w in words:
            cells = byte_cells(w)
            rows.add(VGroup(data_text(w, font=MONO, font_size=28, color=TEXT_C), cells,
                            label(rf"${len(w.encode('utf-8'))}$ bytes", font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-1.5, 0.0, 0])
        rl = label(r"UTF-8: \ every character as $1$ to $4$ bytes, \ $256$ possible values \\ byte values shown in hexadecimal", font_size=22, color=GREY_A)
        rl.next_to(rows, UP, buff=0.3).align_to(rows, LEFT)
        probs = VGroup(*[label(t, font_size=22, color=C.SURPRISE) for t in (
            r"a character the vocabulary never saw: \ unknown", r"letters hidden inside a token: \ spelling is hard",
            r"other languages cut into more tokens: \ they cost more")]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for p_ in probs:
            p_.scale(1.15)
        probs.to_edge(UP, buff=0.4)
        probs_top = probs.copy()
        probs.scale(1.25).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(RIGHT * 0.3)
        marks = VGroup(*[Dot(radius=0.07, color=C.SURPRISE).next_to(p_, LEFT, buff=0.25) for p_ in probs])
        txt = []
        if "novels_cut" in b:
            cut = [str(x) for x in b["novels_cut"]]
            chips = token_chips(cut, font_size=22, height=0.44, buff=0.04)
            if chips.width > 12.6:
                chips.width = 12.6
            nl = label(rf"the series' own model: \ byte-level BPE, \ ${int(b['novels_vocab']):,}$ tokens; \ "
                       rf"${float(b['novels_cpt']):.2f}$ characters a token on the passage".replace(",", "{,}"),
                       font_size=22, color=TEXT_C)
            txt = [VGroup(nl, chips).arrange(DOWN, buff=0.2).move_to(DOWN * 2.0)]
        cite_ = cite(r"A.~Radford et al., \textit{GPT-2} (2019)", corner=DL)
        own = (f" The series' own language model, the one Parts 18 to 30 train and probe, uses a byte-level BPE "
               f"with {int(b['novels_vocab']):,} tokens; on the passage it averages {float(b['novels_cpt']):.2f} "
               "characters a token.") if "novels_cut" in b else ""
        with self.voiceover(
            "Tokenizers fail in their own ways. <bookmark mark='a'/> A character the vocabulary never saw becomes "
            "unknown. Letters hidden inside one token are hard to count or spell. And a vocabulary learned mostly on "
            "English cuts other languages into more tokens, so they cost more. <bookmark mark='b'/> GPT-2's fix, in "
            "2019, was to run BPE on bytes. Any text is a sequence of bytes in UTF-8, one to four per character, "
            "with only 256 possible values, so with the bytes as the starting alphabet nothing is ever unknown."
            f"<bookmark mark='c'/>{own}"
        ) as vo:
            self.play(FadeIn(probs[0]), FadeIn(marks[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(p_, m_)) for p_, m_ in zip(probs[1:], marks[1:])], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(Transform(probs, probs_top), FadeOut(marks))
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows], lag_ratio=0.3), FadeIn(cite_),
                      run_time=2.0)
            vo.wait_until("c")
            if txt:
                self.play(FadeIn(txt[0]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def free(self):
        p = patch_data()
        ex = str(p["example"])
        ex = ex[:ex.index(" white") + 6] if " white" in ex else ex[:37]
        # Keep a byte-width bound while retaining complete UTF-8 characters.
        ex = ex.encode("utf-8")[:37].decode("utf-8", "ignore")
        bs = ex.encode("utf-8")
        H = np.asarray(p["example_H"], float)[:len(bs)]
        th = float(p["threshold"])
        cell, buff, gap = 0.28, 0.02, 0.14

        def row(starts, color):
            """The bytes as cells, a gap before each patch start, and a box around each patch."""
            cells = VGroup()
            x = 0.0
            for k, c in enumerate(bs):
                if k and starts[k]:
                    x += gap
                sq = Square(cell, stroke_color=GREY_B, stroke_width=1, fill_color=GREY_B, fill_opacity=0.15)
                sq.move_to([x + cell / 2, 0, 0])
                cells.add(VGroup(sq, data_text(byte_label(c), font=MONO, font_size=12 if c < 33 or c > 126 else 15,
                                               color=WHITE).move_to(sq)))
                x += cell + buff
            boxes = VGroup()
            if color is not None:
                k = 0
                while k < len(bs):
                    m = k + 1
                    while m < len(bs) and not starts[m]:
                        m += 1
                    seg = VGroup(*cells[k:m])
                    boxes.add(SurroundingRectangle(seg, buff=0.04, corner_radius=0.06, stroke_color=color,
                                                   stroke_width=2.5, fill_color=color, fill_opacity=0.18))
                    k = m
            return VGroup(boxes, cells)

        fixed = [k % 4 == 0 for k in range(len(bs))]
        ent = [k == 0 or H[k] > th for k in range(len(bs))]
        n_fix = sum(fixed)
        n_ent = sum(ent)
        lab = [label(t, font_size=22, color=c_) for t, c_ in (
            (rf"bytes: \ ByT5 (2021), \ ${len(bs)}$ positions", GREY_B),
            (rf"fixed patches: \ MegaByte (2023), \ ${n_fix}$ patches, \ up to $4$ bytes each", C.MODEL_Q),
            (rf"entropy patches: \ BLT (2024) idea, \ ${n_ent}$ patches; \ first byte or $H > \tau$", PATCH_C))]
        y = [1.9, 0.2, -1.5]
        groups = []
        for k, (yy, l_) in enumerate(zip(y, lab)):
            base = row([False] * len(bs) if k == 0 else (fixed if k == 1 else ent),
                       None if k == 0 else (C.MODEL_Q if k == 1 else PATCH_C))
            if base.width > 12.8:
                base.scale_to_fit_width(12.8)
            base.move_to([0, yy, 0])
            if l_.width > 13.0:
                l_.scale_to_fit_width(13.0)
            l_.next_to(base, UP, buff=0.18).align_to(base, LEFT)
            groups.append(VGroup(base, l_))
        cite_ = cite(r"Xue et al.\ (2021); \ Yu et al.\ (2023); \ Pagnoni et al.\ (2024)", corner=DR)
        view = note(r"byte labels: \ printable ASCII; \\ other bytes: \ hexadecimal", font_size=15).to_corner(DL, buff=0.25)
        with self.voiceover(
            "Could a model skip the tokenizer and read bytes? <bookmark mark='a'/> Google's ByT5, in 2021, did exactly "
            "that, at the price of sequences several times longer than BPE's. <bookmark mark='b'/> In 2023 Meta's "
            "MegaByte grouped the bytes into fixed patches: a big transformer looks at the patches, and a small one "
            "writes the bytes inside each. <bookmark mark='c'/> But a fixed patch spends as much on the end of a "
            "predictable word as on its surprising start. In December 2024 Meta's Byte Latent Transformer let the "
            "data decide. Here we illustrate the idea, rather than train a BLT: force the initial patch, then start "
            "a new one at each byte whose conditional entropy is greater than the threshold. "
            f"Here, the same {len(bs)} bytes become {n_fix} fixed patches, with a possibly shorter final patch, "
            f"or {n_ent} entropy patches."
        ) as vo:
            self.play(FadeIn(groups[0]), FadeIn(cite_), FadeIn(view))
            vo.wait_until("b")
            self.play(FadeIn(groups[1]))
            vo.wait_until("c")
            self.play(FadeIn(groups[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def entropy(self):
        p = patch_data()
        ex = str(p["example"])
        bs = ex.encode("utf-8")
        H = np.asarray(p["example_H"], float)[:len(bs)]
        S = np.asarray(p["example_S"], float)[:len(bs)]
        th = float(p["threshold"])
        n = len(bs)
        W = 13.0
        dx = W / n
        x0 = -W / 2
        finite = np.concatenate((H[np.isfinite(H)], S[np.isfinite(S)]))
        if not len(finite):
            raise ValueError("The entropy witness has no scored bytes")
        hmax = max(5.0, float(finite.max()) + 0.3)
        sy = 3.6 / hmax
        base_y = -1.2
        bars = VGroup(*[Rectangle(width=dx * 0.8, height=max(h * sy, 0.01), stroke_width=0,
                                  fill_color=PATCH_C if (k == 0 or h > th) else GREY_C, fill_opacity=0.85)
                        .move_to([x0 + dx * (k + 0.5), base_y + h * sy / 2, 0]) for k, h in enumerate(H) if np.isfinite(h)])
        sdots = VGroup(*[Dot([x0 + dx * (k + 0.5), base_y + s * sy, 0], radius=0.035, color=SURP_C)
                         for k, s in enumerate(S) if np.isfinite(s)])
        letters = VGroup(*[data_text(byte_label(c), font=MONO, font_size=11 if c < 33 or c > 126 else 15, color=WHITE)
                           .move_to([x0 + dx * (k + 0.5), base_y - 0.25, 0]) for k, c in enumerate(bs)])
        thl = DashedLine([x0, base_y + th * sy, 0], [x0 + W, base_y + th * sy, 0], color=WHITE, stroke_width=2)
        thlab = label(rf"threshold: \ ${th:.2f}$ bits", font_size=20, color=WHITE).move_to(
            [x0 + W - 1.0, base_y + hmax * sy + 0.25, 0])
        yl = label(r"bars: \ conditional next-byte entropy, \ bits; \ dots: \ observed-byte surprise, \ bits",
                   font_size=20, color=GREY_A).to_edge(UP, buff=0.4)
        bpe = np.asarray(p["example_bpe"], bool)[:n]
        bmarks = VGroup(*[Line([x0 + dx * k, base_y - 0.48, 0], [x0 + dx * k, base_y - 0.68, 0], color=TEXT_C, stroke_width=2.5)
                          for k in range(n) if bpe[k]])
        bml = label(r"BPE's token starts", font_size=18, color=TEXT_C).next_to(bmarks, DOWN, buff=0.08).to_edge(LEFT, buff=0.3)
        tag = note(r"QA candidate: \ byte model, \ seed $0$, \ $1{,}000$ completed steps", font_size=17).to_corner(DR, buff=0.25)
        first = note(r"initial byte: \ unscored, \ forced patch start; \\ byte labels: \ ASCII or hexadecimal",
                     font_size=16).to_corner(DL, buff=0.25)
        with self.voiceover(
            "For this QA candidate, our byte model completed one thousand training steps with seed zero. This does "
            "not establish acceptance of chapter four's fifteen-run experiment. The initial byte has no prediction "
            "score and starts a forced patch. <bookmark mark='a'/> Each bar is conditional entropy: uncertainty "
            "about the next byte, in bits. Each dot is observed surprise: minus log two of the probability assigned "
            "to the byte that arrived. <bookmark mark='b'/> These quantities differ: a confident prediction can be "
            "wrong. Uncertainty may fall inside familiar words, but this is measured, not guaranteed. "
            "<bookmark mark='c'/> Apart from the forced initial patch, start a new patch at every byte where entropy "
            "is greater than the threshold, including consecutive bytes above it. This is a threshold test, not "
            "just an upward crossing."
        ) as vo:
            self.play(FadeIn(yl), FadeIn(letters), FadeIn(tag), FadeIn(first))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.02), run_time=2.0)
            self.play(FadeIn(sdots))
            vo.wait_until("b")
            self.play(FadeIn(bmarks), FadeIn(bml))
            vo.wait_until("c")
            self.play(Create(thl), FadeIn(thlab))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        p = patch_data()
        sw = p["sweep"]
        L = np.array([s["mean_len"] for s in sw])
        Y = np.array([s["surprise_share"] for s in sw])
        j = int(p["match"])
        bl, bs_ = float(p["bpe_len"]), float(p["bpe_share"])
        bpe_start = float(p["bpe_start_share"])
        xm = float(min(8.0, L.max()))
        keep = L <= xm
        ax = axes([1, xm, 1], [0, 1, 0.2], x_length=6.4, y_length=4.2, xlabel=r"mean length, \ full-passage bytes",
                  ylabel=r"scored surprise share at unit starts", xticks=list(range(1, int(xm) + 1)),
                  yticks=[0, 0.5, 1], yfmt=lambda v: f"{int(round(100 * v))}\\%", center=[-3.0, -0.3, 0])
        cv = curve(ax.ax, L[keep][::-1], Y[keep][::-1], PATCH_C, 4)
        md = Dot(ax.ax.c2p(L[j], Y[j]), radius=0.09, color=PATCH_C)
        bd = Dot(ax.ax.c2p(bl, bs_), radius=0.09, color=TEXT_C)
        ml = label(rf"entropy patches: \ ${100 * Y[j]:.0f}\%$", font_size=22, color=PATCH_C).next_to(md, UR, buff=0.1)
        bll = label(rf"BPE tokens: \ ${100 * bs_:.0f}\%$", font_size=22, color=TEXT_C).next_to(bd, DR, buff=0.1)
        res = label(r"BLT paper (Meta, 2024), \ not this pilot: \ up to $8$ billion parameters \\ and $4$ trillion "
                    r"bytes, \ byte patches matched a tokenizer-based model", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        start = float(sw[j]["start_share"])
        # right panel: share of bytes that start a unit vs share of the surprise those bytes carry
        bw, bh = 0.55, 3.0
        x0, y0 = 2.6, -1.9

        def bar(x, v, color, fill):
            r = Rectangle(width=bw, height=max(bh * v, 0.02), stroke_color=color, stroke_width=1.5,
                          fill_color=color, fill_opacity=fill)
            r.move_to([x, y0, 0], aligned_edge=DOWN)
            t = label(rf"${100 * v:.0f}\%$", font_size=20, color=color).next_to(r, UP, buff=0.08)
            return VGroup(r, t)

        base = Line([x0 - 0.3, y0, 0], [x0 + 3.9, y0, 0], stroke_color=GREY_B, stroke_width=1.5)
        pe = VGroup(bar(x0 + 0.4, start, PATCH_C, 0.25), bar(x0 + 1.0, Y[j], PATCH_C, 0.8))
        pb = VGroup(bar(x0 + 2.4, bpe_start, TEXT_C, 0.25), bar(x0 + 3.0, bs_, TEXT_C, 0.8))
        gl = VGroup(label(r"entropy \\ patches", font_size=20, color=PATCH_C).next_to(pe, DOWN, buff=0.15),
                    label(r"BPE \\ tokens", font_size=20, color=TEXT_C).next_to(pb, DOWN, buff=0.15))
        gl[1].align_to(gl[0], UP)
        key = VGroup(
            VGroup(Square(0.22, stroke_color=GREY_A, stroke_width=1.5, fill_color=GREY_A, fill_opacity=0.25),
                   label(r"scored-byte share \\ at unit starts", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.22, stroke_color=GREY_A, stroke_width=1.5, fill_color=GREY_A, fill_opacity=0.8),
                   label(r"scored-surprise share \\ at unit starts", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([x0 + 1.8, 2.5, 0])
        sweep = label(r"high threshold: \ long patches \\[2pt] low threshold: \ short patches", font_size=22,
                      color=GREY_A).move_to([x0 + 1.8, 0.2, 0])
        with self.voiceover(
            "How well do the patches follow the surprise? Mean length divides all passage bytes by all units, "
            "including the forced initial unit. Start shares and surprise shares use scored bytes only; the "
            "initial unscored byte is excluded. <bookmark mark='a'/> Choose the sampled threshold whose measured "
            f"mean length is nearest to BPE's: approximately {L[j]:.3f} bytes per patch, compared with {bl:.3f} "
            f"per BPE token. These lengths need not be equal. {100 * start:.0f} percent of scored bytes start a "
            f"patch, and carry {100 * Y[j]:.0f} percent of scored surprise. <bookmark mark='b'/> For BPE, "
            f"{100 * bpe_start:.0f} percent of scored bytes start a token and carry {100 * bs_:.0f} percent of "
            "scored surprise. <bookmark mark='c'/> This pilot measures boundary placement, not trained BLT "
            "quality. Separately, the BLT paper reported byte patches matching tokenized models at controlled "
            "compute, up to eight billion parameters."
        ) as vo:
            self.play(FadeIn(ax), Create(cv), FadeIn(sweep), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeOut(sweep), FadeIn(md), FadeIn(ml), FadeIn(base), FadeIn(key), FadeIn(pe), FadeIn(gl[0]))
            vo.wait_until("b")
            self.play(FadeIn(bd), FadeIn(bll), FadeIn(pb), FadeIn(gl[1]))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
