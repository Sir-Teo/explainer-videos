from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403


def countdown(radius: float = 0.42) -> VGroup:
    t = ValueTracker(1.0)
    back = Circle(radius=radius, stroke_color=GREY_D, stroke_width=5)
    arc = always_redraw(lambda: Arc(radius=radius, start_angle=PI / 2, angle=-TAU * max(t.get_value(), 1e-3),
                                    stroke_color=E.ACCENT, stroke_width=5).move_arc_center_to(back.get_center()))
    g = VGroup(back, arc)
    g.t = t
    return g


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Play it: \ two baskets", r"Fish doubled in price. How much dearer is living?",
             "Chapter five. Play it: two baskets.", scale=("household",), horizon=("a year",))
        self.baskets()
        self.formulas()
        self.truth()
        self.drift()

    # ------------------------------------------------------------------
    def baskets(self):
        d = load("indices")
        stage = game_stage(13.0, 6.8, center=DOWN * 0.1)
        bo = islander("bo", 1.0, name=True).move_to(stage.box.get_corner(UL) + RIGHT * 1.0 + DOWN * 1.5)
        spend = label(r"spends \$100 a week: \ half on fish, \ half on coconuts", font_size=26, color=BO)
        spend.next_to(bo, RIGHT, buff=0.4)

        def year_row(name, p, q, color):
            t = label(name, font_size=26, color=color)
            fp = VGroup(fish_glyph(0.55), label(rf"\${p[0]:.2f}", font_size=26)).arrange(RIGHT, buff=0.15)
            cp = VGroup(coconut(0.15), label(rf"\${p[1]:.2f}", font_size=26)).arrange(RIGHT, buff=0.15)
            buys = label(rf"Bo buys {q[0]:g} fish and {q[1]:g} coconuts", font_size=24, color=GREY_A)
            return VGroup(t, fp, cp, buys).arrange(RIGHT, buff=0.5)

        calm = year_row(r"calm year", d["p0"], d["q0"], E.FISH)
        storm = year_row(r"stormy year", d["p1"], d["q1"], STORM_C)
        rows = VGroup(calm, storm).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.move_to(stage.box.get_center() + UP * 0.35)
        q = label(r"How much did Bo's cost of living rise?", font_size=32, color=E.ACCENT)
        opts = VGroup(*[label(t, font_size=28) for t in (r"A \ \ 100\%", r"B \ \ 50\%", r"C \ \ 41\%",
                                                         r"D \ \ 33\%")]).arrange(RIGHT, buff=0.9)
        qq = VGroup(q, opts).arrange(DOWN, buff=0.3).move_to(stage.box.get_center() + DOWN * 1.9 + LEFT * 0.5)
        ring = countdown().next_to(qq, RIGHT, buff=0.6)
        tag = island_tag(r"simulated: Bo's household; his tastes are planted, so the true answer is known",
                         corner=UR, font_size=16)
        with self.voiceover(
            "Bo runs the ferry, and his household lives on fish and coconuts. <bookmark mark='a'/> He spends a "
            "hundred dollars a week, and he likes to split it evenly: half on fish, half on coconuts. "
            "<bookmark mark='b'/> In a calm year fish cost two dollars and coconuts one, so Bo buys 25 fish and 50 "
            "coconuts. <bookmark mark='c'/> Then comes a stormy year. The boats stay in more often, and fish "
            "doubles to four dollars. Coconuts stay at one. Bo still spends half on each, so now he buys twelve "
            "and a half fish and the same 50 coconuts. <bookmark mark='d'/> Here's your question. How much did "
            "Bo's cost of living rise? How much more money would he need in the stormy year to be exactly as "
            "well off as in the calm one? A hundred percent, because fish doubled? Fifty? Forty-one? Thirty-three? "
            "Pause, and pick one."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(tag), FadeIn(bo))
            vo.wait_until("a")
            self.play(FadeIn(spend))
            vo.wait_until("b")
            self.play(FadeIn(calm, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(storm, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(q), LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in opts], lag_ratio=0.2),
                      FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=4.0, rate_func=linear)
        self.clear_scene()

    def formulas(self):
        d = load("indices")
        q0, q1 = d["q0"], d["q1"]
        las = VGroup(
            label(r"Laspeyres: \ the calm-year basket, \ 25 fish and 50 coconuts", font_size=25, color=LASP),
            MathTex(r"\frac{25 \times 4 + 50 \times 1}{25 \times 2 + 50 \times 1} = \frac{150}{100}", r"= 1.50",
                    font_size=40, color=LASP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        pas = VGroup(
            label(r"Paasche: \ the stormy-year basket, \ 12.5 fish and 50 coconuts", font_size=25, color=PAAS),
            MathTex(r"\frac{12.5 \times 4 + 50 \times 1}{12.5 \times 2 + 50 \times 1} = \frac{100}{75}", r"= 1.33",
                    font_size=40, color=PAAS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fis = VGroup(
            label(r"Irving Fisher, 1922: \ the geometric mean of the two, \ ``ideal''", font_size=25, color=FISHER),
            MathTex(r"\sqrt{1.50 \times 1.33} = \sqrt{2}", r"= 1.414", font_size=40, color=FISHER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        g = VGroup(las, pas, fis).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(LEFT * 0.6 + DOWN * 0.3)
        top = label(r"Three answers with names", font_size=34).to_edge(UP, buff=0.4)
        verdicts = VGroup(label(r"B \ \ $+50\%$", font_size=30, color=LASP).next_to(las[1], RIGHT, buff=0.8),
                          label(r"D \ \ $+33\%$", font_size=30, color=PAAS).next_to(pas[1], RIGHT, buff=0.8),
                          label(r"C \ \ $+41\%$", font_size=30, color=FISHER).next_to(fis[1], RIGHT, buff=0.8))
        with self.voiceover(
            "Three answers have names. <bookmark mark='a'/> Laspeyres's index prices the calm-year basket, 25 fish "
            "and 50 coconuts. It cost a hundred dollars in the calm year and costs a hundred and fifty in the "
            f"stormy one: up {100 * (d['laspeyres'] - 1):.0f} percent. That's answer B. <bookmark mark='b'/> "
            "Paasche's index prices the stormy-year basket, twelve and a half fish and 50 coconuts. It costs a "
            "hundred now and would have cost seventy-five before: up a third. That's D. <bookmark mark='c'/> In "
            "1922 the American economist Irving Fisher, after comparing well over a hundred formulas, recommended "
            "the geometric mean of the two, which he called ideal. Here it's the square root of two: up "
            f"{100 * (d['fisher'] - 1):.1f} percent. Answer C. Three formulas, three answers, from the same "
            "prices. Which is right?"
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(las[0]), Write(las[1]))
            self.play(FadeIn(verdicts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pas[0]), Write(pas[1]))
            self.play(FadeIn(verdicts[1]))
            vo.wait_until("c")
            self.play(FadeIn(fis[0]), Write(fis[1]))
            self.play(FadeIn(verdicts[2]))
        self.clear_scene()

    def truth(self):
        d = load("indices")
        ax = axes([0, 52], [0, 160], x_length=6.4, y_length=5.4, xticks=[0, 10, 20, 30, 40, 50],
                  yticks=[0, 50, 100, 150], xlabel=r"fish a week", ylabel=r"coconuts a week", font_size=20,
                  center=LEFT * 3.0 + DOWN * 0.2)
        a = ax.ax
        u0 = d["u0"]
        curve = a.plot(lambda f: u0 ** 2 / f, x_range=[u0 ** 2 / 158, 51, 0.25], color=TRUE, stroke_width=3.5)
        cl = label(r"as well off as \\ in the calm year", font_size=20, color=TRUE).move_to(a.c2p(44, 52))

        def budget(pf, inc, color, dashed=False):
            ln = Line(a.c2p(0, inc), a.c2p(inc / pf, 0), color=color, stroke_width=3)
            return DashedVMobject(ln, num_dashes=30) if dashed else ln

        b0 = budget(2, 100, E.FISH)
        b1 = budget(4, 100, STORM_C)
        bl = budget(4, 100 * d["laspeyres"], LASP, dashed=True)
        bt = budget(4, 100 * d["true"], FISHER)
        A = Dot(a.c2p(*d["q0"]), radius=0.08, color=E.FISH)
        B = Dot(a.c2p(*d["q1"]), radius=0.08, color=STORM_C)
        C = Dot(a.c2p(*d["q_lasp"]), radius=0.08, color=LASP)
        D = Dot(a.c2p(*d["q_true"]), radius=0.08, color=FISHER)
        notes = VGroup(
            label(r"calm year: \ \$100 buys 25 fish, 50 coconuts", font_size=22, color=E.FISH),
            label(r"stormy year, \$100: \ a lower curve", font_size=22, color=STORM_C),
            label(r"Laspeyres's \$150: \ the old basket, and more", font_size=22, color=LASP),
            label(rf"\${100 * d['true']:.2f}: \ just as well off", font_size=22, color=FISHER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.5).shift(UP * 0.8)
        ans = label(r"for Bo, \ C is exactly right: \ \textbf{41.4\%}", font_size=30, color=FISHER)
        ans.next_to(notes, DOWN, buff=0.6).align_to(notes, LEFT)
        why = label(r"Laspeyres ignores that Bo can switch; \\ Paasche pretends the switch cost nothing",
                    font_size=22, color=GREY_A).next_to(ans, DOWN, buff=0.35).align_to(notes, LEFT)
        tag = island_tag(r"simulated: Bo's tastes are planted (he always spends half on each)", corner=DR, font_size=16)
        with self.voiceover(
            "On the Island we can check, because Bo's tastes are planted, so we know exactly what makes him "
            "better or worse off. <bookmark mark='a'/> Here are fish across and coconuts up. In the calm year, a "
            "hundred dollars lets Bo reach any point on this line, and he chooses 25 fish and 50 coconuts. "
            "<bookmark mark='b'/> This green curve is every basket that leaves him exactly as well off as that. "
            "<bookmark mark='c'/> In the stormy year his hundred dollars buys less fish, and the best he can do "
            "lies on a lower curve. <bookmark mark='d'/> Laspeyres says: give him fifty percent more. With a "
            "hundred and fifty dollars he could buy his old basket. But he wouldn't: with fish dear and coconuts "
            "cheap, he swaps some fish for coconuts and ends up above the green curve, better off than before. "
            "Laspeyres overpays him. <bookmark mark='e'/> The least that puts him back on the green curve is "
            f"{money_words(100 * d['true'])}: forty-one point four percent more. Answer C. "
            "<bookmark mark='f'/> Laspeyres overstates the rise because it ignores that Bo can switch. Paasche "
            "understates it because it pretends switching cost him nothing. Fisher's mean lands between them. "
            "For tastes like Bo's it is exact, and for most others it comes very close: economists call indexes "
            "like it superlative."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(b0), FadeIn(A, scale=0.5), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(cl))
            vo.wait_until("c")
            self.play(Create(b1), FadeIn(B, scale=0.5), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Create(bl), FadeIn(notes[2]))
            self.play(FadeIn(C, scale=0.5), Flash(C, color=LASP))
            vo.wait_until("e")
            self.play(Create(bt), FadeIn(D, scale=0.5), FadeIn(notes[3]))
            self.play(FadeIn(ans, scale=0.9))
            vo.wait_until("f")
            self.play(FadeIn(why))
        self.clear_scene()

    def drift(self):
        d = load("indices")
        n = d["seasons"]
        ax = axes([0, n], [0, 2.2], x_length=8.0, y_length=4.6, xticks=list(range(0, n + 1, 2)),
                  yticks=[0, 0.5, 1.0, 1.5, 2.0], xlabel=r"season: \ calm, storm, calm, storm, \dots, calm",
                  ylabel=r"chained index, \ first season $= 1$", font_size=20, center=LEFT * 1.6 + DOWN * 0.2)
        a = ax.ax
        lines = VGroup()
        names = VGroup()
        for key, col, nm in (("laspeyres", LASP, r"chained Laspeyres"), ("paasche", PAAS, r"chained Paasche"),
                             ("fisher", FISHER, r"chained Fisher")):
            v = d["chain"][key]
            ln = VMobject(stroke_color=col, stroke_width=3.5).set_points_as_corners(
                [a.c2p(i, x) for i, x in enumerate(v)])
            lines.add(ln)
            names.add(label(rf"{nm}: \ {v[-1]:.2f}", font_size=24, color=col).next_to(a.c2p(n, v[-1]), RIGHT,
                                                                                     buff=0.15))
        head = label(r"Twelve seasons; \ prices end exactly where they began", font_size=28).to_edge(UP, buff=0.35)
        moral = label(r"chain often, \ and chain with a superlative index", font_size=26, color=FISHER)
        moral.next_to(ax, DOWN, buff=0.2).shift(RIGHT * 1.0)
        moral.to_edge(DOWN, buff=0.75)
        tag = island_tag(r"simulated: the storms come and go; Bo always spends half on each", corner=DR, font_size=16)
        with self.voiceover(
            "One more twist. Baskets go out of date, so statistical agencies chain their indexes: they compare "
            "each period with the one before, with up-to-date baskets, and multiply the links together. "
            "<bookmark mark='a'/> Let the storms come and go for twelve seasons, so that at the end prices are "
            "exactly where they started. A good index should end where it began, at one. <bookmark mark='b'/> "
            f"Chained Laspeyres ends at {d['chain']['laspeyres'][-1]:.2f}: it says prices doubled, though "
            "nothing has changed. Each storm it overstates the rise, and each calm it understates the fall. "
            f"<bookmark mark='c'/> Chained Paasche drifts the other way, to {d['chain']['paasche'][-1]:.2f}. "
            "<bookmark mark='d'/> Chained Fisher ends at exactly one. This is called chain drift, and it's why the "
            "United States has measured real GDP with chained Fisher indexes since 1996: the chained 2017 dollars "
            "on the gold line a minute ago."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(DashedLine(a.c2p(0, 1), a.c2p(n, 1), color=GREY_B, stroke_width=1.5)))
            vo.wait_until("b")
            self.play(Create(lines[0], rate_func=linear), run_time=2.5)
            self.play(FadeIn(names[0]))
            vo.wait_until("c")
            self.play(Create(lines[1], rate_func=linear), run_time=2.0)
            self.play(FadeIn(names[1]))
            vo.wait_until("d")
            self.play(Create(lines[2], rate_func=linear), run_time=2.0)
            self.play(FadeIn(names[2]), FadeIn(moral))
        self.clear_scene()
