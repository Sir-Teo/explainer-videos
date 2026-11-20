from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.resumes()
        self.callbacks()
        self.question()
        self.title()
        self.objectives()

    def resumes(self):
        R = load("resume")
        names = (("Emily", WHITE_N), ("Greg", WHITE_N), ("Lakisha", BLACK_N), ("Jamal", BLACK_N))
        cards = VGroup()
        for nm, col in names:
            box = RoundedRectangle(width=2.5, height=3.2, corner_radius=0.08, stroke_color=col, stroke_width=2.5,
                                   fill_color="#141821", fill_opacity=1)
            head = label(nm, font_size=30, color=col).move_to(box.get_top() + DOWN * 0.45)
            lines = VGroup(*[Line(LEFT * 0.9, RIGHT * (0.9 - 0.35 * (k % 3) / 2), stroke_width=3, color=GREY_D)
                             for k in range(7)]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(head, DOWN,
                                                                                                        buff=0.35)
            cards.add(VGroup(box, head, lines))
        cards.arrange(RIGHT, buff=0.45).move_to(UP * 0.4)
        same = label(r"the same r\'esum\'e, \ only the name differs", font_size=24, color=GREY_A).next_to(cards, DOWN,
                                                                                                        buff=0.45)
        facts = VGroup(
            label(rf"Boston and Chicago, \ 2001--02: \ {R['ads']:,} advertisements, \ {R['n']:,} r\'esum\'es",
                  font_size=24, color=WHITE),
            label(r"names chosen to sound White or African American, \ assigned at random", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        tag = data_tag(r"Bertrand and Mullainathan (2004), \ via openintro", corner=DR, font_size=12)
        with self.voiceover(
            "In 2001 and 2002, two economists, Marianne Bertrand and Sendhil Mullainathan, answered help-wanted "
            "advertisements in Boston and Chicago newspapers with invented résumés. <bookmark mark='a'/> Some were "
            "headed Emily or Greg, <bookmark mark='b'/> others Lakisha or Jamal: names chosen because they sound "
            "White or African American. <bookmark mark='c'/> Apart from the name, the résumés were alike, and which "
            f"name went on which résumé was decided at random. <bookmark mark='d'/> In all they sent {R['n']:,} "
            f"résumés to {R['ads']:,} advertisements, and waited for the telephone."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(c[0]) for c in cards], lag_ratio=0.15), run_time=1.5)
            self.play(LaggedStart(*[Create(c[2]) for c in cards], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(cards[0][1]), FadeIn(cards[1][1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2][1]), FadeIn(cards[3][1]))
            vo.wait_until("c")
            self.play(FadeIn(same))
            vo.wait_until("d")
            self.play(FadeIn(facts, shift=UP * 0.15))
        self.clear_scene()

    def callbacks(self):
        R = load("resume")
        nw, kw = R["white"][1], R["white"][2]
        nb, kb = R["black"][1], R["black"][2]
        cols, size = 55, 0.075

        def grid(n, k, col, center):
            g = VGroup(*[Square(side_length=size, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
                         for _ in range(n)])
            g.arrange_in_grid(cols=cols, buff=0.025).move_to(center)
            rng = np.random.default_rng(len(col) + n)
            lit = VGroup(*[g[i] for i in sorted(rng.choice(n, k, replace=False))])
            return g, lit
        gw, lw = grid(nw, kw, WHITE_N, LEFT * 3.5 + DOWN * 0.35)
        gb, lb = grid(nb, kb, BLACK_N, RIGHT * 3.5 + DOWN * 0.35)
        hw = label(rf"White-sounding names: \ {nw:,} r\'esum\'es", font_size=24, color=WHITE_N).next_to(gw, UP,
                                                                                                    buff=0.3)
        hb = label(rf"African-American-sounding: \ {nb:,}", font_size=24, color=BLACK_N).next_to(gb, UP, buff=0.3)
        rw = label(rf"{kw} call-backs: \ {100 * R['white'][0]:.2f}\% \ (one in {R['per_white']:.1f})", font_size=24,
                   color=WHITE_N).next_to(gw, DOWN, buff=0.3)
        rb = label(rf"{kb} call-backs: \ {100 * R['black'][0]:.2f}\% \ (one in {R['per_black']:.1f})", font_size=24,
                   color=BLACK_N).next_to(gb, DOWN, buff=0.3)
        ratio = label(rf"{100 * (R['ratio'] - 1):.0f}\% more call-backs for White names \ (95\% interval "
                      rf"{100 * (R['lo'] - 1):.0f} to {100 * (R['hi'] - 1):.0f}\%)", font_size=26,
                      color=E.ACCENT).to_edge(UP, buff=0.35)
        tag = data_tag(r"Bertrand and Mullainathan (2004), \ via openintro; \ recomputed", corner=DR, font_size=12)
        with self.voiceover(
            "Here is every résumé, one square each. <bookmark mark='a'/> Of the résumés with White-sounding names, "
            f"{kw} were called back, {100 * R['white'][0]:.1f} percent, about one in ten. <bookmark mark='b'/> Of "
            f"those with African-American-sounding names, {kb}, {100 * R['black'][0]:.1f} percent, about one in "
            f"fifteen. <bookmark mark='c'/> The same résumés, with names randomly assigned: White names received "
            f"{say_num(100 * (R['ratio'] - 1), 0)} percent more call-backs, a difference far too large to be chance."
        ) as vo:
            self.play(FadeIn(gw, lag_ratio=0.0005), FadeIn(gb, lag_ratio=0.0005), FadeIn(hw), FadeIn(hb), FadeIn(tag),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[sq.animate.set_fill(WHITE_N, 1) for sq in lw], lag_ratio=0.01), FadeIn(rw),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[sq.animate.set_fill(BLACK_N, 1) for sq in lb], lag_ratio=0.01), FadeIn(rb),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(ratio, shift=DOWN * 0.15))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why did the college premium rise, \ and why has it stalled?", font_size=26, color=COLLEGE),
            label(r"what did computers and robots do to the middle?", font_size=26, color=MIDS),
            label(r"how much of your pay is your employer, \ your union, \ your job's risks?", font_size=26,
                  color=FIRM),
            label(r"what is discrimination, \ and how can it be measured?", font_size=26, color=BLACK_N),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "That is one gap, measured cleanly. This part asks the larger question: why are some people paid so much "
            "more than others, and how much of the gap is unfair? <bookmark mark='a'/> Why did the reward for a "
            "college degree rise, and why has it stalled? <bookmark mark='b'/> What did computers and robots do to "
            "the jobs in the middle? <bookmark mark='c'/> How much of a person's pay is their employer, their union, "
            "the risks of their job? <bookmark mark='d'/> And what is discrimination, and how can anyone measure it?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1979, 2025], [1.3, 1.9], x_length=4.2, y_length=1.4)
        logo = path(mini, F["t"], F["v"], COLLEGE, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 39 \ $\cdot$ \ The Wage Structure", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirty-nine: the wage structure."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VIII \ $\cdot$ \ Work and the State", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the wage distribution since 1979; \ the race between education and technology",
            r"a game; \ tasks, \ polarization and robots",
            r"firms, \ superstars and unions; \ the price of a job's risks",
            r"discrimination in theory and measured; \ the gender gap and the child penalty",
            r"three dials; \ pay audits; \ transparency and algorithms",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> How the wage distribution has moved since 1979, and the race "
            "between education and technology. <bookmark mark='b'/> A game, and then tasks, polarization and "
            "robots. <bookmark mark='c'/> Firms, superstars and unions, and the price of a job's risks. "
            "<bookmark mark='d'/> Discrimination, in theory and measured, and the gender gap. <bookmark mark='e'/> "
            "Three dials, pay audits, and the frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
