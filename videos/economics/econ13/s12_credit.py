from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403

BANK = "#7EC8F5"


class Credit(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Credit rationing", r"Why would a bank refuse a borrower willing to pay more?", "Chapter ten. "
             r"Credit rationing.", lit={1981: r"Stiglitz and Weiss"}, scale=("person", "firm", "market"),
             horizon=("a year",))
        self.curve()
        self.ration()

    def curve(self):
        c = load("credit")
        R = np.array(c["R"])
        ret = np.array(c["bank_return"])
        ax = plane([100, 280], [40, 120], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[100, 150, 177.8, 220, 260], yticks=[50, 75, 100, 106.4], xlabel=r"repayment the bank asks "
                   r"for, \ per \$100 lent", ylabel=r"what the bank expects back, \ \$", font_size=16,
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}" if v % 1 else f"{v:.0f}")
        a = ax.ax
        lo = R <= c["safe_leave"]
        hi = (R > c["safe_leave"]) & (R < c["risky_leave"])
        p1 = path(ax, R[lo], ret[lo], color=BANK, width=3.5, smooth=False)
        p2 = path(ax, R[hi], ret[hi], color=BANK, width=3.5, smooth=False)
        drop = DashedLine(a.c2p(c["safe_leave"], ret[lo][-1]), a.c2p(c["safe_leave"], ret[hi][0]), color=LOSS,
                          stroke_width=2)
        star = Dot(a.c2p(c["R_star"], c["return_star"]), radius=0.09, color=EQ)
        par = DashedLine(a.c2p(100, 100), a.c2p(280, 100), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            label(rf"safe borrowers: \ succeed {100 * c['s_safe']:.0f}\% of the time; \\ risky ones: \ "
                  rf"{100 * c['s_risky']:.0f}\%; \ half of each; \\ the bank can't tell them apart", font_size=20),
            label(r"a failed borrower repays nothing, \\ and chasing them costs the bank \$60", font_size=20,
                  color=GREY_A),
            label(r"raising the rate earns more from each borrower \\ who stays", font_size=20, color=BANK),
            label(rf"but above \${c['safe_leave']:.0f} the safe borrowers' projects \\ no longer pay: \ they leave, \\ "
                  r"and the bank's expected return drops", font_size=20, color=LOSS),
            label(rf"the bank does best at \${c['R_star']:.0f}: \\ \${c['return_star']:.2f} back for every \$100",
                  font_size=21, color=EQ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"after Stiglitz and Weiss, AER 71(3) (1981); \ the numbers: \ Agora", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Lenders face the same problem as insurers. <bookmark mark='a'/> On the Island, two kinds of borrower ask "
            "the bank for a hundred dollars each. Safe borrowers' projects succeed nine times in ten, risky ones' half "
            "the time, and the bank cannot tell them apart. <bookmark mark='b'/> A borrower whose project fails repays "
            "nothing, and chasing them costs the bank sixty dollars. <bookmark mark='c'/> As the bank raises the "
            "repayment it asks for, it earns more from each borrower who stays. <bookmark mark='d'/> But above about "
            "a hundred and seventy-eight dollars, the safe borrowers' projects no longer pay them enough, and they "
            "stop applying. The bank is left with the risky ones, and what it expects back drops sharply. "
            "<bookmark mark='e'/> So the bank does best by asking a hundred and seventy-eight dollars, and expects "
            "about a hundred and six dollars back for every hundred it lends."
        ) as vo:
            self.play(FadeIn(ax), Create(par), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(p1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(drop), Create(p2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(star, scale=1.5), FadeIn(side[4]))
        self.clear_scene()

    def ration(self):
        rows = VGroup(
            label(r"Joseph Stiglitz and Andrew Weiss (1981): \ the interest rate also sorts borrowers", font_size=24),
            label(r"if more people want loans at that rate than the bank can fund, \ it won't raise the rate: \ it "
                  r"refuses some", font_size=23, color=LOSS),
            label(r"credit rationing: \ applicants turned away who would gladly pay more", font_size=24, color=EQ),
            label(r"collateral, \ track records and relationships are how lenders screen instead", font_size=23,
                  color=SIGNAL),
            label(r"banks and runs: \ Part 26; \ group lending and microfinance: \ Part 46", font_size=23,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Stiglitz and Weiss, AER 71(3) (1981)", corner=DR, font_size=13)
        with self.voiceover(
            "Joseph Stiglitz and Andrew Weiss drew the conclusion in 1981. <bookmark mark='a'/> The interest rate is "
            "not just a price; it also sorts borrowers, and raising it drives away the safe ones first. "
            "<bookmark mark='b'/> If more people want loans at the bank's best rate than it can fund, it won't raise "
            "the rate to clear the market. It refuses some applicants instead. <bookmark mark='c'/> That is credit "
            "rationing: borrowers turned away who would gladly pay more, in a market that never clears. "
            "<bookmark mark='d'/> Lenders screen in other ways instead: collateral, credit records, and long "
            "relationships. <bookmark mark='e'/> Part twenty-six returns to banks, and Part forty-six to group "
            "lending among the poor."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
