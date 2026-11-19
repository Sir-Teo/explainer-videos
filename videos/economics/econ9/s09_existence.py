from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

GOOD = (r"fish", r"coconuts", r"timber")


class Simplex(VGroup):
    """The price simplex for three goods: the corner for good k is where only good k has a price."""

    def __init__(self, side=6.0, center=ORIGIN):
        super().__init__()
        h = side * np.sqrt(3) / 2
        self.V = [center + np.array([-side / 2, -h / 3, 0]), center + np.array([side / 2, -h / 3, 0]),
                  center + np.array([0, 2 * h / 3, 0])]
        self.tri = Polygon(*self.V, stroke_color=GREY_B, stroke_width=2.5)
        self.add(self.tri)
        self.corners = VGroup()
        for k, (v, d) in enumerate(zip(self.V, (DOWN, DOWN, UP))):
            self.corners.add(label(rf"only {GOOD[k]} \\ has a price" if k < 2 else rf"only {GOOD[k]} has a price",
                                   font_size=18, color=GOODS3[k]).next_to(v, d, buff=0.15))
        self.add(self.corners)

    def p2p(self, p):
        p = np.asarray(p, float)
        p = p / p.sum()
        return p[0] * self.V[0] + p[1] * self.V[1] + p[2] * self.V[2]

    def g2p(self, i, j, N):
        return self.p2p([i, j, N - i - j])


class Existence(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Existence: \ Sperner's lemma and Scarf's walk", r"How do we know there are prices that clear "
             r"every market at once?", "Chapter seven. Existence: Sperner's lemma and Scarf's walk.",
             lit={1954: r"Arrow and Debreu; \ McKenzie"})
        self.triangle()
        self.fixed_point()
        self.colouring()
        self.walk()

    def triangle(self):
        s = load("simplex")
        S = Simplex(5.6, center=LEFT * 2.8 + DOWN * 0.2)
        arrows = VGroup()
        for p, z in s["arrows"]:
            z = np.array(z)
            d = z - z.mean()
            start = S.p2p(p)
            end = S.p2p(np.array(p) + 0.06 * d / max(np.linalg.norm(d), 1e-9))
            arrows.add(Arrow(start, end, buff=0, stroke_width=2.5, color=GREY_A, max_tip_length_to_length_ratio=0.35,
                             max_stroke_width_to_length_ratio=8))
        eq = Dot(S.p2p(s["exact"]), radius=0.09, color=E.ACCENT)
        side = VGroup(
            label(r"three goods now: \ Ana owns the fish, \\ Bo the coconuts, \ Friday the timber", font_size=22),
            label(r"only relative prices matter: \ scale them to add to 1, \\ and every price list is a point in "
                  r"this triangle", font_size=22),
            label(r"the arrows: \ which prices are too low, \\ where demand exceeds supply", font_size=22,
                  color=GREY_A),
            label(r"is there always a point where every market clears?", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "With two goods, finding the equilibrium meant finding where one curve crosses zero. With more goods "
            "it's harder. <bookmark mark='a'/> Take three: Ana owns the fish, Bo the coconuts, and Friday a stock "
            "of timber. <bookmark mark='b'/> Only relative prices matter, so scale every price list to add up to "
            "one. Then every possible price list is a point in this triangle. At a corner only one good has a "
            "price; in the middle all three are equal. <bookmark mark='c'/> At each point, the arrow shows which "
            "way the prices are wrong: it points away from goods in excess supply, toward goods in excess demand. "
            "<bookmark mark='d'/> Somewhere the arrows must vanish, at a price list where every market clears. But "
            "how do we know that, for any economy at all?"
        ) as vo:
            self.play(Create(S.tri), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(S.corners), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.03), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(eq, scale=0.5), FadeIn(side[3]))
        self.clear_scene()

    def fixed_point(self):
        rows = VGroup(
            label(r"raise the price of every good in excess demand, \ then rescale:", font_size=26),
            MathTex(r"f(p)_k = \frac{p_k + \max(z_k(p), 0)}{1 + \sum_j \max(z_j(p), 0)}", font_size=40,
                    color=E.ACCENT),
            label(r"$f$ maps the triangle into itself, \ continuously", font_size=26),
            label(r"Brouwer (1912): \ such a map has a fixed point, \ $f(p) = p$", font_size=26, color=CC),
            label(r"at a fixed point no good is in excess demand: \ an equilibrium", font_size=26, color=CC),
        ).arrange(DOWN, buff=0.38)
        hc = history_card(1954, r"Arrow and Debreu; \ Lionel McKenzie", r"existence proved with fixed-point theorems, "
                          r"for economies with production, \ many goods and many traders", color=E.ACCENT, width=10.8,
                          font_size=22)
        VGroup(rows, hc).arrange(DOWN, buff=0.45)
        with self.voiceover(
            "The proof turns the question into a fixed point. <bookmark mark='a'/> Define a rule: take a price "
            "list, raise the price of every good in excess demand, and rescale so the prices still add to one. "
            "<bookmark mark='b'/> That rule takes each point of the triangle to another point of the triangle, and "
            "it moves smoothly: nearby prices go to nearby prices. <bookmark mark='c'/> A theorem of Brouwer's, "
            "from 1912, says that any such map of a triangle into itself leaves some point where it was. "
            "<bookmark mark='d'/> And at a point the rule doesn't move, no good can be in excess demand. With "
            "Walras's law, every market clears. <bookmark mark='e'/> Arrow and Debreu, and independently Lionel "
            "McKenzie, proved existence in 1954 with fixed-point theorems of this kind, for economies with "
            "production, any number of goods and traders."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Write(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.clear_scene()

    def colouring(self):
        s = load("simplex")
        g = s["grids"]["12"]
        N = 12
        S = Simplex(5.8, center=LEFT * 2.8 + DOWN * 0.25)
        lines = VGroup()
        for k in range(1, N):
            for a_, b_ in (((k, 0), (k, N - k)), ((0, k), (N - k, k)), ((k, 0), (0, k))):
                lines.add(Line(S.g2p(*a_, N), S.g2p(*b_, N), color=GREY_D, stroke_width=1))
        dots = VGroup(*[Dot(S.g2p(i, j, N), radius=0.075, color=GOODS3[k]) for i, j, k in g["labels"]])
        legend = VGroup(*[VGroup(Dot(radius=0.08, color=GOODS3[k]), label(rf"{GOOD[k]} in excess supply",
                                                                         font_size=19, color=GOODS3[k])).arrange(
            RIGHT, buff=0.12) for k in range(3)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side = VGroup(
            label(r"cut the triangle into small triangles; \\ colour each corner by a good \\ that is \emph{not} "
                  r"in excess demand", font_size=22),
            legend,
            label(r"on the bottom edge timber is free, \\ so everyone wants it: \ never timber's colour",
                  font_size=21, color=GREY_A),
            label(r"Sperner (1928): \ some small triangle \\ has all three colours", font_size=23, color=CC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "There's a way to see Brouwer's theorem with nothing but colouring. <bookmark mark='a'/> Cut the "
            "triangle into small triangles. At each corner of each small one, compute the excess demands, and "
            "colour the point by a good that is not in excess demand there: blue for fish, orange for coconuts, "
            "green for timber. By Walras's law there is always at least one. <bookmark mark='b'/> The colouring "
            "obeys one rule on the edges. Along the bottom, timber's price is zero, so everyone wants it and it "
            "is never the colour; the same goes for the other edges. <bookmark mark='c'/> In 1928 Emanuel Sperner "
            "proved that any colouring that obeys this rule has a small triangle with all three colours. In such "
            "a triangle every good is in excess supply at one corner or another, so if the triangles are small, "
            "its corners are all close to an equilibrium."
        ) as vo:
            self.play(Create(S.tri), FadeIn(S.corners), FadeIn(lines), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.01), FadeIn(side[1]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def walk(self):
        s = load("simplex")
        N = 12
        g = s["grids"][str(N)]
        S = Simplex(5.8, center=LEFT * 2.8 + DOWN * 0.25)
        lines = VGroup()
        for k in range(1, N):
            for a_, b_ in (((k, 0), (k, N - k)), ((0, k), (N - k, k)), ((k, 0), (0, k))):
                lines.add(Line(S.g2p(*a_, N), S.g2p(*b_, N), color=GREY_D, stroke_width=1))
        dots = VGroup(*[Dot(S.g2p(i, j, N), radius=0.075, color=GOODS3[k]) for i, j, k in g["labels"]])
        rooms = VGroup(*[Polygon(*[S.g2p(i, j, N) for i, j in t], stroke_width=0, fill_color=E.ACCENT,
                                 fill_opacity=0.35) for t in g["walk"]["path"]])
        last = Polygon(*[S.g2p(i, j, N) for i, j in g["walk"]["room"]], stroke_color=E.ACCENT, stroke_width=4,
                       fill_color=E.ACCENT, fill_opacity=0.6)
        eq = Dot(S.p2p(s["exact"]), radius=0.07, color=WHITE)
        errs = VGroup(label(r"grid \quad rooms walked \quad error in prices", font_size=20, color=GREY_A))
        for n_ in ("6", "12", "48"):
            gg = s["grids"][n_]
            errs.add(label(rf"{n_} \quad\quad {gg['walk']['rooms']} \quad\quad\quad {gg['error']:.3f}",
                           font_size=21, color=CC))
        errs.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        side = VGroup(
            label(r"a door: \ an edge coloured fish and coconuts", font_size=22),
            label(r"enter through a door on the bottom edge; \\ leave each room by its other door", font_size=22),
            label(r"you can't go round in circles, \ and you can't leave: \\ you must reach a room with all "
                  r"three colours", font_size=21, color=CC),
            errs,
            label(r"Scarf (1967): \ the first algorithm for equilibrium", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Sperner's proof is also a way to find the triangle. <bookmark mark='a'/> Call an edge a door if its "
            "ends are coloured fish and coconuts. Along the bottom edge there must be an odd number of doors, "
            "because the colour changes from fish at one corner to coconuts at the other. <bookmark mark='b'/> "
            "Walk in through the first one. Each room you enter has either one more door, which you leave by, or "
            "a third colour, and you've arrived. <bookmark mark='c'/> You can never re-enter a room, and you can "
            "never walk back outside, so the walk must end in a room with all three colours. Here it takes eleven "
            "rooms. <bookmark mark='d'/> Make the triangles smaller and the walk gets longer, but the room it "
            "finds gets closer to the exact equilibrium: an error of a hundredth or less with a grid of forty-"
            "eight. <bookmark mark='e'/> Herbert Scarf turned this walk into the first general algorithm for "
            "computing equilibria, in 1967. A proof that something exists became a way of finding it."
        ) as vo:
            self.play(FadeIn(S.tri), FadeIn(S.corners), FadeIn(lines), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rooms], lag_ratio=0.6), run_time=0.45 * len(rooms))
            vo.wait_until("c")
            self.play(FadeIn(last), FadeIn(eq), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
