from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import MONO, PART, TEXT_C, load, token_chips

UNI_C = C.MODEL_Q


def lattice_word(word: str, logp: dict, maxlen=12):
    """The pieces of ``word`` in the vocabulary (start, end, log p), and the most probable cut (Viterbi)."""
    arcs = [(i, j, logp[word[i:j]]) for j in range(1, len(word) + 1) for i in range(max(0, j - maxlen), j)
            if word[i:j] in logp]
    best = [0.0] + [-math.inf] * len(word)
    back = [0] * (len(word) + 1)
    for i, j, p in sorted(arcs, key=lambda a: a[1]):
        if best[i] + p > best[j]:
            best[j], back[j] = best[i] + p, i
    path, j = [], len(word)
    while j > 0:
        path.append((back[j], j))
        j = back[j]
    return arcs, path[::-1]


class Unigram(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.lattice()
        self.training()
        self.compare()

    def card(self):
        card = chapter_card(3, r"A probability for every cut", r"Is there a best way to cut a word?", part=PART)
        with self.voiceover("Chapter three. A probability for every cut."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def model(self):
        u = load("unigram")
        V = int(u["sizes"][-1])
        voc = {str(p): float(lp) for p, lp in u[f"vocab{V}"]}
        word = " armchair"

        def all_cuts(w):
            if not w:
                return [[]]
            return [[w[:k]] + rest for k in range(1, len(w) + 1) if w[:k] in voc for rest in all_cuts(w[k:])]

        cuts = sorted(all_cuts(word), key=lambda c: -sum(voc[p] for p in c))[:3]
        dc = definition_card(r"the unigram language model",
                             r"a vocabulary of pieces $v$ with probabilities $p(v)$; \ a cut $s_1 s_2 \dots s_m$ of a word "
                             r"scores $p(s_1)\,p(s_2)\cdots p(s_m)$; \ the word's probability adds up every cut; \ the "
                             r"tokenizer keeps the most probable", width=7.0, color=UNI_C)
        dc.to_corner(UL, buff=0.4)
        eq = cmath(r"P(x)", r"=", r"\sum_{\text{cuts } s \text{ of } x}", r"\ \prod_{i} p(s_i)", font_size=40,
                   colors={r"P(x)": UNI_C}).next_to(dc, DOWN, buff=0.5).align_to(dc, LEFT)
        rows = VGroup()
        for c in cuts:
            chips = token_chips(c, font_size=28, height=0.52)
            sc = sum(voc[p] for p in c)
            val = MathTex(rf"\log_2 p = {sc / math.log(2):.1f}", font_size=28, color=UNI_C)
            rows.add(VGroup(chips, val).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.4, -1.6, 0])
        rl = label(rf"cuts of ``{word.strip()}'' \ (learned probabilities, \ ${V:,}$ pieces)".replace(",", "{,}"),
                   font_size=22, color=GREY_A).next_to(rows, UP, buff=0.3).align_to(rows, LEFT)
        top = int(np.argmax([sum(voc[p] for p in c) for c in cuts]))
        best = SurroundingRectangle(rows[top], color=UNI_C, buff=0.12, corner_radius=0.1)
        cite_ = cite(r"T.~Kudo, \textit{Subword Regularization} (2018)", corner=DR)
        with self.voiceover(
            "Byte-pair encoding cuts each word one way, fixed by the order of its merges. In 2018 Taku Kudo proposed a "
            "model instead. <bookmark mark='a'/> A vocabulary of pieces, each with a probability. A cut of a word "
            "into pieces scores the product of their probabilities, and the word's probability is the sum over every "
            "cut. <bookmark mark='b'/> Here are a few ways to write armchair with the pieces our model learned. "
            "<bookmark mark='c'/> The tokenizer keeps the most probable cut."
        ) as vo:
            self.play(FadeIn(dc), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(best))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lattice(self):
        u = load("unigram")
        V = int(u["sizes"][0])
        voc = {str(p): float(lp) for p, lp in u[f"vocab{V}"]}
        word = " cigarette"
        arcs, path = lattice_word(word, voc)
        n = len(word)
        x0, dx, y0 = -6.2, 0.6, 1.5
        X = [x0 + dx * i for i in range(n + 1)]
        nodes = VGroup(*[Dot([X[i], y0, 0], radius=0.07, color=GREY_B) for i in range(n + 1)])
        letters = VGroup(*[data_text(ch if ch != " " else "·", font=MONO, font_size=28, color=WHITE)
                           .move_to([(X[i] + X[i + 1]) / 2, y0 - 0.35, 0]) for i, ch in enumerate(word)])
        lo, hi = min(p for _, _, p in arcs), max(p for _, _, p in arcs)
        arc_m = VGroup()
        on_path = set(path)
        for i, j, p in arcs:
            if j - i == 1:
                continue
            w = (p - lo) / max(hi - lo, 1e-9)
            a = ArcBetweenPoints([X[i], y0, 0], [X[j], y0, 0], angle=-PI * 0.75, color=UNI_C if (i, j) in on_path else GREY_C,
                                 stroke_width=1 + 4 * w)
            a.set_stroke(opacity=1.0 if (i, j) in on_path else 0.25 + 0.5 * w)
            arc_m.add(a)
        best = token_chips([word[i:j] for i, j in path], font_size=28, height=0.52).move_to([(X[n] + x0) / 2, y0 - 1.5, 0])
        bl = label(r"the most probable cut", font_size=22, color=UNI_C).next_to(best, DOWN, buff=0.15)
        colors = {r"\alpha_j": UNI_C, r"\alpha_i": UNI_C}
        rows = [cmath(r"\alpha_j", r"=", r"\sum_{i < j}", r"\alpha_i", r"\, p(x_{i+1..j})", colors=colors, font_size=34),
                cmath(r"\beta_j", r"=", r"\max_{i < j}", r"\beta_i", r"\, p(x_{i+1..j})", font_size=34),
                MathTex(r"\mathbb{E}[\#v] = \frac{1}{P(x)} \sum_{(i,j):\, x_{i+1..j} = v} \alpha_i\, p(v)\, \beta'_j",
                        font_size=30)]
        whys = [why(r"forward: \ the last piece ends at $j$", font_size=20),
                why(r"Viterbi: \ the best cut instead of the sum", font_size=20),
                why(r"EM's counts, \ from forward $\alpha$ and backward $\beta'$", font_size=20)]
        for r_ in rows:
            r_.scale(0.9)
        step = ladder(self, rows, whys, keep=3, top=0.9, x=3.5, align_index=None, buff=0.38, edge=6.9)
        tag = note(rf"arcs: \ every piece of ``cigarette'' among the ${V:,}$, \ thicker = more probable".replace(",", "{,}"),
                   font_size=20).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Every cut of a word is a path through a lattice. <bookmark mark='a'/> Put a node between each pair of "
            "letters, and an arc for every piece in the vocabulary. A cut is a path from the first node to the last. "
            "<bookmark mark='b'/> The sum over all cuts is computed left to right: the probability of reaching node j "
            "adds up every arc that ends there, from every earlier node, the forward algorithm of Part 7's hidden "
            "Markov models. <bookmark mark='c'/> Replace the sum with a maximum and you get the best cut. <bookmark "
            "mark='d'/> Run it backward as well, and you get how often each piece is expected to be used: what "
            "training needs."
        ) as vo:
            self.play(FadeIn(nodes), FadeIn(letters), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a) for a in arc_m], lag_ratio=0.05), run_time=2.5)
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            self.play(FadeIn(best), FadeIn(bl))
            vo.wait_until("d")
            step(2, transform=False)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        u = load("unigram")
        rep = np.asarray(u["replay"], float)
        sizes = [int(s) for s in u["sizes"]]
        x = np.log10(rep[:, 0])
        y = -rep[:, 1] / math.log(2)  # bits per character
        ax = axes([math.floor(x.min() * 2) / 2, math.ceil(x.max() * 2) / 2, 0.5], [math.floor(y.min() * 10) / 10 - 0.1,
                  math.ceil(y.max() * 10) / 10 + 0.1, 0.2], x_length=7.0, y_length=4.0, xlabel=r"pieces in the vocabulary",
                  ylabel=r"bits per character, \ the unigram model of the novels' words",
                  xticks=[3, 4], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[round(v, 1) for v in np.arange(math.ceil(y.min() * 5) / 5, y.max() + 0.01, 0.2)],
                  center=[-1.8, -0.4, 0])
        pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.06, color=UNI_C) for a, b in zip(x, y)])
        line = curve(ax.ax, x[::-1], y[::-1], UNI_C, 3)
        marks = VGroup()
        for V in sizes:
            k = int(np.argmin(np.abs(rep[:, 0] - V)))
            marks.add(VGroup(Dot(ax.ax.c2p(x[k], y[k]), radius=0.1, color=WHITE),
                             label(rf"${V:,}$: \ ${y[k]:.2f}$".replace(",", "{,}"), font_size=22, color=WHITE)
                             .next_to(ax.ax.c2p(x[k], y[k]), UR, buff=0.15)))
        steps = VGroup(*[label(t, font_size=22, color=c_) for t, c_ in (
            (r"1.\ \ start: \ the most frequent substrings", GREY_A),
            (r"2.\ \ E: \ expected uses of every piece", UNI_C),
            (r"3.\ \ M: \ $p(v) \propto$ its expected uses", UNI_C),
            (r"4.\ \ prune: \ keep the $75\%$ whose loss \\ \ \ \ \ \ \ would cost the most, \ and every letter", GREY_A),
            (r"5.\ \ repeat from 2", GREY_A))]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.45)
        n0 = int(rep[0, 0])
        with self.voiceover(
            "Training starts from far too many pieces: the most frequent substrings of the text, "
            f"{n0:,} of them after the first round. <bookmark mark='a'/> Then expectation-maximization, Part 7's EM: "
            "compute how often each piece is expected to be used, summed over every cut of every word, and set each "
            "probability in proportion. <bookmark mark='b'/> Then prune: for each piece, measure how much the "
            "likelihood would fall without it, keep the three quarters that matter most and every single letter, "
            "and repeat. <bookmark mark='c'/> Here is the model's own measure of the novels, in bits per character, "
            f"as the vocabulary shrinks: smaller vocabularies cost bits, {y[-1] - y[0]:.2f} of them from the first "
            f"round down to {sizes[-1]:,} pieces."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(steps[0]))
            self.play(LaggedStart(*[FadeIn(p_, scale=1.5) for p_ in pts], lag_ratio=0.15), Create(line), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("b")
            self.play(FadeIn(steps[3]), FadeIn(steps[4]))
            vo.wait_until("c")
            self.play(FadeIn(marks))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        u = load("unigram")
        V = int(u["sizes"][-1])
        Vb = int(u["sizes"][0])
        rows = VGroup()
        for name, key, col in ((r"BPE", f"bpe_cut{V}", TEXT_C), (r"unigram", f"cut{V}", UNI_C)):
            chips = token_chips([str(x) for x in u[key]], font_size=22, height=0.44, buff=0.04)
            if chips.width > 10.2:
                chips.width = 10.2
            rows.add(VGroup(label(name, font_size=24, color=col), chips).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 2.3)
        rl = label(rf"the same sentence, \ ${V:,}$ pieces each".replace(",", "{,}"), font_size=22, color=GREY_A)
        rl.next_to(rows, UP, buff=0.15)
        tab = VGroup()
        for VV in (V, Vb):
            tab.add(label(rf"${VV:,}$ pieces: \ ${float(u[f'bpe_cpt_passage{VV}']):.2f}$ (BPE) \ and \ "
                          rf"${float(u[f'cpt_passage{VV}']):.2f}$ (unigram) characters a token; \ "
                          rf"${100 * float(u[f'differ{VV}']):.0f}\%$ of the words cut differently".replace(",", "{,}"),
                          font_size=22, color=GREY_A))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(UP * 0.55)
        if tab.width > 13:
            tab.width = 13
        samp = u[f"samples{Vb}"]
        sw = " cigarette"
        cuts = [[str(x) for x in c] for c in samp[sw]]
        uniq = []
        for c in cuts:
            if c not in uniq:
                uniq.append(c)
        sg = VGroup(*[token_chips(c, font_size=24, height=0.46) for c in uniq[:4]]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        sl = label(r"sampled cuts \ ($p^{0.3}$): \ subword regularization", font_size=22, color=UNI_C)
        sgg = VGroup(sl, sg).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([-3.3, -1.9, 0])
        sp = label(r"SentencePiece (2018): \ the unigram model or BPE \\ on raw text, \ spaces as a symbol \ ($\_$); \\ "
                   r"used by T5, \ Llama 1 and 2, \ Gemma", font_size=22, color=GREY_A).move_to([3.4, -1.9, 0])
        cpb, cpu = float(u[f"bpe_cpt_passage{V}"]), float(u[f"cpt_passage{V}"])
        differ = 100 * float(u[f"differ{V}"])
        verdict = ("the unigram model's tokens are a little longer" if cpu > cpb + 0.02 else
                   "BPE's tokens are a little longer" if cpb > cpu + 0.02 else "the two come out almost the same length")
        with self.voiceover(
            f"How different are the two? <bookmark mark='a'/> At {V:,} pieces each, on the scoreboard's passage, "
            f"{verdict}: {cpb:.2f} characters a token for BPE, {cpu:.2f} for the unigram model, and "
            f"{differ:.0f} percent of the words are cut differently. <bookmark mark='b'/> The "
            "unigram model can also sample cuts instead of taking the best, so a model in training sees the same "
            "word written several ways; Kudo called it subword regularization. <bookmark mark='c'/> His "
            "SentencePiece library runs either method on raw text, with the space as just another symbol, and it "
            "cut the text for T5, the first two Llamas and Gemma."
        ) as vo:
            self.play(FadeIn(rl), FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(sl), LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.2) for s_ in sg], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(sp))
        self.wait(0.3)
        self.clear_scene()
