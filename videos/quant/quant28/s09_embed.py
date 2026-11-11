from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import HURDLE, PART, WORD, comma, fit_right, load

HILITE = {"inflation": QC.LOSS, "unemployment": QC.CASH, "purchases": QC.OPTION, "housing": QC.VEGA,
          "liquidity": QC.SPOT, "tightening": QC.DELTA}


class Embeddings(VoiceoverScene):
    def construct(self):
        e = load("embed")
        self.card()
        self.idea()
        self.ladder_()
        self.neighbours(e)
        self.map_(e)
        self.analogy(e)
        self.question()

    def card(self):
        c = chapter_card(8, r"Embeddings: meaning from neighbours", r"Can a machine learn that easing is the opposite "
                         r"of tightening, from co-occurrence alone?", part=PART)
        with self.voiceover("Chapter eight. A bag of words treats easing and tightening as unrelated symbols. Can a "
                            "machine learn what words mean, with no dictionary at all?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self):
        quote = label(r"``You shall know a word by the company it keeps.''", font_size=36).shift(UP * 1.6)
        who = label(r"J.\ R.\ Firth, 1957", font_size=24, color=GREY_B).next_to(quote, DOWN, buff=0.25)
        s1 = label(r"the Committee decided to \textbf{raise} the target range", font_size=26, color=GREY_A)
        s2 = label(r"the Committee decided to \textbf{lower} the target range", font_size=26, color=GREY_A)
        pair = VGroup(s1, s2).arrange(DOWN, buff=0.35).shift(DOWN * 0.6)
        note_ = wrapped_label(r"\emph{raise} and \emph{lower} share their neighbours, so they land close together; an "
                              r"embedding is a vector per word that summarises its neighbours", 10.6, 20,
                              GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The idea is from the linguist J. R. Firth in 1957: you shall know a word by the company it keeps. "
            "<bookmark mark='a'/> Raise and lower appear in the same places: the committee decided to blank the "
            "target range. Words that share neighbours share meaning, or at least a role. <bookmark mark='b'/> An "
            "embedding gives each word a vector that summarises its neighbours, so that words used alike point the "
            "same way."
        ) as vo:
            self.play(FadeIn(quote), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(pair))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def ladder_(self):
        rows = [cmath(r"C_{wc}", r"=", r"\sum_{\text{pairs within 5 words}} \frac{1}{\text{distance}}", font_size=32,
                      colors={r"C_{wc}": WORD}),
                cmath(r"\mathrm{PPMI}_{wc}", r"=", r"\max\Big(0,\ \log\frac{P(w, c)}{P(w)\,P_\alpha(c)}\Big)", font_size=32,
                      colors={r"\mathrm{PPMI}_{wc}": HURDLE}),
                cmath(r"\mathrm{PPMI}", r"\approx", r"U_k \Sigma_k V_k^\top,\qquad e_w = (U_k\Sigma_k^{1/2})_{w\cdot}", font_size=32,
                      colors={r"\mathrm{PPMI}": HURDLE}),
                cmath(r"\text{SGNS optimum}", r"\sim", r"\text{factorising a shifted PMI matrix}", font_size=30)]
        whys = [why(r"count how often each word appears near each other word, closer pairs counting more"),
                why(r"pointwise mutual information: how much more often than chance; negative values (rare, noisy) set "
                    r"to zero; context frequencies smoothed by $\alpha = 0.75$"),
                why(r"keep the top $k = 50$ singular directions: each word becomes a 50-dimensional vector"),
                why(r"Levy and Goldberg (2014): word2vec's skip-gram with negative sampling implicitly does this "
                    r"factorisation; the neural and the counting views agree")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Here is how, with nothing but counting and linear algebra. <bookmark mark='a'/> Count how often each word "
            "appears within five words of each other word, nearer pairs counting more. <bookmark mark='b'/> Convert "
            "counts to a positive PMI variant using context frequencies raised to the power zero point seven five and renormalised; this differs from the unsmoothed independence baseline. Set negative values to zero. <bookmark mark='c'/> Factor that matrix with a singular value decomposition "
            "and keep fifty directions: each word is now a point in fifty dimensions. <bookmark mark='d'/> Omer Levy "
            "and Yoav Goldberg relate skip-gram with negative sampling to a shifted PMI objective under their assumptions. A finite SVD of positive smoothed PMI is a related construction, not numerical equivalence to every word2vec model."
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

    def neighbours(self, e):
        show = [w for w in ("inflation", "purchases", "housing", "tightening", "liquidity", "uncertainty") if w in e["neighbours"]]
        cols = VGroup()
        for w in show:
            g = VGroup(label(rf"\texttt{{{w}}}", font_size=22, color=HILITE.get(w, WORD)),
                       *[label(rf"\texttt{{{n}}}\ {s:.2f}", font_size=16, color=GREY_A) for n, s in e["neighbours"][w][:6]])
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            cols.add(g)
        cols.arrange_in_grid(rows=2, cols=3, buff=(1.0, 0.6)).move_to(UP * 0.1)
        foot = wrapped_label(rf"nearest words by cosine similarity, from {comma(e['n_tokens'])} words of FOMC minutes, "
                             rf"1996--2020, the {comma(e['V'])} most common words, {e['dim']} dimensions; no dictionary, "
                             r"no labels", 11.4, 17, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Train it on the minutes, and ask for each word's nearest neighbours. <bookmark mark='a'/> Inflation sits "
            "next to expectations, core and survey-based; purchases next to asset, large-scale and the mortgage-backed "
            "securities the Fed bought; housing next to residential, homebuilding and construction. "
            "<bookmark mark='b'/> Tightening's nearest neighbour is easing: opposites that play the same role. And "
            "liquidity lives with facilities, swap lines and emergency provision, the vocabulary of 2008. None of this "
            "was supplied as sentiment labels. Shared contexts can put antonyms together, so proximity does not mean equal polarity or guarantee useful return features."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cols[:3]], lag_ratio=0.3), FadeIn(foot))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cols[3:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def map_(self, e):
        xy = np.asarray(e["map_xy"], float)
        xy = xy / np.abs(xy).max(0) * np.array([5.4, 3.0])
        words = e["map_words"]
        dots = VGroup(*[Dot([a, b - 0.2, 0], radius=0.03, color=GREY_C) for a, b in xy])
        tags, leaders = VGroup(), VGroup()
        selected = ["inflation", "employment", "housing", "prices", "credit", "purchases", "banks", "securities", "growth"]
        anchors = {w: np.array([a, b - 0.2, 0]) for w, (a,b) in zip(words, xy)}
        placed = []
        for w in selected:
            if w not in anchors:
                continue
            m = label(rf"\texttt{{{w}}}", font_size=18, color=HILITE.get(w, WORD))
            anchor = anchors[w]
            found = False
            for radius in [0.25, 0.5, 0.8, 1.1, 1.4]:
                for angle in [PI/2, -PI/2, 0, PI, PI/4, 3*PI/4, -PI/4, -3*PI/4]:
                    m.move_to(anchor + radius * np.array([np.cos(angle), np.sin(angle), 0]))
                    left, right, bottom, top = m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1]
                    if left < -6.6 or right > 6.6 or bottom < -3.25 or top > 3.05:
                        continue
                    if any(not(right + 0.14 < x0 or left - 0.14 > x1 or top + 0.12 < y0 or bottom - 0.12 > y1)
                           for x0,x1,y0,y1 in placed):
                        continue
                    placed.append((left,right,bottom,top));found=True;break
                if found:
                    break
            if not found:
                raise RuntimeError("No non-overlapping map-label position for " + w)
            leaders.add(Line(anchor, m.get_center(), color=GREY_B, stroke_width=0.8, stroke_opacity=0.65))
            tags.add(m)
        head = label(r"the 250 most common words, projected onto their first two principal directions", font_size=20,
                     color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Project the two hundred and fifty most common words onto the two directions that spread them most. "
            "<bookmark mark='a'/> The map is crude, two of fifty dimensions, but neighbourhoods appear: words about "
            "prices and inflation in one region, about the labour market in another, financial plumbing in a third."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.004), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(leaders), LaggedStart(*[FadeIn(t_) for t_ in tags], lag_ratio=0.05))
        self.add(note(r"original PCA dots; selected labels offset with leaders. Two dimensions retain only part of the fifty-dimensional geometry",
                      font_size=16, color=GREY_B).to_edge(DOWN, buff=0.3))
        self.wait(0.4)
        self.clear_scene()

    def analogy(self, e):
        an = e["analogies"][0] if e["analogies"] else None
        if an is None:
            return
        eq = MathTex(rf"e_{{\text{{{an['a']}}}}} - e_{{\text{{{an['b']}}}}} + e_{{\text{{{an['c']}}}}}", r"\approx",
                     rf"e_{{\text{{{an['best'][0]}}}}}", font_size=44)
        eq[0].set_color(WORD)
        eq[2].set_color(HURDLE)
        eq.shift(UP * 0.6)
        sub = label(rf"the three nearest: \texttt{{{an['best'][0]}}}, \texttt{{{an['best'][1]}}}, "
                    rf"\texttt{{{an['best'][2]}}}", font_size=22, color=GREY_A).next_to(eq, DOWN, buff=0.4)
        foot = wrapped_label(r"directions in the space carry relations: \emph{tightening} is to \emph{raise} what "
                             r"\emph{easing} is to \emph{lower}. Mikolov et al.\ (2013) made this famous with "
                             r"king $-$ man $+$ woman $\approx$ queen", 10.6, 18, GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Directions carry relations, too. <bookmark mark='a'/> Take the vector for tightening, subtract raise, add "
            f"lower, and ask which word is nearest. The answer is {an['best'][0]}. <bookmark mark='b'/> Tightening is to "
            "raise what easing is to lower: arithmetic on meaning, the trick that made Tomas Mikolov's word2vec famous "
            "in 2013, reproduced here from nothing but the Fed's own minutes."
        ) as vo:
            self.play(Write(eq))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(sub), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"`tightening's nearest neighbour is `easing'. Would a sentiment score built on these vectors tell a "
                       r"hawkish statement from a dovish one?")
        with self.voiceover(
            "Pause and predict. Tightening's nearest neighbour is easing. Would a sentiment score built on these vectors "
            "tell a hawkish statement from a dovish one?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
