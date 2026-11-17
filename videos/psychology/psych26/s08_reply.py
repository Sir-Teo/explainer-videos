from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Reply(VoiceoverScene):
    def construct(self):
        self.card()
        self.frequencies()
        self.ttb_rule()
        self.ttb_test()

    def card(self):
        card = chapter_card(7, r"The reply: \ frequencies and fast, \ frugal rules", r"Are the biases errors at all?",
                            lit={1995: r"Gigerenzer \& Hoffrage", 1996: r"Gigerenzer \& Goldstein",
                                 1999: r"Gigerenzer, \ Todd \& ABC"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter seven. The reply: frequencies and fast, frugal rules."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def frequencies(self):
        d = load("bayes")
        nf = d["mam_nf"]
        head = heading(r"Natural frequencies")
        probf = rows_of([
            (r"as probabilities: \ 1\% of women screened have breast cancer; \ a mammogram detects 80\% of "
             r"cancers; \ 9.6\% of healthy women also test positive", WHITE),
            (r"as frequencies: \ of 1{,}000 women, \ 10 have cancer, \ and 8 of them test positive; \ of the 990 "
             r"without, \ 95 also test positive", GAIN),
        ], 12.0, 23, 0.3).move_to([0, 2.0, 0])
        root = label(r"1{,}000 women", font_size=24).move_to([0, 0.5, 0])
        n1 = label(rf"{nf['sick']} with cancer", font_size=22, color=LOSS).move_to([-3.0, -0.6, 0])
        n2 = label(rf"{nf['well']} without", font_size=22, color=SURE).move_to([3.0, -0.6, 0])
        l1 = label(rf"{nf['true_pos']} positive", font_size=22, color=LOSS).move_to([-3.0, -1.7, 0])
        l2 = label(rf"{nf['false_pos']} positive", font_size=22, color=SURE).move_to([3.0, -1.7, 0])
        edges = VGroup(Line(root.get_bottom(), n1.get_top(), color=GREY_C), Line(root.get_bottom(), n2.get_top(),
                                                                                  color=GREY_C),
                       Line(n1.get_bottom(), l1.get_top(), color=GREY_C), Line(n2.get_bottom(), l2.get_top(),
                                                                               color=GREY_C))
        ans = MathTex(rf"P(\text{{cancer}} \mid +) = \frac{{{nf['true_pos']}}}{{{nf['true_pos']} + "
                      rf"{nf['false_pos']}}} \approx {100 * d['mam']:.1f}\%", font_size=36, color=NORM)
        ans.to_edge(DOWN, buff=1.15)
        foot = wrapped_label(r"Gigerenzer and Hoffrage, \ 1995: \ Bayesian answers rose from about 16\% to 46\% "
                             r"when the same problems were given in frequencies", 12.0, 22, MODEL).to_edge(DOWN,
                                                                                                         buff=0.5)
        tag = psyche_tag(r"\texttt{choice.natural\_frequencies}; \ Gigerenzer \& Hoffrage (1995)")
        with self.voiceover(
            "The most influential critic was Gerd Gigerenzer, and his first point was about format. "
            "<bookmark mark='a'/> Here is a screening problem in probabilities. One percent of women screened have "
            "breast cancer. A mammogram detects eighty percent of cancers, and nine point six percent of healthy "
            "women also test positive. A woman tests positive. What's the chance she has cancer? Many people, "
            "doctors included, answer far too high, often near eighty percent. <bookmark mark='b'/> Now the same numbers as "
            "natural frequencies, the counts you'd see if you watched a thousand women. Ten have cancer, and eight "
            "of them test positive. Of the nine hundred and ninety without, about ninety-five also test positive. "
            f"<bookmark mark='c'/> So of the hundred and three positives, eight have cancer: about "
            f"{100 * d['mam']:.0f} percent. The arithmetic does itself. <bookmark mark='d'/> In 1995 Gigerenzer and "
            "Ulrich Hoffrage gave people problems like this in both formats, and the share of correct Bayesian "
            "answers roughly tripled with frequencies. The mind, Gigerenzer argued, evolved to count events, not to "
            "multiply single-case probabilities."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(probf[0]))
            vo.wait_until("b")
            self.play(FadeIn(probf[1]))
            self.play(FadeIn(root), Create(edges[:2]), FadeIn(n1), FadeIn(n2))
            self.play(Create(edges[2:]), FadeIn(l1), FadeIn(l2))
            vo.wait_until("c")
            self.play(Write(ans))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def ttb_rule(self):
        head = heading(r"Take-the-best")
        q = label(r"Which city has more people: \ A or B?", font_size=28, color=WHITE).move_to([0, 2.2, 0])
        cues = [(r"is it a capital?", "?", "?", r"neither knows: \ next cue"),
                (r"has a top-league football team?", "yes", "no", r"it discriminates: \ choose A, \ stop")]
        rows_g = VGroup()
        for k, (cue, a, b, act) in enumerate(cues):
            col = GREY_B if k == 0 else GAIN
            r = VGroup(label(rf"cue {k + 1}: \ {cue}", font_size=24, color=col),
                       label(rf"A: \ {a}", font_size=24, color=SURE), label(rf"B: \ {b}", font_size=24, color=RISKY),
                       label(act, font_size=22, color=col)).arrange(RIGHT, buff=0.5)
            rows_g.add(r)
        rows_g.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.8, 0])
        rows = rows_of([
            (r"order the cues by validity: \ how often each, \ when it discriminates, \ points the right way", WHITE),
            (r"look up cues in that order; \ the first that discriminates decides; \ ignore the rest", HEUR),
            (r"no weights, \ no adding: \ Gigerenzer and Goldstein, \ 1996, \ called it fast and frugal", MODEL),
        ], 12.0, 24, 0.3).move_to([0, -1.6, 0])
        tag = published_tag(r"Gigerenzer \& Goldstein (1996)")
        with self.voiceover(
            "His second point was more radical: that simple rules aren't a poor substitute for rational "
            "calculation, and can beat it. <bookmark mark='a'/> Which of two German cities has more people? "
            "<bookmark mark='b'/> Take-the-best answers like this. Order the cues you know, such as whether a city "
            "is a capital or has a team in the top football league, by their validity: how often each, when it "
            "tells the cities apart, points the right way. <bookmark mark='c'/> Then look them up in order. The "
            "first cue that discriminates decides, and everything else is ignored. <bookmark mark='d'/> No weights, "
            "no adding up. Gigerenzer and Daniel Goldstein called it fast and frugal, in 1996, and showed it could "
            "match strategies that weigh every cue."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows_g[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows_g[1]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def ttb_test(self):
        d = load("ttb")
        head = heading(r"Out of sample: \ the simple rule against regression")
        tr = d["train"]
        def panel(world, title, center, ylo, yhi):
            A = axes([5, 85], [ylo, yhi], x_length=5.2, y_length=3.4, xticks=[10, 20, 40, 60, 80],
                     yticks=[ylo, (ylo + yhi) / 2, yhi], xfmt=lambda v: f"{v:.0f}",
                     yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"objects to learn from",
                     ylabel=r"correct on new pairs", center=center, font_size=16)
            t = label(title, font_size=22, color=GREY_A).next_to(A, UP, buff=0.12)
            cs = VGroup(curve(A.ax, tr, d[f"{world}_ttb"], HEUR, 4), curve(A.ax, tr, d[f"{world}_regression"], NORM, 4),
                        curve(A.ax, tr, d[f"{world}_tally"], GREY_B, 3))
            return VGroup(A, t), cs
        g1, c1 = panel("noncompensatory", r"cue weights 8, 4, 2, 1, \ldots", [-3.4, 0.25, 0], 0.6, 0.85)
        g2, c2 = panel("compensatory", r"cue weights all equal", [3.4, 0.25, 0], 0.55, 0.7)
        key = legend([(HEUR, r"take-the-best"), (NORM, r"regression"), (GREY_B, r"tallying")], font_size=18)
        key.arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=1.1)
        foot = wrapped_label(rf"with little data the simple rule wins, \ in both worlds; \ regression catches up by "
                             rf"about {d['ttb_wins_upto'] + 5} objects; \ the environment decides how fast",
                             12.4, 22, MODEL).to_edge(DOWN, buff=0.55)
        tag = psyche_tag(r"\texttt{choice.heuristics\_cv}: \ 6 binary cues, \ 120 objects, \ 300 worlds a point")
        lead = 100 * d["ttb_lead_small"]
        with self.voiceover(
            "Can ignoring information really pay? Psyche can test it. <bookmark mark='a'/> We build a world of a "
            "hundred and twenty objects with six yes-or-no cues and a noisy criterion, learn from some of the "
            "objects, and judge pairs of the others: out of sample, as in the 1999 study by Jean Czerlinski, "
            "Gigerenzer and Goldstein across twenty real datasets. Three strategies: take-the-best, least-squares "
            "regression on all six cues, and tallying, which just counts the cues on each side. "
            "<bookmark mark='b'/> In a world where each cue matters about twice as much as the next, take-the-best "
            f"beats regression by about {lead:.0f} points when there are only eight objects to learn from. "
            "Regression, with its seven parameters, fits the noise. With more data it catches up and pulls ahead. "
            "<bookmark mark='c'/> In a world where all the cues count equally, tallying comes into its own as data "
            "grows, but with very little data take-the-best still wins. <bookmark mark='d'/> This is what "
            "Gigerenzer calls ecological rationality: a rule is neither good nor bad in itself, but good or bad "
            "in an environment. Ignoring information trades a little bias for a lot less variance, the same "
            "trade a statistician makes with a simpler model."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(key))
            vo.wait_until("b")
            self.play(Create(c1), run_time=2)
            vo.wait_until("c")
            self.play(Create(c2), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
