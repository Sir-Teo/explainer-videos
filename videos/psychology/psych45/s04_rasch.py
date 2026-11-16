from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Rasch(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.objectivity()
        self.sufficiency()

    def card(self):
        card = chapter_card(3, r"The Rasch model", r"What if success depends only on ability minus difficulty?",
                            lit={1960: r"Rasch"}, part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter three. The Rasch model."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def model(self):
        head = heading(r"One encounter")
        eq = MathTex(r"P(X_{pi} = 1) = \frac{e^{\theta_p - b_i}}{1 + e^{\theta_p - b_i}}", font_size=40,
                     color=MODEL).move_to([-3.4, 2.0, 0])
        A = axes([-4, 4], [0, 1], x_length=5.6, y_length=2.8, xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"ability $\theta$",
                 ylabel=r"P(correct)", center=[-3.4, -1.0, 0], font_size=13)
        cols = (GOOD, SYMP, PERSON, AUTH)
        curves = VGroup(*[icc(A.ax, 1.0, bb, c) for bb, c in zip((-2.0, -0.5, 0.8, 2.0), cols)])
        half = DashedLine(A.ax.c2p(-4, 0.5), A.ax.c2p(4, 0.5), color=GREY_B, stroke_width=1.5)
        rows = rows_of([
            (r"person $p$ has ability $\theta_p$; \ item $i$ has difficulty $b_i$, \ on the same scale", WHITE),
            (r"the log-odds of success is $\theta_p - b_i$: \ a person whose ability equals the item's difficulty "
             r"has an even chance", MODEL),
            (r"every item's curve has the same shape, \ shifted: \ an item characteristic curve", PERSON),
            (r"one encounter, \ two parameters; \ everything else follows from multiplying encounters", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "Rasch's model is one encounter. <bookmark mark='a'/> A person has an ability, theta. An item has a "
            "difficulty, b, on the same scale. <bookmark mark='b'/> The log-odds of success is ability minus "
            "difficulty. So a person whose ability equals the item's difficulty has an even chance. "
            "<bookmark mark='c'/> Every item's curve has the same shape, shifted along the ability axis. It's called "
            "the item characteristic curve. <bookmark mark='d'/> One encounter, two parameters. Everything else "
            "follows from multiplying encounters together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq), FadeIn(A), FadeIn(half))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(curves[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[Create(curves[k]) for k in (0, 2, 3)], lag_ratio=0.4),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def objectivity(self):
        head = heading(r"Specific objectivity")
        eqs = VGroup(
            MathTex(r"\log\frac{P_{1i}}{1 - P_{1i}} - \log\frac{P_{2i}}{1 - P_{2i}} = \theta_1 - \theta_2", font_size=36,
                    color=MODEL),
            MathTex(r"\log\frac{P_{pi}}{1 - P_{pi}} - \log\frac{P_{pj}}{1 - P_{pj}} = b_j - b_i", font_size=36,
                    color=GOOD),
        ).arrange(DOWN, buff=0.5).move_to([0, 1.2, 0])
        rows = rows_of([
            (r"compare two people on any item: \ the difference in log-odds is their difference in ability, \ "
             r"whichever item is used", MODEL),
            (r"compare two items on any person: \ the difference is their difference in difficulty, \ whoever answers",
             GOOD),
            (r"Rasch called this specific objectivity: \ comparisons of people free of the items, \ and of items free "
             r"of the people", PERSON),
            (r"it holds only if every item's curve has the same slope; \ with different slopes, \ the comparison "
             r"depends on where you look", AUTH),
        ], 12.4, 21, 0.38).move_to([0, -1.7, 0])
        with self.voiceover(
            "Now the property Rasch prized. <bookmark mark='a'/> Compare two people on any item. The difference in "
            "their log-odds is their difference in ability, whichever item is used. <bookmark mark='b'/> Compare two "
            "items on any person. The difference is their difference in difficulty, whoever answers. "
            "<bookmark mark='c'/> Rasch called this specific objectivity: comparisons of people free of the items, "
            "and of items free of the people. <bookmark mark='d'/> It holds only if every item's curve has the same "
            "slope. With different slopes, the comparison depends on where you look."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def sufficiency(self):
        d = load("lsat")
        head = heading(r"The sum score is enough")
        eq = MathTex(r"P(\mathbf{x} \mid r) = \frac{\prod_i e^{x_i(\theta - b_i)}/(1 + e^{\theta - b_i})}"
                     r"{\sum_{\mathbf{y}:\,\sum y = r} \prod_i e^{y_i(\theta - b_i)}/(1 + e^{\theta - b_i})}"
                     r"= \frac{e^{-\sum_i x_i b_i}}{\gamma_r(e^{-b_1}, \dots, e^{-b_k})}",
                     font_size=30, color=MODEL).move_to([0, 2.0, 0])
        pats = (r"1 1 0 0 0", r"0 0 1 1 0", r"1 0 0 0 1", r"0 1 1 0 0")
        hdr = VGroup(*[label(t, font_size=17, color=GREY_A) for t in (r"pattern, \ 2 right", r"$\theta = -2$",
                                                                     r"$\theta = 0$", r"$\theta = 2$")])
        table = VGroup(hdr)
        for k, p in enumerate(pats):
            table.add(VGroup(label(p, font_size=18, color=WHITE),
                             *[label(f"{d[key][k]:.3f}", font_size=18, color=c)
                               for key, c in (("pg_m2", SYMP), ("pg_0", MODEL), ("pg_2", GOOD))]))
        for row in table:
            for j, cell in enumerate(row):
                cell.move_to([-5.0 + 1.9 * j, 0, 0])
        table.arrange(DOWN, buff=0.22).move_to([-3.3, -1.3, 0])
        for row in table:
            for j, cell in enumerate(row):
                cell.set_x(-5.6 + 1.6 * j)
        rows = rows_of([
            (r"$\theta$ cancels: \ the chance of each pattern, \ given its score, \ involves only the items", MODEL),
            (r"on the LSAT's five items: \ the same probabilities at every ability", WHITE),
            (r"so the sum score carries everything the answers say about ability, \ and the items can be estimated "
             r"by conditioning it away: \ conditional maximum likelihood", GOOD),
        ], 5.6, 18, 0.36).move_to([3.6, -1.3, 0])
        tag = psyche_tag(r"\texttt{irt.fit\_cml}; \ LSAT data (ltm)")
        with self.voiceover(
            "And the Rasch model's best property. <bookmark mark='a'/> Ask how likely a pattern of answers is, given "
            "its sum score. Write it out, and ability cancels. What's left involves only the items. "
            "<bookmark mark='b'/> Here are four patterns with two right, on five items from a law-school admission "
            "test, at three very different abilities. The probabilities are identical. <bookmark mark='c'/> So the "
            "sum score carries everything the answers say about ability. And the items can be estimated with ability "
            "conditioned away entirely. It's called conditional maximum likelihood."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(table), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
