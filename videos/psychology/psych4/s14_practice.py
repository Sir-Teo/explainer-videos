from __future__ import annotations

import numpy as np

from videos.psychology.psych4.common import *  # noqa: F403

METRICS = [r"sign-ups", r"checkout rate", r"time on page", r"clicks", r"searches", r"returns", r"scroll depth",
           r"session length", r"cart adds", r"bounce rate", r"shares", r"reviews", r"support tickets", r"page load",
           r"repeat visits", r"wishlist adds", r"coupon use", r"app opens", r"refunds", r"basket size"]


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.dashboard()
        self.rules()

    def card(self):
        card = chapter_card(13, r"In practice: \ twenty metrics on a dashboard", r"Where does the same arithmetic "
                            r"turn up outside the laboratory?", lit=(), part=PART, scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter thirteen. In practice: twenty metrics on a dashboard."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def dashboard(self):
        d = load("dashboard")
        ps, hit = np.asarray(d["example_p"]), d["example_hit"]
        head = heading(r"A new button colour, one week later")
        cells = VGroup()
        for i, (name, p) in enumerate(zip(METRICS, ps)):
            lit = i == hit
            box = RoundedRectangle(width=1.6, height=0.98, corner_radius=0.08, stroke_width=3 if lit else 1.5,
                                   color=(TRUTH if lit else GREY_D), fill_color=("#12301F" if lit else "#111722"),
                                   fill_opacity=1)
            nm = label(name, font_size=21, color=(WHITE if lit else GREY_A))
            if nm.width > 1.42:
                nm.width = 1.42
            pv = label(rf"$p = {p_text(p)}$", font_size=24, color=(TRUTH if lit else GREY_B))
            VGroup(nm, pv).arrange(DOWN, buff=0.1).move_to(box)
            cells.add(VGroup(box, nm, pv))
        cells.arrange_in_grid(4, 5, buff=0.14).move_to([-2.6, -0.45, 0])
        ks, any_ = np.asarray(d["k"]), np.asarray(d["any"])
        A = axes([0, 40], [0, 1.0], x_length=4.3, y_length=3.0, xticks=[1, 5, 10, 20, 30, 40],
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"metrics on the dashboard",
                 ylabel=r"chance that at least one is green", center=[4.55, -0.85, 0], font_size=18)
        ax = A.ax
        line = curve(ax, ks, any_, TRUTH, stroke_width=4)
        marks = VGroup()
        for k, v, dirn in ((5, d["at_5"], DR), (20, d["at_20"], DR)):
            dot = Dot(ax.c2p(k, v), radius=0.08, color=WHITE)
            marks.add(VGroup(dot, label(rf"{k}: \ {pct(v)}", font_size=24, color=WHITE).next_to(dot, dirn, buff=0.06)))
        say = wrapped_label(rf"``{METRICS[hit].capitalize()} up, $p = {p_text(ps[hit])}$. \ Ship it.''", 4.6, 28,
                            TRUTH).move_to([4.55, 1.9, 0])
        tag = note(rf"simulated: twenty metrics on which nothing changed; \ dataset {d['example_seed']}, the first "
                   r"with exactly one below .05").to_corner(DR, buff=0.2)
        with self.voiceover(
            "None of this is special to psychology, and most of you will meet it at work before you meet it in "
            "a journal. <bookmark mark='a'/> A product team changes the colour of a button. A week later the "
            "dashboard shows the test: twenty metrics, each compared between the old colour and the new. "
            f"<bookmark mark='b'/> Nineteen are grey. One is green: {METRICS[hit]}, with a p-value of "
            f"{ps[hit]:.2f}. <bookmark mark='c'/> Somebody writes the announcement. <bookmark mark='d'/> But in "
            "this simulation the button did nothing. With one metric, the chance of a false alarm is five per "
            f"cent. With five metrics, the chance that at least one lights up is {100 * d['at_5']:.0f} per cent. "
            f"With twenty, it's {100 * d['at_20']:.0f} per cent. On a dashboard this size, a green tile is the "
            "expected result of changing nothing. It's chapter four again, with the forks laid out side by side "
            "on one screen. And the dashboard refreshes every morning, so chapter six is there too: every "
            "refresh is another look, and the team stops the test on the morning it turns green."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(c_[0], c_[1])) for c_ in cells], lag_ratio=0.08), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_[2]) for c_ in cells], lag_ratio=0.05), run_time=2.0)
            self.play(Indicate(cells[hit], color=TRUTH, scale_factor=1.12))
            vo.wait_until("c")
            self.play(FadeIn(say, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(A), Create(line), run_time=3.0)
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.8), run_time=4.0)
        self.clear_scene()

    def rules(self):
        d = load("dashboard")
        head = heading(r"The same four repairs, in a product team")
        items = [
            (r"One primary metric, named before launch.", r"preregistration", TRUTH),
            (r"A sample size or a stopping rule fixed in advance.", r"no optional stopping", SIG),
            (rf"Every other metric is exploratory: \ hold it to {d['bonferroni_20']:.4f}".rstrip("0")
             + r", or confirm it in a second test.", r"correction, replication", REP),
            (r"Report the tests that found nothing.", r"no file drawer", ORIG),
        ]
        rows = VGroup()
        for i, (text, name, color) in enumerate(items):
            num = label(rf"{i + 1}", font_size=40, color=color)
            body = VGroup(wrapped_label(text, 9.6, 30, WHITE), label(name, font_size=24, color=color)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)
            rows.add(VGroup(num, body).arrange(RIGHT, buff=0.45, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.1, 0])
        also = label(r"The same holds for a biomarker among thousands, a subgroup in a drug trial, a backtest "
                     r"among many strategies.", font_size=25, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The repairs carry over one for one. <bookmark mark='a'/> Name one primary metric before the test "
            "starts. That's preregistration. <bookmark mark='b'/> Fix the sample size, or a proper stopping "
            "rule, in advance. <bookmark mark='c'/> Treat every other metric as exploratory. Either hold it to "
            "a stricter line, the usual threshold divided by the number of metrics, or better, run a second "
            "test to confirm it. That's replication. <bookmark mark='d'/> And keep a record of the tests that "
            "found nothing, or the company builds its own file drawer and its own inflated beliefs about what "
            "works. <bookmark mark='e'/> The arithmetic doesn't care what the numbers are about. A biomarker "
            "picked from thousands of candidates, a subgroup that responded in a drug trial, a trading strategy "
            "chosen from many backtests: each is a garden of forking paths, and each has the same four "
            "repairs."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r_ in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(also, shift=UP * 0.1))
        self.clear_scene()
