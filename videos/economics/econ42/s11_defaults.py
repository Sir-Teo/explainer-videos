from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Defaults(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Defaults", r"Can a form raise saving more than a subsidy?",
             "Chapter nine. Defaults.", lit={2001: r"Madrian and Shea", 2004: r"Thaler and Benartzi",
                                            2014: r"Chetty et al."},
             scale=("person", "firm"), horizon=("a year", "a decade"))
        self.firm()
        self.island()
        self.denmark()

    def firm(self):
        M = tables.MADRIAN_SHEA_2001.data
        p = M["participation"]
        before = p["hired the year before, same tenure"]
        after = p["auto-enrolled (3-15 months' tenure)"]
        vals = [(r"hired the year before, \\ same tenure: \ opt in", before, GREY_B),
                (r"hired after the switch: \\ enrolled unless they opt out", after, GAIN)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(vals):
            x = -3.6 + 3.0 * k
            h = v * 4.4
            r = Rectangle(width=1.6, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([x, -2.5 + h / 2, 0]))
            bars.add(VGroup(r, label(nm, font_size=17, color=WHITE).next_to(r, DOWN, buff=0.15),
                            label(rf"{100 * v:.0f}\%", font_size=26, color=col).next_to(r, UP, buff=0.12)))
        side = VGroup(
            label(rf"one large American firm, \\ {M['date']}: \ new hires \\ enrolled automatically", font_size=18,
                  color=GREY_A),
            label(rf"at {100 * M['default_rate']:.0f}\% of pay, \\ in {M['default_fund']}", font_size=18,
                  color=WHITE),
            label(rf"{100 * M['at_default']:.0f}\% of them stayed \\ at the default rate", font_size=18,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        head = label(r"401(k) participation", font_size=24, color=E.ACCENT).next_to(bars, UP, buff=0.9)
        tag = published_tag(tables.MADRIAN_SHEA_2001.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Part seven met Brigitte Madrian and Dennis Shea's study; here is what it means for policy. "
            f"<bookmark mark='a'/> On {M['date']}, a large American firm changed one thing about its retirement "
            "plan: new employees were enrolled automatically, unless they asked not to be. "
            "<bookmark mark='b'/> Among workers hired the year before, who had to sign up, "
            f"{say_pct(before, 0)} were saving at the same tenure. "
            f"Among those hired after the switch, {say_pct(after, 0)}. "
            "<bookmark mark='c'/> The default was three percent of pay, in a money market fund, "
            f"<bookmark mark='d'/> and {say_pct(M['at_default'], 0)} of the automatically enrolled stayed at "
            "exactly that rate, although few had chosen it before. A default is not neutral: it is a decision made "
            "for everyone who does not decide."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(side[0]), *[FadeIn(b_[1]) for b_ in bars], run_time=1.2)
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b_[0], DOWN) for b_ in bars])
            vo.wait_until("b")
            self.play(*[FadeIn(b_[2]) for b_ in bars])
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def island(self):
        D = load("defaults")
        t = np.array(D["t"])
        ax = plane([0, 48], [0, 1.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 12, 24, 36, 48], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"months in the job",
                   ylabel=r"share of employees", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        lo = path(ax, t, D["opt_in"], GREY_B, 3.2)
        la = path(ax, t, D["auto"], GAIN, 3.2)
        ld = path(ax, t, D["at_default"], PENSION, 2.6)
        side = VGroup(
            label(rf"each month, \ a {100 * D['attention']:.1f}\% chance \\ of acting on the choice; \\ "
                  rf"{100 * D['want']:.0f}\% would choose to save", font_size=17, color=GREY_A),
            label(rf"grey: \ opt in: \\ {100 * D['m15_opt']:.0f}\% at 15 months", font_size=18, color=GREY_B),
            label(rf"green: \ automatic: \\ {100 * D['m15_auto']:.0f}\% at 15 months", font_size=18, color=GAIN),
            label(rf"gold: \ still at the default: \\ {100 * D['m15_default']:.0f}\%", font_size=18, color=PENSION),
            label(r"the gap closes \\ only slowly", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Why does a default matter so much? Inertia is enough. <bookmark mark='a'/> On the Island, employees "
            "get round to choosing a savings plan only occasionally, about once in two years on average, and when "
            "they do, three in four choose to save. <bookmark mark='b'/> If they must opt in, "
            f"{say_pct(D['m15_opt'], 0)} are saving after fifteen months. <bookmark mark='c'/> Enrolled "
            f"automatically, {say_pct(D['m15_auto'], 0)}: close to the firm's numbers. <bookmark mark='d'/> And "
            f"{say_pct(D['m15_default'], 0)} are still at the default rate, not because they chose it but because "
            "they have not yet chosen. <bookmark mark='e'/> The gap closes only slowly, as people get round to "
            "deciding; meanwhile, the default decides."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            self.play(Create(lo), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(lo, color=WHITE, scale_factor=1.0))
            vo.wait_until("c")
            self.play(Create(la), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(ld), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def denmark(self):
        K = tables.CHETTY_DK_2014.data
        T = tables.THALER_BENARTZI_2004.data
        cards = point_cards([
            (rf"{K['passive']}\% passive", r"Danes who do not \\ respond to subsidies, \\ but keep what is \\ saved "
                                           r"for them", GAIN),
            (rf"{K['active']}\% active", r"respond to subsidies \\ mostly by moving \\ money between \\ accounts",
             HOLD),
            (rf"{K['cents']} cent", r"extra saving per \\ dollar of subsidy", LOSS),
            (r"Save More Tomorrow", rf"commit now to save \\ from future raises: \\ {100 * T['before']:.1f}\% to "
                                    rf"{100 * T['after']:.1f}\% \\ in {T['months']} months", UNEMP),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"defaults against subsidies", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.CHETTY_DK_2014.tag + r"; \ " + tables.THALER_BENARTZI_2004.tag, corner=DR,
                            font_size=10)
        with self.voiceover(
            "Do defaults raise saving, or just move it? Raj Chetty and coauthors followed the savings of Danes in "
            f"{K['obs_millions']} million records. <bookmark mark='a'/> About {K['passive']} percent are passive: "
            "they do not respond to tax subsidies at all, but they keep whatever an employer or the government "
            "saves for them automatically, so automatic contributions raise their total saving. "
            f"<bookmark mark='b'/> About {K['active']} percent are active, and respond to a subsidy mostly by moving "
            "money from one account to another. <bookmark mark='c'/> So each dollar of subsidy raised total saving "
            "by about one cent. <bookmark mark='d'/> Richard Thaler and Shlomo Benartzi's Save More Tomorrow uses "
            "inertia the other way: employees commit now to save part of future raises, and in the first firm to "
            f"try it, saving rates rose from {say_pct(T['before'], 1)} to {say_pct(T['after'], 1)} in "
            f"{T['months']} months, among those who chose to join."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
