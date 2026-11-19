from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403

NAMES = {"bo": "Bo", "ana": "Ana", "chidi": "Chidi", "dara": "Dara"}


class Revealed(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Revealed preference", r"When do choices contradict each other?",
             "Chapter seven. Revealed preference.")
        self.receipts()
        self.chains()
        self.islanders()
        self.afriat()

    def receipts(self):
        r = load("receipts")
        P, X = np.array(r["P"]), np.array(r["X"])
        ax = goods_axes(center=LEFT * 3.0 + DOWN * 0.25, top=19, ticks=(0, 6, 12, 18), x_length=5.0, y_length=5.0)
        a = ax.ax
        cols = (BUDGET, GREY_B, "#F28C6F")
        lines, dots = VGroup(), VGroup()
        for k in (0, 2):
            m = P[k] @ X[k]
            lines.add(budget_line(ax, m / P[k, 0], m / P[k, 1], color=cols[k]))
            dots.add(Dot(a.c2p(*X[k]), radius=0.11, color=cols[k]))
        dl = VGroup(label(r"week 1", font_size=19, color=cols[0]).next_to(dots[0], UR, buff=0.05),
                    label(r"week 3", font_size=19, color=cols[2]).next_to(dots[1], DR, buff=0.05))
        rows = VGroup(
            label(r"week 1: \ fish \$4, coconuts \$3: \ he chose 3 fish, 8 coconuts", font_size=22, color=cols[0]),
            label(r"week 3's bundle (4, 6) cost only \$34 at week 1's prices: \\ affordable, \ and not chosen",
                  font_size=21),
            label(r"week 3: \ fish \$6, coconuts \$2: \ he chose 4 fish, 6 coconuts", font_size=22, color=cols[2]),
            label(r"week 1's bundle (3, 8) cost only \$34 at week 3's prices: \\ affordable, \ and not chosen",
                  font_size=21),
            label(r"each was chosen when the other was cheaper: \\ the weak axiom of revealed preference fails",
                  font_size=23, color=VIOL),
            label(rf"shrink week 1's budget to {100 * r['ccei']:.1f}\% \ (\$34 of \$36) \ and the clash goes: \\ "
                  rf"at worst, \ {100 * (1 - r['ccei']):.1f}\% of a week's money was wasted", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"simulated: Bo's receipts, from the opening", corner=DR, font_size=13)
        with self.voiceover(
            "Back to Bo's receipts. Is he consistent? <bookmark mark='a'/> In week one fish cost four dollars and "
            "coconuts three. He bought three fish and eight coconuts. <bookmark mark='b'/> But the bundle he bought "
            "in week three, four fish and six coconuts, would have cost him only thirty-four dollars at week one's "
            "prices. He could have had it, and chose otherwise. So, as Samuelson put it, he revealed that he "
            "prefers week one's bundle. <bookmark mark='c'/> In week three fish cost six and coconuts two, and he "
            "bought four fish and six coconuts. <bookmark mark='d'/> Yet week one's bundle would have cost him "
            "thirty-four dollars then. <bookmark mark='e'/> Each bundle was chosen when the other was affordable and "
            "cheaper. No single ranking can do that. This is Samuelson's weak axiom of revealed preference, and Bo "
            "breaks it. <bookmark mark='f'/> How badly? Shrink week one's budget to thirty-four dollars of its "
            "thirty-six, and week three's bundle is no longer affordable then: the contradiction disappears. At "
            "worst Bo wasted five and a half percent of a week's money."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(dots[0], scale=1.5), FadeIn(dl[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots[1].copy().set_opacity(0.5)), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lines[1]), FadeIn(dots[1], scale=1.5), FadeIn(dl[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Indicate(dots[0], color=cols[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            shrunk = budget_line(ax, 34 / P[0, 0], 34 / P[0, 1], color=cols[0], opacity=0.6)
            self.play(Transform(lines[0].copy(), shrunk), FadeIn(rows[5]))
        self.clear_scene()

    def chains(self):
        nodes = VGroup()
        names = (r"x_1", r"x_2", r"x_3")
        pos = (LEFT * 4.5 + UP * 0.6, LEFT * 1.6 + UP * 0.6, LEFT * 3.05 + DOWN * 1.6)
        for nm, p_ in zip(names, pos):
            c = Circle(radius=0.45, stroke_color=GREY_B, stroke_width=2.5).move_to(p_)
            nodes.add(VGroup(c, MathTex(nm, font_size=34).move_to(c)))
        arr = VGroup(Arrow(pos[0], pos[1], buff=0.5, color=GREY_B, stroke_width=3),
                     Arrow(pos[1], pos[2], buff=0.5, color=GREY_B, stroke_width=3),
                     Arrow(pos[2], pos[0], buff=0.5, color=VIOL, stroke_width=3))
        rows = VGroup(
            label(r"Samuelson (1938), WARP: \ no two choices \\ that each reveal the other worse", font_size=23),
            label(r"Houthakker (1950), SARP: \ no chains either: \\ $x_1$ over $x_2$, $x_2$ over $x_3$, \ then "
                  r"$x_3$ over $x_1$", font_size=23, color=E.ACCENT),
            label(r"GARP (Afriat 1967; named by Varian 1982): \\ the same, \ allowing ties, \ so flat stretches "
                  r"\\ of indifference are no crime", font_size=23, color=PASS),
            label(r"one comparison is easy; \ the chains make it a graph \\ problem: \ Warshall's algorithm finds "
                  r"them all", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        tag = published_tag(r"Samuelson (1938); Houthakker, Economica 17 (1950); Afriat, IER 8 (1967); Varian, "
                            r"Econometrica 50 (1982)", corner=DR, font_size=12)
        with self.voiceover(
            "Two choices can contradict each other directly. More can contradict each other in a chain. "
            "<bookmark mark='a'/> Samuelson's weak axiom only forbids the pair. <bookmark mark='b'/> In 1950 "
            "Hendrik Houthakker added the strong axiom: if one bundle is revealed better than a second, and the "
            "second better than a third, the third must not be revealed better than the first. "
            "<bookmark mark='c'/> Sidney Afriat's version, which Hal Varian named the generalized axiom, GARP, "
            "allows for ties, so someone indifferent between two bundles isn't accused of anything. "
            "<bookmark mark='d'/> With eleven choices there are many possible chains. A computer finds them all "
            "with an algorithm from graph theory, Stephen Warshall's, in a fraction of a second."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(n_) for n_ in nodes], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arr[0]), GrowArrow(arr[1]))
            self.play(GrowArrow(arr[2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def islanders(self):
        ch = load("choosers")
        L = np.array(load("budgets")["lines"])
        panels = VGroup()
        for who in ("bo", "ana", "chidi", "dara"):
            ax = goods_axes(top=13, x_length=2.7, y_length=2.7, font_size=14, xlabel=r"", ylabel=r"",
                            ticks=(0, 6, 12))
            a = ax.ax
            ls = VGroup(*[budget_line(ax, A, B, color=GREY_D, width=1.5) for A, B in L])
            X = np.array(ch[who]["X"])
            bad = {i for pair in ch[who]["violations"] for i in pair}
            ds = VGroup(*[Dot(a.c2p(*x), radius=0.06, color=VIOL if i in bad else WHO[who])
                          for i, x in enumerate(X)])
            ok = ch[who]["ccei"] >= 1.0
            verdict = label((r"passes GARP" if ok else rf"fails: \ {len(bad)} choices in cycles, \\ CCEI "
                             rf"{ch[who]['ccei']:.3f}"), font_size=17, color=PASS if ok else VIOL)
            t = label(NAMES[who], font_size=24, color=WHO[who])
            panels.add(VGroup(t, VGroup(ax, ls, ds), verdict).arrange(DOWN, buff=0.12))
        panels.arrange(RIGHT, buff=0.35).move_to(DOWN * 0.2)
        if panels.width > 13.4:
            panels.width = 13.4
        desc = VGroup(label(r"Cobb--Douglas, \ with a tremble", font_size=15, color=GREY_B),
                      label(r"one fish per coconut", font_size=15, color=GREY_B),
                      label(r"all on the cheaper good", font_size=15, color=GREY_B),
                      label(r"a point at random", font_size=15, color=GREY_B))
        for d_, p_ in zip(desc, panels):
            d_.next_to(p_[0], DOWN, buff=0.04)
        tag = island_tag(r"simulated: four islanders on the eleven lines of Play it", corner=DR, font_size=13)
        head = label(r"Four islanders, \ the same eleven lines", font_size=32).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Now let four islanders shop on the eleven lines you saw in Play it. <bookmark mark='a'/> Bo spends "
            "about sixty percent on fish, with a small random tremble each time. His choices pass. Trembles that "
            "small don't create a contradiction. <bookmark mark='b'/> Ana always buys fish and coconuts one for one. "
            "Her choices pass. <bookmark mark='c'/> Chidi spends everything on whichever good is cheaper for him: "
            "all corners, and they pass too. Rational choices can look very different from each other. "
            "<bookmark mark='d'/> Dara, on a distracted day, picks a point at random on each line. Her choices "
            f"fall into cycles: {len({i for p in ch['dara']['violations'] for i in p})} of her eleven choices are "
            "caught in contradictions. Yet her efficiency index is "
            f"{ch['dara']['ccei']:.2f}: shrinking her budgets by under five percent removes them. Keep that in "
            "mind. It means a high score alone doesn't prove much."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            for mk, p_, d_ in zip("abcd", panels, desc):
                vo.wait_until(mk)
                self.play(FadeIn(p_, shift=UP * 0.15), FadeIn(d_))
        self.clear_scene()

    def afriat(self):
        ch = load("choosers")
        L = np.array(load("budgets")["lines"])
        bo = ch["bo"]
        X = np.array(bo["X"])
        af = bo["afriat"]
        ax = goods_axes(center=LEFT * 3.0 + DOWN * 0.25, top=13, x_length=5.2, y_length=5.2)
        a = ax.ax
        ls = VGroup(*[budget_line(ax, A, B, color=GREY_D, width=1.5) for A, B in L])
        ds = VGroup(*[Dot(a.c2p(*x), radius=0.07, color=WHO["bo"]) for x in X])
        xs = np.array(af["xs"])
        ics = VGroup(*[VMobject(stroke_color=IC, stroke_width=3).set_points_as_corners(
            [a.c2p(x, y) for x, y in zip(xs, np.array(ys)) if np.isfinite(y) and y <= 13])
            for ys in af["curves"].values()])
        eqs = VGroup(
            label(r"Afriat (1967): \ the choices satisfy GARP \\ if and only if numbers $U_i$, $\lambda_i > 0$ "
                  r"exist with", font_size=22, color=E.ACCENT),
            MathTex(r"U_j \le U_i + \lambda_i\, p_i\cdot(x_j - x_i)\quad \text{for all } i, j", font_size=32),
            label(r"a linear programme: \ $11 \times 10$ inequalities", font_size=21, color=GREY_A),
            MathTex(r"u(x) = \min_i \big[\,U_i + \lambda_i\, p_i\cdot(x - x_i)\,\big]", font_size=32, color=IC),
            label(r"concave, increasing, and on every budget \\ it is maximized at the bundle chosen", font_size=21),
            label(r"a test that runs on a receipt: \\ consistent choices are exactly utility maximization",
                  font_size=23, color=PASS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Why does GARP matter so much? Because of a theorem Sidney Afriat proved in 1967. "
            "<bookmark mark='a'/> If a list of choices satisfies GARP, there's a utility function that explains "
            "every one of them, and if it doesn't, there isn't. To find it, look for numbers, one utility level and "
            "one multiplier per choice, satisfying a set of inequalities. <bookmark mark='b'/> That's a linear "
            "programme: a computer solves Bo's hundred and ten inequalities instantly. <bookmark mark='c'/> The "
            "solution builds a utility function out of flat pieces. <bookmark mark='d'/> Here are three of its "
            "indifference curves through Bo's choices. On every one of his eleven budgets, the bundle he chose is "
            "the best he could afford, by this utility. <bookmark mark='e'/> So Samuelson's programme succeeds. "
            "Rationality, in the economist's sense, is nothing more and nothing less than consistency, and "
            "consistency can be checked on a receipt."
        ) as vo:
            self.play(FadeIn(ax), LaggedStart(*[Create(l_) for l_ in ls], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in ds], lag_ratio=0.05), FadeIn(eqs[0]))
            vo.wait_until("a")
            self.play(Write(eqs[1]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[2]))
            vo.wait_until("c")
            self.play(Write(eqs[3]), FadeIn(eqs[4]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(c_) for c_ in ics], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(eqs[5]))
        self.clear_scene()
