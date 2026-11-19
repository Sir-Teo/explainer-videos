from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


class Equivalence(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Revenue equivalence", r"Different rules, \ different bids: \ does the seller's money "
             r"differ?", "Chapter five. Revenue equivalence.",
             lit={1961: r"Vickrey", 1981: r"Myerson; \ Riley and Samuelson"}, scale=("market",), horizon=("a day",))
        self.simulate()
        self.spread()
        self.theorem()
        self.six()

    def simulate(self):
        f = load("formats")
        names = ["first-price", "Dutch", "second-price", "English", "all-pay"]
        cols = [FIRST, FIRST, SECOND, SECOND, ALLPAY]
        ax = plane([-0.5, 4.5], [0, 0.8], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.0, y_length=4.8, xticks=[],
                   yticks=[0, 0.2, 0.4, 0.6, 0.8], ylabel=r"the seller's average revenue", font_size=16,
                   yfmt=lambda v: f"{v:.1f}")
        a = ax.ax
        bars, vals, labs = VGroup(), VGroup(), VGroup()
        for i, (nm, c) in enumerate(zip(names, cols)):
            m = f["formats"][nm]["mean"]
            lo, hi = a.c2p(i - 0.3, 0), a.c2p(i + 0.3, m)
            r = Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0, fill_color=c, fill_opacity=0.8)
            r.move_to((lo + hi) / 2)
            bars.add(r)
            vals.add(label(rf"{m:.3f}", font_size=17, color=c).next_to(r, UP, buff=0.08))
            labs.add(label(nm, font_size=17, color=GREY_A).next_to(a.c2p(i, 0), DOWN, buff=0.15))
        theory = VGroup(DashedLine(a.c2p(-0.5, f["theory"]), a.c2p(4.5, f["theory"]), color=E.ACCENT, stroke_width=2),
                        label(r"theory: \ $\tfrac{n-1}{n+1} = 0.6$", font_size=18, color=E.ACCENT).next_to(
                            a.c2p(4.5, f["theory"]), UP, buff=0.4).shift(LEFT * 0.6))
        side = VGroup(
            label(rf"{f['draws']:,} auctions, \\ four bidders each, \\ values uniform on 0 to 1".replace(",", "{,}"),
                  font_size=20, color=GREY_A),
            label(r"the same draws of values \\ run through every format", font_size=20, color=GREY_A),
            label(r"all-pay: \ every bidder pays its bid, \\ win or lose \ (a lobbying race)", font_size=20,
                  color=ALLPAY),
            label(r"five rules, \ one revenue", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Sale A has lower bids than sale B, but its winner pays its own bid, not the next one down. Which raises "
            "more money for the seller? <bookmark mark='a'/> Agora's auction house drew sixty thousand sets of four "
            "values, <bookmark mark='b'/> and ran the same draws through every format, with every bidder bidding as "
            "the equilibrium says. <bookmark mark='c'/> First-price and Dutch, second-price and English, and a fifth "
            "rule, the all-pay auction, in which every bidder pays its bid, win or lose, as in a race to lobby a "
            "government. Bidders there shade hard, since losing costs them too. <bookmark mark='d'/> Every format "
            "raises six tenths on average, in units where values run from nothing to one, just as the theory says it "
            "must: n minus one over n plus one, three fifths. Five rules, one revenue."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(vals),
                      FadeIn(side[2]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(theory), FadeIn(side[3]))
        self.clear_scene()

    def spread(self):
        f = load("formats")
        edges = np.array(f["edges"])
        h1, h2 = np.array(f["hist_first"], float), np.array(f["hist_second"], float)
        h1, h2 = h1 / h1.sum(), h2 / h2.sum()
        top = max(h1.max(), h2.max()) * 1.1
        axs, bars = [], []
        for k, (h, c, t) in enumerate(((h1, FIRST, r"first-price: \ the price paid"),
                                       (h2, SECOND, r"second-price: \ the price paid"))):
            ax = plane([0, 1], [0, top], center=(LEFT * 3.4 + RIGHT * 6.8 * k) + DOWN * 0.4, x_length=5.6,
                       y_length=3.6, xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[], xlabel=t, font_size=15,
                       xfmt=lambda v: f"{v:g}")
            a = ax.ax
            g = VGroup()
            for i in range(len(h)):
                lo, hi = a.c2p(edges[i], 0), a.c2p(edges[i + 1], h[i])
                if hi[1] - lo[1] < 1e-3:
                    continue
                r = Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0.5, stroke_color=BACKGROUND,
                              fill_color=c, fill_opacity=0.8).move_to((lo + hi) / 2)
                g.add(r)
            axs.append(ax)
            bars.append(g)
        notes = VGroup(
            label(rf"spread (standard deviation): \ {f['sd_first']:.2f}", font_size=20, color=FIRST).next_to(
                axs[0], UP, buff=0.15),
            label(rf"spread: \ {f['sd_second']:.2f}", font_size=20, color=SECOND).next_to(axs[1], UP, buff=0.15),
        )
        foot = label(r"the same average, \ different risk: \ a seller who fears a bad day \ prefers to be paid the "
                     r"bids", font_size=21, color=E.ACCENT).to_edge(DOWN, buff=0.42).shift(LEFT * 1.3)
        head = label(r"what the seller receives, \ auction by auction", font_size=27, color=GREY_A).to_edge(UP,
                                                                                                    buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The averages match, but not the auctions one by one. <bookmark mark='a'/> Here is the price paid in "
            "first-price auctions, sale by sale. It is the winner's shaded bid, and since the winner has the highest "
            "value, it rarely falls very low. <bookmark mark='b'/> In second-price auctions the price is the second "
            "value, which can be anything: sometimes high, sometimes very low. <bookmark mark='c'/> The same "
            "average, with less than two thirds of the spread. A seller who fears a bad day, like a government with "
            "a budget to meet, should prefer to be paid the bids."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axs[0]), FadeIn(axs[1]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars[0]], lag_ratio=0.05), FadeIn(notes[0]),
                      run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars[1]], lag_ratio=0.05), FadeIn(notes[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def theorem(self):
        head = label(r"why: \ the envelope argument", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        eqs = VGroup(
            MathTex(r"U(v) = v\,P(v) - T(v)", font_size=38),
            MathTex(r"U'(v) = P(v)", font_size=38, color=YOU),
            MathTex(r"U(v) = U(0) + \int_0^v P(s)\,ds", font_size=38, color=YOU),
            MathTex(r"T(v) = v\,P(v) - \int_0^v P(s)\,ds - U(0)", font_size=40, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(LEFT * 2.3 + UP * 0.2)
        keys = VGroup(
            label(r"$P$: \ the chance a value $v$ wins; \ $T$: \ its expected payment", font_size=20, color=GREY_A),
            label(r"a bidder who could pretend to have \\ value $v + dv$ gains just $P(v)\,dv$", font_size=20,
                  color=YOU),
            label(r"so payments are fixed by who wins, \\ and by what the lowest type gets", font_size=21,
                  color=E.ACCENT),
            label(r"highest value wins: \ $P(v) = v^{n-1}$; \\ lowest gets nothing: \ $U(0) = 0$", font_size=21,
                  color=PRICE),
            label(r"then $T(v) = \tfrac{n-1}{n}\,v^n$ in every format", font_size=22, color=PRICE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        foot = label(r"Vickrey (1961); \ Myerson (1981); \ Riley and Samuelson (1981)", font_size=19,
                     color=GREY_B).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Why must they match? The argument is short. <bookmark mark='a'/> Take a bidder with value v. Let P be "
            "its chance of winning, and T its expected payment, so its expected gain U is v times P minus T. "
            "<bookmark mark='b'/> In equilibrium, no bidder wants to act like a slightly different one. A bidder "
            "who acted as if its value were a little higher would win a little more often, and the gain from that, "
            "to first order, is just P. So the slope of U is P. <bookmark mark='c'/> Add up the slopes, and U at v is "
            "U at the bottom plus the area under P. <bookmark mark='d'/> Rearranged, the expected payment is fixed "
            "by two things only: who wins, and what the lowest possible bidder gets. <bookmark mark='e'/> In all five "
            "formats the highest value wins, so P is v to the n minus one, and a bidder with the lowest value gets "
            "nothing. <bookmark mark='f'/> So every bidder expects to pay the same in all five, and the seller "
            "expects the same. Vickrey saw it in 1961; Roger Myerson, and John Riley with William Samuelson, proved "
            "it in general in 1981."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(keys[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(eqs[3]), FadeIn(keys[2]))
            vo.wait_until("e")
            self.play(FadeIn(keys[3]))
            vo.wait_until("f")
            self.play(FadeIn(keys[4]))
        self.clear_scene()

    def six(self):
        p = load("playit")
        rows = VGroup(
            MathTex(r"U(v) = \int_0^v s^{\,n-1}\,ds = \frac{v^{\,n}}{n}", font_size=44, color=YOU),
            label(rf"Play it: \ $v = 0.7$, \ $n = 4$: \ $0.7^4 / 4 = 0.060$, \ so {p['profit_first']:.1f} shells in "
                  r"either sale", font_size=26, color=YOU),
            label(r"the bidder's profit is equivalent too, \ and for the same reason", font_size=24, color=GREY_A),
            label(r"so the choice of format turns on everything the theorem assumes away:", font_size=25,
                  color=E.ACCENT),
            label(r"risk, \ shared values, \ unequal bidders, \ collusion, \ who turns up", font_size=25,
                  color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "And now the six shells from Play it. <bookmark mark='a'/> Your expected gain is the area under P, which "
            "for four bidders with even values is v to the fourth over four. With a value of seven tenths, that is "
            "six hundredths of a hundred shells: six shells, in either sale. <bookmark mark='b'/> The bidder's profit "
            "is the same across formats too, for the same reason. <bookmark mark='c'/> So the theorem tells a seller "
            "that the format doesn't matter, and therefore that the choice turns on everything the theorem assumed "
            "away. <bookmark mark='d'/> Bidders who fear risk, values that are shared, bidders who are unequal, "
            "bidders who collude, and who turns up at all. That is the rest of this part."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
