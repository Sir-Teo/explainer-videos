from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403


class Search(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Search: \ the reservation wage", r"What is the best rule, \ and what moves it?",
             "Chapter three. Search: the reservation wage.", lit={1961: r"Stigler", 1970: r"McCall",
                                                                  1990: r"Katz and Meyer"},
             scale=("person",), horizon=("months",))
        self.stigler()
        self.derive()
        self.picture()
        self.statics()
        self.evidence()

    def stigler(self):
        rows = VGroup(
            label(r"George Stigler, \ 1961: \ prices differ from shop to shop, \ and finding the low one takes time",
                  font_size=24, color=GREY_A),
            label(r"his searcher asks a fixed number of shops, \ then buys at the cheapest", font_size=23,
                  color=JOB),
            label(r"John McCall, \ 1970: \ a searcher who decides after \emph{each} offer whether to stop", font_size=24,
                  color=WORKER),
            label(r"so dispersion and unemployment are not mistakes: \ they are what looking costs", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.2)
        tag = published_tag(r"Stigler, JPE 69(3) (1961): \ 213--225; \ McCall, QJE 84(1) (1970): \ 113--126",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The economics of looking begins with George Stigler in 1961. <bookmark mark='a'/> Prices for the same "
            "thing differ from shop to shop, he observed, and finding the low one takes time. "
            "<bookmark mark='b'/> His searcher decides in advance how many shops to visit, then buys at the cheapest. "
            "<bookmark mark='c'/> In 1970 John McCall turned it into the problem you just played: decide after each "
            "offer whether to stop. <bookmark mark='d'/> In both, the spread of prices or wages, and the time spent "
            "unemployed, are not mistakes. They are what looking costs, chosen by people doing the best they can."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def derive(self):
        rows = VGroup(
            MathTex(r"W(w) \;=\; w + \beta w + \beta^2 w + \dots \;=\; \frac{w}{1-\beta}", font_size=42, color=WAGE),
            label(r"the value of a job at wage $w$, \ kept for ever", font_size=21, color=GREY_B),
            MathTex(r"U \;=\; b \;+\; \beta\, \mathbb{E}\big[\max\{W(w'),\, U\}\big]", font_size=42, color=WORKER),
            label(r"the value of looking: \ the benefit now, \ then the better of next month's offer and looking on",
                  font_size=21, color=GREY_B),
            MathTex(r"W(w^*) = U \;\Longrightarrow\; w^* - b \;=\; \frac{\beta}{1-\beta} \int_{w^*} (w - w^*)\, "
                    r"dF(w)", font_size=40, color=E.ACCENT),
            label(r"the cost of one more month of looking \ $=$ \ the expected gain from one more offer", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).move_to(UP * 0.1)
        with self.voiceover(
            "Here is the best rule. <bookmark mark='a'/> A job at wage w, kept for ever, is worth w this month, beta "
            "w next month, and so on: w over one minus beta. <bookmark mark='b'/> Looking is worth the benefit now, "
            "plus, discounted, the better of two things next month: the job you are offered, or looking on. "
            "<bookmark mark='c'/> Since a job's value rises with its wage and looking's does not, there is a wage "
            "w star at which you are indifferent: the reservation wage. Take any offer above it, refuse any below. "
            "<bookmark mark='d'/> Rearranging gives its condition. On the left, what one more month of looking "
            "costs: the reservation wage you could have had, less the benefit. On the right, what it gains: the "
            "expected amount by which next month's offer beats the reservation wage, valued for ever. Stop when "
            "the two are equal."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]), Indicate(rows[4], color=WHITE))
        self.clear_scene()

    def picture(self):
        p = load("playit")
        lo, hi, b, bt = p["low"], p["high"], p["b"], p["beta"]
        ax = plane([50, 150], [0, 200], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.2, y_length=5.0,
                   xticks=[50, 75, 100, 125, 150], yticks=[0, 50, 100, 150, 200], xlabel=r"a candidate reservation "
                   r"wage $w^*$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        xs = np.linspace(50, 150, 201)
        cost = path(ax, xs, xs - b, color=BENEFIT, width=4, yr=(0, 200))
        gain = path(ax, xs, bt / (1 - bt) * (hi - xs) ** 2 / (2 * (hi - lo)), color=JOB, width=4, yr=(0, 200))
        ws = p["reservation"]
        star = dot(ax, ws, ws - b, color=E.ACCENT, r=0.1)
        drop = seg(ax, ws, 0, ws, ws - b, color=E.ACCENT, width=2, dashed=True)
        side = VGroup(
            label(r"cost of looking on: \\ $w^* - b$", font_size=21, color=BENEFIT),
            label(r"expected gain from \\ one more offer", font_size=21, color=JOB),
            label(rf"they cross at \\ $w^* = {ws:.1f}$", font_size=24, color=E.ACCENT),
            label(rf"chance an offer clears it: \\ {100 * p['accept']:.0f}\%; \ expected search: \\ "
                  rf"{p['duration']:.1f} months", font_size=20, color=WORKER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Draw both sides. <bookmark mark='a'/> The cost of looking on rises one for one with the reservation "
            "wage. <bookmark mark='b'/> The expected gain from one more offer falls: the choosier you already are, "
            "the less likely another offer is to beat your standard, and the less it beats it by. "
            f"<bookmark mark='c'/> They cross at {ws:.1f}, the rule from the game. <bookmark mark='d'/> About "
            f"{100 * p['accept']:.0f} percent of offers clear it, so a searcher expects to look for about "
            f"{p['duration']:.1f} months. That time is unemployment, and none of it is a mistake."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(cost), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(gain), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(star), Create(drop), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def statics(self):
        m = load("mccall")
        p = load("playit")
        ax1 = plane([0, 120], [100, 145], center=LEFT * 3.4 + DOWN * 0.2, x_length=5.2, y_length=4.4,
                    xticks=[0, 40, 80, 120], yticks=[100, 115, 130, 145], xlabel=r"benefit $b$",
                    ylabel=r"reservation wage", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        ax2 = plane([0.5, 1.0], [60, 145], center=RIGHT * 3.2 + DOWN * 0.2, x_length=5.2, y_length=4.4,
                    xticks=[0.5, 0.75, 1.0], yticks=[60, 80, 100, 120, 140], xlabel=r"patience $\beta$",
                    xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        c1 = path(ax1, m["b"], m["res_b"], color=BENEFIT, width=4)
        c2 = path(ax2, m["beta"], m["res_beta"], color=WORKER, width=4)
        here1 = dot(ax1, p["b"], p["reservation"], color=E.ACCENT)
        here2 = dot(ax2, p["beta"], p["reservation"], color=E.ACCENT)
        l1 = label(rf"search lasts {m['dur_b'][0]:.1f} months at $b=0$, \\ {m['dur_b'][-1]:.1f} at $b=120$",
                   font_size=19, color=BENEFIT).next_to(ax1, UP, buff=0.25)
        l2 = label(rf"{m['dur_beta'][0]:.1f} months at $\beta = 0.5$, \\ {m['dur_beta'][-1]:.1f} at $\beta = 0.99$",
                   font_size=19, color=WORKER).next_to(ax2, UP, buff=0.25)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "What moves the rule? <bookmark mark='a'/> A bigger benefit makes looking cheaper, so the searcher "
            f"holds out for more: with no benefit at all, searchers on the Island accept anything above "
            f"{m['res_b'][0]:.0f}, and with a benefit of a hundred and twenty, only offers above "
            f"{m['res_b'][-1]:.0f}. Expected search more than doubles, from {m['dur_b'][0]:.1f} months to "
            f"{m['dur_b'][-1]:.1f}. <bookmark mark='b'/> Patience works the same way. A searcher who discounts next "
            f"month heavily takes almost anything; one who barely discounts it waits for the top of the "
            "distribution. <bookmark mark='c'/> So unemployment insurance has a cost, in longer spells, as well as "
            "a benefit, in better matches and in protecting people who lose their jobs. How big is the cost?"
        ) as vo:
            self.play(FadeIn(ax1), FadeIn(tag), Create(c1), FadeIn(here1), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(ax2), Create(c2), FadeIn(here2), FadeIn(l2), run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(l1), Indicate(l2))
        self.clear_scene()

    def evidence(self):
        rows = VGroup(
            label(r"Katz and Meyer, \ 1990, \ twelve American states' records:", font_size=23, color=GREY_A),
            label(r"one more week of potential benefits \ $\to$ \ spells about 0.16 to 0.20 weeks longer",
                  font_size=25, color=BENEFIT),
            label(r"Card, Chetty and Weber, \ 2007, \ half a million Austrian job losers:", font_size=23,
                  color=GREY_A),
            label(r"a severance payment worth two months' pay \ $\to$ \ slower job finding", font_size=25,
                  color=WORKER),
            label(r"cash, \ not only incentives: \ the searcher who can afford to wait waits \ (Part 22's lesson)",
                  font_size=22, color=E.ACCENT),
            label(r"how to design insurance with both in mind: \ Part 42", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Katz and Meyer, J.\ Public Econ.\ 41(1) (1990): \ 45--72; \ Card, Chetty and Weber, "
                            r"QJE 122(4) (2007): \ 1511--1560", corner=DR, font_size=12)
        with self.voiceover(
            "The evidence agrees with the sign. <bookmark mark='a'/> Lawrence Katz and Bruce Meyer used the records "
            "of unemployment insurance in twelve American states. <bookmark mark='b'/> They found that one more "
            "week of potential benefits lengthened spells by about a sixth to a fifth of a week. "
            "<bookmark mark='c'/> David Card, Raj Chetty and Andrea Weber studied more than half a million job "
            "losers in Austria, where severance pay depends sharply on tenure. <bookmark mark='d'/> Workers who "
            "received a payment worth two months of earnings found jobs more slowly. "
            "<bookmark mark='e'/> A lump sum does not change the reward for taking a job, so that is not the "
            "incentive at work: it is cash. Workers with money in hand can afford to wait for a better offer, "
            "the same lesson as Part twenty-two's households. <bookmark mark='f'/> How to design insurance with "
            "both effects in mind waits for Part forty-two."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
