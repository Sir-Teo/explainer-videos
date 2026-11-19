from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


class Supply(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Profit and supply", r"How much should a firm make at a given price, and when should it stop?",
             "Chapter seven. Profit and supply.", scale=("firm", "market"))
        self.price_equals_mc()
        self.shutdown()
        self.le_chatelier()

    def ucost(self):
        i = load("industry")
        t = island.truths(8)["industry"]
        return i, fm.UCost(t["F"], t["c"], t["d"])

    def price_equals_mc(self):
        i, u = self.ucost()
        qs = np.linspace(0.5, 20, 300)
        ax = plane([0, 20], [0, 2500], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.8, y_length=5.0,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 500, 1000, 1500, 2000, 2500], xlabel=r"boats a month",
                   ylabel=r"\$ a boat", font_size=17)
        a = ax.ax
        mc = path(ax, qs, u.mc(qs), color=MC, width=3.5, yr=(0, 2500))
        atc = path(ax, qs, u.atc(qs), color=ATC, width=3, yr=(0, 2500))
        names = VGroup(label(r"$MC$", font_size=19, color=MC).next_to(a.c2p(20, float(u.mc(20))), RIGHT, buff=0.08),
                       label(r"$ATC$", font_size=19, color=ATC).next_to(a.c2p(20, float(u.atc(20))), RIGHT, buff=0.08))
        p = 1500.0
        q = u.supply(p)
        pl = DashedLine(a.c2p(0, p), a.c2p(20, p), color=PRICE, stroke_width=2.5)
        P = Dot(a.c2p(q, p), radius=0.09, color=PRICE)
        prof = Polygon(a.c2p(0, float(u.atc(q))), a.c2p(q, float(u.atc(q))), a.c2p(q, p), a.c2p(0, p),
                       stroke_width=0, fill_color=PRICE, fill_opacity=0.18)
        side = VGroup(
            label(r"a larger yard: \ \$4{,}000 a month fixed, \\ variable cost $200q + 50q^2$", font_size=23,
                  color=GREY_A),
            label(r"a competitive yard takes the price as given", font_size=24),
            label(rf"profit is greatest where price = marginal cost: \\ at \$1{{,}}500, \ {q:.0f} boats", font_size=24,
                  color=PRICE),
            label(rf"profit: \ (price $-$ average cost) $\times$ boats \\ = \${(p - float(u.atc(q))) * q:,.0f} a "
                  rf"month".replace(",", "{,}"), font_size=23, color=PRICE),
            label(r"one more boat would cost more than it sells for; \\ one fewer would lose a boat worth more \\ "
                  r"than it costs", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Now the firm chooses how much to make. Take a larger yard, with four thousand dollars a month of fixed "
            "costs and variable costs that rise steeply with output. <bookmark mark='a'/> In a competitive market "
            "Crusoe can sell as many boats as he likes at the going price, but can't change it. "
            "<bookmark mark='b'/> At a price of fifteen hundred dollars, his profit is greatest where the price "
            "equals marginal cost: thirteen boats a month. <bookmark mark='c'/> His profit is the shaded rectangle, "
            "price minus average cost, times the number of boats. <bookmark mark='d'/> Build one more and it costs "
            "more than it fetches; build one fewer and you give up a boat that was worth more than its cost. "
            "This is the firm's version of the margin from Part one."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(mc), Create(atc), FadeIn(names))
            vo.wait_until("a")
            self.play(Create(pl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(P, scale=0.5), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(prof), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def shutdown(self):
        i, u = self.ucost()
        qs = np.linspace(0.5, 20, 300)
        ax = plane([0, 20], [0, 2500], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.8, y_length=5.0,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 500, 1000, 1500, 2000, 2500], xlabel=r"boats a month",
                   ylabel=r"\$ a boat", font_size=17)
        a = ax.ax
        mc = path(ax, qs, u.mc(qs), color=MC, width=2.5, yr=(0, 2500))
        atc = path(ax, qs, u.atc(qs), color=ATC, width=3, yr=(0, 2500))
        avc = path(ax, qs, u.avc(qs), color=AVC, width=3, yr=(0, 2500))
        names = VGroup(*(label(rf"${n}$", font_size=19, color=col).next_to(a.c2p(20, float(f(20))), RIGHT, buff=0.08)
                         for n, col, f in (("MC", MC, u.mc), ("ATC", ATC, u.atc), ("AVC", AVC, u.avc))))
        sup = VGroup(Line(a.c2p(0, 0), a.c2p(0, u.shutdown), color=PRICE, stroke_width=6),
                     path(ax, qs, u.mc(qs), color=PRICE, width=6, yr=(u.shutdown, 2500)))
        be = DashedLine(a.c2p(0, u.breakeven), a.c2p(20, u.breakeven), color=ATC, stroke_width=1.8)
        sd = DashedLine(a.c2p(0, u.shutdown), a.c2p(20, u.shutdown), color=AVC, stroke_width=1.8)
        side = VGroup(
            label(rf"break-even: \ the bottom of average total cost, \\ \${u.breakeven:,.0f} at "
                  rf"{u.efficient_scale:.1f} boats".replace(",", "{,}"), font_size=23, color=ATC),
            label(rf"shut-down: \ the bottom of average variable cost, \ \${u.shutdown:.0f}", font_size=23,
                  color=AVC),
            label(r"between them the yard loses money, \\ but less than its fixed cost: \ it keeps building", font_size=22),
            label(r"the short-run supply curve: \\ marginal cost above the shut-down price", font_size=24,
                  color=PRICE),
            label(r"in the long run the fixed cost can be avoided: \\ below break-even the yard closes", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "What if the price falls? <bookmark mark='a'/> Below the bottom of average total cost, a thousand and "
            "ninety-four dollars at nine boats, the yard makes a loss. <bookmark mark='b'/> But in the short run the "
            "four thousand dollars of fixed costs must be paid anyway. So the question is only whether boats cover "
            "their variable cost, which they do above two hundred dollars, the bottom of average variable cost. "
            "<bookmark mark='c'/> Between the two prices Crusoe loses money, but less than he would by building "
            "nothing: he keeps building. <bookmark mark='d'/> So the yard's short-run supply curve is its marginal "
            "cost curve, above the shut-down price. <bookmark mark='e'/> In the long run nothing is fixed, and "
            "below break-even the yard closes. Supply is the cost structure, read off at each price."
        ) as vo:
            self.play(FadeIn(ax), Create(mc), Create(atc), Create(avc), FadeIn(names))
            vo.wait_until("a")
            self.play(Create(be), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(sd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(sup), FadeIn(side[3]), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def le_chatelier(self):
        s = load("supply")
        ps = np.array(s["ps"])
        ax = plane([0, 25], [400, 3000], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.8, y_length=5.0,
                   xticks=[0, 5, 10, 15, 20, 25], yticks=[500, 1000, 1500, 2000, 2500, 3000],
                   xlabel=r"boats a month \ (Crusoe's first yard)", ylabel=r"price of a boat", font_size=17)
        sr = path(ax, s["sr"], ps, color=AVC, width=3.5, xr=(0, 25))
        lr = path(ax, s["lr"], ps, color=COST, width=3.5, xr=(0, 25))
        P = Dot(ax.ax.c2p(s["q_now"], 1200), radius=0.08, color=WHITE)
        srl = label(r"short run", font_size=19, color=AVC).next_to(ax.ax.c2p(12, 3000), RIGHT, buff=0.12)
        lrl = label(r"long run", font_size=19, color=COST).next_to(ax.ax.c2p(24.8, 2148), UP, buff=0.12)
        lc = s["le_chatelier"]
        err = max(s["hotelling"].values())
        side = VGroup(
            label(r"Crusoe's first yard, \ $q = 2K^{0.25}L^{0.5}$", font_size=23, color=GREY_A),
            label(rf"short run (4 slipways): \ supply elasticity {lc['short']:.0f}", font_size=24, color=AVC),
            label(rf"long run (slipways too): \ {lc['long']:.0f}", font_size=24, color=COST),
            label(r"Le Chatelier's principle (Samuelson): \\ more inputs free to adjust, \\ a bigger response",
                  font_size=23, color=E.ACCENT),
            MathTex(r"\frac{\partial \pi}{\partial p} = q, \qquad \frac{\partial \pi}{\partial w} = -L", font_size=34),
            label(rf"Hotelling's lemma, \ checked: \ error {err:.0e}", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Back to Crusoe's first yard, with its decreasing returns. <bookmark mark='a'/> With its four slipways "
            "fixed, a one percent higher price draws out one percent more boats. <bookmark mark='b'/> In the long "
            "run, when it can rent more slipways too, the same price rise draws out three percent more. "
            "<bookmark mark='c'/> Paul Samuelson borrowed the name of a principle in chemistry for this, Le "
            "Chatelier's: the more of its inputs a firm can adjust, the more it responds to a price. That's why "
            "supply is more elastic in the long run than in the short. <bookmark mark='d'/> And the firm's profit "
            "function has its own lemma, Hotelling's: differentiate maximized profit by the price and you get "
            "supply; by the wage, minus the labour hired. Checked here to ten decimal places."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]), FadeIn(P))
            vo.wait_until("a")
            self.play(Create(sr), FadeIn(side[1]), FadeIn(srl))
            vo.wait_until("b")
            self.play(Create(lr), FadeIn(side[2]), FadeIn(lrl))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.clear_scene()
