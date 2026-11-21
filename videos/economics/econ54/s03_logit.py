from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


def heat(ax, xs, ys, Z, lo_color="#0B0F14", hi_color=EST, depth: float = 400.0):
    """A heat map of Z (rows: ys, columns: xs) on axes ``ax``: bright where Z is near its maximum, fading over
    ``depth`` units below it on a log scale."""
    xs, ys, Z = np.asarray(xs), np.asarray(ys), np.asarray(Z)
    top = Z.max()
    g = VGroup()
    dx = (xs[1] - xs[0]) / 2
    dy = (ys[1] - ys[0]) / 2
    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            gap = top - Z[i, j]
            f = float(np.clip(1 - np.log1p(gap) / np.log1p(depth), 0, 1))
            p0, p1 = ax.ax.c2p(x - dx, y - dy), ax.ax.c2p(x + dx, y + dy)
            g.add(Rectangle(width=abs(p1[0] - p0[0]) + 0.01, height=abs(p1[1] - p0[1]) + 0.01, stroke_width=0,
                            fill_color=interpolate_color(ManimColor(lo_color), ManimColor(hi_color), f ** 1.6),
                            fill_opacity=0.9).move_to((p0 + p1) / 2))
    return g


class Logit(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Random utility and maximum likelihood", r"How do choices reveal what a minute is worth?",
             "Chapter two. Random utility and maximum likelihood.", lit={1974: r"McFadden", 1978: r"nested logit"},
             scale=("person",), horizon=("a day",))
        self.derive()
        self.curve()
        self.surface()
        self.results()
        self.rail()

    def derive(self):
        eqs = VGroup(
            MathTex(r"U_{ij} = \underbrace{\beta_{\text{time}}\,\text{minutes}_{ij} + \beta_{\text{cost}}\,"
                    r"\text{dollars}_{ij} + \alpha_j}_{V_{ij}\ :\ \text{what we see}} + "
                    r"\underbrace{\varepsilon_{ij}}_{\text{what we do not}}", font_size=38, color=THEORY),
            MathTex(r"\varepsilon \sim \text{extreme value} \;\Longrightarrow\; \Pr(i \text{ takes the bus}) = "
                    r"\frac{e^{V_{i,\text{bus}}}}{e^{V_{i,\text{car}}} + e^{V_{i,\text{bus}}}}", font_size=38,
                    color=THEORY),
            MathTex(r"\log L(\beta) = \sum_{i=1}^{n} \log \Pr(\text{the choice } i \text{ made} \mid \beta)",
                    font_size=38, color=EST),
        ).arrange(DOWN, buff=0.6).move_to(UP * 0.5)
        notes = VGroup(
            label(r"each commuter takes whichever option gives more utility", font_size=20, color=GREY_A),
            label(r"maximum likelihood: \ the parameters that make the choices people actually made most probable",
                  font_size=20, color=EST),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"McFadden, \ in Zarembka (ed.), \ Frontiers in Econometrics (1974)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "McFadden's model starts from a person, not a zone. <bookmark mark='a'/> Commuter i gets some utility "
            "from each way of getting to work. Part of it we can see: the minutes and the dollars, weighted by "
            "how much each matters, and a constant for what the option is like. Part of it we cannot: the "
            "weather that morning, a dislike of buses, a bag to carry. Each commuter takes whichever option gives "
            "more. <bookmark mark='b'/> If the unseen parts are independent draws from the extreme-value "
            "distribution, the chance of taking the bus has this simple form, a logistic curve in the difference "
            "between the two options' visible utilities. That is the logit. <bookmark mark='c'/> Now turn it "
            "round. For any guess at the weights, the model gives each commuter a probability of doing what they "
            "actually did. Multiply those together over everyone, or add the logarithms, and you have the "
            "likelihood. <bookmark mark='d'/> Maximum likelihood takes the weights that make the choices people "
            "actually made most probable."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(eqs[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]), Indicate(eqs[2], color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def curve(self):
        C = load("commuters")
        ax = plane([-3, 3.4], [0, 1], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.8,
                   xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"how much better the bus looks: \ $V_{\text{bus}} - V_{\text{car}}$",
                   ylabel=r"share who take the bus", xfmt=lambda v: f"{v:.0f}".replace("-", "{-}"),
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        pts = VGroup(*[dot(ax, x, y, DATA, 0.09) for x, y in zip(C["mids"], C["obs"])])
        cur = path(ax, C["xs"], C["curve"], EST, 3.0, xr=(-3, 3.4))
        side = VGroup(
            label(rf"blue: \ the {C['n']:,} commuters, \\ in twelve groups of \\ similar trips", font_size=19,
                  color=DATA),
            label(r"gold: \ the fitted logit", font_size=19, color=EST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        tag = island_tag(r"simulated: \ the Island's commuters", corner=DR, font_size=13)
        with self.voiceover(
            f"The Island has {C['n']:,} commuters, each with a car trip and a bus trip of different lengths and "
            "costs. <bookmark mark='a'/> Group them by how much better the bus looks, under the fitted model, and "
            "plot the share in each group who took it. <bookmark mark='b'/> The logit's curve runs through them. "
            "Where the bus looks much worse, almost nobody takes it, but not quite nobody: the unseen part of "
            "utility means some people always surprise us. That is what the model's randomness is for."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, scale=0.5) for p_ in pts], lag_ratio=0.1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cur), FadeIn(side[1]), run_time=1.6)
        self.clear_scene()

    def surface(self):
        C = load("commuters")
        bt, bc = np.array(C["grid_t"]), np.array(C["grid_c"])
        ax = plane([bt[0], bt[-1]], [bc[0], bc[-1]], center=LEFT * 1.7 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[-0.1, -0.08, -0.06, -0.04, -0.02, 0.0], yticks=[-1.0, -0.75, -0.5, -0.25, 0.0],
                   xlabel=r"weight on a minute, \ $\beta_{\text{time}}$", ylabel=r"weight on a dollar, \ "
                   r"$\beta_{\text{cost}}$", xfmt=lambda v: f"{v:.2f}".replace("-", "{-}"),
                   yfmt=lambda v: f"{v:.2f}".replace("-", "{-}"), font_size=13)
        hm = heat(ax, bt, bc, C["ll"])
        tr = np.array(C["trace"])
        steps = VGroup(*[dot(ax, x, y, WHITE, 0.07) for x, y in tr[:4, :2]])
        legs = VGroup(*[Arrow(ax.ax.c2p(*tr[k, :2]), ax.ax.c2p(*tr[k + 1, :2]), buff=0.05, color=WHITE,
                              stroke_width=2.5, max_tip_length_to_length_ratio=0.15) for k in range(3)])
        truth = Cross(stroke_color=TRUTHC, stroke_width=3).scale(0.12).move_to(ax.ax.c2p(*C["truth"][:2]))
        est = dot(ax, C["b"][0], C["b"][1], EST, 0.1)
        side = VGroup(
            label(r"bright: \ high likelihood \\ (the constant held \\ at its estimate)", font_size=18, color=EST),
            label(rf"Newton's method: \\ from zero to the top \\ in {C['iters'] - 1} steps", font_size=18,
                  color=WHITE),
            label(r"white cross: \ the truth \\ gold: \ the estimate", font_size=18, color=TRUTHC),
            label(r"the curvature at the top \\ gives the standard errors", font_size=18, color=THEORY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here is the log likelihood as a landscape over the two weights, with the constant held at its "
            "estimate. <bookmark mark='a'/> Bright is high. The top is a narrow ridge: people's choices say "
            "clearly how minutes trade against dollars, and a little less clearly how much both matter. <bookmark "
            "mark='b'/> Newton's method climbs it from zero by fitting a bowl to the surface where it stands and "
            f"jumping to the bowl's top. It arrives in {C['iters'] - 1} steps. <bookmark mark='c'/> The white cross "
            "is the truth we planted; the gold dot is the estimate. <bookmark mark='d'/> And the curvature at the "
            "top gives the uncertainty: a sharp peak means the data pin the parameters down, a flat one means "
            "they do not. Its inverse is the estimate's variance, Fisher's information at work."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(hm), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]), FadeIn(side[1]))
            for k in range(3):
                self.play(GrowArrow(legs[k]), FadeIn(steps[k + 1]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(truth), FadeIn(est, scale=1.4), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(est, color=WHITE))
        self.clear_scene()

    def results(self):
        C = load("commuters")
        names = [r"a minute, \ $\beta_{\text{time}}$", r"a dollar, \ $\beta_{\text{cost}}$",
                 r"the bus itself, \ $\alpha_{\text{bus}}$"]
        rows = VGroup(VGroup(label(r"", font_size=20), label(r"truth", font_size=20, color=TRUTHC),
                             label(r"estimate", font_size=20, color=EST), label(r"standard error", font_size=20,
                                                                                color=THEORY)))
        for nm, t, b, s in zip(names, C["truth"], C["b"], C["se"]):
            rows.add(VGroup(label(nm, font_size=20, color=WHITE),
                            label(f"{t:.3f}".replace("-", "{-}"), font_size=21, color=TRUTHC),
                            label(f"{b:.3f}".replace("-", "{-}"), font_size=21, color=EST),
                            label(f"{s:.3f}", font_size=21, color=THEORY)))
        grid = VGroup(*[c for r in rows for c in r]).arrange_in_grid(rows=4, cols=4, buff=(0.7, 0.3),
                                                                      col_alignments="lccc")
        grid.move_to(UP * 1.4)
        vot = MathTex(r"\text{value of time} = 60 \times \frac{\beta_{\text{time}}}{\beta_{\text{cost}}} = "
                      rf"\${C['vot']:.2f} \pm {C['se_vot']:.2f} \text{{ an hour}}", font_size=38, color=EST)
        vot.next_to(grid, DOWN, buff=0.7)
        truth = label(rf"planted: \ \${C['vot_truth']:.2f} an hour", font_size=22, color=TRUTHC).next_to(vot, DOWN,
                                                                                                    buff=0.3)
        note_ = label(r"the ratio of two weights: \ a price nobody posted, \ read off choices", font_size=21,
                      color=GREY_A).next_to(truth, DOWN, buff=0.4)
        with self.voiceover(
            "The estimates. <bookmark mark='a'/> Each lies within one and a half standard errors of the value we "
            "planted. <bookmark mark='b'/> The number transport planners most want is a ratio: how many dollars a "
            "commuter will pay to save an hour, sixty times the weight on a minute over the weight on a dollar. "
            f"The estimate is {money_words(C['vot'])} an hour, give or take {C['se_vot']:.2f}, against "
            f"{money_words(C['vot_truth'])} planted. <bookmark mark='c'/> That is a price nobody ever posted, read "
            "off the choices people made. It is the number that goes into every appraisal of a new road or "
            "railway."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.4), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(vot), FadeIn(truth))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.clear_scene()

    def rail(self):
        R = load("rail")
        bt, at, al = R["before"], R["after_true"], R["after_logit_rightconst"]
        ax = plane([0.3, 3.7], [0, 0.65], center=LEFT * 1.6 + DOWN * 0.35, x_length=7.4, y_length=4.6, xticks=[],
                   yticks=[0, 0.2, 0.4, 0.6], ylabel=r"share of commuters", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=15)
        cols = (CAR, BUS, RAIL)
        names = (r"car", r"bus", r"rail")
        bars = VGroup()
        for j in range(3):
            g = VGroup()
            for k, (vals, op, dx) in enumerate(((bt + [0.0], 0.35, -0.27), (al, 0.95, 0.0), (at, 0.55, 0.27))):
                v = vals[j]
                x = j + 1 + dx
                p0, p1 = ax.ax.c2p(x - 0.12, 0), ax.ax.c2p(x + 0.12, max(v, 1e-4))
                r = Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), fill_color=cols[j],
                              fill_opacity=op, stroke_color=TRUTHC if k == 2 else cols[j],
                              stroke_width=2 if k == 2 else 0).move_to((p0 + p1) / 2)
                g.add(r)
            g.add(label(names[j], font_size=20, color=cols[j]).next_to(ax.ax.c2p(j + 1, 0), DOWN, buff=0.2))
            bars.add(g)
        key = VGroup(
            label(r"faint: \ before the railway", font_size=17, color=GREY_A),
            label(r"solid: \ the logit's forecast", font_size=17, color=EST),
            label(r"outlined: \ what happens \\ (a nested logit: \ bus and rail \\ are close substitutes)",
                  font_size=17, color=TRUTHC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35).shift(UP * 1.2)

        def from_bus(b0, a1):
            return (b0[1] - a1[1]) / ((b0[0] - a1[0]) + (b0[1] - a1[1]))

        fb_l, fb_t = from_bus(R["before_hat"], al), from_bus(bt, at)
        side = VGroup(
            label(rf"rail's riders from the bus: \\ logit {100 * fb_l:.0f}\%, \ truth {100 * fb_t:.0f}\%",
                  font_size=19, color=BUS),
            label(rf"cars left: \ logit {100 * al[0]:.0f}\%, \ truth {100 * at[0]:.0f}\%", font_size=19,
                  color=CAR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(key, DOWN, buff=0.5, aligned_edge=LEFT)
        tag = island_tag(r"simulated: \ the Island's commuters", corner=DR, font_size=13)
        with self.voiceover(
            "Now the reason for all this: a forecast. The Island opens a railway, "
            f"{R['rail']['time']:.0f} minutes and {money_words(R['rail']['cost'])} for everyone. <bookmark mark='a'/> "
            "Before it, the commuters split between car and bus. <bookmark mark='b'/> The logit, given the "
            f"railway's time and fare and its constant, forecasts that rail takes {say_pct(al[2], 0)} of "
            f"commuters. <bookmark mark='c'/> In fact it takes {say_pct(at[2], 0)}, close. But look where its "
            f"riders come from. The logit says {100 * fb_l:.0f} percent of them leave the bus and the rest leave "
            f"their cars; in truth {100 * fb_t:.0f} percent leave the bus, and "
            f"{say_pct(at[0], 0)} still drive, not {say_pct(al[0], 0)}. <bookmark mark='d'/> The logit's hidden "
            "assumption is that a new option draws from the old ones in proportion to their shares, because the "
            "unseen parts of utility are independent. On the Island, people who dislike the car's alternatives "
            "dislike both of them: rail and bus are close substitutes. McFadden's nested logit of 1978 lets the "
            "unseen parts be correlated within a nest. A forecast of traffic on the roads depends on getting "
            "that right."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), *[FadeIn(b[3]) for b in bars])
            vo.wait_until("a")
            self.play(*[FadeIn(b[0]) for b in bars[:2]], FadeIn(key[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(b[1], shift=UP * 0.1) for b in bars], FadeIn(key[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(b[2], shift=UP * 0.1) for b in bars], FadeIn(key[2]))
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Indicate(bars[0][2], color=WHITE, scale_factor=1.04))
        self.clear_scene()
