from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.measure()
        self.thurstone()
        self.many()
        self.open()

    def card(self):
        card = chapter_card(14, r"Frontier: \ what the numbers measure", r"Is a sensation the kind of thing that has a size?",
                            lit=(), part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter fourteen. The frontier: what the numbers measure."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def measure(self):
        head = heading(r"Did Fechner measure a sensation?")
        left = VGroup(label(r"what is solid", font_size=34, color=MODEL),
                      rows_of([(r"thresholds: \ curves fitted to counts, \ with intervals", WHITE),
                               (r"Weber's law over the middle of each range", WHITE),
                               (r"power-law form in magnitude estimates, \ and matches that agree", WHITE)], 5.6, 28, 0.25)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right = VGroup(label(r"what is argued", font_size=34, color=BAD),
                       rows_of([(r"that a just noticeable step is a unit of sensation (Fechner)", WHITE),
                                (r"that the numbers people say form a ratio scale (Stevens)", WHITE),
                                (r"that a sensation has a size at all, \ apart from what people can tell apart", WHITE)],
                               5.6, 28, 0.25)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 0.5, 0])
        end = wrapped_label(r"Part 3's lesson, \ at the root of the subject: \ a number is a measurement only if the "
                            r"structure it claims is really there. \ For discrimination, \ it is. \ For the size of a "
                            r"sensation, \ the case is still open.", 12.4, 30, THRESH).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here's the frontier, and it's at the root of the subject. Did Fechner, or anyone since, "
            "measure a sensation? <bookmark mark='a'/> What's solid: thresholds, as curves fitted to "
            "counts, with honest intervals. Weber's law, over the middle of each range. And the power "
            "form of magnitude estimates, with matches across senses that agree. "
            "<bookmark mark='b'/> What's argued: that a just noticeable step is a unit of sensation. That "
            "the numbers people say form a ratio scale, in Part 3's sense, where twice the number means "
            "twice the sensation. And, deepest, that a sensation has a size at all, apart from what a "
            "person can tell apart. <bookmark mark='c'/> It's Part 3's lesson: a number is a measurement "
            "only if the structure it claims is really there. For telling things apart, it is. For the "
            "size of a sensation, the case is still open, and Kant's first objection still has a foothold."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(FadeIn(left[1], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(right[1], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def thurstone(self):
        d = load("thurstone")
        src = archive.THURSTONE_1927
        names = d["names"]
        m = len(names)
        head = heading(r"Thurstone, \ 1927: \ a scale with no ruler")
        cell = 0.62
        grid = VGroup()
        for i in range(m):
            for j in range(m):
                v = float(d["p"][i, j])
                sq = Square(side_length=cell, stroke_width=1, stroke_color=GREY_D,
                            fill_color=interpolate_color(ManimColor("#1b2430"), ManimColor(MODEL), v), fill_opacity=1.0)
                sq.move_to([j * cell, -i * cell, 0])
                txt = label("" if i == j else f"{100 * v:.0f}", font_size=17, color=WHITE).move_to(sq)
                grid.add(VGroup(sq, txt))
        rowlab = VGroup(*[label(n, font_size=21, color=GREY_A).next_to(grid[i * m][0], LEFT, buff=0.12) for i, n in enumerate(names)])
        cap = wrapped_label(r"\% of 200 judges calling the row's offence more serious than the column's", 4.8, 22,
                            GREY_A)
        mat = VGroup(grid, rowlab)
        mat.move_to([-3.7, 0.75, 0])
        cap.next_to(mat, DOWN, buff=0.22).align_to(mat, LEFT)
        # the recovered scale on a line
        lo, hi = -1.1, 1.1
        L = NumberLine(x_range=[lo, hi, 0.5], length=5.6, include_numbers=False, color=GREY_B).move_to([3.5, 1.45, 0])
        ll = label(r"green: \ the recovered scale (Case V)", font_size=22, color=MODEL)
        marks = VGroup()
        for k, (n, v, t) in enumerate(zip(names, d["scale"], d["planted_scaled"])):
            dot = Dot(L.n2p(float(v)), radius=0.07, color=MODEL)
            tick = Line(L.n2p(float(t)) + DOWN * 0.18, L.n2p(float(t)) + DOWN * 0.34, color=THRESH, stroke_width=4)
            lift = (0.3, 0.68, 1.06)[k % 3]
            nm = label(n, font_size=19, color=GREY_A).move_to(L.n2p(float(v)) + UP * lift)
            lead = Line(L.n2p(float(v)) + UP * 0.08, nm.get_bottom() + DOWN * 0.04, color=GREY_D, stroke_width=1.5)
            marks.add(VGroup(dot, tick, lead, nm))
        tl = label(r"orange: \ the scale planted in the judges", font_size=22, color=THRESH)
        VGroup(ll, tl).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(L, DOWN, buff=0.5).align_to(L, LEFT)
        rows = rows_of([
            (r"no physical scale at all: \ only which of two is judged more", WHITE),
            (r"assume each item gives an impression with noise, \ as Psyche's patches did: \ a proportion becomes a "
             r"distance, \ in units of the noise", MODEL),
            (rf"the scale comes back to within {d['max_error']:.2f} of the planted one", MODEL),
            (r"Thurstone scaled the seriousness of nineteen crimes this way. \ Elo ratings and rankings of AI models "
             r"are its descendants (Part 46)", THRESH),
        ], 5.4, 25, 0.2).move_to([3.75, -1.42, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(src.cite), simulated_tag(r"simulated: \ 200 judges with a planted scale"))
        with self.voiceover(
            "One bold answer came early, in 1927, and it runs the other way: measure with no physical "
            "stimulus at all. "
            "<bookmark mark='a'/> Louis Thurstone asked: what if there is no physical scale at all? Which "
            "of two crimes is more serious, which of two pictures is more beautiful. All you have is "
            "which of each pair people choose. <bookmark mark='b'/> Thurstone's move was to assume what "
            "this part assumed about grey patches: each item gives an impression with noise, and the "
            "share of people who pick one over another depends on the distance between them, measured in "
            "units of that noise. Turn every proportion into a distance, and average. "
            "<bookmark mark='c'/> Here two hundred simulated judges compare six offences whose seriousness "
            "is planted in them. Thurstone's simplest case gives the scale back to within "
            f"{d['max_error']:.2f} units. <bookmark mark='d'/> Thurstone himself scaled nineteen crimes this "
            "way. The idea runs straight on to the Elo ratings of chess players and the leaderboards that "
            "rank AI models by which answer people prefer. That's Part 46. And it is Fechner's bet in its "
            "boldest form: wherever people can tell two things apart, noise turns telling apart into "
            "distance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rowlab), FadeIn(grid, lag_ratio=0.02), FadeIn(cap), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(L), FadeIn(ll), LaggedStart(*[FadeIn(mk) for mk in marks], lag_ratio=0.2), FadeIn(tl),
                      FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def many(self):
        q = archive.LESMES_2010.data
        head = heading(r"Measuring a whole curve, \ not one point")
        A = axes([-0.3, 1.6], [0, 2.4], x_length=6.4, y_length=4.0, xticks=[0, 0.5, 1, 1.5], yticks=[0, 1, 2],
                 xfmt=lambda v: {0: "1", 0.5: r"3", 1: "10", 1.5: "30"}[v], yfmt=lambda v: f"10^{{{int(v)}}}",
                 xlabel=r"how fine the stripes are (cycles per degree)", ylabel=r"sensitivity to contrast", center=[-3.0, -0.35, 0])
        ax = A.ax
        f = np.linspace(0.5 - 0.55 * np.sqrt(2.1), 0.5 + 0.55 * np.sqrt(2.1), 200)
        csf = 2.1 - ((f - 0.5) / 0.55) ** 2
        c = curve(ax, f, np.clip(csf, 0, None), WEBERC, stroke_width=5)
        rows = rows_of([
            (r"a threshold at every stripe width: \ a contrast sensitivity curve", WHITE),
            (rf"the quick CSF (2010): \ a Bayesian rule like QUEST, \ but for the curve's {q['parameters']} numbers at once", WEBERC),
            (rf"accurate in under {q['trials']} trials: \ a test that fits in a clinic visit", MODEL),
            (r"the frontier: \ adaptive methods for many unknowns, \ chosen trial by trial", THRESH),
        ], 5.0, 28, 0.3).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        src = published_tag(archive.LESMES_2010.cite)
        tag = note(r"the curve: \ a drawing of the usual shape").to_corner(DR, buff=0.3)
        with self.voiceover(
            "On the method side, the frontier is measuring whole curves instead of single points. Take "
            "vision: how much contrast you need to see stripes depends on how fine the stripes are, and "
            "the thresholds across all widths make a curve. <bookmark mark='a'/> Measuring it point by "
            "point takes hours. <bookmark mark='b'/> In 2010 a method called the quick CSF applied QUEST's "
            "idea to the curve's four numbers at once, choosing each trial to teach the most about all of "
            f"them. <bookmark mark='c'/> It's accurate in under {q['trials']} trials. "
            "<bookmark mark='d'/> Adaptive methods for many unknowns, chosen trial by trial, are where "
            "this chapter's ideas are being pushed now, from the eye clinic to the testing of children."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), Create(c), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def open(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"why the near miss? \ Loud tones beat Weber's law slightly, \ and no one account has won", STEVC),
            (r"growing noise or a compressed code? \ Thresholds cannot say; \ confidence, \ times and cells might", WEBERC),
            (r"why do exponents differ between senses, \ and how much of each is made by the experiment?", THRESH),
            (r"$\star$ \ design an experiment that tells Psyche's two observers of chapter 10 apart, \ using anything but "
             r"thresholds", YOU),
        ], 12.4, 31, 0.4).move_to([0, -0.1, 0])
        with self.voiceover(
            "Four questions to carry out of this part. <bookmark mark='a'/> Why the near miss? Loud tones "
            "beat Weber's law slightly, and no single account has won. <bookmark mark='b'/> Growing noise "
            "or a compressed code? Thresholds can't say. Confidence, response times and the cells "
            "themselves might. <bookmark mark='c'/> Why do the exponents differ between senses, and how "
            "much of each is made by the experiment? <bookmark mark='d'/> And the starred problem: design "
            "an experiment that tells Psyche's two observers of chapter ten apart, using anything except "
            "their thresholds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            for mark_, r in zip("bcd", rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
