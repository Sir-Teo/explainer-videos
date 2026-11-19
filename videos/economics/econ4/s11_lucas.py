from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403

SIXTIES = "#5DADEC"
SEVENTIES = "#F28C6F"
CALM = "#9AA5B8"
PUSH = "#F2B84B"


class Lucas(VoiceoverScene):
    def construct(self):
        card(self, 9, r"The Lucas critique", r"Will a pattern in the past hold once policy leans on it?",
             "Chapter nine. The Lucas critique.", lit=("government", "banks"), scale=("nation",),
             horizon=("a decade",))
        self.menu()
        self.island()
        self.critique()

    def menu(self):
        ph = load("phillips")
        ax = axes([2, 10], [0, 12], x_length=6.4, y_length=4.8, xticks=[3, 5, 7, 9], yticks=[0, 4, 8, 12],
                  xlabel=r"unemployment, \%", ylabel=r"inflation, \%", font_size=20, center=LEFT * 2.6 + DOWN * 0.2)
        a = ax.ax
        pts = [a.c2p(u, p) for u, p in zip(ph["u"], ph["pi"])]
        years = ph["years"]
        i70 = years.index(1970)
        dots60 = VGroup(*[Dot(p, radius=0.07, color=SIXTIES) for p in pts[:i70]])
        path60 = VMobject(stroke_color=SIXTIES, stroke_width=2.5).set_points_as_corners(pts[:i70])
        dots70 = VGroup(*[Dot(p, radius=0.07, color=SEVENTIES) for p in pts[i70:]])
        path70 = VMobject(stroke_color=SEVENTIES, stroke_width=2.5).set_points_as_corners(pts[i70 - 1:])
        yl = VGroup()
        for y, p in zip(years, pts):
            if y in (1961, 1969, 1975, 1979):
                d = {1961: DOWN, 1969: LEFT, 1975: RIGHT, 1979: UP}[y]
                yl.add(label(str(y), font_size=18, color=SIXTIES if y < 1970 else SEVENTIES).next_to(p, d, buff=0.1))
        rows = VGroup(
            label(r"the 1960s: \ less unemployment, \\ more inflation", font_size=25, color=SIXTIES),
            label(r"Samuelson and Solow, 1960: \ a ``menu of choice''", font_size=24, color=GREY_A),
            label(r"Friedman (1968), Phelps (1967): \\ once people expect the inflation, \\ it buys nothing",
                  font_size=24, color=E.ACCENT),
            label(r"the 1970s: \ both rose together", font_size=25, color=SEVENTIES),
            label(r"the whole story: \ Part 28", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45).shift(UP * 0.3)
        tag = data_tag(rf"BLS unemployment rate and CPI-U, annual averages ({ph['cite']})", corner=DL, font_size=14)
        with self.voiceover(
            "The last warning in this part is about time. <bookmark mark='a'/> Through the 1960s, American "
            "unemployment and inflation moved like a seesaw: as unemployment fell, year by year, inflation rose. "
            "<bookmark mark='b'/> In 1960 Paul Samuelson and Robert Solow had called such a curve a menu of choice: "
            "pick less unemployment, and pay for it in inflation. <bookmark mark='c'/> Milton Friedman and Edmund "
            "Phelps argued that the menu would vanish as soon as anyone ordered from it. Once people came to expect "
            "the inflation, they'd build it into their wages and prices, and it would buy nothing. "
            "<bookmark mark='d'/> The 1970s proved them right. Inflation and unemployment rose together. "
            "<bookmark mark='e'/> Part 28 tells that story in full. Here the question is what it means for "
            "evidence."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(path60), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots60], lag_ratio=0.2),
                      FadeIn(yl[0]), FadeIn(yl[1]), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(path70), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots70], lag_ratio=0.2),
                      FadeIn(yl[2:]), FadeIn(rows[3]), run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def island(self):
        L = load("lucas")
        pi, y, E_, calm = (np.array(L[k]) for k in ("pi", "y", "expected", "calm"))
        calm = calm.astype(bool)
        T1 = int(calm.sum())
        ax = axes([-2, 10], [96, 107], x_length=5.6, y_length=4.4, xticks=[0, 2, 4, 6, 8], yticks=[97, 100, 103, 106],
                  xlabel=r"inflation, \%", ylabel=r"output \ ($y^\ast = 100$)", font_size=19,
                  center=LEFT * 3.4 + DOWN * 0.35)
        a = ax.ax
        cd = VGroup(*[Dot(a.c2p(p, v), radius=0.06, color=CALM) for p, v in zip(pi[calm], y[calm])])
        b0, b1 = L["calm_intercept"], L["calm_slope"]
        fit = Line(a.c2p(-1.8, b0 + b1 * -1.8), a.c2p(9.6, b0 + b1 * 9.6), color=OLSC, stroke_width=3.5)
        pred = Dot(a.c2p(L["pi_push"], L["predicted_y_at_push"]), radius=0.1, color=OLSC)
        pl = label(rf"the menu says {L['predicted_y_at_push']:.1f}", font_size=20, color=OLSC).next_to(pred, LEFT,
                                                                                                      buff=0.15)
        pd = [Dot(a.c2p(p, v), radius=0.065, color=PUSH) for p, v in zip(pi[~calm], y[~calm])]
        star = DashedLine(a.c2p(-2, 100), a.c2p(10, 100), color=E.TRUTH, stroke_width=2)
        # inflation and what the islanders expect, year by year
        tx = axes([0, 50], [-2, 10], x_length=5.2, y_length=2.6, xticks=[0, 10, 20, 30, 40, 50], yticks=[0, 4, 8],
                  xlabel=r"year", ylabel=r"inflation, \%", font_size=17, center=RIGHT * 3.6 + UP * 1.35)
        t_ = tx.ax
        act = VMobject(stroke_color=GREY_A, stroke_width=2.5).set_points_as_corners(
            [t_.c2p(k + 0.5, p) for k, p in enumerate(pi)])
        exp = VMobject(stroke_color=PUSH, stroke_width=3.5).set_points_as_corners(
            [t_.c2p(k + 0.5, e) for k, e in enumerate(E_)])
        tkey = VGroup(label(r"actual", font_size=17, color=GREY_A), label(r"expected", font_size=17, color=PUSH)
                      ).arrange(RIGHT, buff=0.3).next_to(tx, UP, buff=0.05)
        push_line = DashedLine(t_.c2p(T1, -2), t_.c2p(T1, 10), color=GREY_C, stroke_width=1.5)
        rows = VGroup(
            label(rf"first year of the push: \ output {L['y_push_first']:.1f}", font_size=22, color=PUSH),
            label(rf"its last ten years: \ {L['y_push_last']:.1f}", font_size=22, color=PUSH),
            label(r"only a surprise moves output, \\ and a policy that repeats \\ stops being a surprise",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tx, DOWN, buff=0.75).align_to(tx, LEFT)
        tag = island_tag(r"simulated: the Island; output responds only to inflation it did not expect "
                         r"(expectations adapt)", corner=DR, font_size=13)
        with self.voiceover(
            "Here is the same thing on the Island, where we know the rules. <bookmark mark='a'/> For thirty years "
            "the Island's council left inflation to chance. In years when prices rose faster than people expected, "
            "fishers mistook higher prices for better demand and worked harder, so output rose. Collect the "
            f"thirty years, and a statistician finds a reliable pattern: <bookmark mark='b'/> each point of "
            f"inflation goes with {b1:.2f} points of extra output. <bookmark mark='c'/> The council reads this as a "
            f"menu. Hold inflation at {L['pi_push']:.0f} percent, and output should reach "
            f"{L['predicted_y_at_push']:.0f}. <bookmark mark='d'/> So it tries. The first year works: output jumps. "
            "Then it falls back, year after year, to where it started. <bookmark mark='e'/> The reason is in "
            "people's heads. The islanders learn to expect eight percent, and once they expect it, it fools no one. "
            "<bookmark mark='f'/> Nothing in the thirty calm years was wrong. The pattern was real. It just "
            "described how people behaved under one policy, and the council changed the policy."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(star))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in cd], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(fit))
            vo.wait_until("c")
            self.play(FadeIn(pred, scale=1.5), FadeIn(pl))
            vo.wait_until("d")
            self.play(FadeIn(tx), FadeIn(tkey), FadeIn(push_line), Create(act), run_time=1.5)
            self.play(FadeIn(pd[0], scale=1.6), FadeIn(rows[0]))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in pd[1:]], lag_ratio=0.25), run_time=3.5)
            vo.wait_until("e")
            self.play(Create(exp, run_time=3.0), FadeIn(rows[1]))
            vo.wait_until("f")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def critique(self):
        t = tables.LUCAS_1976.data
        who = history_card(r"1976", r"Robert Lucas, ``Econometric Policy Evaluation: A Critique''",
                           r"the Carnegie-Rochester conference; Nobel prize, 1995", color=E.ACCENT, width=7.4,
                           font_size=24)
        who.to_edge(UP, buff=0.45)
        q = quote_card(t["quote"], r"Lucas (1976), p.\ 41", width=11.8, font_size=27, color=E.ACCENT)
        q.next_to(who, DOWN, buff=0.35)
        rows = VGroup(
            label(r"what moves: \ patterns that summarize behaviour under one policy", font_size=24, color=PUSH),
            label(r"what may not: \ tastes, technology, how people form expectations \ (``deep'' parameters)",
                  font_size=24, color=E.TRUTH),
            label(r"Haavelmo's word for a relation that survives a change of regime: \ \emph{autonomous}",
                  font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(q, DOWN, buff=0.35)
        tag = published_tag(r"Lucas, Carnegie-Rochester Conference Series 1 (1976); Haavelmo (1944), ch.\ II",
                            corner=DR, font_size=13)
        with self.voiceover(
            "In 1976 Robert Lucas turned this into a principle that changed macroeconomics. <bookmark mark='a'/> "
            "The relations in an econometric model, he argued, are summaries of people's decisions; their "
            "decisions depend on the policies they expect; <bookmark mark='b'/> so any change in policy will "
            "systematically alter the structure of econometric models. <bookmark mark='c'/> What moves are the "
            "patterns that summarize behaviour under one policy. <bookmark mark='d'/> What may stay put are the "
            "things underneath: what people want, what technology allows, how they form their expectations. "
            "<bookmark mark='e'/> Haavelmo had a word for relations that survive a change of regime: autonomous. "
            "The search for them is the subject of the next chapter."
        ) as vo:
            self.play(FadeIn(who, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(q, color=E.ACCENT, scale_factor=1.02))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
