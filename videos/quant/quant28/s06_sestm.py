from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import text as TX
from videos.quant.quant28.common import DOVE, HAWK, HURDLE, IS_C, OOS_C, PART, WORD, fit_right, house_lab, load


class SESTM(VoiceoverScene):
    def construct(self):
        s = load("sestm")
        self.card()
        self.paper()
        self.model()
        self.screen(s)
        self.topics(s)
        self.lab(s)
        self.result(s)
        self.question(s)

    def card(self):
        c = chapter_card(5, r"Supervised words: SESTM", r"Can the market's reactions teach us which words matter?",
                         part=PART)
        with self.voiceover("Chapter five. Instead of deciding in advance which words are good or bad, let the market's "
                            "reactions decide. Can a model learn which words matter, and how much?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def paper(self):
        card = firm_card(r"Ke, Kelly and Xiu (2019)", r"`Predicting returns with text data' (SESTM: sentiment "
                         r"extraction via screening and topic modelling): Dow Jones Newswires, 1989--2017, 22.5 million "
                         r"articles, each tagged to the stock it is about and labelled by that stock's return",
                         numbers=((r"4.29", r"annualised Sharpe ratio, equal-weighted daily long-short on next-day "
                                            r"returns, before costs"),
                                  (r"1.33", r"value-weighted"), (r"\checkmark", r"beats the Loughran--McDonald "
                                                                        r"dictionary and RavenPack's commercial scores")),
                         source=r"Ke, Kelly and Xiu, NBER working paper 26186", kind=r"Paper file", width=10.6,
                         font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "In 2019 Zheng Tracy Ke, Bryan Kelly and Dacheng Xiu took twenty-two and a half million Dow Jones news "
            "articles, each about one stock, and labelled each with that stock's return. <bookmark mark='a'/> Their "
            "method learned its own positive and negative words from the returns. Trading on it the next day, "
            "equal-weighted, earned an annualised Sharpe ratio of four point two nine before costs; value-weighted, "
            "one point three three. <bookmark mark='b'/> In the authors' reported stock sample, it beat the Loughran and McDonald dictionary and "
            "RavenPack's scores. Those are attributed paper results, not our FOMC replication or a promise of attainable returns."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def model(self):
        rows = [cmath(r"d_{i,[S]}", r"\sim", r"\mathrm{Multinomial}\big(s_i,\ p_i\,O_+ + (1 - p_i)\,O_-\big)", font_size=32,
                      colors={r"d_{i,[S]}": WORD}),
                cmath(r"\Pr(y_i > 0 \mid p_i)", r"=", r"g(p_i),\qquad g \text{ increasing}", font_size=32, colors={r"\Pr(y_i > 0 \mid p_i)": HAWK}),
                cmath(r"f_j", r"=", r"\frac{\#\{i : \text{word } j \in i,\ y_i > 0\}}{\#\{i : \text{word } j \in i\}}", font_size=32,
                      colors={r"f_j": HURDLE}),
                cmath(r"\hat p", r"=", r"\arg\max_p \sum_{j \in \hat S} d_j \log\big(p\,\hat O_{+,j} + (1 - p)\,\hat O_{-,j}\big) + "
                      r"\lambda\log p(1 - p)", font_size=28, colors={r"\hat p": WORD})]
        whys = [why(r"the model: only the sentiment-charged words $S$ carry the article's tone $p_i$, as a mixture of a "
                    r"positive topic and a negative topic; neutral words are left unmodelled"),
                why(r"the return depends on the text only through $p_i$, and more positive tone means a higher chance "
                    r"of a positive return"),
                why(r"screen: of the articles containing word $j$, the share with positive returns. Keep the words far "
                    r"from the overall share, seen in at least $\kappa$ articles"),
                why(r"then estimate $O_\pm$ by regressing word frequencies on the articles' return ranks, and score a new "
                    r"article by penalized likelihood (the penalty pulls $\hat p$ toward $\frac12$)")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The model is simple enough to write down. <bookmark mark='a'/> Each article has a tone p between zero and "
            "one. Its sentiment-charged words are drawn from a mixture: a positive topic with weight p, a negative topic "
            "with weight one minus p. Every other word is left out of the model. <bookmark mark='b'/> The return depends "
            "on the text only through p, and a more positive tone means a higher chance of a positive return. "
            "<bookmark mark='c'/> Step one, the screen: for each word, among the articles that contain it, what share "
            "had positive returns? Keep the words whose share is far from the overall one, and that appear often "
            "enough to trust. <bookmark mark='d'/> Step two, estimate the two topics by regressing the kept words' "
            "frequencies on the articles' return ranks. Step three, score a new article by penalized maximum "
            "likelihood on a finite grid; the penalty pulls every score toward neutral. The rank regression is clipped at zero and its two columns normalised; it is an implementation choice, not an exact latent-topic posterior."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def screen(self, s):
        f = np.asarray(s["f_all"], float)
        k = np.asarray(s["k_all"], float)
        vocab = s["vocab"]
        g = axes([np.log10(3), np.log10(max(k.max(), 10)) + 0.05], [0, 1], x_length=7.6, y_length=4.6,
                 xlabel=r"statements containing the word (log scale)", ylabel=r"$f_j$: share of them with the yield up",
                 xticks=[np.log10(3), 1, 2], yticks=[0, 0.5, 1], xfmt=lambda v: f"{10 ** v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        sel_p = set(int(i) for i in np.flatnonzero((k >= s["kappa"]) & (f >= s["pi"] + s["alpha"])))
        sel_n = set(int(i) for i in np.flatnonzero((k >= s["kappa"]) & (f <= s["pi"] - s["alpha"])))
        jit = np.random.default_rng(0).uniform(-0.012, 0.012, len(f))
        dots = VGroup(*[Dot(ax.c2p(np.log10(max(kk, 3)), min(max(ff + jj, 0), 1)), radius=0.028,
                            color=HAWK if i in sel_p else DOVE if i in sel_n else GREY_C,
                            fill_opacity=0.9 if (i in sel_p or i in sel_n) else 0.35)
                        for i, (ff, kk, jj) in enumerate(zip(f, k, jit)) if kk >= 3])
        hi = DashedLine(ax.c2p(np.log10(3), s["pi"] + s["alpha"]), ax.c2p(ax.x_range[1], s["pi"] + s["alpha"]), color=HURDLE)
        lo = DashedLine(ax.c2p(np.log10(3), s["pi"] - s["alpha"]), ax.c2p(ax.x_range[1], s["pi"] - s["alpha"]), color=HURDLE)
        kap = DashedLine(ax.c2p(np.log10(s["kappa"]), 0), ax.c2p(np.log10(s["kappa"]), 1), color=HURDLE)
        side = VGroup(label(r"kept, yield up", font_size=18, color=HAWK),
                      *[label(rf"\texttt{{{w}}}\ {ff:.2f}", font_size=16) for w, ff, _ in s["pos"][:7]],
                      label(r"kept, yield down", font_size=18, color=DOVE),
                      *[label(rf"\texttt{{{w}}}\ {ff:.2f}", font_size=16) for w, ff, _ in s["neg"][:7]]
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.09).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            f"Here is the screen on the FOMC statements, trained on the {s['n_train']} statements to 2012, with the "
            "two-year yield's move as the label. <bookmark mark='a'/> Each dot is a word: how many statements contain "
            "it, across, and the share of those statements on which the yield rose, up. <bookmark mark='b'/> The "
            f"thresholds were chosen by validating on 2007 to 2012: keep words at least {s['alpha']:.2f} away from the "
            f"overall share, in at least {s['kappa']} statements. {s['n_pos']} words survive on the hawkish side and "
            f"{s['n_neg']} on the dovish. <bookmark mark='c'/> Some make sense: inflationary, robust, removed, as in "
            "removing accommodation, on the side of rising yields; slower, constrained, wealth on the other. Others, "
            "like even and after, look like accidents of a small sample. The vocabulary was built through 2012 before the early fit, so validation-year document frequencies enter preprocessing. Zero and missing yield changes are excluded. This is not a fully point-in-time validation pipeline."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.002), run_time=2)
            vo.wait_until("b")
            self.play(Create(hi), Create(lo), Create(kap))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def topics(self, s):
        w = s["words"]
        Op, On = np.asarray(s["O_pos"], float), np.asarray(s["O_neg"], float)
        d = Op - On
        order = np.argsort(d)
        pick = list(order[:6]) + list(order[-6:])
        g = axes([-0.12, 0.12], [0, len(pick)], x_length=7.0, y_length=4.8, xlabel=r"$\hat O_{+,j} - \hat O_{-,j}$: weight in "
                 r"the hawkish topic minus the dovish", ylabel=r"", xticks=[-0.1, 0, 0.1], yticks=[], font_size=15).move_to(
            RIGHT * 0.6 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for k, j in enumerate(pick):
            y = k + 0.5
            v = float(np.clip(d[j], -0.12, 0.12))
            b = Line(ax.c2p(0, y), ax.c2p(v, y), color=HAWK if v > 0 else DOVE, stroke_width=14)
            t = label(rf"\texttt{{{w[j]}}}", font_size=16, color=GREY_A).next_to(ax.c2p(0, y), LEFT if v > 0 else RIGHT, buff=0.15)
            bars.add(VGroup(b, t))
        with self.voiceover(
            "Step two turns the kept words into two topics. <bookmark mark='a'/> Regress each statement's frequencies of "
            "the kept words on its rank among the yield moves: the fitted weights at the top rank are the hawkish "
            "topic, at the bottom the dovish one. <bookmark mark='b'/> Here is each word's weight in the hawkish topic "
            "minus its weight in the dovish. These are the weights the score will use; a new statement's tone is "
            "whichever mixture of the two topics best explains its words."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.1))
        self.wait(0.4)
        self.clear_scene()


    def lab(self, s):
        card = house_lab(r"SESTM, step one", TX.sestm_screen, "D = np.asarray(D)", 12, width=8.6)
        card.to_edge(LEFT, buff=0.4).shift(UP * 0.5)
        with self.voiceover(
            "The screen itself is a dozen lines of the House's text module. <bookmark mark='a'/> Which documents contain "
            "each word; how many; the share with a positive label; and two thresholds. Run on the statements to 2012, "
            f"it keeps {s['n_pos'] + s['n_neg']} words out of {s['n_vocab']}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"vocabulary {s['n_vocab']} words; pi = {s['pi']:.3f}",
                                 f"alpha = {s['alpha']:.2f}, kappa = {s['kappa']}",
                                 f"kept: {s['n_pos']} hawkish, {s['n_neg']} dovish"], direction=RIGHT, aligned_edge=UP)
        self.wait(0.4)
        self.clear_scene()

    def result(self, s):
        panels = VGroup()
        for key_s, key_y, title, col in (("train_score", "train_y", r"trained on: 1997--2012", IS_C),
                                         ("test_score", "test_y", r"never seen: 2013--2020", OOS_C)):
            g = axes([0, 1], [-30, 30], x_length=5.2, y_length=3.6, xlabel=r"SESTM score $\hat p$", ylabel=title,
                     xticks=[0, 0.5, 1], yticks=[-30, 0, 30], font_size=14)
            ax = g.ax
            dots = VGroup(*[Dot(ax.c2p(a, max(min(b, 30), -30)), radius=0.045, color=col, fill_opacity=0.8)
                            for a, b in zip(s[key_s], s[key_y])])
            panels.add(VGroup(g, dots))
        panels.arrange(RIGHT, buff=0.9).move_to(UP * 0.3)
        foot = wrapped_label(rf"rank correlation of score with the two-year move: {s['rho_train']:.2f} on the training "
                             rf"statements, {s['rho']:.2f} on the {s['n_test']} later ones ($p = {s['p_rho']:.2f}$); the sign "
                             rf"is right on {100 * s['hit']:.0f}\% of them", 11.4, 18, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Did it learn anything? <bookmark mark='a'/> On the statements it was trained on, the score lines up with "
            f"the yield's move: a rank correlation of {s['rho_train']:.2f}. <bookmark mark='b'/> On the {s['n_test']} "
            f"statements from 2013 to 2020 that it never saw, the correlation is {s['rho']:.2f}, with a p-value of "
            f"{s['p_rho']:.2f}."
            f" The sign is right {100 * s['hit']:.0f} percent of the time. <bookmark mark='c'/> Ke, Kelly and Xiu had "
            f"twenty-two million articles; we have {s['n_train']} statements. Screening hundreds of words on "
            "a hundred labels can fit chance, and regime change or misspecification can also weaken transfer. This comparison alone does not identify the cause. How many documents the screen needs is a "
            "theorem, and it is this part's research chapter."
        ) as vo:
            self.play(FadeIn(panels[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(foot))
            vo.wait_until("c")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def question(self, s):
        q = pause_card(rf"with {s['n_train']} statements and {s['n_vocab']} candidate words, how many words would pass "
                       rf"the screen at $\alpha = {s['alpha']:.2f}$, $\kappa = {s['kappa']}$ if the labels were coin flips?")
        with self.voiceover(
            f"Pause and predict. With {s['n_train']} statements and {s['n_vocab']} candidate words, how many words "
            "would pass this screen if the labels were coin flips?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
