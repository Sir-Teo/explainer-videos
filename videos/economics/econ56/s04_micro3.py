from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"Two risk-neutral bidders have private values drawn independently and uniformly from $[0, 1]$. \ The seller, "
    r"who values the object at 0, \ runs a first-price sealed-bid auction with a reserve price $r = 0.5$.",
    r"(a) \ Find the symmetric equilibrium bid function. \quad (10 marks)",
    r"(b) \ Find the seller's expected revenue, \ and compare it with no reserve. \quad (8 marks)",
    r"(c) \ Why would a seller who values the object at 0 refuse to sell below 0.5? \quad (7 marks)",
]


class Micro3(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Micro: \ a first-price auction with a reserve", r"How should you bid when the seller may "
             r"keep the object?", "Question three. Microeconomics: a first-price auction with a reserve.",
             lit={1961: r"Vickrey", 1981: r"Myerson; \ Riley and Samuelson"}, scale=("person", "market"),
             horizon=("a day",))
        self.statement()
        self.bid()
        self.revenue()
        self.picture()
        self.marks()

    def statement(self):
        paper = exam_paper(3, "micro", r"an auction with a reserve", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question three. Two bidders, values uniform between zero and one, a first-price sealed-bid auction, "
            "and a reserve price of one half. <bookmark mark='a'/> Part a: the equilibrium bid. <bookmark "
            "mark='b'/> Part b: expected revenue, with and without the reserve. <bookmark mark='c'/> Part c: why "
            "would a seller who values the object at nothing refuse to sell it for less than a half? Pause, and "
            "write the bidder's problem."
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("abc", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def bid(self):
        tag = part_tag(3, "a", "micro")
        rows = steps([
            (r"\max_b\ (v - b)\,\Pr(\text{win}) = (v - b)\,\beta^{-1}(b)",
             r"the rival bids $\beta(v')$, \ increasing; \ $\Pr(v' < z) = z$"),
            (r"-\beta^{-1}(b) + (v - b)\,\big(\beta^{-1}\big)'(b) = 0 \ \Rightarrow\ v\,\beta'(v) + \beta(v) = v",
             r"first-order condition, \ evaluated at $b = \beta(v)$"),
            (r"\frac{d}{dv}\big[v\,\beta(v)\big] = v \ \Rightarrow\ v\,\beta(v) = \frac{v^2}{2} + C",
             r"integrate"),
            (r"\beta(r) = r \ \Rightarrow\ C = \frac{r^2}{2}",
             r"the type at the reserve bids the reserve, \ and wins only if alone"),
            (r"\beta(v) = \frac{v^2 + r^2}{2v} = \frac{v^2 + 0.25}{2v}, \quad v \ge 0.5; \qquad \text{no bid below}",
             r"the answer", GAIN),
        ])
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[4][0])
        with self.voiceover(
            "Part a. <bookmark mark='a'/> Guess that the rival uses an increasing bid function, beta. A bidder of "
            "value v who bids b wins when the rival's value is below beta inverse of b, which with uniform values "
            "is just beta inverse of b. <bookmark mark='b'/> Differentiate, and evaluate where the bid is the "
            "bidder's own equilibrium bid: v times beta prime, plus beta, equals v. <bookmark mark='c'/> The left "
            "side is the derivative of v times beta, so v beta equals v squared over two, plus a constant. "
            "<bookmark mark='d'/> The constant comes from the boundary, and this is where marks are won: a bidder "
            "whose value is exactly the reserve can only bid the reserve, so beta of r is r, and the constant is r "
            "squared over two. <bookmark mark='e'/> So beta of v is v squared plus a quarter, over two v, for "
            "values above a half; below, no bid at all."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
            self.play(Create(box))
        self.clear_scene()

    def revenue(self):
        M = load("micro3")
        tag = part_tag(3, "b, c", "micro")
        rows = steps([
            (r"R = 2\int_r^1 \Big(v - \frac{1 - F(v)}{f(v)}\Big) F(v)\, f(v)\,dv = 2\int_{0.5}^1 (2v - 1)\,v\,dv",
             r"revenue equivalence: \ the expected virtual value of the winner"),
            (r"= \tfrac{4}{3}\,(1 - r^3) - (1 - r^2) = \tfrac{5}{12} \approx 0.417",
             r"against $\tfrac{1}{3}$ with no reserve", GAIN),
            (rf"\Pr(\text{{no sale}}) = r^2 = {M['p_no_sale']:.2f}", r"both values below the reserve"),
            (rf"\text{{simulated, }} {M['draws'] // 1000}{{,}}000 \text{{ auctions: first price }} "
             rf"{M['rev_fp_sim']:.3f}, \ \text{{second price }} {M['rev_sp_sim']:.3f}",
             r"the two formats agree, \ as the theorem says"),
            (r"2v - 1 = 0 \ \Rightarrow\ r^* = \tfrac{1}{2}", r"(c) \ Myerson: \ sell only when the winner's "
             r"virtual value is positive, \ whatever the number of bidders", GAIN),
        ])
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[1][0])
        with self.voiceover(
            "Part b. <bookmark mark='a'/> Use revenue equivalence: expected revenue is the expected virtual value "
            "of the winner, v minus one minus F over f, which with uniform values is two v minus one, counted "
            "only when the object sells. <bookmark mark='b'/> The integral is five twelfths, about 0.417, against "
            "a third with no reserve. <bookmark mark='c'/> The price of that gain: with probability one quarter "
            "both values are below the reserve and the object is not sold. <bookmark mark='d'/> A check by "
            f"simulation: in {M['draws'] // 1000} thousand auctions, the first-price room raises "
            f"{M['rev_fp_sim']:.3f} and a second-price room with the same reserve {M['rev_sp_sim']:.3f}. <bookmark "
            "mark='e'/> Part c. Selling to a bidder whose virtual value is negative lowers expected revenue: the "
            "seller gains the low price but must offer every higher type the same deal. Roger Myerson showed the "
            "best reserve sets the virtual value to zero: one half, however many bidders there are. The reserve "
            "raises revenue and destroys some trade."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if mk == "b":
                    self.play(Create(box))
        self.clear_scene()

    def picture(self):
        M = load("micro3")
        v = np.array(M["v"], float)
        b = np.array([np.nan if x is None else x for x in M["bid"]], float)
        b0 = np.array(M["bid0"], float)
        axl = plane([0, 1], [0, 1], center=LEFT * 3.4 + DOWN * 0.35, x_length=5.0, y_length=4.6,
                    xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], xlabel=r"value $v$", ylabel=r"bid",
                    xfmt=lambda x: f"{x:.1f}", yfmt=lambda y: f"{y:.1f}", font_size=15)
        diag = seg(axl, 0, 0, 1, 1, GREY_D, 1.5, dashed=True)
        l0 = path(axl, v, b0, GREY_B, 2.4)
        ok = v >= M["r"]
        l1 = path(axl, v[ok], b[ok], MICRO, 3.0)
        rdot = dot(axl, M["r"], M["r"], EST)
        bb, pp = np.array(M["dev_bids"]), np.array(M["dev_payoff"])
        axr = plane([0.5, 0.8], [0, float(pp.max()) * 1.2], center=RIGHT * 2.6 + DOWN * 0.35, x_length=4.6,
                    y_length=4.6, xticks=[0.5, 0.6, 0.7, 0.8], yticks=[], xlabel=r"bid of a bidder with $v = 0.8$",
                    ylabel=r"expected payoff", xfmt=lambda x: f"{x:.1f}", font_size=15)
        lp = path(axr, bb, pp, EST, 2.8)
        star = dot(axr, M["b_08"], float(pp.max()), GAIN)
        sl = label(rf"$\beta(0.8) = {M['b_08']:.3f}$", font_size=18, color=GAIN).next_to(star, UP, buff=0.15)
        key = VGroup(label(r"grey: \ no reserve, \ $v/2$", font_size=18, color=GREY_B),
                     label(r"blue: \ reserve 0.5", font_size=18, color=MICRO)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.15)
        key.next_to(axl, UP, buff=0.2)
        with self.voiceover(
            "The picture. <bookmark mark='a'/> With no reserve each bidder bids half their value. <bookmark "
            "mark='b'/> With the reserve, the bid starts at the reserve itself and lies above the old one: a "
            "bidder who would have won cheaply now faces a floor, and raises the bid to stay competitive. "
            "<bookmark mark='c'/> And a check that the bid is a best response: for a bidder with value 0.8, the "
            f"expected payoff from every bid between the reserve and 0.8 peaks at {M['b_08']:.3f}, exactly beta of "
            "0.8."
        ) as vo:
            self.play(FadeIn(axl), FadeIn(diag), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(l0))
            vo.wait_until("b")
            self.play(FadeIn(rdot), Create(l1), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(axr), Create(lp), run_time=1.5)
            self.play(FadeIn(star), FadeIn(sl))
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"the boundary condition $\beta(0) = 0$: \ with a reserve it is $\beta(r) = r$",
            r"letting types below the reserve bid, \ or bid the reserve",
            r"revenue that forgets the chance of no sale",
            r"calling the reserve efficient: \ it raises revenue and destroys trade a quarter of the time",
        ]).move_to(UP * 0.2)
        take = label(r"bids from the first-order condition and a boundary; \ revenue from virtual values", font_size=23,
                     color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> The wrong boundary condition, which gives the no-reserve "
            "bid back. <bookmark mark='b'/> Letting types below the reserve bid. <bookmark mark='c'/> Forgetting "
            "that sometimes nothing is sold. <bookmark mark='d'/> And calling the reserve efficient. <bookmark "
            "mark='e'/> The idea to keep: bids come from a first-order condition and a boundary; revenue comes "
            "from virtual values, which is Part sixteen's argument in one line."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()
