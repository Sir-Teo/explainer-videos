from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Logit(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The logit, \ the red bus and the nest", r"What does the simplest model get wrong?",
             "Chapter five. The logit, the red bus and the nest.", lit={1974: r"McFadden", 1994: r"Berry"},
             scale=("market",), horizon=("a year",))
        self.formula()
        self.redbus()
        self.diversion()
        self.nested()

    def formula(self):
        lines = VGroup(
            MathTex(r"s_j \;=\; \frac{e^{\delta_j}}{1 + \sum_k e^{\delta_k}}, \qquad \delta_j = x_j\beta - \alpha p_j "
                    r"+ \xi_j", font_size=40),
            MathTex(r"\ln s_j - \ln s_0 \;=\; x_j\beta - \alpha p_j + \xi_j", font_size=42, color=E.ACCENT),
            MathTex(r"\frac{\partial s_j}{\partial p_j}\frac{p_j}{s_j} = -\alpha p_j (1 - s_j), \qquad "
                    r"\frac{\partial s_j}{\partial p_k}\frac{p_k}{s_j} = \alpha p_k s_k", font_size=36,
                    color=PRICE),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.7)
        notes = VGroup(
            label(r"if each buyer's taste $\varepsilon$ is independent across products \ (McFadden)", font_size=19,
                  color=GREY_A).next_to(lines[0], UP, buff=0.3),
            label(r"Berry's inversion: \ a linear equation, \ so price can be instrumented", font_size=20,
                  color=E.ACCENT).next_to(lines[1], DOWN, buff=0.2),
        )
        foot = label(r"the cross-elasticity depends on $k$'s price and share, \ not on how similar $j$ and $k$ are",
                     font_size=21, color=LOSS).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.LANCASTER_1966.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The simplest version makes each buyer's idiosyncratic taste, epsilon, independent across products, "
            "with a particular distribution. Then Daniel McFadden's logit gives the shares in closed form: each "
            "product's share is e to its mean utility, delta, over one plus the sum over all products, the one "
            "standing for buying nothing. <bookmark mark='a'/> In 1994 Steven Berry noticed what this allows. Take "
            "logs, subtract the log of the outside share, and the mean utility appears alone: a linear equation in "
            "price and characteristics, with the unseen quality as its error. Price can then be instrumented, as in "
            "any linear regression. <bookmark mark='b'/> But look at the elasticities the logit implies. "
            "<bookmark mark='c'/> The cross-elasticity of product j's sales with respect to product k's price "
            "depends only on k's price and share. It does not depend on how similar j and k are."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(notes[0]), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(Write(lines[1]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(Write(lines[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def bars(self, vals, names, colors, x0, title, title_color):
        g = VGroup()
        for k, (v, nm, col) in enumerate(zip(vals, names, colors)):
            x = x0 + 1.2 * k
            r = Rectangle(width=0.8, height=max(v * 6.0, 0.02), stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to(np.array([x, -2.2 + v * 3.0, 0]))
            g.add(VGroup(r, label(nm, font_size=17, color=col).next_to(np.array([x, -2.2, 0]), DOWN, buff=0.15),
                         label(rf"{100 * v:.0f}\%", font_size=19, color=WHITE).next_to(r, UP, buff=0.1)))
        head = label(title, font_size=21, color=title_color).next_to(g, UP, buff=0.5)
        head.set_y(1.9)
        return VGroup(g, head)

    def redbus(self):
        L = load("logit")
        blue, red = "#5DA9E9", "#F25F5C"
        before = self.bars(L["logit2"], (r"car", r"blue bus"), (GREY_B, blue), -5.6, r"before: \ two options",
                           WHITE)
        logit3 = self.bars(L["logit3"], (r"car", r"blue bus", r"red bus"), (GREY_B, blue, red), -1.6,
                           r"logit: \ a new red bus", LOSS)
        sense = self.bars(L["nest3"], (r"car", r"blue bus", r"red bus"), (GREY_B, blue, red), 2.6,
                          r"common sense \ (and a nest)", GAIN)
        head = label(r"the red bus and the blue bus", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.4)
        tag = published_tag(r"McFadden (1974), \ the classic example", corner=DR, font_size=11)
        with self.voiceover(
            "The classic illustration involves buses. <bookmark mark='a'/> Commuters choose between a car and a "
            "blue bus, and split half and half. <bookmark mark='b'/> Now a red bus appears, identical to the blue "
            "one except for its colour. The logit treats it as a new product with its own independent appeal, and "
            "predicts that each option now gets a third: the car loses a third of its riders to a bus nobody needed. "
            "<bookmark mark='c'/> Common sense says the car keeps half, and the two buses split the other half. This "
            "is the independence of irrelevant alternatives: under the logit, the ratio of any two shares ignores "
            "every other option, so a new product draws from all others in proportion to their shares."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(before))
            vo.wait_until("b")
            self.play(FadeIn(logit3))
            vo.wait_until("c")
            self.play(FadeIn(sense))
        self.clear_scene()

    def diversion(self):
        L = load("logit")
        names = L["names"]
        j = L["from"]
        others = [k for k in range(5) if k != j]
        lab = [names[k] for k in others] + [r"no cereal"]
        cols = [NEST[TRUTH["playit"]["nests"][k]] for k in others] + [GREY_B]
        plain = [L["plain"][k] for k in others] + [L["outside_plain"]]
        nest = [L["nested"][k] for k in others] + [L["outside_nested"]]
        rows = VGroup()
        for k, (nm, a, b, col) in enumerate(zip(lab, plain, nest, cols)):
            y = 1.3 - 0.75 * k
            ra = Rectangle(width=a * 6, height=0.26, stroke_width=0, fill_color=LOSS, fill_opacity=0.8).move_to(
                np.array([-0.4 + a * 3, y + 0.15, 0]))
            rb = Rectangle(width=b * 6, height=0.26, stroke_width=0, fill_color=GAIN, fill_opacity=0.8).move_to(
                np.array([-0.4 + b * 3, y - 0.15, 0]))
            rows.add(VGroup(label(nm, font_size=19, color=col).next_to(np.array([-0.55, y, 0]), LEFT, buff=0.1),
                            ra, label(rf"{100 * a:.0f}\%", font_size=15, color=LOSS).next_to(ra, RIGHT, buff=0.1),
                            rb, label(rf"{100 * b:.0f}\%", font_size=15, color=GAIN).next_to(rb, RIGHT, buff=0.1)))
        head = label(rf"{names[j]} raises its price: \ where do its lost shoppers go?", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        key = VGroup(label(r"red: \ plain logit", font_size=19, color=LOSS),
                     label(r"green: \ the game's nested logit", font_size=19, color=GAIN)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.6)
        tag = island_tag(corner=DL, font_size=14)
        with self.voiceover(
            "The same flaw matters for mergers. Take the game's market, and suppose Bran Buds raises its price. "
            "<bookmark mark='a'/> Under plain logit, its lost shoppers spread across everything in proportion to "
            f"size: only {say_pct(plain[3], 0)} go to Bran Twigs, its near twin, and most stop buying cereal. "
            "<bookmark mark='b'/> Under the nested logit that generated the game, "
            f"{say_pct(nest[3], 0)} go to Bran Twigs. A plain logit would have called merger X harmless. The "
            "assumption chosen for demand decides the answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(r_[0]) for r_ in rows], run_time=1.2)
            vo.wait_until("a")
            self.play(*[GrowFromEdge(r_[1], LEFT) for r_ in rows], *[FadeIn(r_[2]) for r_ in rows],
                      FadeIn(key[0]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(r_[3], LEFT) for r_ in rows], *[FadeIn(r_[4]) for r_ in rows],
                      FadeIn(key[1]))
        self.clear_scene()

    def nested(self):
        P = TRUTH["playit"]
        root = label(r"a shopper", font_size=22, color=WHITE).move_to(UP * 2.3)
        mids = VGroup(*[label(t, font_size=20, color=c) for t, c in ((r"no cereal", GREY_B), (r"sweet", NEST[0]),
                                                                     (r"nutty", NEST[1]), (r"bran", NEST[2]))])
        mids.arrange(RIGHT, buff=1.4).move_to(UP * 0.9)
        leaves = VGroup()
        groups = {0: [0, 1], 1: [2], 2: [3, 4]}
        for g, js in groups.items():
            for j in js:
                leaves.add(label(P["names"][j], font_size=16, color=NEST[g]))
        leaves.arrange(RIGHT, buff=0.35).move_to(DOWN * 0.5)
        edges = VGroup(*[Line(root.get_bottom(), m.get_top(), stroke_width=1.6, color=GREY_B) for m in mids])
        k = 0
        for g, js in groups.items():
            for _ in js:
                edges.add(Line(mids[g + 1].get_bottom(), leaves[k].get_top(), stroke_width=1.6, color=NEST[g]))
                k += 1
        eq = MathTex(r"u_{ij} = \delta_j + \zeta_{ig}(\sigma) + (1 - \sigma)\,\varepsilon_{ij}", font_size=36,
                     color=E.ACCENT).to_edge(DOWN, buff=1.3)
        foot = label(rf"$\sigma$ from 0 \ (plain logit) \ to 1 \ (perfect substitutes in a nest); \ the game used "
                     rf"$\sigma$ = {P['sigma']}", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"McFadden (1978); \ Cardell (1997)", corner=DR, font_size=11)
        with self.voiceover(
            "The nested logit is the first repair. <bookmark mark='a'/> The economist groups products into nests "
            "that are likely substitutes, here sweet, nutty and bran, with not buying cereal as its own nest. "
            "<bookmark mark='b'/> Each buyer shares a taste for everything in a nest, so shoppers who leave one bran "
            "cereal tend to choose the other. <bookmark mark='c'/> One parameter, sigma, measures how strong that "
            "shared taste is: zero gives back the plain logit, and as it approaches one, products in a nest become "
            "perfect substitutes. The game used 0.6. <bookmark mark='d'/> The weakness is that the economist must "
            "draw the nests in advance, and every product sits in exactly one. A sweet bran cereal has to choose. "
            "The next chapter removes the need to choose."
        ) as vo:
            self.play(FadeIn(root), FadeIn(tag), FadeIn(mids[0]), Create(edges[0]))
            vo.wait_until("a")
            self.play(*[FadeIn(m) for m in mids[1:]], *[Create(e) for e in edges[1:4]])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(lf) for lf in leaves], lag_ratio=0.2), *[Create(e) for e in edges[4:]])
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(foot))
            vo.wait_until("d")
            self.play(Indicate(VGroup(leaves[0], leaves[3]), color=WHITE, scale_factor=1.06))
        self.clear_scene()
