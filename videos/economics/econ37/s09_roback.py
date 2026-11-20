from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


def town_bars(names, values, color, x0, width=2.8, scale=4.0, y_top=1.6, step=0.62, fmt="{:+.2f}"):
    """One horizontal bar per town around a zero line at ``x0``."""
    g = VGroup()
    for k, (n, v) in enumerate(zip(names, values)):
        y = y_top - step * k
        r = Rectangle(width=max(abs(v) * scale, 0.01), height=0.36, stroke_width=0, fill_color=color,
                      fill_opacity=0.85).move_to(np.array([x0 + v * scale / 2, y, 0]))
        t = label(fmt.format(v), font_size=15, color=WHITE).next_to(r, RIGHT if v >= 0 else LEFT, buff=0.08)
        g.add(VGroup(r, t))
    axis = Line(np.array([x0, y_top + 0.35, 0]), np.array([x0, y_top - step * (len(names) - 1) - 0.35, 0]),
                color=GREY_B, stroke_width=1.5)
    return VGroup(axis, g)


class Roback(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Spatial equilibrium", r"Why do nice places have high rents and low wages?",
             "Chapter seven. Spatial equilibrium.", lit={1979: r"Rosen", 1982: r"Roback"},
             scale=("household", "nation"), horizon=("a decade",))
        self.towns()
        self.qol()
        self.shocks()

    def towns(self):
        T = load("towns")
        names, base = T["names"], T["base"]
        lw = np.array(base["logw"]) - np.mean(base["logw"])
        lr = np.array(base["logr"]) - np.mean(base["logr"])
        nm = VGroup(*[label(n, font_size=19, color=TOWN_COLORS[k]).move_to(np.array([-5.6, 1.6 - 0.62 * k, 0]))
                      for k, n in enumerate(names)])
        wb = town_bars(names, lw, WAGE, -2.6)
        rb = town_bars(names, lr, RENT, 2.4, scale=2.6)
        hw = label(r"wage \ (log, \ relative)", font_size=18, color=WAGE).move_to(np.array([-2.6, 2.4, 0]))
        hr = label(r"rent \ (log, \ relative)", font_size=18, color=RENT).move_to(np.array([2.4, 2.4, 0]))
        eq = MathTex(r"\log w_j - \alpha \log r_j + q_j = \bar v \quad \text{in every town}", font_size=32).to_edge(
            DOWN, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Sherwin Rosen in 1979 and Jennifer Roback in 1982 asked what happens when both workers and firms can "
            "move. The Island now has six towns. <bookmark mark='a'/> Here are their wages, <bookmark mark='b'/> and "
            "their rents. They differ a lot. <bookmark mark='c'/> But if people can move, no town can be better "
            "than another, all things counted: a high wage must be offset by a high rent or by a place nobody "
            "enjoys, and a lovely place must cost more or pay less. Utility, not income, is equalized."
        ) as vo:
            self.play(FadeIn(nm), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hw), FadeIn(wb), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(hr), FadeIn(rb), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(eq))
        self.clear_scene()

    def qol(self):
        T = load("towns")
        names = T["names"]
        q = np.array(T["q"]) - np.mean(T["q"])
        rec = np.array(T["base"]["qol"])
        ax = plane([-0.15, 0.2], [-0.15, 0.2], center=LEFT * 2.2 + DOWN * 0.4, x_length=4.8, y_length=4.8,
                   xticks=[-0.1, 0, 0.1, 0.2], yticks=[-0.1, 0, 0.1, 0.2], xlabel=r"amenity planted on the Island",
                   ylabel=r"read from prices: \ $\alpha \log r - \log w$", xfmt=lambda v: f"{v:+.1f}",
                   yfmt=lambda v: f"{v:+.1f}", font_size=13)
        diag = seg(ax, -0.15, -0.15, 0.2, 0.2, GREY_B, 1.5, dashed=True)
        pts = VGroup(*[VGroup(dot(ax, a, b, TOWN_COLORS[k], 0.1),
                              label(names[k], font_size=14, color=TOWN_COLORS[k]).next_to(ax.ax.c2p(a, b), LEFT,
                                                                                          buff=0.15))
                       for k, (a, b) in enumerate(zip(q, rec))])
        side = VGroup(
            label(r"quality of life, \ read from prices:", font_size=21, color=AMENITY),
            label(r"the rent people pay \\ beyond what the wage \\ makes up for", font_size=19, color=WHITE),
            label(rf"Lagoon: \ the nicest \ ({q[5]:+.2f}); \\ Ridge: \ the least \ ({q[4]:+.2f})", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.6)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "That turns prices into a measuring instrument. <bookmark mark='a'/> Whatever people pay in rent beyond "
            "what the local wage makes up for, they pay for the place itself: its weather, its coast, its schools, "
            "its safety. <bookmark mark='b'/> On the Island the amenities are planted, and reading them back from "
            "wages and rents recovers them exactly. <bookmark mark='c'/> Lagoon, by the beach, is the nicest; Ridge "
            "the least. David Albouy built indices like this for American cities, and Part forty-eight uses the "
            "same logic to value clean air."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in pts], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def shocks(self):
        T = load("towns")
        P, A = T["prod"], T["amen"]
        rows = [(r"wage", "dlogw", WAGE), (r"rent", "dlogr", RENT), (r"people", "dlogN", CITY),
                (r"everyone's utility", "dv", AMENITY)]

        def panel(d, x0, title, col):
            head = label(title, font_size=21, color=col).move_to(np.array([x0, 2.3, 0]))
            g = VGroup(head)
            for k, (nm, key, c) in enumerate(rows):
                v = d[key]
                y = 1.3 - 0.85 * k
                r = Rectangle(width=max(abs(v) * 18, 0.02), height=0.42, stroke_width=0, fill_color=c,
                              fill_opacity=0.85).move_to(np.array([x0 + 0.4 + v * 9, y, 0]))
                g.add(VGroup(label(nm, font_size=16, color=GREY_A).move_to(np.array([x0 - 1.7, y, 0])), r,
                             label(f"{100 * v:+.1f}\\%", font_size=16, color=WHITE).next_to(
                                 r, RIGHT if v >= 0 else LEFT, buff=0.08)))
            g.add(Line(np.array([x0 + 0.4, 1.75, 0]), np.array([x0 + 0.4, 1.3 - 0.85 * 3 - 0.45, 0]),
                       color=GREY_B, stroke_width=1.5))
            return g

        left = panel(P, -3.5, r"Harbour: \ productivity +10\%", WAGE)
        right = panel(A, 3.3, r"Lagoon: \ amenity +10\%", AMENITY)
        foot = label(r"in spatial equilibrium a local boom shows up in rents and people, \ while the gain in "
                     r"welfare spreads across the Island", font_size=18, color=E.ACCENT).to_edge(DOWN, buff=0.45)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now shock the Island. <bookmark mark='a'/> Harbour's firms become ten percent more productive. Its "
            f"wages rise {100 * P['dlogw']:.1f} percent, people arrive, its population grows "
            f"{100 * P['dlogN']:.0f} percent, and its rents rise {100 * P['dlogr']:.0f} percent. Everyone's "
            f"utility, everywhere, rises {100 * P['dv']:.1f} percent: the gain spreads across the Island, because "
            "people move until it does. <bookmark mark='b'/> Instead make Lagoon ten percent nicer. People move "
            f"in, rents rise {100 * A['dlogr']:.0f} percent, and wages fall {abs(100 * A['dlogw']):.1f} percent: "
            "the newcomers pay for the view twice, in rent and in pay. <bookmark mark='c'/> The lesson of spatial "
            "equilibrium: a local boom shows up in rents and in the number of people, not in the welfare of the "
            "people who live there, and the owners of local land are its surest beneficiaries."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(left[0]), FadeIn(right[0]), FadeIn(left[-1]), FadeIn(right[-1]),
                      FadeIn(VGroup(*[r_[0] for r_ in left[1:-1]])), FadeIn(VGroup(*[r_[0] for r_ in right[1:-1]])))
            vo.wait_until("a")
            self.play(*[FadeIn(r_[1:]) for r_ in left[1:-1]], run_time=2.0)
            vo.wait_until("b")
            self.play(*[FadeIn(r_[1:]) for r_ in right[1:-1]], run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
