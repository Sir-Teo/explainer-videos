from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class DLW(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Markups from production data", r"Has market power risen across the whole economy?",
             "Chapter eleven. Markups from production data.",
             lit={2012: r"De Loecker and Warzynski", 2020: r"De Loecker, \ Eeckhout and Unger"},
             scale=("firm", "nation"), horizon=("a decade",))
        self.formula()
        self.island()
        self.rise()
        self.critics()

    def formula(self):
        lines = VGroup(
            MathTex(r"\min\; P_V V + \ldots \quad \text{s.t.}\quad Q(V, K) \ge \bar Q", font_size=36,
                    color=GREY_A),
            MathTex(r"P_V \;=\; \lambda\,\frac{\partial Q}{\partial V}", r"\quad\Rightarrow\quad",
                    r"\frac{\partial Q}{\partial V}\frac{V}{Q} \;=\; \frac{P_V V}{\lambda\, Q}", font_size=40),
            MathTex(r"\mu \;=\; \frac{P}{\lambda} \;=\; \theta_V \cdot \frac{P\,Q}{P_V V}", font_size=48,
                    color=E.ACCENT),
        ).arrange(DOWN, buff=0.55).move_to(UP * 0.8)
        notes = VGroup(
            label(r"$\theta_V$: \ the flexible input's output elasticity \ (from a production function)",
                  font_size=20, color=BLP_C),
            label(r"$P_V V / P Q$: \ its share of revenue \ (from the accounts)", font_size=20, color=PRICE),
            label(r"no demand system, \ no conduct assumption: \ any firm, \ any industry", font_size=21,
                  color=GAIN),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.55)
        tag = published_tag(tables.DLW_2012.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Demand systems need years of work for one industry. In 2012 Jan De Loecker and Frederic Warzynski "
            "proposed a way to measure markups for any firm from its accounts. <bookmark mark='a'/> A firm "
            "minimizing cost uses a flexible input, such as materials or labour, until its price equals its "
            "marginal product valued at marginal cost, lambda. Rearranged, the input's output elasticity equals its "
            "cost divided by marginal cost times output. <bookmark mark='b'/> Since the markup is price over "
            "marginal cost, it equals the output elasticity divided by the input's share of revenue. "
            "<bookmark mark='c'/> The elasticity comes from a production function, estimated as in the last "
            "chapter. <bookmark mark='d'/> The share comes from the accounts. <bookmark mark='e'/> No demand system "
            "and no assumption about how firms compete: any firm, in any industry."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(Write(lines[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(lines[2]))
            for mk, n_ in zip("cde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_, shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        D = load("dlw")
        e = np.array(D["edges"])
        mids = (e[1:] + e[:-1]) / 2
        H = {k: np.array(v) / max(np.max(D["hist"]["truth"]), 1) for k, v in D["hist"].items()}
        ax = plane([0.6, 3.0], [0, 1.1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[1.0, 1.5, 2.0, 2.5, 3.0], yticks=[], xlabel=r"plant markup, \ price over marginal cost",
                   xfmt=lambda v: f"{v:.1f}", font_size=14)

        def hist(h, col, op):
            g = VGroup()
            w = (e[1] - e[0])
            for x, v in zip(mids, h):
                if v <= 0:
                    continue
                p0, p1 = ax.ax.c2p(x - w / 2, 0), ax.ax.c2p(x + w / 2, v)
                g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                fill_opacity=op).move_to((p0 + p1) / 2))
            return g
        tr = hist(H["truth"], TRUTH_C, 0.55)
        ac = hist(H["acf"], BLP_C, 0.0)
        for r_, (x, v) in zip(ac, [(x, v) for x, v in zip(mids, H["acf"]) if v > 0]):
            r_.set_stroke(BLP_C, 2.0)
        ol = hist(H["ols"], OLS_C, 0.55)
        th = D["theta"]
        md = D["median"]
        side = VGroup(
            label(rf"green: \ the planted \\ markups, \ median {md['truth']:.2f}", font_size=18, color=TRUTH_C),
            label(rf"outline: \ with ACF's \\ $\theta$ = {th['acf']:.2f}: \ median {md['acf']:.2f}", font_size=18,
                  color=BLP_C),
            label(rf"red: \ with OLS's \\ $\theta$ = {th['ols']:.2f}: \ median {md['ols']:.2f}", font_size=18,
                  color=OLS_C),
            label(r"the level rides on \\ the elasticity", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island shows what the formula needs. <bookmark mark='a'/> Its plants were given markups around "
            f"{md['truth']:.1f}, and they spend on labour the share of revenue that cost minimization implies. "
            "<bookmark mark='b'/> With labour's elasticity from Ackerberg, Caves and Frazer, the formula recovers "
            f"the markups almost exactly: median {md['acf']:.2f}. <bookmark mark='c'/> With the elasticity from "
            f"ordinary least squares, {th['ols']:.2f}, every markup is inflated in the same proportion, to a median "
            f"of {md['ols']:.2f}. <bookmark mark='d'/> The ratio between firms survives a wrong elasticity; the "
            "level does not. And the level is what a debate about rising market power is about."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in tr], lag_ratio=0.02), FadeIn(side[0]),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ac), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in ol], lag_ratio=0.02), FadeIn(side[2]),
                      run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def rise(self):
        D = load("dlw")
        F = load("film")
        d = D["deu"]
        ax = plane([1975, 2021], [1.0, 1.7], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[1.0, 1.2, 1.4, 1.6],
                   ylabel=r"markup, \ price over marginal cost", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        p0 = dot(ax, 1980, d["m1980"], PRICE, 0.11)
        p1 = dot(ax, 2016, d["m2016"], LOSS, 0.11)
        conn = DashedLine(ax.ax.c2p(1980, d["m1980"]), ax.ax.c2p(2016, d["m2016"]), color=GREY_B, stroke_width=2.0)
        l0 = label(rf"1980: \ {d['m1980']:.2f}", font_size=18, color=PRICE).next_to(p0, DOWN, buff=0.15)
        l1 = label(rf"2016: \ {d['m2016']:.2f}", font_size=18, color=LOSS).next_to(p1, UP, buff=0.15)
        side = VGroup(
            label(r"American public firms, \\ weighted by sales", font_size=18, color=WHITE),
            label(r"the median firm's \\ markup: \ unchanged", font_size=18, color=GREY_A),
            label(r"the rise: \ in the upper \\ tail and in the \\ reallocation of sales \\ toward it", font_size=18,
                  color=LOSS),
            label(rf"the intermission: \ profits \\ {F['m1980_2000']:.0f}\% of GDP in 1980--2000, \\ "
                  rf"{F['m2010_2026']:.0f}\% since 2010", font_size=18, color=PROFIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.DLW_2012.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 2020 De Loecker, Jan Eeckhout and Gabriel Unger applied the formula to every American public firm. "
            f"<bookmark mark='a'/> The sales-weighted average markup was {d['m1980']:.2f} in 1980, "
            f"<bookmark mark='b'/> and {d['m2016']:.2f} by 2016: from twenty-one percent above marginal cost to "
            "sixty-one. <bookmark mark='c'/> The median firm's markup barely moved. The rise came from the top: "
            "high-markup firms charged more, and sales shifted toward them. <bookmark mark='d'/> It fits the "
            f"intermission's picture, profits after tax rising from about {F['m1980_2000']:.0f} percent of GDP "
            f"between 1980 and 2000 to about {F['m2010_2026']:.0f} percent since 2010, though profits and markups "
            "are not the same thing."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(p0, scale=1.5), FadeIn(l0))
            vo.wait_until("b")
            self.play(Create(conn), FadeIn(p1, scale=1.5), FadeIn(l1))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def critics(self):
        cards = point_cards([
            (r"which costs vary?", r"count selling and \\ overhead costs as \\ variable, \ and the \\ rise flattens "
                                   r"\\ (Traina)", HOLD),
            (r"revenue, \ not quantity", r"with revenue data the \\ estimated elasticity \\ is not the one \\ the "
                                         r"formula needs \\ (Bond et al.)", LOSS),
            (r"which firms?", r"public firms are \\ not the economy", DEMAND),
            (r"the open question", r"a rise in the \\ typical markup, \ or \\ a shift of sales \\ "
                                   r"toward high-markup \\ firms?", GAIN),
        ], width=12.8, cols=4, font_size=17).move_to(DOWN * 0.1)
        head = label(r"how much has market power risen?", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.MARKUP_CRITIQUE.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The finding set off a debate that is still open. <bookmark mark='a'/> James Traina showed that "
            "counting selling, general and administrative costs as variable, as many modern firms' costs are, "
            "makes the rise much flatter. <bookmark mark='b'/> Stephen Bond and coauthors showed that with revenue "
            "rather than quantity data, the production-function elasticity is not the one the formula needs, as the "
            "Island just showed for a wrong elasticity. <bookmark mark='c'/> Public firms are not the whole "
            "economy. <bookmark mark='d'/> Susanto Basu's review found the broader evidence for a large rise in the "
            "typical firm's markup inconclusive. Whether the typical firm gained power, or sales shifted toward "
            "firms that always had it, is the open question, and the markups dial records where things stand."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
