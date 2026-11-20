from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class PIH(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Permanent income and the life cycle", r"How should a household that looks ahead spread its "
             r"income over its life?", "Chapter three. Permanent income and the life cycle.",
             lit={1954: r"Modigliani and Brumberg", 1957: r"Friedman"}, scale=("household",),
             horizon=("a lifetime",))
        self.euler()
        self.annuity()
        self.lifecycle()
        self.growth()

    def euler(self):
        rows = VGroup(
            label(r"from Part 7: \ a household choosing consumption over time", font_size=24, color=GREY_A),
            MathTex(r"u'(c_t) \;=\; \beta (1+r)\, \mathbb{E}_t\, u'(c_{t+1})", font_size=48, color=WHITE),
            label(r"give up a dollar today, \ get $1+r$ tomorrow, \ valued at $\beta$: \ at the best plan, \ no gain "
                  r"either way", font_size=22, color=GREY_A),
            MathTex(r"\beta(1+r) = 1 \;\Rightarrow\; c_t = \mathbb{E}_t\, c_{t+1}", font_size=44, color=SPEND),
            label(r"plan a flat path of consumption: \ smooth", font_size=24, color=SPEND),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "Both answers start from Part seven's Euler equation. <bookmark mark='a'/> A household choosing how much "
            "to consume today and tomorrow sets the marginal utility of a dollar spent today equal to the discounted "
            "marginal utility of what that dollar becomes tomorrow, one plus r of it, valued at beta. "
            "<bookmark mark='b'/> At the best plan there is no gain from shifting a dollar either way. "
            "<bookmark mark='c'/> If patience just offsets the interest rate, beta times one plus r equals one, and "
            "with marginal utility falling in consumption, the plan is flat: expected consumption tomorrow equals "
            "consumption today. <bookmark mark='d'/> The household smooths."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            for mk, r_ in zip("bcd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def annuity(self):
        p = load("pih")
        rows = VGroup(
            MathTex(r"\sum_{t \ge 0} \frac{c_t}{(1+r)^t} \;=\; A_0 + \underbrace{\sum_{t \ge 0} "
                    r"\frac{\mathbb{E}\,y_t}{(1+r)^t}}_{\text{human wealth } H}", font_size=40),
            MathTex(r"c \;=\; \frac{r}{1+r}\,\big(A_0 + H\big) \;\equiv\; y^P \quad \text{(permanent income)}",
                    font_size=42, color=INCOME),
            VGroup(
                label(r"a windfall of \$1, \ once:", font_size=24, color=SAVE),
                MathTex(r"\Delta c = \frac{r}{1+r} = " + f"{p['share_year']:.3f}", font_size=36, color=SAVE),
                label(rf"{100 * p['share_year']:.1f} cents a year, \ for ever", font_size=22, color=SAVE),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                label(r"a raise of \$1 a year, \ for good:", font_size=24, color=SPEND),
                MathTex(r"\Delta c = \frac{r}{1+r}\cdot\frac{1+r}{r} = 1", font_size=36, color=SPEND),
                label(r"spent in full", font_size=22, color=SPEND),
            ).arrange(RIGHT, buff=0.3),
            label(r"only news moves consumption: \ an income change foreseen is already in the plan", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "Now add the budget. <bookmark mark='a'/> The present value of everything the household will consume "
            "equals what it owns today plus the present value of everything it expects to earn, its human wealth. "
            "<bookmark mark='b'/> With a flat plan and a long horizon, consumption is the interest on total wealth: "
            "r over one plus r, times assets plus human wealth. Friedman called that permanent income. "
            "<bookmark mark='c'/> So a windfall of one dollar, once, raises consumption by r over one plus r: at "
            f"three percent, {100 * p['share_year']:.1f} cents a year, for ever. Under one cent a quarter. That was "
            "the answer the theory gave in the game. <bookmark mark='d'/> A raise of a dollar a year, for good, "
            "raises human wealth by one plus r over r dollars, and consumption by the whole dollar. "
            "<bookmark mark='e'/> And a change that was foreseen, like a cheque whose date was announced, is already "
            "in the plan. Only news moves consumption."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def lifecycle(self):
        p = load("pih")
        l_ = p["life"]
        age = np.array(l_["age"], float)
        ax = plane([25, 85], [0, 15], center=LEFT * 1.4 + DOWN * 0.75, x_length=8.8, y_length=4.4,
                   xticks=[25, 45, 65, 85], yticks=[0, 5, 10, 15], xlabel=r"age",
                   ylabel=r"years of average income", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                   font_size=16)
        ax2 = plane([25, 85], [0, 1.5], center=LEFT * 1.4 + DOWN * 0.75, x_length=8.8, y_length=4.4,
                    xticks=[], yticks=[], font_size=16)
        ax2.set_opacity(0)
        inc = path(ax2, age, l_["income"], color=INCOME, width=4, smooth=False)
        con = path(ax2, age, l_["consumption"], color=SPEND, width=4, smooth=False)
        ast = path(ax, age, l_["assets"], color=SAVE, width=4, smooth=False)
        side = VGroup(
            label(r"income: \ rises, \ peaks, \ stops at 65", font_size=20, color=INCOME),
            label(r"consumption: \ flat for life", font_size=20, color=SPEND),
            label(rf"wealth: \ a hump, \ peaking at {l_['peak_age']} \\ (scale on the left)", font_size=20,
                  color=SAVE),
            label(r"the young save, \ the old dissave", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        note_ = label(r"income and consumption drawn at ten times their scale", font_size=15,
                      color=GREY_B).next_to(ax, DOWN, buff=0.45)
        hc = history_card(1954, r"Franco Modigliani and Richard Brumberg", r"the life-cycle hypothesis",
                          color=SAVE, width=6.4, font_size=19).to_corner(UR, buff=0.25)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Franco Modigliani and Richard Brumberg, in 1954, gave the same logic a lifetime with an end. "
            "<bookmark mark='a'/> Income rises through a working life, peaks, and stops at retirement. "
            "<bookmark mark='b'/> Consumption, by the Euler equation, stays flat. <bookmark mark='c'/> The gap is "
            "saving, so wealth follows a hump: built up while working, it peaks at retirement, at "
            f"{l_['peak_age']} here, at about {max(l_['assets']):.0f} years of average income, and is run down to "
            "nothing by the end. <bookmark mark='d'/> The young save, the old dissave."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(hc), FadeIn(tag), FadeIn(note_))
            vo.wait_until("a")
            self.play(Create(inc), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(con), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ast), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def growth(self):
        rows = rows_card([
            (r"what the life cycle says about nations", E.ACCENT, 28),
            (r"saving comes from the young, \ dissaving from the old", GREY_A, 24),
            (r"faster income growth: \ the young are richer than the old were, \ so the nation saves more", SAVE, 24),
            (r"an ageing population: \ more retirees running down wealth, \ so the nation saves less", OLD, 24),
            (r"no Keynesian constant needed: \ the ratio of saving to income depends on growth and age", SPEND, 24),
            (r"Modigliani's Nobel prize, \ 1985: \ for his analyses of saving and of financial markets", GREY_B, 21),
        ], buff=0.4)
        with self.voiceover(
            "The life cycle says something about nations, too. <bookmark mark='a'/> Saving comes from the young and "
            "dissaving from the old. <bookmark mark='b'/> If income grows quickly, each young generation is richer "
            "than the old one was, its saving outweighs the old's dissaving, and the nation saves more. "
            "<bookmark mark='c'/> If the population ages, more retirees are running down their wealth, and the "
            "nation saves less. <bookmark mark='d'/> No psychological law is needed. A country's saving rate depends "
            "on its growth and its age structure, which is why it was stable while America's growth was. "
            "<bookmark mark='e'/> Modigliani's Nobel prize, in 1985, was for his analyses of saving and of financial "
            "markets."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
