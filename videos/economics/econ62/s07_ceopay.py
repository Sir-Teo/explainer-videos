from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class CEOPay(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Executive pay", r"Why is a chief executive paid so much, \ and for what?",
             "Chapter six. Executive pay.", lit={1990: r"Jensen and Murphy", 2001: r"Bertrand and Mullainathan",
                                                 2008: r"Gabaix and Landier"},
             scale=("person", "firm"), horizon=("a decade",))
        self.size()
        self.luck()

    def size(self):
        C = load("ceo")
        rank = np.array(C["rank"], float)
        pay, pay6 = np.array(C["pay"]), np.array(C["pay_x6"])
        top = pay[0]
        lr = np.log10(rank)
        ax = plane([0, 2.75], [-1.0, 1.0], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.6,
                   xticks=[0, 1, 2, np.log10(500)], yticks=[-1, 0, 1], xlabel=r"the firm's rank by size \ (log "
                   r"scale)", ylabel=r"the CEO's pay \ (top CEO in the first year = 1, \ log scale)",
                   xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{10 ** v:g}", font_size=14)
        p1 = path(ax, lr, np.log10(pay / top), CEO, 3.0)
        p6 = path(ax, lr, np.log10(pay6 / top), GAIN, 3.0)
        side = VGroup(
            label(r"talent differs only a little between CEOs; \\ but a little more talent at a huge firm is worth "
                  r"a lot", font_size=19, color=WHITE),
            label(rf"across firms: \ pay rises with the firm's size to the power {C['elasticity_own_size']:.2f}",
                  font_size=19, color=CEO),
            label(rf"the top firm's CEO earns {C['top_over_250th']:.1f} times the 250th's", font_size=19,
                  color=CEO),
            label(rf"make every firm six times larger: \ pay rises {C['ratio_after_sixfold']:.0f}-fold", font_size=20,
                  color=GAIN),
            label(r"American CEO pay rose about six-fold from 1980 to 2003, \\ as large firms' market values did "
                  r"\ (Gabaix and Landier)", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Gabaix and Landier, \ Quarterly Journal of Economics 123(1) (2008); \ computed: \ "
                            r"agora.org.ceo\_pay", corner=DL, font_size=12)
        with self.voiceover(
            "Why are chief executives paid so much? One answer is a market. Xavier Gabaix and Augustin Landier "
            "assign managers to firms like Part seventeen's matching: the most talented to the largest firm. "
            "<bookmark mark='a'/> Talent differs only a little between the best chief executives and the "
            "five-hundredth, but a little more talent applied to a huge firm is worth a great deal, so firms bid "
            "for it. <bookmark mark='b'/> In equilibrium, across firms, pay rises with the firm's size to the power "
            f"of about a third. <bookmark mark='c'/> The largest firm's chief executive earns "
            f"{C['top_over_250th']:.1f} times as much as the two-hundred-and-fiftieth's. <bookmark mark='d'/> And "
            "if every firm grows six-fold, every chief executive's pay grows six-fold too, because what a manager "
            "is worth moves with the size of the firms bidding. <bookmark mark='e'/> That is what happened in "
            "America: chief executives' pay rose about six-fold between 1980 and 2003, and so did the market "
            "value of large companies. The theory explains the level without anyone behaving badly; it does not "
            "say the pay is deserved, only that it is what this market produces."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(p1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(TransformFromCopy(p1, p6), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def luck(self):
        L = load("ceo")["luck"]
        keys = ("strong board", "weak board")
        vals_p = [L[k]["on_performance"] for k in keys]
        vals_l = [L[k]["on_luck"] for k in keys]
        ax = plane([-0.6, 1.6], [-0.1, 0.65], center=LEFT * 3.0 + DOWN * 0.4, x_length=5.6, y_length=4.4,
                   xticks=[], yticks=[0, 0.2, 0.4, 0.6], ylabel=r"pay's response, \ per unit",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        bp = bars(ax, np.arange(2) - 0.16, vals_p, [CEO, CEO], width=0.3)
        bl = bars(ax, np.arange(2) + 0.16, vals_l, [COST, COST], width=0.3)
        labs = VGroup(*[label(k, font_size=15, color=c).next_to(ax.ax.c2p(i, -0.1), DOWN, buff=0.1)
                        for i, (k, c) in enumerate(zip(keys, (OWN, COST)))])
        side = VGroup(
            label(r"a firm's results = \ the CEO's skill \ + \ luck everyone can see \ (an oil price)",
                  font_size=19, color=WHITE),
            label(r"orange: \ pay's response to results; \ red: \ to luck alone", font_size=19, color=CEO),
            label(rf"a strong board pays for skill: \ {vals_l[0]:+.2f} for luck".replace("-", "{-}"), font_size=19,
                  color=OWN),
            label(rf"a weak board pays for luck as much as for skill: \ {vals_l[1]:+.2f}", font_size=19, color=COST),
            label(r"American firms: \ pay rose with oil prices and exchange rates the CEO did not set, \\ least where "
                  r"a large shareholder sat on the board \ (Bertrand and Mullainathan)", font_size=17,
                  color=E.ACCENT),
            label(r"how much does a CEO's wealth move with the firm's? \ the Dials", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Bertrand and Mullainathan, \ Quarterly Journal of Economics 116(3) (2001); \ the "
                            r"Island: \ agora.org.pay\_for\_luck", corner=DL, font_size=12)
        with self.voiceover(
            "The other answer is that pay is set by people the chief executive has some influence over. <bookmark "
            "mark='a'/> A firm's results are partly the chief executive's skill and partly luck that everyone can "
            "see, such as the price of oil for an oil company. Part fourteen's theory says to pay for the first "
            "and filter out the second. <bookmark mark='b'/> On the Island, compare how pay responds to results, "
            "and to luck alone. <bookmark mark='c'/> A strong board pays for skill and nothing for luck. <bookmark "
            "mark='d'/> A weak board pays for luck as much as for skill. <bookmark mark='e'/> Marianne Bertrand and "
            "Sendhil Mullainathan found exactly this in American firms: pay rose with oil prices and exchange rates "
            "no chief executive set, and least where a large shareholder sat on the board to object. Their title "
            "said it: are chief executives rewarded for luck? The ones without principals are. <bookmark "
            "mark='f'/> How strongly a chief executive's own wealth moves with the shareholders' is one of this "
            "part's Dials."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bp[0], DOWN), FadeIn(bl[0]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bp[1], DOWN), GrowFromEdge(bl[1], DOWN), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
