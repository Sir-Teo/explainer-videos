from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class SCP(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Structure, \ conduct, \ performance", r"Does concentration cause high margins?",
             "Chapter one. Structure, conduct, performance.", lit={1951: r"Bain", 1973: r"Demsetz"},
             scale=("industry",), horizon=("a decade",))
        self.bain()
        self.island()
        self.within()
        self.formula()

    def bain(self):
        B = tables.BAIN_1951.data
        steps = flow_chain([(r"structure", LOSS), (r"conduct", PRICE), (r"performance", DEMAND)],
                           notes=[r"how many firms, \\ how concentrated", r"how they price \\ and compete",
                                  r"profits, \ margins, \\ efficiency"], box_w=3.0, font_size=24,
                           note_size=17).move_to(UP * 1.7)
        bars = VGroup()
        for k, (nm, v, col) in enumerate(((rf"the eight largest firms \\ make {B['cut']}\% or more", B["high"], LOSS),
                                          (r"the rest", B["low"], DEMAND))):
            y = -0.9 - 1.15 * k
            w = v * 0.42
            r = Rectangle(width=w, height=0.62, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-0.6 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=19, color=col).next_to(np.array([-0.75, y, 0]), LEFT, buff=0.1), r,
                            label(rf"about {v}\%", font_size=21, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        sub = label(rf"Bain: \ {B['industries']} American industries, \ {B['years']}: \ profit rates", font_size=20,
                    color=GREY_A).next_to(bars, UP, buff=0.3)
        tag = published_tag(tables.BAIN_1951.tag, corner=DR, font_size=11)
        with self.voiceover(
            "For thirty years after the Second World War, industrial organization had one organizing idea. "
            "<bookmark mark='a'/> Structure, conduct, performance: the structure of an industry, how many firms and "
            "how concentrated, shapes their conduct, how they price and compete, which shapes performance, the "
            "profits and margins they earn. <bookmark mark='b'/> In 1951 Joe Bain sorted forty-two American "
            "industries of the late 1930s by whether their eight largest firms made at least seventy percent of the "
            f"output. In the concentrated half, profit rates averaged about {B['high']} percent; "
            f"<bookmark mark='c'/> in the rest, about {B['low']} percent. Concentration, it seemed, let firms "
            "collude and raise prices, and the cure was to break them up or keep them from merging."
        ) as vo:
            self.play(FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("b")
            self.play(FadeIn(sub), FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
        self.clear_scene()

    def island(self):
        S = load("scp")
        T = TRUTH["scp"]
        hhi, pcm = np.array(S["hhi"]), np.array(S["pcm"])
        ax = plane([1500, 7000], [0.1, 0.6], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[2000, 3000, 4000, 5000, 6000, 7000], yticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                   xlabel=r"concentration: \ the Herfindahl index", ylabel=r"the industry's price-cost margin",
                   xfmt=lambda v: f"{v:,.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        pts = VGroup(*[dot(ax, x, y, PRICE, 0.035) for x, y in zip(hhi, pcm)])
        fit = np.polyfit(hhi, pcm, 1)
        ln = seg(ax, 1700, np.polyval(fit, 1700), 6800, np.polyval(fit, 6800), LOSS, 3.0)
        side = VGroup(
            label(rf"{T['n_ind']} industries: \\ the same demand, \\ {T['n_firms']} firms each, \\ all playing "
                  r"Cournot", font_size=18, color=WHITE),
            label(r"they differ only in \\ how unequal their \\ firms' costs are", font_size=18, color=GREY_A),
            label(rf"correlation: \ {S['corr']:.2f}", font_size=20, color=LOSS),
            label(r"conduct is identical: \\ no industry colludes", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1973 Harold Demsetz pointed to another explanation. Suppose some firms are simply better: lower "
            "costs, better products. They grow large, so the industry becomes concentrated, and they earn high "
            "margins, because they are better, not because they collude. <bookmark mark='a'/> The Island can check "
            f"the logic. Here are {T['n_ind']} industries with the same demand and {T['n_firms']} firms each, all "
            "competing in the same way, by choosing quantities as in Part twelve's Cournot game. "
            "<bookmark mark='b'/> They differ only in how unequal their firms' costs are. <bookmark mark='c'/> "
            "Plot each industry's concentration against its margin, and they rise together, with a correlation of "
            f"{S['corr']:.2f}. <bookmark mark='d'/> Yet conduct is identical everywhere: no industry colludes. "
            "Bain's correlation, on its own, cannot tell market power from efficiency."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(side[0], color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ln), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def within(self):
        S = load("scp")
        sh, mg = np.array(S["share"]), np.array(S["margin"])
        ax = plane([0, 0.8], [-0.1, 0.8], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                   xlabel=r"a firm's share of its industry", ylabel=r"the firm's own margin",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        pts = VGroup(*[dot(ax, x, y, DEMAND, 0.04) for x, y in zip(sh, mg) if -0.1 <= y <= 0.8])
        side = VGroup(
            label(r"inside each industry: \\ the larger firms are \\ the low-cost firms", font_size=18,
                  color=DEMAND),
            label(rf"correlation: \ {S['within_corr']:.2f}", font_size=20, color=WHITE),
            label(r"Demsetz's test: \\ do the small firms \\ in concentrated \\ industries earn more \\ too?",
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Demsetz also suggested a test. <bookmark mark='a'/> Look inside industries. On the Island, a firm's "
            "margin rises with its share, because the large firms are the ones with low costs; "
            f"<bookmark mark='b'/> the correlation is {S['within_corr']:.2f}. <bookmark mark='c'/> If collusion "
            "raised prices, every firm in a concentrated industry, large or small, would earn more. If efficiency "
            "explains it, only the large ones do. Demsetz found the second pattern in American data, and the debate "
            "turned from correlations to conduct."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def formula(self):
        lines = VGroup(
            MathTex(r"\frac{p - c_i}{p} \;=\; \frac{s_i}{\varepsilon}", font_size=46),
            MathTex(r"\sum_i s_i\,\frac{p - c_i}{p} \;=\; \frac{\sum_i s_i^2}{\varepsilon} \;=\; "
                    r"\frac{\mathrm{HHI}}{10{,}000\;\varepsilon}", font_size=42, color=E.ACCENT),
        ).arrange(DOWN, buff=0.6).move_to(UP * 0.9)
        notes = VGroup(
            label(r"a Cournot firm's margin is its share over the elasticity of market demand", font_size=21,
                  color=GREY_A),
            label(r"so the industry's margin is the Herfindahl index over the elasticity", font_size=21,
                  color=GREY_A),
            label(r"structure and performance are both outcomes: \ the cause is in costs and conduct",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Cowling and Waterson (1976); \ Part 12", corner=DR, font_size=11)
        with self.voiceover(
            "The Island's pattern is not an accident; it is algebra. <bookmark mark='a'/> In the Cournot game of "
            "Part twelve, each firm's margin equals its share of the market divided by the elasticity of market "
            "demand. <bookmark mark='b'/> Average over firms, weighting by their shares, and the industry's margin "
            "equals the sum of squared shares, the Herfindahl index, divided by the same elasticity. "
            "<bookmark mark='c'/> So concentration and margins move together whenever costs differ, with no change "
            "in conduct at all. Structure and performance are both outcomes; the causes are in costs and conduct. "
            "To measure market power, economists had to measure conduct directly."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2], shift=UP * 0.1))
        self.clear_scene()
