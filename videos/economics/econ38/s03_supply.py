from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Supply(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Labour supply", r"How much do people choose to work when pay rises?",
             "Chapter two. Labour supply.", lit={1930: r"Robbins on the backward bend", 2011: r"Chetty et al."},
             scale=("person", "household"), horizon=("a year",))
        self.curve()
        self.elasticities()
        self.participation()

    def curve(self):
        S = load("supply")
        w, h = np.array(S["w"]), 100 * np.array(S["h"])
        ax = plane([15, 40], [0, 50], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.0, y_length=4.6,
                   xticks=[20, 25, 30, 35, 40], yticks=[0, 10, 20, 30, 40, 50],
                   xlabel=r"hours worked, \ of 100 waking hours a week", ylabel=r"hourly wage, \ \$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = path(ax, h, w, SUPPLY, 3.4, xr=(15, 40), yr=(0, 50))
        k = int(np.argmax(h))
        bend = dot(ax, h[k], w[k], E.ACCENT, 0.09)
        eq = MathTex(r"\max_{c,\,h}\ \frac{c^{1-\gamma}}{1-\gamma} - \psi\,\frac{h^{1+1/\varphi}}{1+1/\varphi}"
                     r"\quad \text{s.t.}\quad c = w h + y", font_size=30).to_edge(UP, buff=0.3)
        side = VGroup(
            label(r"a higher wage: \\ work pays more \ (substitution) \\ but you are richer \ (income)", font_size=18,
                  color=WHITE),
            label(rf"here the income effect \\ wins above \${S['peak']:.0f} an hour: \\ the curve bends back",
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Start with a worker on the Island choosing how many hours to work. More hours mean more to spend and "
            "less time for everything else. <bookmark mark='a'/> The choice, written out: enjoy consumption, dislike "
            "hours, and earn the wage on every hour worked, plus some income from elsewhere. <bookmark mark='b'/> A "
            "higher wage pulls two ways. Each hour now buys more, so work more: the substitution effect. But you are "
            "richer, and can afford more time off: the income effect. <bookmark mark='c'/> For this worker the "
            f"substitution effect wins at low wages and the income effect above about {S['peak']:.0f} dollars an hour, "
            "so the supply curve bends backwards: one reason hours in rich countries fell as wages rose over the "
            "twentieth century."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(bend, scale=1.5), FadeIn(side[1]))
        self.clear_scene()

    def elasticities(self):
        S = load("supply")
        lo, hi = S["el"]["6"], S["el"]["30"]
        rows = [(r"Marshallian", r"the wage rises, \ nothing else", "marshallian", SUPPLY),
                (r"income effect", r"$w\,\partial h/\partial y$", "income_effect", LOSS),
                (r"Hicksian", r"the rise is compensated: \\ substitution alone", "hicksian", WAGE),
                (r"Frisch", r"a temporary rise: \\ wealth unchanged", "frisch", E.ACCENT)]
        head = VGroup(label(r"elasticity", font_size=20, color=GREY_A), label(r"what it holds fixed", font_size=20,
                                                                              color=GREY_A),
                      label(r"at \$6", font_size=20, color=GREY_A), label(r"at \$30", font_size=20, color=GREY_A))
        xs = (-4.6, -1.2, 2.4, 4.6)
        for m, x in zip(head, xs):
            m.move_to(np.array([x, 2.2, 0]))
        table = VGroup(head)
        for k, (nm, what, key, col) in enumerate(rows):
            y = 1.2 - 1.05 * k
            r = VGroup(label(nm, font_size=22, color=col).move_to(np.array([xs[0], y, 0])),
                       label(what, font_size=17, color=WHITE).move_to(np.array([xs[1], y, 0])),
                       label(f"{lo[key]:+.2f}", font_size=24, color=col).move_to(np.array([xs[2], y, 0])),
                       label(f"{hi[key]:+.2f}", font_size=24, color=col).move_to(np.array([xs[3], y, 0])))
            table.add(r)
        foot = label(r"Slutsky: \ Hicksian = Marshallian $-$ income effect", font_size=21, color=GREY_A).to_edge(
            DOWN, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "So 'how much do people respond to pay' has three answers, and economists mix them up at their peril. "
            "<bookmark mark='a'/> The Marshallian elasticity: raise the wage and nothing else. For this worker it is "
            f"{lo['marshallian']:+.2f} at six dollars and {hi['marshallian']:+.2f} at thirty. <bookmark mark='b'/> "
            "Strip out the income effect <bookmark mark='c'/> and what remains is the Hicksian, or compensated, "
            f"elasticity: {lo['hicksian']:+.2f} and {hi['hicksian']:+.2f}, positive at both. It is the one that "
            "measures the harm of a tax, because taxes are spent on something. <bookmark mark='d'/> And the Frisch "
            f"elasticity, {lo['frisch']:.1f}, answers a temporary rise: work hard while pay is high, rest when it is "
            "low. It is the number business-cycle models need."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r in zip("abcd", table[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()

    def participation(self):
        S = load("supply")
        Ch = S["chetty"]
        w, p = np.array(S["w"]), np.array(S["participation"])
        ax = plane([0, 40], [0, 1], center=LEFT * 2.8 + DOWN * 0.4, x_length=6.4, y_length=4.4,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 0.25, 0.5, 0.75, 1], xlabel=r"hourly wage, \ \$",
                   ylabel=r"share who work at all", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: rf"{100 * v:.0f}\%",
                   font_size=14)
        ln = path(ax, w, p, EMP, 3.4)
        bars = VGroup()
        vals = ((r"Hicksian, \ hours", Ch["hicks_int"]), (r"Hicksian, \ whether", Ch["hicks_ext"]),
                (r"Frisch, \ hours", Ch["frisch_int"]), (r"Frisch, \ whether", Ch["frisch_ext"]))
        for k, (nm, v) in enumerate(vals):
            y = 1.4 - 0.75 * k
            r = Rectangle(width=v * 5, height=0.38, stroke_width=0, fill_color=WAGE if k < 2 else E.ACCENT,
                          fill_opacity=0.85).move_to(np.array([2.6 + v * 2.5, y, 0]))
            bars.add(VGroup(label(nm, font_size=16, color=GREY_A).next_to(r, LEFT, buff=0.15).align_to(
                np.array([2.5, 0, 0]), RIGHT), r, label(f"{v:.2f}", font_size=16, color=WHITE).next_to(r, RIGHT,
                                                                                                     buff=0.1)))
        bh = label(r"the micro evidence, \ synthesized", font_size=18, color=GREY_A).next_to(bars, UP, buff=0.3)
        tag = published_tag(tables.CHETTY_2011.tag + r"; \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "Hours are one margin; whether to work at all is the other. <bookmark mark='a'/> If people differ in the "
            "lowest wage at which work is worth it, the share who work rises with the wage, along this curve. "
            "<bookmark mark='b'/> Raj Chetty, Adam Guren, Day Manoli and Andrea Weber pulled together the "
            "quasi-experimental evidence in 2011: permanent, Hicksian elasticities of about "
            f"{Ch['hicks_int']:.1f} for hours and {Ch['hicks_ext']:.2f} for participation, and Frisch elasticities of "
            f"about {Ch['frisch_int']:.1f} and {Ch['frisch_ext']:.2f}. Modest numbers, and an order of magnitude below "
            "what business-cycle models need to explain the swings in hours by workers' choices alone."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(ln, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.1) for b_ in bars], lag_ratio=0.3),
                      run_time=2.0)
        self.clear_scene()
