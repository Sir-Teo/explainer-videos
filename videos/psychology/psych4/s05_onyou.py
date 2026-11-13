from __future__ import annotations

from videos.psychology.psych4.common import *  # noqa: F403

CHOICE = [(r"Which outcome?", r"reaction time", r"error rate"),
          (r"Outliers?", r"keep everyone", r"drop anyone beyond 2.5 SD"),
          (r"Adjust for age?", r"no", r"yes"),
          (r"More people?", r"stop at 20 a group", r"add 10 a group")]


class OnYou(VoiceoverScene):
    def construct(self):
        self.card()
        self.exercise()
        self.reveal()
        self.rates()

    def card(self):
        card = chapter_card(4, r"On you: \ the garden of forking paths", r"Can you make nothing significant, "
                            r"without cheating?", lit={2011: r"``False-positive psychology''"}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter four. On you: the garden of forking paths."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _rows(self, d, picked=None):
        """The four choices as rows of two options; ``picked`` marks one option per row."""
        rows = VGroup()
        for i, (q, a, b) in enumerate(CHOICE):
            ql = label(q, font_size=28, color=GREY_A)
            opts = VGroup()
            for j, t in enumerate((a, b)):
                on = picked is not None and picked[i] == j
                txt = label(t, font_size=26, color=WHITE if on or picked is None else GREY_C)
                box = SurroundingRectangle(txt, buff=0.14, corner_radius=0.08, stroke_width=3 if on else 1.5,
                                           color=(SIG if on else GREY_D))
                opts.add(VGroup(box, txt))
            opts.arrange(RIGHT, buff=0.3)
            rows.add(VGroup(ql, opts))
        for r in rows:
            r[0].move_to([-6.3, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-3.6, 0, 0], aligned_edge=LEFT)
        rows.arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        return rows

    def exercise(self):
        d = load("forking")
        stage = demo_stage(13.2, 6.4, tag=r"On you", center=[0, -0.15, 0])
        setup = wrapped_label(r"A study of a game that does nothing: \ two groups, 20 people each, with a "
                              r"reaction time, an error rate and an age for every person. \ The plan was the "
                              r"left-hand option of each row.", 11.6, 27, WHITE).move_to([0, 2.1, 0])
        rows = self._rows(d).move_to([-1.2, -0.15, 0])
        plan = VGroup(label(r"the plan", font_size=26, color=GREY_A),
                      label(rf"$p = {r2(d['planned_p'])}$", font_size=56, color=NULLC)).arrange(DOWN, buff=0.1)
        plan.move_to([4.6, 0.35, 0])
        ask = label(r"Change as few rows as you like. \ Which changes would you try first?", font_size=28,
                    color=P.ACCENT).move_to([-0.9, -2.75, 0])
        ring = countdown_ring(0.36).move_to([5.6, -2.75, 0])
        with self.voiceover(
            "Your turn. Here's a study of a game that does nothing; in the simulation we made sure of that. "
            "<bookmark mark='a'/> Two groups of twenty. For each person there's a reaction time, an error rate, "
            "and their age. Before looking, the plan was to compare reaction times, keep everyone, make no "
            f"adjustment, and stop at twenty. <bookmark mark='b'/> That analysis gives p of "
            f"{d['planned_p']:.2f}. Nothing. Which is the right answer. <bookmark mark='c'/> But suppose you'd "
            "spent a year on this. Look at the four rows. Every option on the right is something a careful "
            "researcher might do, and could defend. Errors are a reasonable measure of performance. Dropping "
            "extreme scores is standard. Age does affect reaction time. And twenty a group is on the small "
            "side. <bookmark mark='d'/> So: which would you try first?"
        ) as vo:
            self.play(FadeIn(stage), FadeIn(setup))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(plan, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(ask), FadeIn(ring))
        self.play(ring.t.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        d = load("forking")
        head = heading(r"Sixteen analyses of one dataset")
        keys, ps = d["keys"], d["ps"]
        # a 4 x 4 grid: rows by (measure, outliers), columns by (covariate, more)
        cell = 1.22
        grid = VGroup()
        for k, p in zip(keys, ps):
            r, c = 2 * k[0] + k[1], 2 * k[2] + k[3]
            sq = Square(cell, stroke_color=BACKGROUND, stroke_width=3, fill_color=(SIG if p < 0.05 else "#1B2333"),
                        fill_opacity=1).move_to([c * cell, -r * cell, 0])
            txt = label(p_text(p) if p < 0.995 else r"1.00", font_size=28, color=(BLACK if p < 0.05 else GREY_A))
            txt.move_to(sq)
            grid.add(VGroup(sq, txt))
        grid.move_to([-1.95, -0.7, 0])
        left, top = grid.get_left()[0], grid.get_top()[1]
        rl = VGroup(*[label(t, font_size=22, color=GREY_A) for t in (
            r"reaction time", r"\dots\ outliers dropped", r"error rate", r"\dots\ outliers dropped")])
        for i, t in enumerate(rl):
            t.next_to([left, top - (i + 0.5) * cell, 0], LEFT, buff=0.15)
        cl = VGroup(*[label(t, font_size=22, color=GREY_A) for t in (r"as planned", r"$+10$", r"age", r"age, $+10$")])
        for j, t in enumerate(cl):
            t.next_to([left + (j + 0.5) * cell, top, 0], UP, buff=0.12)
        plan_box = SurroundingRectangle(grid[keys.index([0, 0, 0, 0])][0], color=WHITE, buff=0, stroke_width=4)
        best_box = SurroundingRectangle(grid[keys.index(d["best"])][0], color=WHITE, buff=0, stroke_width=4)
        side = VGroup(
            label(rf"the plan: \ $p = {r2(d['planned_p'])}$", font_size=30, color=NULLC),
            label(rf"{d['significant_paths']} of the 16 analyses give $p < .05$", font_size=30, color=SIG),
            wrapped_label(rf"the best: \ error rate, adjusted for age: \ $p = {p_text(d['best_p'])}$, an effect "
                          rf"of {r2(abs(d['best_d']))} SD", 4.9, 28, WHITE),
            wrapped_label(r"Written up, it reads: ``the game reduced errors, controlling for age.'' \ Every word "
                          r"is true. \ The game does nothing.", 4.9, 27, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, -0.4, 0])
        keep_in_frame(VGroup(grid, rl, cl))
        tag = note(rf"simulated: dataset {d['seed']}, the first in which the plan fails and another analysis "
                   r"succeeds").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here are all sixteen ways through those four choices, with the p-value each one gives. "
            f"<bookmark mark='a'/> Top left is the plan: {d['planned_p']:.2f}. <bookmark mark='b'/> "
            f"{d['significant_paths']} of the sixteen come out below point oh five. If you switched the outcome "
            "from reaction time to errors, you found one. <bookmark mark='c'/> The best of them: errors, "
            f"adjusted for age, p of {d['best_p']:.2f}, and an effect of {abs(d['best_d']):.1f} standard "
            "deviations, which would count as large. <bookmark mark='d'/> And you could write that up without a "
            "single false statement. The game reduced errors, controlling for age. Every word is true. And the "
            "game does nothing; we built it that way. Notice what you did not do. You didn't invent data. You "
            "didn't hide a failed experiment. You made reasonable choices, after seeing which way each one "
            "pointed. The data were allowed to pick the analysis, and an analysis picked by the data will find "
            "what the data happen to contain, which is noise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid, lag_ratio=0.04), FadeIn(rl), FadeIn(cl), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(plan_box), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(ReplacementTransform(plan_box, best_box), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def rates(self):
        d = load("forking")
        r, s = d["rates"], d["sns"]
        head = heading(r"How often does a study of nothing ``find'' something?")
        unit = 9.0
        names = [r"the plan, and nothing else", r"\dots\ or the other outcome", r"\dots\ or dropping outliers",
                 r"\dots\ or adjusting for age", r"\dots\ or ten more people", r"all four choices open"]
        vals = [r["planned"], *r["single"], r["any"]]
        cols = [NULLC, GREY_B, GREY_B, GREY_B, GREY_B, SIG]
        rows = VGroup()
        for i, (n_, v, c) in enumerate(zip(names, vals, cols)):
            y = 1.75 - 0.6 * i
            bar = Rectangle(width=max(unit * v, 0.02), height=0.36, stroke_width=0, fill_color=c, fill_opacity=0.9)
            bar.move_to([-1.9 + unit * v / 2, y, 0])
            nm = label(n_, font_size=24, color=WHITE).next_to([-1.9, y, 0], LEFT, buff=0.2)
            val = label(pct(v), font_size=26, color=c).next_to(bar, RIGHT, buff=0.15)
            rows.add(VGroup(nm, bar, val))
        y = 1.75 - 0.6 * 6 - 0.45
        sbar = Rectangle(width=unit * s["ABCD"], height=0.44, stroke_width=0, fill_color=BAD, fill_opacity=0.9)
        sbar.move_to([-1.9 + unit * s["ABCD"] / 2, y, 0])
        snm = VGroup(label(r"four stronger choices", font_size=24, color=WHITE),
                     label(r"(Simmons, Nelson and Simonsohn)", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.05)
        snm.next_to([-1.9, y, 0], LEFT, buff=0.2)
        sval = label(rf"{pct(s['ABCD'])} \ (published: {pct(d['sns_published'], 1)})", font_size=26, color=BAD)
        sval.next_to(sbar, RIGHT, buff=0.15)
        keep_in_frame(sval)
        five = DashedLine([-1.9 + unit * 0.05, 2.1, 0], [-1.9 + unit * 0.05, y - 0.35, 0], color=NULLC, stroke_width=2)
        five_l = label(r"the 5\% that was promised", font_size=20, color=NULLC).next_to(five, UP, buff=0.05)
        src = published_tag(archive.SIMMONS_2011.cite)
        tag = note(rf"simulated: {fmt_int(r['datasets'])} datasets with no effect").to_corner(DR, buff=0.2)
        with self.voiceover(
            "That was one dataset. How often does it work? Run three thousand studies of nothing. "
            f"<bookmark mark='a'/> Stick to the plan, and you're wrong {100 * r['planned']:.0f} per cent of the "
            "time, which is what p below point oh five promises. <bookmark mark='b'/> Allow any one of the "
            "choices, and the rate creeps up, to somewhere between five and nine per cent. None looks dangerous alone. "
            f"<bookmark mark='c'/> Allow all four, and it's {100 * r['any']:.0f} per cent. Nearly four times what "
            "was promised, from four innocent decisions. <bookmark mark='d'/> In 2011, the same year as Bem's "
            "paper, three psychologists named Simmons, Nelson and Simonsohn ran this calculation with four "
            "choices that were in everyday use: two outcome measures, adding more people after a look, "
            f"a covariate, and dropping one of three conditions. They got {100 * d['sns_published']:.0f} per cent. "
            f"We've rerun their simulation, and get {100 * s['ABCD']:.0f}. More often than not, a study of "
            "nothing could be reported as a finding. Their title was False-Positive Psychology. Then, to make "
            "the point, they used these methods on real data to show that listening to a song about being "
            "sixty-four makes people younger."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(five), FadeIn(five_l))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]))
            vo.wait_until("b")
            for row in rows[1:5]:
                self.play(FadeIn(row[0]), GrowFromEdge(row[1], LEFT), FadeIn(row[2]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(rows[5][0]), GrowFromEdge(rows[5][1], LEFT), FadeIn(rows[5][2]))
            vo.wait_until("d")
            self.play(FadeIn(snm), FadeIn(src))
            self.wait(9.0)
            self.play(GrowFromEdge(sbar, LEFT), FadeIn(sval), run_time=1.5)
        self.clear_scene()
