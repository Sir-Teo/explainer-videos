from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Codes(VoiceoverScene):
    def construct(self):
        self.card()
        self.adrian()
        self.on_you()
        self.noise()

    def card(self):
        card = chapter_card(10, r"On you: \ reading a spike train", r"If every signal is the same size, how is "
                            r"anything said?", lit={1926: r"Adrian and Zotterman"}, part=PART,
                            scale=("neuron", "circuit"), marr=("what",))
        with self.voiceover(
            "Chapter ten. On you: reading a spike train."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def adrian(self):
        d = load("codes")
        a = archive.ADRIAN_1926.data
        head = heading(r"1926: \ one fibre, one size of signal, and a rate")
        rng = np.random.default_rng(7)
        rows = VGroup()
        for i, (name, rate) in enumerate(((r"a light load", 8.0), (r"a heavier load", 25.0), (r"heavier still", 60.0))):
            y = 2.1 - 0.95 * i
            n = int(rate)
            times = np.sort(rng.uniform(0, 1, n)) * 0.6 + np.linspace(0, 1, n) * 0.4  # fairly regular
            ticks = VGroup(*[Line([-4.0 + 5.8 * t_, y - 0.28, 0], [-4.0 + 5.8 * t_, y + 0.28, 0], color=VOLT, stroke_width=2.5)
                             for t_ in times])
            base = Line([-4.0, y - 0.28, 0], [1.8, y - 0.28, 0], color=GREY_D, stroke_width=1.5)
            rows.add(VGroup(label(name, font_size=26, color=DATA).next_to([-4.2, y, 0], LEFT, buff=0.1), base, ticks))
        keep_in_frame(rows)
        side = VGroup(
            wrapped_label(r"Every impulse is the same size.", 4.0, 28, WHITE),
            wrapped_label(r"More stretch: \ more of them per second.", 4.0, 28, THRESH),
            wrapped_label(r"The strength of a stimulus is carried by the rate.", 4.0, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 1.15, 0])
        keep_in_frame(side)
        A = axes([-1.3, 1.2], [0, 160], x_length=5.8, y_length=1.5, xticks=[-1, 0, 1], xfmt=lambda v: f"{10 ** v:g}",
                 yticks=[0, 75, 150], xlabel=r"load (log scale)", ylabel=r"impulses a second", center=[-1.1, -2.0, 0],
                 font_size=18)
        same = VGroup(*[Line([-2.4 + 0.8 * i, 0.1, 0], [-2.4 + 0.8 * i, 1.1, 0], color=VOLT, stroke_width=4) for i in range(7)])
        puzzle = VGroup(same,
                        label(r"one size of signal", font_size=28, color=GREY_A).next_to(same, UP, buff=0.25),
                        label(r"So how does a nerve say ``heavy'', or ``bright''?", font_size=32, color=P.ACCENT).next_to(
                            same, DOWN, buff=0.4))
        line = curve(A.ax, np.log10(d["stretch"]), d["adrian"], THRESH, stroke_width=3)
        tag = note(r"schematic trains; \ the curve is illustrative, not their record").to_corner(DR, buff=0.2)
        src = historical_tag(archive.ADRIAN_1926.cite)
        with self.voiceover(
            "Chapter six left a puzzle. A fibre has one size of signal. So how does a nerve tell the brain "
            "that a weight is heavy and not light, or a light bright and not dim? The answer was found in "
            "1926 by Edgar Adrian and Yngve Zotterman, in Cambridge. <bookmark mark='a'/> They took a muscle "
            "from a frog, with the nerve that reports how much the muscle is stretched, and cut the nerve "
            "down until a single fibre was left. Then they hung weights on the muscle and listened. "
            "<bookmark mark='b'/> With a light load, the fibre sent a slow trickle of impulses. Every one the "
            "same size. <bookmark mark='c'/> With a heavier load, the impulses were no bigger. There were more "
            "of them. Heavier still, more again. <bookmark mark='d'/> So the strength of the stimulus isn't in "
            "the signal. It's in how often the signal comes. This is the rate code, and it's the first "
            "sentence in the language of the nervous system. The rate rises steeply at first and then levels "
            "off, so a fibre covers a wide range of loads with a limited range of rates. You'll see that "
            "compression again and again in Act three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            self.play(FadeIn(same, lag_ratio=0.15), FadeIn(puzzle[1]), run_time=2.5)
            self.play(FadeIn(puzzle[2], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(puzzle), run_time=0.6)
            self.play(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in rows])
            vo.wait_until("b")
            self.play(FadeIn(rows[0][2], lag_ratio=0.2), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[1][2], lag_ratio=0.1), run_time=2.0)
            self.play(FadeIn(rows[2][2], lag_ratio=0.05), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(A), Create(line), run_time=2.5)
        self.clear_scene()

    def on_you(self):
        d = load("codes")
        quiz, cnt, rates = d["quiz"], d["quiz_counts"], d["quiz_rates"]
        stage = demo_stage(13.2, 6.4, tag=r"On you", center=[0, -0.15, 0])
        ask = label(r"Three stimuli, one second each, one cell. \ Which was the strongest?", font_size=30,
                    color=P.ACCENT).move_to([-0.6, 2.35, 0])
        ring = countdown_ring(0.34).move_to([5.7, 2.35, 0])
        rows = VGroup()
        for i, tr in enumerate(quiz):
            y = 1.1 - 1.35 * i
            ticks = VGroup(*[Line([-4.6 + 8.6 * t_, y - 0.35, 0], [-4.6 + 8.6 * t_, y + 0.35, 0], color=VOLT, stroke_width=2.5)
                             for t_ in tr])
            base = Line([-4.6, y - 0.35, 0], [4.0, y - 0.35, 0], color=GREY_D, stroke_width=1.5)
            name = label("ABC"[i], font_size=38, color=WHITE).move_to([-5.5, y, 0])
            ans = label(rf"{cnt[i]} signals", font_size=28, color=(THRESH if cnt[i] == max(cnt) else GREY_A)).move_to(
                [5.2, y, 0])
            rows.add(VGroup(name, base, ticks, ans))
        note_ = note(r"simulated: three random trains from one model cell").move_to([0, -3.05, 0])
        best = "ABC"[int(np.argmax(cnt))]
        with self.voiceover(
            "Your turn, as the brain. You're a cell downstream, and all you get is impulses. "
            "<bookmark mark='a'/> Here are three one-second recordings from the same sensory cell, made while "
            "three different stimuli were applied. A, B and C. <bookmark mark='b'/> Which stimulus was the "
            "strongest? And put the other two in order while you're at it."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(ask))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), FadeIn(r_[1]), FadeIn(r_[2], lag_ratio=0.03))
                                    for r_ in rows], lag_ratio=0.6), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(ring))
        self.play(ring.t.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        with self.voiceover(
            f"{best}, by a distance. <bookmark mark='a'/> {cnt[0]} signals in A, {cnt[1]} in B, {cnt[2]} in C. "
            "You didn't need to be taught how to do that. You counted, or you judged how crowded each line "
            "looked, which is counting without numbers. That's what a rate code asks of whoever reads it: add "
            "up the impulses over some stretch of time. And you know a device that does exactly that. The "
            "leaky membrane of chapter three adds up what arrives within its time constant. A neuron reading "
            "another neuron is the reader you just were."
        ) as vo:
            self.play(FadeOut(ring), FadeIn(note_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[3], shift=LEFT * 0.15) for r_ in rows], lag_ratio=0.5), run_time=3.0)
        self.clear_scene()

    def noise(self):
        d = load("codes")
        head = heading(r"The same stimulus, eight times")
        trains = d["rasters"]["r20"]
        ras = raster(trains, -6.4, 1.9, 5.6, row=0.36, color=VOLT, tick=0.26)
        ras_l = label(r"one second, the same input each time", font_size=22, color=GREY_A).next_to(ras, DOWN, buff=0.2)
        edges = np.asarray(d["edges"])
        top = float(max(d["hist"].max(), d["hist_ref"].max())) * 1.15
        A = axes([0, 45], [0, top], x_length=5.4, y_length=2.6, xticks=[0, 10, 20, 30, 40],
                 xlabel=r"signals counted in one second", center=[3.5, 0.9, 0], font_size=19)
        h1 = hist(A.ax, edges, d["hist"], VOLT, 0.7)
        h2 = hist(A.ax, edges, d["hist_ref"], MODEL, 0.75)
        leg = VGroup(label(rf"at random: \ spread/mean = {d['fano']:.1f}", font_size=22, color=VOLT),
                     label(rf"with a dead time: \ {d['fano_ref']:.1f}", font_size=22, color=MODEL)).arrange(
                         DOWN, aligned_edge=LEFT, buff=0.08).next_to(A, UP, buff=0.15)
        w, c = np.asarray(d["windows"]), np.asarray(d["correct"])
        i50, i1 = list(w).index(0.05), list(w).index(1.0)
        facts = VGroup(
            label(r"Telling 20 a second from 30, by counting:", font_size=28, color=WHITE),
            label(rf"over 50 ms: \ right {pct(c[i50])} of the time \ \ \ \ over 1 s: \ {pct(c[i1])}", font_size=28,
                  color=THRESH),
            label(r"A reader in a hurry must pool many cells.", font_size=28, color=P.ACCENT),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.75)
        tag = note(r"simulated: Poisson trains; \ 2,000 repeats for the counts").to_corner(DR, buff=0.2)
        with self.voiceover(
            "There's a catch, and it shapes the whole brain. <bookmark mark='a'/> Give a cortical cell exactly "
            "the same stimulus eight times and you get eight different trains. The rate is the same; the "
            "moments aren't. To a first approximation each impulse arrives at random, like raindrops. "
            "<bookmark mark='b'/> Count the impulses in each second, over many repeats, and the counts are "
            f"spread out. For a purely random train the spread, the variance, equals the mean. That ratio is "
            "called the Fano factor, and for many cortical cells it's close to one. <bookmark mark='c'/> A "
            "dead time after each impulse makes the train more regular, and the ratio falls. "
            "<bookmark mark='d'/> Now think of the reader. Suppose it has to tell twenty impulses a second "
            f"from thirty. If it can count for a full second, it's right {100 * c[i1]:.0f} per cent of the "
            f"time. If it has fifty milliseconds, which is nearer the time you take to see something, it's "
            f"right {100 * c[i50]:.0f} per cent of the time, not much better than a coin. <bookmark mark='e'/> "
            "A brain can't wait a second. So it does the other thing: it listens to many cells at once and "
            "adds them up. That's one reason there are so many neurons. Whether the exact timing of impulses "
            "also carries messages is a live question, and we'll meet cases where it clearly does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, lag_ratio=0.05) for r_ in ras], lag_ratio=0.3), FadeIn(ras_l), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(h1, lag_ratio=0.03), FadeIn(leg[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(h2, lag_ratio=0.03), FadeIn(leg[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("e")
            self.play(FadeIn(facts[2], shift=UP * 0.1))
        self.clear_scene()
