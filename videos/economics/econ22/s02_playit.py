from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403

LETTERS = "ABCD"
CHIP = ("#F2C14E", "#7EC8F5", "#7BD88F", "#F2788F")
SAY = ("two cents", "twenty-five cents", "fifty cents", "ninety cents")
SHOW = (r"2 cents", r"25 cents", r"50 cents", r"90 cents")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ what happened to the cheques?", r"Of each rebate dollar, \ how much went on "
             r"nondurables in the quarter it arrived?", "Chapter one. Play it: what happened to the cheques?",
             lit={2001: r"the rebates", 2006: r"Johnson, Parker, Souleles"}, scale=("household",),
             horizon=("a quarter",))
        self.guess()
        self.yours()
        self.reveal()

    def guess(self):
        stage = game_stage(12.6, 6.4, center=DOWN * 0.1)
        head = label(r"a household's rebate cheque arrives in the week its digit says", font_size=23,
                     color=GREY_A).move_to(stage.box.get_top() + DOWN * 0.55)
        q = label(r"of each dollar, \ how much went on nondurables within the quarter?", font_size=27,
                  color=E.ACCENT).next_to(head, DOWN, buff=0.35)
        note_ = label(r"nondurables, \ as the survey counts them: \ food, \ fuel, \ utilities, \ clothes, \ health, "
                      r"\ entertainment", font_size=18, color=GREY_B).next_to(q, DOWN, buff=0.2)
        chips = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.0, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(rf"{LETTERS[i]}: \ {SHOW[i]}", font_size=24, color=c))
                         for i, c in enumerate(CHIP)]).arrange(RIGHT, buff=0.3)
        for ch in chips:
            ch[1].move_to(ch[0])
        chips.next_to(note_, DOWN, buff=0.6)
        ring = countdown().next_to(chips, DOWN, buff=0.5)
        with self.voiceover(
            "Your turn. A household's rebate arrives in the week its digit says. <bookmark mark='a'/> Of each dollar, "
            "how much did it spend on nondurable goods and services, in the three months the cheque arrived? "
            "Nondurables as the survey counts them: food, fuel, utilities, clothes, health, entertainment. Not cars "
            "or furniture. <bookmark mark='b'/> A, " + SAY[0] + "; B, " + SAY[1] + "; C, " + SAY[2] + "; or D, "
            + SAY[3] + ". <bookmark mark='c'/> Pause, and choose."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q), FadeIn(note_))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.4), run_time=3.5)
            vo.wait_until("c")
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def yours(self):
        stage = game_stage(12.6, 5.2, tag=r"and you", center=DOWN * 0.1)
        rows = VGroup(
            label(r"one more number to hold on to", font_size=26, color=E.ACCENT),
            label(r"an unexpected payment equal to a month of your income arrives today", font_size=24, color=WHITE),
            label(r"how much of it would you spend in the next three months?", font_size=24, color=YOU),
            label(r"write it down: \ chapter 10 compares it with what thousands of people said", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.4).move_to(stage.box)
        with self.voiceover(
            "And one more number to hold on to, about you this time. <bookmark mark='a'/> An unexpected payment "
            "equal to a month of your income arrives today. <bookmark mark='b'/> How much of it would you spend in "
            "the next three months? <bookmark mark='c'/> Write it down. Chapter ten compares it with what thousands "
            "of people told surveys, and with what lottery winners actually did."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(rows[0]))
            for mk, r_ in zip("abc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.wait(3.0)
        self.clear_scene()

    def reveal(self):
        p = load("playit")
        rows = [
            (r"permanent income: \ the theory of the day", 100 * p["pih_quarter"], 100 * p["pih_quarter"],
             INCOME, r"under 1 cent"),
            (r"2001 rebates \ (Johnson, Parker, Souleles)", 100 * p["jps"][0], 100 * p["jps"][1], SAVE,
             r"20 to 40 cents"),
            (r"2008 payments \ (Parker et al.)", 100 * p["parker2013"][0], 100 * p["parker2013"][1], SPEND,
             r"12 to 30 cents"),
            (r"2008, \ counting cars \ (Parker et al.)", 100 * p["parker2013_total"][0],
             100 * p["parker2013_total"][1], HOUSE, r"50 to 90 cents"),
        ]
        x0, x1 = -1.2, 5.6

        def X(v):
            return x0 + (x1 - x0) * v / 100

        axis_y = -2.3
        axis = Line([x0, axis_y, 0], [x1, axis_y, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(v), axis_y - 0.06, 0], [X(v), axis_y + 0.06, 0], color=GREY_C),
                                MathTex(f"{v}", font_size=22, color=GREY_B).move_to([X(v), axis_y - 0.3, 0]))
                         for v in (0, 25, 50, 75, 100)])
        unit = label(r"cents of each dollar spent within the quarter", font_size=18, color=GREY_B).next_to(
            ticks, DOWN, buff=0.12)
        marks = VGroup()
        for k, (name, lo, hi, col, say) in enumerate(rows):
            y = 1.7 - 1.1 * k
            nm = label(name, font_size=19, color=col).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            if hi - lo < 1:
                bar = Dot([X(lo), y, 0], radius=0.09, color=col)
            else:
                bar = RoundedRectangle(width=X(hi) - X(lo), height=0.36, corner_radius=0.08, stroke_width=0,
                                       fill_color=col, fill_opacity=0.85).move_to([(X(lo) + X(hi)) / 2, y, 0])
            val = label(say, font_size=17, color=col).next_to(bar, RIGHT, buff=0.15)
            marks.add(VGroup(nm, bar, val))
        guides = VGroup(*[DashedLine([X(v), axis_y + 0.1, 0], [X(v), 2.3, 0], color=c, stroke_width=1.5,
                                     dash_length=0.08).set_opacity(0.6)
                          for v, c in zip((2, 25, 50, 90), CHIP)])
        glab = VGroup(*[label(L, font_size=17, color=c).next_to(g, UP, buff=0.05)
                        for L, g, c in zip(LETTERS, guides, CHIP)])
        tag = published_tag(r"Johnson, Parker and Souleles (2006); \ Parker, Souleles, Johnson and McClelland "
                            r"(2013), \ abstracts", corner=DR, font_size=12)
        with self.voiceover(
            "Here are the answers, with your four choices marked as dashed lines. <bookmark mark='a'/> Friedman's "
            "theory says a household should spread a windfall over the rest of its life. At an interest rate of "
            "three percent that is under one cent of each dollar a quarter. <bookmark mark='b'/> Johnson, Parker "
            "and Souleles found that households spent twenty to forty cents of each rebate dollar on nondurables in "
            "the three months it arrived, and more in the three months after. If you chose B, you were right. "
            "<bookmark mark='c'/> In 2008 a second round of payments, again timed by Social Security numbers, gave "
            "twelve to thirty cents on nondurables. <bookmark mark='d'/> And counting what people spent on cars and "
            "other durable goods, fifty to ninety cents. If you chose D thinking of a new car, that is not far off "
            "either. Either way, the theory of the day missed by a factor of twenty or more."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(ticks), FadeIn(unit), FadeIn(guides), FadeIn(glab), FadeIn(tag))
            for mk, m in zip("abcd", marks):
                vo.wait_until(mk)
                self.play(FadeIn(m[0]), GrowFromCenter(m[1]), FadeIn(m[2]))
        self.clear_scene()
