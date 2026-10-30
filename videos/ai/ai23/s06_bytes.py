from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import MONO, PART, SURP_C, TEXT_C, load, token_chips

PATCH_C = C.CONTEXT


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
        rl = label(r"UTF-8: \ every character as $1$ to $4$ bytes, \ $256$ possible values", font_size=22, color=GREY_A)
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
        p = load("patches")
        ex = str(p["example"])[:40]
        bs = ex.encode("utf-8")
        H = np.asarray(p["example_H"], float)[:len(bs)]
        th = float(p["threshold"])
        cell = 0.3
        rows = VGroup()
        # bytes
        r0 = VGroup(*[Square(cell, stroke_color=GREY_B, stroke_width=1, fill_color=GREY_B, fill_opacity=0.15) for _ in bs])
        r0.arrange(RIGHT, buff=0.02)
        letters = VGroup(*[data_text(chr(c) if c != 32 else "·", font=MONO, font_size=16, color=WHITE).move_to(sq)
                           for c, sq in zip(bs, r0)])

        def grouped(starts, color):
            g = VGroup()
            i = 0
            while i < len(bs):
                j = i + 1
                while j < len(bs) and not starts[j]:
                    j += 1
                w = (j - i) * (cell + 0.02) - 0.02
                g.add(RoundedRectangle(width=w, height=cell + 0.08, corner_radius=0.06, stroke_color=color, stroke_width=2,
                                       fill_color=color, fill_opacity=0.15).move_to(
                    r0[i].get_left() + RIGHT * w / 2))
                i = j
            return g

        fixed = [k % 4 == 0 for k in range(len(bs))]
        ent = [k == 0 or H[k] > th for k in range(len(bs))]
        lab = [label(t, font_size=22, color=c_) for t, c_ in ((r"bytes: \ ByT5 (2021)", GREY_B),
                                                              (r"fixed patches: \ MegaByte (2023)", C.MODEL_Q),
                                                              (r"entropy patches: \ BLT (2024)", PATCH_C))]
        y = [1.6, 0.0, -1.6]
        groups = []
        for k, (yy, l_) in enumerate(zip(y, lab)):
            base = VGroup(r0.copy(), letters.copy()).move_to([0.6, yy, 0])
            l_.next_to(base, UP, buff=0.18).align_to(base, LEFT)
            if k == 0:
                groups.append(VGroup(base, l_))
            else:
                box = grouped(fixed if k == 1 else ent, C.MODEL_Q if k == 1 else PATCH_C)
                box.move_to(base[0]).align_to(base[0], LEFT)
                groups.append(VGroup(base, box, l_))
        n_fix = sum(fixed)
        n_ent = sum(ent)
        cite_ = cite(r"Xue et al.\ (2021); \ Yu et al.\ (2023); \ Pagnoni et al.\ (2024)", corner=DR)
        with self.voiceover(
            "Could a model skip the tokenizer and read bytes? <bookmark mark='a'/> Google's ByT5, in 2021, did exactly "
            "that, at the price of sequences several times longer than BPE's. <bookmark mark='b'/> In 2023 Meta's "
            "MegaByte grouped the bytes into fixed patches: a big transformer looks at the patches, and a small one "
            "writes the bytes inside each. <bookmark mark='c'/> But a fixed patch spends as much on the end of a "
            "predictable word as on its surprising start. In December 2024 Meta's Byte Latent Transformer let the "
            "data decide: a small byte model reads ahead, and a new patch starts wherever it is unsure of the next "
            f"byte. Here, the same {len(bs)} bytes become {n_fix} fixed patches or {n_ent} entropy patches."
        ) as vo:
            self.play(FadeIn(groups[0]), FadeIn(cite_))
            vo.wait_until("b")
            self.play(FadeIn(groups[1]))
            vo.wait_until("c")
            self.play(FadeIn(groups[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def entropy(self):
        p = load("patches")
        ex = str(p["example"])
        bs = ex.encode("utf-8")
        H = np.nan_to_num(np.asarray(p["example_H"], float)[:len(bs)])
        S = np.nan_to_num(np.asarray(p["example_S"], float)[:len(bs)])
        th = float(p["threshold"])
        n = len(bs)
        W = 13.0
        dx = W / n
        x0 = -W / 2
        hmax = max(5.0, float(H.max()) + 0.3)
        sy = 3.6 / hmax
        base_y = -1.2
        bars = VGroup(*[Rectangle(width=dx * 0.8, height=max(h * sy, 0.01), stroke_width=0,
                                  fill_color=PATCH_C if (k == 0 or h > th) else GREY_C, fill_opacity=0.85)
                        .move_to([x0 + dx * (k + 0.5), base_y + h * sy / 2, 0]) for k, h in enumerate(H)])
        sdots = VGroup(*[Dot([x0 + dx * (k + 0.5), base_y + min(s, hmax) * sy, 0], radius=0.035, color=SURP_C)
                         for k, s in enumerate(S)])
        letters = VGroup(*[data_text(chr(c) if c != 32 else "·", font=MONO, font_size=15, color=WHITE)
                           .move_to([x0 + dx * (k + 0.5), base_y - 0.25, 0]) for k, c in enumerate(bs)])
        thl = DashedLine([x0, base_y + th * sy, 0], [x0 + W, base_y + th * sy, 0], color=WHITE, stroke_width=2)
        thlab = label(rf"threshold: \ ${th:.2f}$ bits", font_size=20, color=WHITE).move_to(
            [x0 + W - 1.0, base_y + hmax * sy + 0.25, 0])
        yl = label(r"bars: \ the byte model's uncertainty about the next byte (entropy, \ bits); \ dots: \ "
                   r"its surprise at the byte that came", font_size=20, color=GREY_A).to_edge(UP, buff=0.4)
        bpe = np.asarray(p["example_bpe"], bool)[:n]
        bmarks = VGroup(*[Line([x0 + dx * k, base_y - 0.48, 0], [x0 + dx * k, base_y - 0.68, 0], color=TEXT_C, stroke_width=2.5)
                          for k in range(n) if bpe[k]])
        bml = label(r"BPE's token starts", font_size=18, color=TEXT_C).next_to(bmarks, DOWN, buff=0.08).to_edge(LEFT, buff=0.3)
        tag = note(r"our byte model: \ the byte-level transformer of chapter four (seed $0$)", font_size=18).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Here is that idea on our own byte model, the byte-level transformer from chapter four, reading a line "
            "of the passage. <bookmark mark='a'/> Each bar is how unsure the model is about the next byte: its "
            "entropy, in bits. The dots are how surprised it was by the byte that actually came. <bookmark mark='b'/> "
            "At the start of a word the next letter is wide open; inside a word, after a few letters, the rest is "
            "almost certain. <bookmark mark='c'/> Start a new patch wherever the entropy crosses a threshold, and the "
            "patches follow the information: short where the text is surprising, long where it is predictable."
        ) as vo:
            self.play(FadeIn(yl), FadeIn(letters), FadeIn(tag))
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
        p = load("patches")
        sw = p["sweep"]
        L = np.array([s["mean_len"] for s in sw])
        Y = np.array([s["surprise_share"] for s in sw])
        j = int(p["match"])
        bl, bs_ = float(p["bpe_len"]), float(p["bpe_share"])
        xm = float(min(8.0, L.max()))
        keep = L <= xm
        ax = axes([1, xm, 1], [0, 1, 0.2], x_length=6.4, y_length=4.2, xlabel=r"average patch length, \ bytes",
                  ylabel=r"share of the surprise on a patch's first byte", xticks=list(range(1, int(xm) + 1)),
                  yticks=[0, 0.5, 1], yfmt=lambda v: f"{int(round(100 * v))}\\%", center=[-2.6, -0.3, 0])
        cv = curve(ax.ax, L[keep][::-1], Y[keep][::-1], PATCH_C, 4)
        md = Dot(ax.ax.c2p(L[j], Y[j]), radius=0.09, color=PATCH_C)
        bd = Dot(ax.ax.c2p(bl, bs_), radius=0.09, color=TEXT_C)
        ml = label(rf"entropy patches: \ ${100 * Y[j]:.0f}\%$", font_size=22, color=PATCH_C).next_to(md, UR, buff=0.1)
        bll = label(rf"BPE tokens: \ ${100 * bs_:.0f}\%$", font_size=22, color=TEXT_C).next_to(bd, DR, buff=0.1)
        res = label(r"BLT (Meta, 2024): \ in a FLOP-controlled study up to $8$ billion parameters \\ and $4$ trillion "
                    r"bytes, \ byte patches matched a tokenizer-based model", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        start = float(sw[j]["start_share"])
        with self.voiceover(
            "How well do the patches follow the surprise? Sweep the threshold, and for each, measure the average "
            "patch length and the share of the model's total surprise that falls on the first byte of a patch. "
            f"<bookmark mark='a'/> At the threshold where patches are as long as our BPE tokens, {bl:.2f} bytes on "
            f"average, {100 * start:.0f} percent of the bytes start a patch, and they carry {100 * Y[j]:.0f} percent "
            f"of the surprise. <bookmark mark='b'/> BPE's token starts, about as many, carry {100 * bs_:.0f} percent. "
            "<bookmark mark='c'/> That is the case for patches: spend the big model's steps where the information "
            "is. Meta's study found byte patches matching a tokenized model of the same compute, up to 8 billion "
            "parameters."
        ) as vo:
            self.play(FadeIn(ax), Create(cv), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(md), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(bd), FadeIn(bll))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
