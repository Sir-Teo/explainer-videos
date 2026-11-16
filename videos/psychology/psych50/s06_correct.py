from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Correct(VoiceoverScene):
    def construct(self):
        self.card()
        self.methods()
        self.grade()
        self.lesson()

    def card(self):
        card = chapter_card(5, r"Correcting for it", r"Can the filter be undone after the fact?", lit=(), part=PART,
                            scale=("society",), marr=("how",))
        with self.voiceover("Chapter five. Correcting for it."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def methods(self):
        head = heading(r"Five ways to correct")
        items = [
            (r"trim-and-fill", r"Duval and Tweedie: \ trim the studies that make the funnel lopsided, \ add their "
                               r"mirror images, \ re-pool", SYMP),
            (r"PET-PEESE", r"Stanley and Doucouliagos: \ the effect at zero standard error, \ from the regression of "
                           r"chapter four", MODEL),
            (r"selection models", r"Vevea and Hedges: \ model the filter itself, \ the chance a non-significant study "
                                  r"is published, \ and estimate it with the effect", PERSON),
            (r"p-curve", r"Simonsohn, \ Nelson and Simmons: \ use only the significant results, \ and ask what true "
                         r"effect makes their $p$-values look the way they do", GOOD),
            (r"z-curve", r"Bartos and Schimmack: \ the same idea, \ allowing studies to differ in power", AUTH),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(word_chip(name, col, 20, width=3.4), wrapped_label(what, 8.6, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.3, 0])
        with self.voiceover(
            "Five families of correction. <bookmark mark='a'/> Trim-and-fill trims the studies that make the funnel "
            "lopsided, adds their mirror images, and pools again. <bookmark mark='b'/> PET-PEESE takes the effect at "
            "zero standard error, from the last chapter's regression. <bookmark mark='c'/> Selection models model the "
            "filter itself, the chance a non-significant study is published, and estimate it along with the effect. "
            "<bookmark mark='d'/> P-curve uses only the significant results, and asks what true effect makes their "
            "p-values look the way they do. <bookmark mark='e'/> And z-curve does the same while letting studies "
            "differ in power."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def grade(self):
        d = load("grade")
        head = heading(r"Every method, \ every literature")
        R = np.asarray(d["rmse"])
        Mn = np.asarray(d["mean"])
        cell_w, cell_h = 1.55, 0.62
        grid = VGroup()
        for i in range(R.shape[0]):
            for j in range(R.shape[1]):
                v = float(R[i, j])
                t = min(1.0, v / 0.3)
                sq = Rectangle(width=cell_w, height=cell_h, stroke_width=1, stroke_color=BLACK, fill_opacity=1,
                               fill_color=interpolate_color(ManimColor(GOOD), ManimColor(AUTH), t))
                sq.move_to([j * cell_w, -i * cell_h, 0])
                grid.add(VGroup(sq, label(rf"{Mn[i, j]:.2f}", font_size=15, color=BLACK).move_to(sq)))
        grid.move_to([0.9, 0.0, 0])
        cols = VGroup(*[wrapped_label(m, 1.4, 13, GREY_A).next_to(grid[j], UP, buff=0.1)
                        for j, m in enumerate(d["methods"])])
        rlab = VGroup(*[wrapped_label(rf"{s} (truth {t:.1f})", 3.2, 13, WHITE).next_to(grid[i * R.shape[1]], LEFT,
                                                                                      buff=0.15)
                        for i, (s, t) in enumerate(zip(d["scenarios"], d["true"]))])
        foot = rows_of([
            (r"50 simulated literatures of 150 studies per row; \ each cell is the average estimate; \ green is close "
             r"to the truth, \ red far (by root mean squared error)", WHITE),
        ], 12.6, 17, 0.2).to_edge(DOWN, buff=0.35)
        tag = psyche_tag(r"\texttt{meta.grade}").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Psyche runs all of them on literatures where the truth is known. <bookmark mark='a'/> Fifty simulated "
            "literatures per row. Each cell is a method's average estimate, green when close to the truth and red when "
            "far. <bookmark mark='b'/> With no filter, at the bottom, everything works. <bookmark mark='c'/> With a "
            "filter, the naive estimate and trim-and-fill stay well above the truth. <bookmark mark='d'/> PET-PEESE is "
            "unbiased on average, but swings widely when there's nothing there. <bookmark mark='e'/> P-curve breaks "
            "when studies really differ: in the heterogeneous row it reports more than twice the truth. "
            "<bookmark mark='f'/> The selection model does best, but only because Psyche's filter is exactly the one it "
            "assumes. Real filters aren't so tidy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cols), FadeIn(rlab))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.02), FadeIn(foot), run_time=2.0)
            n = R.shape[1]
            for m, i, j in (("b", 5, None), ("c", 1, (0, 1)), ("d", 0, (2,)), ("e", 3, (4,)), ("f", None, (3,))):
                vo.wait_until(m)
                if i is not None and j is None:
                    self.play(*[Indicate(grid[i * n + k], color=WHITE) for k in range(n)])
                elif i is not None:
                    self.play(*[Indicate(grid[i * n + k], color=WHITE) for k in j])
                else:
                    self.play(*[Indicate(grid[r * n + j[0]], color=WHITE) for r in range(R.shape[0])])
        self.clear_scene()

    def lesson(self):
        head = heading(r"No method works everywhere")
        rows = rows_of([
            (r"Carter, \ Sch\"onbrodt, \ Gervais and Hilgard, \ 2019: \ the same exercise across many simulated "
             r"literatures; \ every method failed somewhere", WHITE),
            (r"each correction assumes a particular filter; \ when the real one differs, \ so does the answer", AUTH),
            (r"report several, \ and treat their disagreement as the honest uncertainty", PERSON),
            (r"the methods detect a problem better than they fix it: \ the fix is to stop filtering", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = published_tag(r"Carter et al.\ (2019)")
        with self.voiceover(
            "So no method works everywhere. <bookmark mark='a'/> In 2019 Evan Carter and colleagues ran the same "
            "exercise across many kinds of simulated literature, and every method failed somewhere. "
            "<bookmark mark='b'/> Each correction assumes a particular filter. When the real one differs, so does the "
            "answer. <bookmark mark='c'/> Report several, and treat their disagreement as the honest uncertainty. "
            "<bookmark mark='d'/> The methods detect a problem better than they fix it. The fix is to stop filtering."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
