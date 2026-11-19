from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ insurance and pensions", r"How do insurers, employers and governments use "
             r"these ideas?", "Chapter fourteen. In practice: insurance and pensions.",
             scale=("household", "firm", "market", "nation"), horizon=("a year", "a decade", "a century"))
        self.pooling()
        self.defaults()
        self.discount_rate()

    def pooling(self):
        b = load("insurance")
        loss, p = b["boat"], b["storm"]
        mean = p * loss
        sd = loss * np.sqrt(p * (1 - p))
        ns = [1, 10, 100, 1000, 10_000]
        rows = VGroup(*[VGroup(label((rf"{n:,} boats" if n > 1 else r"1 boat").replace(",", "{,}"), font_size=26),
                               label(rf"\${mean:.0f} $\pm$ \${sd / np.sqrt(n):.2f}", font_size=28,
                                     color=SAFE if n > 1 else RISKY)).arrange(RIGHT, buff=0.7) for n in ns])
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.22).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        head = label(r"the insurer's claims per boat \ (mean $\pm$ s.d.)", font_size=24, color=GREY_B).next_to(rows, UP,
                                                                                                         buff=0.3)
        side = VGroup(
            label(r"why an insurer can be calm \\ about risks that frighten Ana:", font_size=25),
            label(r"pooled independent risks average out: \\ the spread per policy falls like $1/\sqrt{n}$",
                  font_size=24, color=SAFE),
            label(r"so a premium of expected loss \\ plus a loading is enough", font_size=24),
            label(r"but a storm hits every boat at once: \\ correlated risk doesn't pool; \\ that is what "
                  r"reinsurance \\ and catastrophe bonds are for", font_size=23, color=RISKY),
            label(r"and buyers know their own risks: \\ adverse selection, \ Part 13", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        tag = island_tag(r"computed: the Island's boats", corner=DR, font_size=15)
        with self.voiceover(
            "In practice, insurance works because of the law of large numbers. <bookmark mark='a'/> One boat's "
            "expected claim is fifteen dollars a year, with a standard deviation of forty-five: frightening for Ana. "
            "<bookmark mark='b'/> An insurer with a hundred independent boats faces claims of fifteen dollars per "
            "boat, give or take four fifty. With ten thousand boats, give or take forty-five cents. "
            "<bookmark mark='c'/> The insurer can be almost risk neutral about a risk that terrifies each owner, "
            "and charge expected loss plus a loading for its costs. <bookmark mark='d'/> Pooling fails when risks "
            "move together. A storm that wrecks one boat wrecks the rest, and that's what reinsurance and "
            "catastrophe bonds exist to spread, across the whole world's capital. <bookmark mark='e'/> And buyers "
            "often know their own risks better than the insurer does, a problem big enough for its own part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows[1:]], lag_ratio=0.5),
                      FadeIn(side[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def defaults(self):
        ms = tables.MADRIAN_SHEA_2001.data
        tb = tables.THALER_BENARTZI_2004.data
        ax = plane([0, 2], [0, 100], center=LEFT * 3.6 + DOWN * 0.5, x_length=4.0, y_length=4.4, xticks=[],
                   yticks=[0, 25, 50, 75, 100], ylabel=r"in the 401(k) plan, \ \%", font_size=16)
        a = ax.ax
        vals = list(ms["participation"].items())
        bars = VGroup()
        for i, (name, v) in enumerate(vals[::-1]):
            col = SAFE if "auto" in name else GREY_B
            h = a.c2p(0, 100 * v)[1] - a.c2p(0, 0)[1]
            r_ = Rectangle(width=0.7, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                a.c2p(0.5 + i, 0), aligned_edge=DOWN)
            bars.add(VGroup(r_, label(rf"{100 * v:.0f}\%", font_size=24, color=col).next_to(r_, UP, buff=0.06),
                            label(r"hired the year \\ before" if i == 0 else r"enrolled \\ by default", font_size=17,
                                  color=GREY_A).next_to(a.c2p(0.5 + i, 0), DOWN, buff=0.12)))
        auto_ = 100 * ms["participation"]["auto-enrolled (3-15 months' tenure)"]
        before_ = 100 * ms["participation"]["hired the year before, same tenure"]
        side = VGroup(
            label(r"Madrian and Shea (2001): \ a firm enrols new hires \\ automatically from April 1998, at 3\%, \\ in "
                  r"the money market fund", font_size=23),
            label(rf"after 3--15 months: \ {auto_:.0f}\% in the plan, \\ against {before_:.0f}\% of those hired "
                  r"the year before", font_size=23, color=SAFE),
            label(rf"but {100 * ms['at_default']:.0f}\% stayed at the 3\% default: \\ inertia cuts both ways",
                  font_size=23, color=RISKY),
            label(rf"Save More Tomorrow (Thaler and Benartzi, 2004): \\ commit now to save from \emph{{future}} "
                  rf"raises; \\ saving rates {100 * tb['before']:.1f}\% $\to$ {100 * tb['after']:.1f}\% in "
                  rf"{tb['months']} months \\ (for those who chose to join)", font_size=22, color=LATER),
            label(r"present bias, \ used rather than fought", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Madrian and Shea (NBER WP 7682); Thaler and Benartzi, JPE (2004)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "The present bias of chapter eleven has changed how pensions are designed. <bookmark mark='a'/> In "
            "April 1998 a large American firm started enrolling new employees in its retirement plan automatically, "
            "at three percent of pay, unless they opted out. <bookmark mark='b'/> Brigitte Madrian and Dennis Shea "
            "compared them with people hired the year before, at the same length of service. Eighty-six percent of "
            "the new hires were in the plan, against thirty-seven percent of the earlier ones. Nothing about the "
            "plan's money had changed, only what happens if you do nothing. <bookmark mark='c'/> But seventy-six "
            "percent of the automatically enrolled stayed at the default three percent, in the default fund: inertia "
            "cuts both ways. <bookmark mark='d'/> Richard Thaler and Shlomo Benartzi designed a plan that uses the "
            "bias instead of fighting it: Save More Tomorrow asks people to commit now to saving more out of future "
            "pay rises, when the sacrifice is far away. Among those who joined, saving rates rose from three and a "
            "half percent to nearly fourteen in forty months. <bookmark mark='e'/> Commitment, offered at the moment "
            "it's cheap."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.6), FadeIn(side[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def discount_rate(self):
        years = 75
        lo, hi = 0.01, 0.05
        v_lo, v_hi = 100 / (1 + lo) ** years, 100 / (1 + hi) ** years
        ramsey = MathTex(r"r \;=\; \rho \;+\; \eta\, g", font_size=48, color=TODAY).to_edge(UP, buff=0.6)
        parts = label(r"Ramsey (1928): \ impatience $\rho$, \ plus how fast marginal utility falls ($\eta$) \\ times "
                      r"how fast consumption grows ($g$)", font_size=24, color=GREY_A).next_to(ramsey, DOWN, buff=0.3)
        io = is_ought_card(
            rf"\$100 of damage in 2100 is worth \${v_lo:.2f} today at 1\% a year, \ and \${v_hi:.2f} at 5\%",
            r"choose the discount rate for a public project, \ such as acting on the climate",
            r"how much a future person's consumption counts against ours: \ $\rho$ and $\eta$ are value "
            r"judgments, \ not only facts about markets", width=12.2, font_size=23).next_to(parts, DOWN, buff=0.5)
        foot = label(r"the Stern Review (2006) and William Nordhaus disagreed mostly about this: \ Part 48",
                     font_size=23, color=GREY_A).to_edge(DOWN, buff=0.4)
        tag = illustrative_tag(r"illustrative rates; \ computed", corner=DR, font_size=14)
        with self.voiceover(
            "Governments discount too, and there the choice of rate is not only a technical matter. "
            "<bookmark mark='a'/> Frank Ramsey's formula of 1928 says the rate should be impatience, rho, plus how "
            "fast marginal utility falls, eta, times how fast consumption grows. <bookmark mark='b'/> Here's what is "
            "at stake. A hundred dollars of damage in the year 2100 is worth forty-seven dollars today at one "
            "percent a year, and two dollars fifty-eight at five percent. <bookmark mark='c'/> Which rate to use, for "
            "a dam or for the climate, depends on how much a future person's consumption should count against ours. "
            "Rho and eta can be read from markets, but whether those are the right numbers for a whole society, "
            "including people not yet born, is a value judgment. <bookmark mark='d'/> When the Stern Review of 2006 "
            "and William Nordhaus reached very different answers about acting on the climate, this was mostly why. "
            "Part forty-eight takes it up."
        ) as vo:
            self.play(FadeIn(tag), Write(ramsey))
            vo.wait_until("a")
            self.play(FadeIn(parts))
            vo.wait_until("b")
            self.play(FadeIn(io.card), FadeIn(io.is_row))
            vo.wait_until("c")
            self.play(FadeIn(io[1][1]), FadeIn(io.judgment))
            self.play(FadeIn(io[1][3]), FadeIn(io.ought))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
