from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 13, r"In practice: \ how memos are used", r"Who writes them, \ who reads them, \ and how they go "
                                                               r"wrong",
             "Chapter thirteen. In practice: how memos are used, and misused.",
             lit={1974: r"CBO", 2003: r"Circular A-4", 2021: r"Corinth et al."}, scale=("nation",),
             horizon=("a year", "a decade"))
        self.people()
        self.misuse()
        self.called()

    def people(self):
        rows = VGroup(
            label(r"budget offices: \ the cost of a bill, \ year by year, \ over a ten-year window", font_size=22,
                  color=BUDGET),
            label(r"tax analysts: \ revenue, \ and who pays, \ by income group", font_size=22, color=NEW),
            label(r"regulators: \ costs and benefits, \ under written guidance such as Circular A-4 or the Green "
                  r"Book", font_size=22, color=WORK),
            label(r"ministries and think tanks: \ memos for and against, \ often on the same numbers", font_size=22,
                  color=CHILD),
            label(r"evaluators: \ the trial or the staggered start that tests the policy afterwards", font_size=22,
                  color=EVIDENCE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        head = label(r"the people who write and read memos", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Who writes memos like this, and for whom? <bookmark mark='a'/> Budget offices, such as America's "
            "Congressional Budget Office, created in 1974, which estimate what a bill costs, year by year, over a "
            "ten-year window. <bookmark mark='b'/> Tax analysts, who estimate revenue and who pays it, by income "
            "group. <bookmark mark='c'/> Regulators, who weigh costs and benefits under written guidance: "
            "America's Circular A-4, Britain's Green Book. <bookmark mark='d'/> Ministries and think tanks, who "
            "write memos for and against a policy, often from the same numbers. <bookmark mark='e'/> And "
            "evaluators, who test a policy after it starts, when it is designed so that it can be tested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def misuse(self):
        cards = point_cards([
            (r"the window", r"a policy made temporary to look cheap: \ the 2021 credit was enacted for one year",
             BUDGET),
            (r"one number", r"a point estimate with no range, \ read as a fact", HOLD),
            (r"the chosen dial", r"an elasticity picked for the answer it gives, \ high or low", LOSS),
            (r"static or dynamic", r"ignoring behaviour, \ or assuming too much of it", WORK),
            (r"the missing table", r"an average gain that hides who loses", CHILD),
            (r"the hidden judgment", r"a value judgment presented as a finding", NEW),
        ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.2)
        head = label(r"six ways a memo goes wrong", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "And how do memos go wrong? Six ways, each of which this film has tried to avoid. <bookmark mark='a'/> "
            "The window: a policy made temporary so that its cost within the window looks small. The 2021 credit "
            "was enacted for a single year. <bookmark mark='b'/> One number: a point estimate with no range, read "
            "as a fact. <bookmark mark='c'/> The chosen dial: an elasticity picked for the answer it gives, by "
            "supporters or by opponents. <bookmark mark='d'/> Static or dynamic: a cost that ignores behaviour, or "
            "one that assumes far more of it than the evidence supports. <bookmark mark='e'/> The missing table: "
            "an average gain that hides who loses. <bookmark mark='f'/> And the hidden judgment: a value judgment, "
            "such as the weight on poor children's incomes, dressed as a finding."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcdef", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["corinth_2021"]
        A = tables.ALLOWANCE_50.data
        I = load("island")
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 1.5)
        ax = plane([0, 3], [0, 3.2], center=DOWN * 2.1 + LEFT * 1.2, x_length=6.4, y_length=2.4, xticks=[],
                   yticks=[0, 1, 2, 3], ylabel=r"working parents who stop, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=12)

        def bar(x, v, col, txt):
            p0, p1 = ax.ax.c2p(x - 0.35, 0), ax.ax.c2p(x + 0.35, max(v, 0.02))
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            return VGroup(r, label(txt, font_size=13, color=col).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.1))

        b1 = bar(0.5, float(A["exit_share"]), LOSS, r"their simulation")
        b2 = bar(1.5, 100 * I["exit_share"], NEW, r"the Island, \ 0.25")
        b3 = VGroup(label(r"$\approx 0$?", font_size=22, color=EVIDENCE).move_to(ax.ax.c2p(2.5, 0.5)),
                    label(r"2021, \ measured", font_size=13, color=EVIDENCE).next_to(ax.ax.c2p(2.5, 0), DOWN,
                                                                                    buff=0.1))
        cap = label(r"temporary payments: \\ effects too small \\ to detect", font_size=12, color=GREY_A).next_to(
            ax, RIGHT, buff=0.35)
        tag = published_tag(r"Corinth et al. (2021); \ Ananat et al. (2022); \ Baker et al. (2023)", corner=DL,
                            font_size=11)
        with self.voiceover(
            "Called it? A forecast about this very policy. <bookmark mark='a'/> In September 2021, while the "
            "monthly payments were arriving, Kevin Corinth, Bruce Meyer, Matthew Stadnicki and Derek Wu "
            f"forecast that a permanent allowance would lead about {A['exits']} million working parents to leave "
            f"work, {A['exit_share']} percent of them, and that child poverty would fall by at most "
            f"{A['max_cut']} percent. <bookmark mark='b'/> The Island's central case is gentler, "
            f"{100 * I['exit_share']:.1f} percent. <bookmark mark='c'/> What happened: the temporary payments of "
            "2021 showed no detectable effect on parents' work, and Canada's permanent benefit showed none "
            "either. <bookmark mark='d'/> The verdict: too early to say. America has not tried a permanent "
            "allowance, and a payment expected to end may not change behaviour as a permanent one would. The "
            "forecast was the right question, asked carefully; the evidence that would settle it does not yet "
            "exist."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ax), GrowFromEdge(b1[0], DOWN), FadeIn(b1[1]), run_time=1.0)
            vo.wait_until("b")
            self.play(GrowFromEdge(b2[0], DOWN), FadeIn(b2[1]))
            vo.wait_until("c")
            self.play(FadeIn(cc.right), FadeIn(b3), FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
