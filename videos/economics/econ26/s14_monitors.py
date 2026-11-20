from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class Monitors(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Banks as monitors", r"Why have banks at all, \ and what is lost when they fail?",
             "Chapter twelve. Banks as monitors.", lit={1983: r"Bernanke", 1984: r"Diamond"},
             scale=("firm", "nation"), horizon=("years",))
        self.delegate()
        self.diversify()
        self.lost()

    def delegate(self):
        M = load("monitor")
        rows = VGroup(
            label(r"why not lend to firms directly?", font_size=28, color=E.ACCENT),
            label(rf"a firm needs money from {M['depositors']:,} savers; \ checking on it costs {M['cost']} each",
                  font_size=23, color=GREY_A),
            label(rf"if every saver checks: \ {M['depositors']:,} $\times$ {M['cost']} $=$ {M['direct_cost']:.0f}; "
                  r"\ if none does, \ nobody is watching", font_size=23, color=RUN),
            label(rf"delegate it to a bank: \ {M['bank_cost']} \ once", font_size=24, color=LOAN),
            label(r"but then who watches the bank?", font_size=25, color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Diamond, \ Review of Economic Studies 51(3) (1984): \ 393--414", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Douglas Diamond asked a more basic question in 1984. <bookmark mark='a'/> Why lend through a bank at "
            "all? <bookmark mark='b'/> Suppose a firm needs money from a thousand savers, and checking on what the "
            "firm does with it costs each of them a little. <bookmark mark='c'/> If every saver checks, the checking "
            "is done a thousand times. If nobody checks, nobody is watching, and the firm can claim it did badly and "
            "pay little. <bookmark mark='d'/> Delegate the checking to a bank, and it is done once. "
            "<bookmark mark='e'/> But then the savers have a new problem: who watches the bank?"
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def diversify(self):
        M = load("monitor")
        n = np.array(M["n"], float)
        ax = plane([0, 3], [0, 0.12], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=4.8,
                   xticks=[0, 1, 2, 3], yticks=[0, 0.04, 0.08, 0.12], xlabel=r"loans the bank makes \ (log scale)",
                   ylabel=r"chance it cannot repay its depositors", xfmt=lambda v: f"{10 ** v:,.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        curve = path(ax, np.log10(n), M["fail"], color=LOAN, width=4, smooth=False)
        P = M["points"]
        dots = VGroup(*[dot(ax, np.log10(int(k)), v, color=STAY, r=0.08) for k, v in P.items()])
        side = VGroup(
            label(rf"each loan repays {M['R']} \\ with probability {M['p']}, \ else nothing; \\ depositors are "
                  rf"promised {M['D']:.0f} a loan", font_size=19, color=GREY_A),
            label(rf"1 loan: \ {100 * P['1']:.0f}\%", font_size=20, color=STAY),
            label(rf"10 loans: \ {100 * P['10']:.0f}\%", font_size=20, color=STAY),
            label(rf"100 loans: \ {100 * P['100']:.3f}\%", font_size=20, color=STAY),
            label(r"diversification makes the bank's \\ promise nearly safe: \\ the depositors need hardly watch",
                  font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Diamond's answer is diversification. <bookmark mark='a'/> On the Island, each loan repays "
            f"{M['R']} with probability {M['p']} and nothing otherwise, and the bank promises its depositors one "
            f"for every loan. <bookmark mark='b'/> With a single loan, the bank fails to pay them one time in ten. "
            f"<bookmark mark='c'/> With ten loans, about {100 * P['10']:.0f} percent of the time. "
            f"<bookmark mark='d'/> With a hundred, about four times in a hundred thousand. <bookmark mark='e'/> A bank "
            "with many independent loans can promise a fixed payment and nearly always keep it, so its depositors "
            "hardly need to watch it. That is why a bank's liabilities are simple debts. The catch is the word "
            "independent: in a crisis, loans go bad together."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(curve), FadeIn(side[0]), run_time=1.5)
            for k, (mk, r_) in enumerate(zip("bcd", side[1:4])):
                vo.wait_until(mk)
                self.play(FadeIn(r_), FadeIn(dots[k]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def lost(self):
        rows = VGroup(
            label(r"Bernanke, \ 1983: \ what is lost when banks fail", font_size=27, color=E.ACCENT),
            label(r"a bank's knowledge of its borrowers is capital, \ built over years, \ and it dies with the bank",
                  font_size=22, color=LOAN),
            label(r"1930--33: \ farmers, \ households and small firms lost credit that no one else would give",
                  font_size=22, color=RUN),
            label(r"the failures help explain the fall in output, \ beyond the fall in the money supply",
                  font_size=22, color=GREY_A),
            label(r"2022: \ the Nobel prize, \ to Bernanke, \ Diamond and Dybvig, \ for research on banks and "
                  r"financial crises", font_size=22, color=STAY),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Bernanke, \ AER 73(3) (1983): \ 257--276", corner=DR, font_size=12)
        with self.voiceover(
            "If banks exist to know their borrowers, a bank failure destroys something. <bookmark mark='a'/> That "
            "was Ben Bernanke's argument in 1983. <bookmark mark='b'/> What a bank knows about its borrowers is a "
            "kind of capital, built up over years of lending, and it dies with the bank. "
            "<bookmark mark='c'/> When thousands of banks failed from 1930 to 1933, farmers, households and small "
            "firms lost credit that no other lender knew them well enough to give. <bookmark mark='d'/> In his "
            "regressions, the failures help explain the collapse of output, beyond what the fall in the money "
            "supply explains. <bookmark mark='e'/> In 2022, Bernanke, Diamond and Dybvig shared the Nobel prize "
            "for their research on banks and financial crises."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
