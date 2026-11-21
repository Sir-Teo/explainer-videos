from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Market(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Market definition", r"Where does a market end?", "Chapter three. Market definition.",
             lit={1956: r"cellophane", 1982: r"the hypothetical monopolist", 1989: r"critical loss"},
             scale=("market",), horizon=("a year",))
        self.hmt()
        self.critical()
        self.cellophane()

    def hmt(self):
        Mk = load("market")
        xs = np.array(Mk["xs"])
        C = Mk["cands"]
        ax = plane([0, 25], [-0.8, 0.9], center=LEFT * 2.7 + DOWN * 0.4, x_length=6.6, y_length=4.8,
                   xticks=[0, 5, 10, 15, 20, 25], yticks=[-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75],
                   xlabel=r"price rise on the candidate products, \ \%", ylabel=r"the monopolist's profit change",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:+.0f}\\%".replace("-", "{-}") if v else "0",
                   font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(25, 0), color=GREY_C, stroke_width=1.2)
        five = vline(ax, 5, -0.8, 0.9, E.ACCENT, 1.6)
        fl = label(r"5\%", font_size=16, color=E.ACCENT).next_to(ax.ax.c2p(5, 0.85), RIGHT, buff=0.08)
        cols = {"Alder alone": ALDER, "Alder and Birch": BIRCH, "the three superstores": WHITE}
        curves = VGroup(*[path(ax, xs, C[k]["curve"], cols[k], 3.0, yr=(-0.8, 0.9)) for k in cols])
        side = VGroup()
        for k in cols:
            h = C[k]
            side.add(label(rf"{k}: \ {'passes' if h['passes'] else 'fails'}", font_size=21, color=cols[k]))
        side.add(label(r"the market: \ the smallest set that passes, \\ starting from the merging products",
                       font_size=19, color=E.ACCENT))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        tag = island_tag(r"the Island: \ a town with all three chains; \ others' prices held fixed", corner=DL,
                         font_size=12)
        with self.voiceover(
            "The test you just played is the hypothetical-monopolist test, written into the American merger "
            "guidelines in 1982. Start with the merging product, imagine one owner of a candidate set, and ask "
            "whether a small but significant and non-transitory increase in price, usually five percent, would "
            "pay. <bookmark mark='a'/> Here it is in a town with all three chains, with every other price held "
            "fixed. A monopolist of Alder alone loses money on any rise: too many customers walk to Birch or Cedar. "
            "<bookmark mark='b'/> A monopolist of Alder and Birch gains from a five percent rise. <bookmark "
            "mark='c'/> And one of all three superstores gains handsomely. <bookmark mark='d'/> The rule takes the "
            "smallest set that passes, so on the Island the market is at most the superstores, not everyone who "
            "sells a pen. In the real case Judge Hogan accepted something similar: office supplies sold through "
            "office superstores."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), Create(five), FadeIn(fl), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(side[k]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def critical(self):
        Mk = load("market")
        h = Mk["cands"]["the three superstores"]
        rows = VGroup(
            MathTex(r"(p - c)\,q \;\le\; \big(p(1 + X) - c\big)\,q\,(1 - L)", font_size=34, color=WHITE),
            MathTex(r"\Longleftrightarrow\quad L \;\le\; \frac{X}{X + M} \quad\text{(the critical loss)}",
                    font_size=34, color=E.ACCENT),
            label(rf"the three superstores: \ margin {100 * h['margin']:.1f}\%, \ critical loss "
                  rf"{100 * h['critical_loss']:.0f}\%, \ actual loss {100 * h['actual_loss']:.1f}\%", font_size=23,
                  color=WHITE),
        ).arrange(DOWN, buff=0.45).to_edge(UP, buff=0.7)
        trap = point_cards([
            (r"the defence's argument", r"margins are high, \ so the critical loss is small: \ losing a few "
             r"customers would sink the rise, \ so the market must be broad", DEF),
            (r"the reply", r"a high margin also says each firm's own customers are hard to lose: \ high margins "
             r"mean small actual losses too, \ unless the lost sales escape the candidate set", GOV),
        ], width=12.4, cols=2, font_size=20).next_to(rows, DOWN, buff=0.55)
        tag = published_tag(r"Harris and Simons (1989); \ Katz and Shapiro (2003); \ O'Brien and Wickelgren (2003)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Courts often meet the test as critical-loss analysis, introduced by Barry Harris and Joseph Simons in "
            "1989. <bookmark mark='a'/> Before the rise, profit is the margin times sales. After, the margin is "
            "bigger but sales fall by a fraction L. <bookmark mark='b'/> The rise pays only if L is below X over X "
            f"plus M: the critical loss. <bookmark mark='c'/> For the three superstores the margin is "
            f"{100 * h['margin']:.1f} percent, so the critical loss is {100 * h['critical_loss']:.0f} percent, and "
            f"the actual loss from a five percent rise is only {100 * h['actual_loss']:.1f}. <bookmark mark='d'/> "
            "Defendants long used the formula the other way. Our margins are high, they said, so the critical loss "
            "is small; losing only a few customers would sink a price rise; so the market must be broad. <bookmark "
            "mark='e'/> Michael Katz and Carl Shapiro, and separately Daniel O'Brien and Abraham Wickelgren, "
            "pointed out the catch in 2003. A high margin also tells you that each firm's own customers are hard to "
            "lose, or it would have cut its price. High margins mean small actual losses too, unless the customers "
            "who leave escape the candidate set altogether. The margin cannot be used for one half of the test and "
            "ignored for the other."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=DOWN * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(trap.cards[0], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(trap.cards[1], shift=UP * 0.1))
        self.clear_scene()

    def cellophane(self):
        Mk = load("market")
        cel = Mk["cellophane"]
        xs = np.array(Mk["xs"])
        ax = plane([0, 25], [-0.6, 0.9], center=LEFT * 2.7 + DOWN * 0.5, x_length=6.4, y_length=4.4,
                   xticks=[0, 5, 10, 15, 20, 25], yticks=[-0.5, -0.25, 0, 0.25, 0.5, 0.75],
                   xlabel=r"a further price rise, \ \%", ylabel=r"the monopolist's profit change",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:+.0f}\\%".replace("-", "{-}") if v else "0",
                   font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(25, 0), color=GREY_C, stroke_width=1.2)
        comp = path(ax, xs, Mk["cands"]["the three superstores"]["curve"], WHITE, 3.0, yr=(-0.6, 0.9))
        mono = path(ax, xs, Mk["curve_mono"], CARTEL, 3.0, yr=(-0.6, 0.9))
        pc, pm = cel["p_comp"], cel["p_mono"]
        side = VGroup(
            label(rf"at competitive prices \ (Alder \${pc[0]:.2f}): \ the rise pays", font_size=20, color=WHITE),
            label(rf"at monopoly prices \ (Alder \${pm[0]:.2f}): \ it does not", font_size=20, color=CARTEL),
            label(r"so a firm that already has market power \\ looks as if it has none", font_size=21,
                  color=E.ACCENT),
            history_card(1956, r"United States v. du Pont", r"cellophane competes with every flexible wrapping, "
                         r"\ the Supreme Court found; \ at du Pont's prices, \ perhaps it did", color=DEF, width=5.8,
                         font_size=17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ the three superstores priced as one, \ then tested", corner=DL,
                         font_size=12)
        with self.voiceover(
            "The test has a trap, named after a case about cellophane. <bookmark mark='a'/> At competitive prices "
            "the three superstores pass easily. <bookmark mark='b'/> Now suppose they already behaved as one firm, "
            f"with Alder at {pm[0]:.2f} dollars instead of {pc[0]:.2f}. Run the same test at those prices, and a "
            "further rise does not pay: the monopolist has already raised prices to the point where customers start "
            "to leave. <bookmark mark='c'/> So a firm that already has market power looks as if it has none, "
            "because at its high price everything looks like a substitute. <bookmark mark='d'/> In 1956 the Supreme "
            "Court found that du Pont's cellophane competed with every flexible wrapping, so du Pont had no "
            "monopoly. Economists later pointed out that at du Pont's prices that may have been true, and proved "
            "nothing. For a merger the test is run at today's prices, which is mostly fine; when the question is "
            "whether a firm is already a monopolist, it is not."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(comp), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mono), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()
