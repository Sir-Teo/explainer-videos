from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Adaptive(VoiceoverScene):
    def construct(self):
        self.card()
        self.staircase()
        self.derive()
        self.quest()
        self.race()

    def card(self):
        card = chapter_card(7, r"Asking efficiently", r"Why waste trials where the answer is obvious?",
                            lit={1971: r"Levitt's staircases", 1983: r"QUEST"}, part=PART, scale=("mind",), marr=("how",))
        with self.voiceover(
            "Chapter seven. Asking efficiently."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _track(self, d, key, center, color, y_max=32):
        lv, ok = d[f"{key}_levels"], d[f"{key}_correct"]
        A = axes([0, 80], [0, y_max], x_length=6.8, y_length=3.8, xticks=[0, 20, 40, 60, 80], yticks=[0, 10, 20, 30],
                 xlabel=r"trial", ylabel=r"the increment", center=center)
        ax = A.ax
        line = VMobject(color=GREY_B, stroke_width=2).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(lv)])
        dots = VGroup(*[Dot(ax.c2p(i, v), radius=0.05, color=MODEL if o else BAD) for i, (v, o) in enumerate(zip(lv, ok))])
        return A, ax, line, dots

    def staircase(self):
        d = load("stairs")
        head = heading(r"A staircase: \ harder after success, \ easier after failure")
        A, ax, line, dots = self._track(d, "k2", [-2.9, -0.35, 0], MODEL)
        lvl = DashedLine(ax.c2p(0, d["k2_level"]), ax.c2p(80, d["k2_level"]), color=THRESH, stroke_width=3)
        ll = label(r"the 70.7\% level", font_size=25, color=THRESH).next_to(ax.c2p(60, d["k2_level"]), DOWN, buff=0.15)
        rows = rows_of([
            (r"two right in a row: \ make it harder (one step down)", MODEL),
            (r"one wrong: \ make it easier (one step up)", BAD),
            (r"the track falls fast, \ then wanders about one level, \ spending its trials where they are informative", WHITE),
            (rf"the estimate: \ the average of the last turning points, \ ${d['k2_estimate']:.1f}$", THRESH),
        ], 5.0, 28, 0.3).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: one run, \ the middle one of 101")
        with self.voiceover(
            "The method of constant stimuli spends most of its trials where the answer is obvious: far "
            "below threshold, or far above it. A staircase spends them where they count. "
            "<bookmark mark='a'/> The rule: after two right answers in a row, make the next trial "
            "harder. <bookmark mark='b'/> After one wrong answer, make it easier. <bookmark mark='c'/> The "
            "track falls quickly from an easy start, and then wanders about one level, turning down and "
            "up. <bookmark mark='d'/> The estimate is the average of the last turning points: here "
            f"{d['k2_estimate']:.1f}, in eighty trials. But which level is it wandering around, and why "
            "that one?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(dots, lag_ratio=0.02), FadeIn(rows[2]), run_time=5.0, rate_func=linear)
            vo.wait_until("d")
            self.play(Create(lvl), FadeIn(ll), FadeIn(rows[3]))
        self.clear_scene()

    def derive(self):
        d = load("stairs")
        lv = archive.LEVITT_1971.data["targets"]
        head = heading(r"Where a staircase settles")
        lines = VGroup(
            label(r"at the level it settles on, \ going down is as likely as going up", font_size=31),
            MathTex(r"P(\text{down}) = p^{2}", r"\qquad", r"P(\text{up}) = 1 - p^{2}", font_size=42),
            MathTex(r"p^{2} = \tfrac12 \quad\Longrightarrow\quad p = \sqrt{\tfrac12} = 0.707", font_size=46, color=THRESH),
            MathTex(r"k \text{ right in a row:}\quad p = 0.5^{1/k}", font_size=40, color=WEBERC),
        ).arrange(DOWN, buff=0.4).move_to([0, 1.05, 0])
        tbl = VGroup(*[label(rf"{k}-down: \ ${100 * t:.1f}\%$", font_size=30, color=WEBERC if k > 1 else GREY_A)
                       for k, t in lv]).arrange(RIGHT, buff=0.7).next_to(lines, DOWN, buff=0.45)
        rows = rows_of([
            (rf"on Psyche, \ 101 runs of a 3-down staircase, \ 200 trials each: \ median ${d['k3_median']:.1f}$, \ the "
             rf"79.4\% level ${d['k3_level']:.1f}$", MODEL),
            (rf"a small-step result: \ with large steps the estimate sits low \ (${d['coarse_median']:.1f}$ against "
             rf"${d['fine_median']:.1f}$, \ aim ${d['k2_level']:.1f}$)", BAD),
        ], 12.6, 29, 0.22).to_edge(DOWN, buff=0.6)
        src = published_tag(archive.LEVITT_1971.cite)
        with self.voiceover(
            "Here's the answer, worked out by Harry Levitt in 1971. <bookmark mark='a'/> At the level "
            "where the staircase settles, it must be as likely to step down as to step up. It steps down "
            "after two right answers in a row, which happens with probability p squared. "
            "<bookmark mark='b'/> Set p squared equal to a half, and p is the square root of a half: "
            "seventy point seven percent. <bookmark mark='c'/> Require three right in a row and it settles "
            "at seventy-nine point four percent; four, at eighty-four. So you pick the rule for the point "
            "of the curve you want. <bookmark mark='d'/> On Psyche, a hundred and one three-down staircases of "
            f"two hundred trials each have a median of {d['k3_median']:.1f}, against a seventy-nine percent "
            f"level of {d['k3_level']:.1f}. <bookmark mark='e'/> One caution the derivation hides: it assumes small steps. With "
            "large steps the estimate sits low. Levitt's numbers are a limit, not a promise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(Write(lines[2]))
            vo.wait_until("c")
            self.play(FadeIn(lines[3]), FadeIn(tbl, lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def quest(self):
        q = load("quest")
        head = heading(r"QUEST: \ keep a belief, \ and test where it is least sure")
        n = len(q["placed"])
        A = axes([0, n], [0, 16], x_length=6.4, y_length=3.8, xticks=[0, 10, 20, 30, 40], yticks=[0, 4, 8, 12, 16],
                 xlabel=r"trial", ylabel=r"the increment tested", center=[-3.1, -0.35, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(i, v), radius=0.07, color=MODEL if o else BAD)
                        for i, (v, o) in enumerate(zip(q["placed"], q["correct"]))])
        band = VGroup()
        for i in range(n):
            m, s = q["estimates"][i], q["log_sd"][i]
            band.add(Line(ax.c2p(i, max(m * np.exp(-s), 0)), ax.c2p(i, min(m * np.exp(s), 16)), color=WEBERC, stroke_width=3,
                          stroke_opacity=0.5))
        lvl = DashedLine(ax.c2p(0, q["level"]), ax.c2p(n, q["level"]), color=THRESH, stroke_width=3)
        rows = rows_of([
            (r"a probability for every possible threshold: \ the belief", WEBERC),
            (r"test at the believed threshold; \ update the belief by Bayes's rule; \ repeat", WHITE),
            (rf"the belief narrows trial by trial: \ after {n} trials, \ ${q['estimate']:.1f}$ \ (the 82\% level: "
             rf"${q['level']:.1f}$)", THRESH),
            (r"Watson and Pelli, 1983: \ the method in the eye clinic's computers", GREY_A),
        ], 5.2, 28, 0.3).move_to([4.2, -0.25, 0])
        keep_in_frame(rows)
        src = published_tag(archive.WATSON_PELLI_1983.cite)
        tag = psyche_tag(r"simulated: one run, \ the middle one of 101")
        with self.voiceover(
            "A staircase only remembers the last few answers. QUEST, published by Andrew Watson and Denis "
            "Pelli in 1983, remembers everything. <bookmark mark='a'/> It keeps a probability for every "
            "possible threshold: a belief. <bookmark mark='b'/> Each trial is placed at the threshold it "
            "currently believes in. The answer updates the belief by Bayes's rule, and "
            "the next trial moves. <bookmark mark='c'/> The belief narrows, trial by trial. After "
            f"{n} trials its estimate is {q['estimate']:.1f}, against a true eighty-two percent level of "
            f"{q['level']:.1f}. <bookmark mark='d'/> Methods descended from it run in the computers of "
            "vision laboratories, and in some clinical tests."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), Create(lvl), FadeIn(rows[0]))
            vo.wait_until("a")
            self.wait(0.3)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(dots, lag_ratio=0.05), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(band, lag_ratio=0.05), FadeIn(rows[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def race(self):
        q = load("quest")
        head = heading(r"Three methods, \ the same budget of trials")
        A = axes([0, 130], [0, 1.2], x_length=7.0, y_length=4.2, xticks=[16, 32, 64, 96, 128], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:g}", xlabel=r"trials", ylabel=r"typical error, \ in log units", center=[-2.9, -0.35, 0])
        ax = A.ax
        ns = q["ns"]
        cs = [(q["sd_constant"], GREY_A, r"constant stimuli"), (q["sd_staircase"], MODEL, r"2-down staircase"),
              (q["sd_quest"], WEBERC, r"QUEST")]
        lines = VGroup(*[VGroup(curve(ax, ns, y, col, stroke_width=4), *[Dot(ax.c2p(a, b), radius=0.06, color=col) for a, b in zip(ns, y)])
                         for y, col, _ in cs])
        lg = legend([(col, name) for _, col, name in cs], font_size=27).move_to(ax.c2p(92, 1.0))
        i32 = list(ns).index(32)
        rows = rows_of([
            (r"each method aimed at its own level; \ error measured against that level", WHITE),
            (rf"at 32 trials: \ constant stimuli ${q['sd_constant'][i32]:.2f}$, \ staircase ${q['sd_staircase'][i32]:.2f}$, \ "
             rf"QUEST ${q['sd_quest'][i32]:.2f}$", THRESH),
            (r"a log error of 0.35 is a factor of 1.4 either way", GREY_A),
            (r"the smarter the placement, \ the fewer trials: \ a hearing test takes minutes, \ not an afternoon", MODEL),
        ], 5.0, 28, 0.3).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: 120 runs at each budget")
        with self.voiceover(
            "How much does it matter? Give each method the same budget of trials, run it a hundred and "
            "twenty times, and measure how far its threshold lands from the level it aims at. "
            f"<bookmark mark='a'/> At thirty-two trials, constant stimuli are typically off by "
            f"{q['sd_constant'][i32]:.2f} log units, the staircase by {q['sd_staircase'][i32]:.2f}, and "
            f"QUEST by {q['sd_quest'][i32]:.2f}. <bookmark mark='b'/> A log error of point three five is "
            "a factor of one point four either way. <bookmark mark='c'/> So the smarter the placement, the "
            "fewer trials. It's why a hearing test takes minutes and not an afternoon."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lg), FadeIn(rows[0]),
                      LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
