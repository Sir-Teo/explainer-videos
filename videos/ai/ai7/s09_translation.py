from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import HIDDEN, MONO, PART, card_in, heat_grid, load, recolor_grid

FR, EN = "#58A6FF", "#FF9F45"
ALIGN = C.BITS


def words_row(ws, color, font_size=24, buff=0.25) -> VGroup:
    return VGroup(*[data_text(w, font=MONO, font_size=font_size, color=color) for w in ws]).arrange(RIGHT, buff=buff)


class Translation(VoiceoverScene):
    def construct(self):
        card_in(self, 8, r"Translation by counting", r"Can a machine learn to translate from examples alone?",
                "Chapter eight. Translation by counting.")
        self.channel()
        self.model1()
        self.bleu()

    # ------------------------------------------------------------------
    def channel(self):
        q = VGroup(label(r"``When I look at an article in Russian, I say: \ `This is really written in English, \\ but it "
                         r"has been coded in some strange symbols. \ I will now proceed to decode.'\,''", font_size=26,
                         color=C.HUMAN),
                   label(r"--- Warren Weaver, letter to Norbert Wiener (1947), quoted in his memorandum \textit{Translation} "
                         r"(1949)", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        e = VGroup(RoundedRectangle(width=2.6, height=0.9, corner_radius=0.12, stroke_color=EN),
                   label(r"English $e$", font_size=26, color=EN))
        ch = VGroup(RoundedRectangle(width=2.8, height=0.9, corner_radius=0.12, stroke_color=GREY_B),
                    label(r"a noisy channel", font_size=26, color=GREY_B))
        f = VGroup(RoundedRectangle(width=2.6, height=0.9, corner_radius=0.12, stroke_color=FR),
                   label(r"French $f$", font_size=26, color=FR))
        for b in (e, ch, f):
            b[1].move_to(b[0])
        row = VGroup(e, ch, f).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.3)
        arr = VGroup(Arrow(e.get_right(), ch.get_left(), buff=0.1, color=GREY_B),
                     Arrow(ch.get_right(), f.get_left(), buff=0.1, color=GREY_B))
        colors = {r"P(e)": EN, r"P(f \mid e)": FR}
        eq = cmath(r"\hat e", r"=", r"\arg\max_e", r"\;P(e)", r"\;P(f \mid e)", colors=colors, font_size=46)
        eq.next_to(row, DOWN, buff=0.6)
        br = VGroup(brace_note(term(eq, r"\;P(e)"), r"a language model \\ (counting, chapter 9)", color=EN, font_size=22),
                    brace_note(term(eq, r"\;P(f \mid e)"), r"a translation model \\ (learned by EM)", color=FR, font_size=22))
        hist = VGroup(history_card(1966, r"the ALPAC report", r"machine translation judged a failure; \ funding cut",
                                   width=4.2),
                      history_card(1990, r"P.~Brown, J.~Cocke, S.~Della Pietra, V.~Della Pietra, F.~Jelinek, \dots",
                                   r"IBM: \ translation learned from the Canadian parliament's French and English "
                                   r"records", width=5.6)).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 1947 Warren Weaver, who had run wartime research for the United States, wrote that a Russian article "
            "might be English written in a strange code, waiting to be decoded. <bookmark mark='a'/> The first decades "
            "of machine translation used rules instead, and in 1966 a government report, ALPAC, judged them a failure. "
            "<bookmark mark='b'/> Twenty years later, Jelinek's speech group at IBM took Weaver literally. Pretend "
            "the French was English, sent through a noisy channel. <bookmark mark='c'/> To decode, find the English "
            "sentence that is likely in itself, by a language model, and likely to come out as this French, by a "
            "translation model. <bookmark mark='d'/> They learned the translation model, with EM, from more than a "
            "million pairs of sentences from the Canadian parliament's proceedings, published in both languages."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(hist[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(e), GrowArrow(arr[0]), FadeIn(ch), GrowArrow(arr[1]), FadeIn(f))
            vo.wait_until("c")
            self.play(Write(eq), FadeOut(hist[0]))
            self.play(FadeIn(br))
            vo.wait_until("d")
            self.play(FadeOut(br), FadeIn(hist[1], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model1(self):
        d = load("ibm1")
        A = np.asarray(d["align"])
        lls = np.asarray(d["lls"])
        fr, en = d["example"][0].split(), d["example"][1].split()
        pairs = [("la maison", "the house"), ("la maison bleue", "the blue house"), ("le chat", "the cat"),
                 ("le chat noir", "the black cat"), ("le chien mange", "the dog eats"),
                 ("le chat mange le poisson", "the cat eats the fish"), ("un poisson rouge", "a red fish"),
                 ("le chat voit un poisson", "the cat sees a fish")]
        corpus = VGroup(*[VGroup(data_text(f, font=MONO, font_size=17, color=FR),
                                 data_text(e, font=MONO, font_size=17, color=EN)) for f, e in pairs])
        for r in corpus:
            r[1].next_to(r[0], RIGHT, buff=0.3)
        corpus.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-4.6, 0.4, 0])
        cl = label(rf"$8$ of our ${d['n_train']}$ sentence pairs", font_size=20, color=GREY_A).next_to(corpus, UP, buff=0.2)
        grid = heat_grid(A[0], cell=0.62, color=ALIGN).move_to([1.3, 0.2, 0])
        cols = VGroup(*[data_text(w, font=MONO, font_size=20, color=FR if w != "NULL" else GREY_B)
                        .rotate(0.6).next_to(grid[j], UP, buff=0.12) for j, w in enumerate(["NULL"] + fr)])
        rows_ = VGroup(*[data_text(w, font=MONO, font_size=22, color=EN).next_to(grid[i * (len(fr) + 1)], LEFT, buff=0.15)
                         for i, w in enumerate(en)])
        gl = label(r"$p(\text{this French word made this English word})$", font_size=20, color=ALIGN).next_to(grid, DOWN, buff=0.2)
        colors = {r"t(e_j \mid f_i)": ALIGN}
        eq = cmath(r"P(e \mid f)", r"\propto", r"\prod_j \sum_{i}", r"t(e_j \mid f_i)", colors=colors, font_size=34)
        eq.to_edge(UP, buff=0.25).shift(RIGHT * 2.2)
        en_ = label(r"IBM Model 1: \ every alignment equally likely", font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.1)
        rv = Integer(0, font_size=30)
        rl = VGroup(label(r"EM round", font_size=24, color=GREY_A), rv).arrange(RIGHT, buff=0.15).move_to([5.4, 1.4, 0])
        g = axes([0, len(lls), 10], [float(lls.min()) - 5, float(lls.max()) + 5, 20], x_length=2.6, y_length=1.8,
                 ylabel=r"log-likelihood", font_size=16, center=[5.4, -1.0, 0])
        it = ValueTracker(1)
        lc = always_redraw(lambda: curve(g.ax, np.arange(1, int(it.get_value()) + 1), lls[:int(it.get_value())], C.BITS, 3)
                           if it.get_value() >= 2 else VMobject())
        best = d["show_best"]
        with self.voiceover(
            f"Here's IBM's Model 1, on a tiny parallel corpus of {d['n_train']} French and English sentences that we "
            "wrote. <bookmark mark='a'/> The model has one table: t of e given f, the chance that a French word turns "
            "into an English word. Each English word picks some French word to come from, any of them equally "
            "likely, and the words that align are hidden. <bookmark mark='b'/> EM again. Start with every "
            "translation equally likely. <bookmark mark='c'/> In the E step, each English word spreads its credit over "
            "the French words in its sentence; in the M step, the table is rebuilt from that credit. Because 'chat' "
            "appears exactly where 'cat' does, the credit piles up, and 'le' is pushed toward 'the', which frees "
            f"'chat'. <bookmark mark='d'/> After thirty rounds, 'chat' becomes '{best[3][0]}' with probability "
            f"{best[3][1]:.2f}, and the alignment of this sentence is sharp, though Model 1 can't tell the two "
            "'le's apart: it has no idea of word order."
        ) as vo:
            self.play(FadeIn(cl), LaggedStart(*[FadeIn(r) for r in corpus], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(en_))
            vo.wait_until("b")
            self.play(FadeIn(grid), FadeIn(cols), FadeIn(rows_), FadeIn(gl), FadeIn(rl), FadeIn(g))
            vo.wait_until("c")
            self.add(lc)
            for k in (1, 2, 3, 5, 8, 12):
                self.play(*recolor_grid(grid, A[k], color=ALIGN), ChangeDecimalToValue(rv, k), it.animate.set_value(k),
                          run_time=0.9)
            vo.wait_until("d")
            last = len(A) - 1
            self.play(*recolor_grid(grid, A[last], color=ALIGN), ChangeDecimalToValue(rv, last), it.animate.set_value(last),
                      run_time=1.5)
        lc.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bleu(self):
        d = load("ibm1")
        b1, b2 = d["bleu_gloss"], d["bleu_rule"]
        tests = d["test"]
        rows = VGroup()
        for (f, e), h1, h2 in zip(tests, d["hyp_gloss"], d["hyp_rule"]):
            rows.add(VGroup(data_text(f, font=MONO, font_size=18, color=FR), data_text(h1, font=MONO, font_size=18, color=EN),
                            data_text(e, font=MONO, font_size=18, color=GREY_B)))
        for r in rows:
            r[1].move_to([-1.2, 0, 0], aligned_edge=LEFT)
            r[2].move_to([2.9, 0, 0], aligned_edge=LEFT)
            r[0].move_to([-6.6, 0, 0], aligned_edge=LEFT)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for r in rows:
            r[0].set_x(-6.6 + r[0].width / 2)
            r[1].set_x(-2.4 + r[1].width / 2)
            r[2].set_x(1.9 + r[2].width / 2)
        rows.shift(UP * (1.7 - rows.get_y()))
        heads = VGroup(label(r"held-out French", font_size=20, color=FR), label(r"word by word", font_size=20, color=EN),
                       label(r"reference", font_size=20, color=GREY_B))
        for h_, x_ in zip(heads, (-6.6, -2.4, 1.9)):
            h_.next_to(rows, UP, buff=0.2).set_x(x_ + h_.width / 2)
        colors = {r"p_n": C.BITS, r"\mathrm{BP}": GREY_A}
        eq = cmath(r"\mathrm{BLEU}", r"=", r"\mathrm{BP}", r"\cdot", r"\exp\Big(\tfrac14 \sum_{n=1}^{4} \log", r"p_n",
                   r"\Big)", colors=colors, font_size=38).move_to([-3.2, -1.5, 0])
        en_ = label(r"$p_n$: \ the share of the output's $n$-word runs found in the reference; \\ BP: \ a penalty for "
                    r"output shorter than the reference", font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.2)
        pn = np.asarray(b1["p"])
        nums = VGroup(*[label(rf"$p_{n + 1} = {pn[n]:.2f}$", font_size=24, color=C.BITS) for n in range(4)])
        nums.arrange(RIGHT, buff=0.35).move_to([3.4, -1.1, 0])
        s1 = label(rf"BLEU, word by word: \ ${b1['bleu']:.2f}$", font_size=28, color=EN).next_to(nums, DOWN, buff=0.3)
        s2 = label(rf"with one rule, \ adjectives after their noun: \ ${b2['bleu']:.2f}$", font_size=26, color=C.BITS)
        s2.next_to(s1, DOWN, buff=0.25)
        fixes = VGroup(*[SurroundingRectangle(r[1], color=C.SURPRISE, buff=0.05) for r, h1, (f, e) in
                         zip(rows, d["hyp_gloss"], tests) if h1 != e])
        better = b2["bleu"] > b1["bleu"]
        verdict = (f"Word by word, our Model 1 scores {b1['bleu']:.2f}. Swap French adjectives in front of their nouns, "
                   f"one rule a linguist would write, and it rises to {b2['bleu']:.2f}." if better else
                   f"Word by word, our Model 1 scores {b1['bleu']:.2f}; one reordering rule leaves it at {b2['bleu']:.2f}.")
        later = VGroup(label(r"IBM Models 2--5: \ word order, \ fertility", font_size=22, color=GREY_A),
                       label(r"2003: \ phrase-based translation", font_size=22, color=GREY_A),
                       label(r"2014: \ attention, \ a learned soft alignment \ (Part 13)", font_size=22, color=HIDDEN))
        later.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Now translate sentences it never saw, one word at a time, using the table. <bookmark mark='a'/> Some come "
            "out right. Others put the adjective after the noun, French style. How good is that? In 2002 Kishore "
            "Papineni and colleagues at IBM proposed a score anyone can compute: BLEU. <bookmark mark='b'/> Count what "
            "share of the output's single words, pairs, triples and runs of four appear in a human reference, average "
            "their logs, and penalize output that's too short. <bookmark mark='c'/> " + verdict +
            " <bookmark mark='d'/> Real systems learned their own word order: IBM's later models, then phrase-based "
            "translation, which ran Google Translate from 2006 until neural networks replaced it in 2016. And the "
            "alignment table of Model 1 came back as attention, a learned soft alignment, in 2014."
        ) as vo:
            self.play(FadeIn(heads), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(fixes))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(en_))
            self.play(LaggedStart(*[FadeIn(n_) for n_ in nums], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(s1))
            self.play(FadeIn(s2), FadeOut(fixes))
            vo.wait_until("d")
            self.play(FadeOut(VGroup(eq, en_)), LaggedStart(*[FadeIn(m) for m in later], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()
