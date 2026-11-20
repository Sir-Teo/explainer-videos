from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class HandToMouth(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The wealthy hand-to-mouth", r"Why do some households with houses and pensions spend windfalls "
             r"as fast as the poor?", "Chapter eight. The wealthy hand-to-mouth.",
             lit={2014: r"Kaplan, Violante and Weidner"}, scale=("household",), horizon=("a quarter", "a lifetime"))
        self.kvw()
        self.shortcut()
        self.island()

    def kvw(self):
        rows = VGroup(
            label(r"two kinds of wealth", font_size=28, color=E.ACCENT),
            VGroup(label(r"liquid: \ cash, \ checking and savings accounts", font_size=23, color=CASH),
                   label(r"illiquid: \ a house, \ a retirement account", font_size=23, color=HOUSE)).arrange(
                RIGHT, buff=0.8),
            label(r"illiquid wealth pays more \ (rent saved, \ tax breaks, \ an employer's match), \ but is costly to "
                  r"reach", font_size=22, color=GREY_A),
            label(r"hand-to-mouth: \ little or no liquid wealth at payday", font_size=24, color=WHITE),
            label(r"Greg Kaplan, \ Giovanni Violante and Justin Weidner, \ 2014: \ about a third of US households",
                  font_size=23, color=SAVE),
            label(r"and over two-thirds of them are \emph{wealthy} hand-to-mouth: \ they own a house or a pension",
                  font_size=23, color=HOUSE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Kaplan, Violante and Weidner, BPEA Spring 2014: \ 77--138; \ Kaplan and Violante, "
                            r"Econometrica 82(4) (2014)", corner=DR, font_size=12)
        with self.voiceover(
            "The rebates hit hardest where liquid wealth was low. But which households are those? "
            "<bookmark mark='a'/> Wealth comes in two kinds. Liquid wealth is cash and bank accounts, ready to "
            "spend. Illiquid wealth is a house or a retirement account. <bookmark mark='b'/> Illiquid wealth pays "
            "more: the rent you no longer pay, the tax breaks, an employer's matching contribution. But it is costly "
            "to reach. You cannot spend a bedroom. <bookmark mark='c'/> Call a household hand-to-mouth if it has "
            "little or no liquid wealth on payday. <bookmark mark='d'/> Greg Kaplan, Giovanni Violante and Justin "
            "Weidner counted them in 2014: about a third of American households. <bookmark mark='e'/> And over "
            "two-thirds of those were not poor. They owned a house or a pension. They are the wealthy hand-to-mouth, "
            "and they spend a windfall as fast as the poor do."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def shortcut(self):
        h = load("htm")
        rows = VGroup(
            label(r"the Island's version \ (a shortcut to Kaplan and Violante's two-asset model)", font_size=25,
                  color=E.ACCENT),
            label(r"60\% of households own illiquid wealth, \ about three years of income at the median, \ earning "
                  r"7\% against cash's 3\%", font_size=22, color=HOUSE),
            label(r"every dollar an owner keeps in cash gives up the higher return", font_size=22, color=GREY_A),
            MathTex(r"\beta_{\text{cash}} = \beta\,\frac{R}{R_h} = 0.96 \times \frac{1.03}{1.07} = "
                    + f"{h['beta_owner']:.3f}", font_size=40, color=CASH),
            label(r"so on its cash, \ an owner behaves like a less patient household, \ and keeps less of it",
                  font_size=22, color=WHITE),
            label(r"renters solve chapter 6's problem unchanged", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island can show the mechanism with a shortcut. <bookmark mark='a'/> Sixty percent of its households "
            "own illiquid wealth, about three years of income at the median, earning seven percent a year against "
            "three on cash. <bookmark mark='b'/> For an owner, every dollar kept in cash gives up the higher return. "
            "<bookmark mark='c'/> So on its cash, an owner discounts as if it were less patient: a beta of "
            f"{h['beta_owner']:.3f} instead of 0.96. <bookmark mark='d'/> It keeps less cash, and lives closer to "
            "the steep part of the consumption function. <bookmark mark='e'/> Renters solve chapter six's problem "
            "unchanged. Kaplan and Violante's own model has two assets and a cost of moving between them; this is "
            "the part of it that matters here."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        h = load("htm")
        s = h["sample"]
        ax = plane([-2, 1.4], [0, 1.0], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.8, y_length=4.8,
                   xticks=[-2, -1, 0, 1], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"wealth, \ years of income \ (log scale)", ylabel=r"share of a month's windfall spent "
                   r"within the year", xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{v:g}", font_size=16)

        def X(v):
            return float(np.clip(np.log10(v + 0.01), -2, 1.4))
        dots = VGroup()
        targets = []
        for net, liq, mpc, own in zip(s["net"], s["liquid"], s["mpc"], s["owns"]):
            col = HOUSE if own else CASH
            d = Dot(ax.ax.c2p(X(net), min(mpc, 1.0)), radius=0.03, color=col).set_opacity(0.6)
            dots.add(d)
            targets.append(ax.ax.c2p(X(liq), min(mpc, 1.0)))
        side = VGroup(
            label(r"owners", font_size=21, color=HOUSE),
            label(r"renters", font_size=21, color=CASH),
            label(rf"median net worth: \\ owners {h['net_owners']:.1f}, \ renters {h['net_renters']:.2f} \\ years of "
                  r"income", font_size=18, color=GREY_A),
            label(rf"share spent: \\ owners {h['mpc_owners']:.2f}, \ renters {h['mpc_renters']:.2f}", font_size=19,
                  color=WHITE),
            label(rf"against net worth: \ correlation {h['corr_net']:+.2f}", font_size=18, color=GREY_A),
            label(rf"against liquid wealth: \ {h['corr_liquid']:+.2f}", font_size=18, color=SPEND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        xl_liquid = label(r"\emph{liquid} wealth, \ years of income \ (log scale)", font_size=18, color=CASH).move_to(
            ax.xlabel)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here are the Island's households, each a dot: net worth along the bottom, on a log scale, and the "
            "share of a month's windfall it would spend within the year. <bookmark mark='a'/> Owners in purple, "
            "renters in yellow. <bookmark mark='b'/> The owners are far richer: a median net worth of "
            f"{h['net_owners']:.1f} years of income against {h['net_renters']:.2f}. <bookmark mark='c'/> And they "
            f"spend more of a windfall, {h['mpc_owners']:.2f} against {h['mpc_renters']:.2f}. Across all "
            f"households, the share spent rises with net worth: a correlation of {h['corr_net']:+.2f}. Richer "
            "households spending faster looks like a contradiction. <bookmark mark='d'/> Now move every dot to its "
            "liquid wealth instead. <bookmark mark='e'/> They fall onto a single curve. The correlation is "
            f"{h['corr_liquid']:+.2f}. What a household spends out of a windfall depends on the cash it has, not on "
            "what it owns."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.001), FadeIn(side[0]), FadeIn(side[1]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(*[d.animate.move_to(p) for d, p in zip(dots, targets)], FadeOut(ax.xlabel),
                      FadeIn(xl_liquid), run_time=4)
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()
