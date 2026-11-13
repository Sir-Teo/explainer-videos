from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Series(SoundScene):
    def construct(self):
        chapter(self, 1, r"A sum of sines", r"How much of each sine is in a wave?", lit=(1753, 1807))
        self.why_sines()
        self.recipe()
        self.sums()
        self.gibbs()
        self.transform()
        self.quiz()

    # ------------------------------------------------------------------
    def why_sines(self):
        d = load("square")
        head = label(r"Why sines, \ of all shapes?", font_size=38, color=TUNE).to_edge(UP, buff=0.45)
        box = RoundedRectangle(width=2.6, height=1.3, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2, fill_color=GREY_D, fill_opacity=0.15)
        boxes = VGroup(box.copy().move_to(UP * 1.1), box.copy().move_to(DOWN * 1.7))
        btxt = VGroup(*[label(r"anything that rings: \\ a string, \ a pipe, \ a room", font_size=22, color=GREY_A).move_to(b) for b in boxes])
        rows = VGroup()
        for b, kin, kout, col in ((boxes[0], "sin_in", "sin_out", GOOD), (boxes[1], "sq_in", "sq_out", BAD)):
            a = Scope(width=3.6, height=1.3, color=col).next_to(b, LEFT, buff=0.9)
            a.set_wave(d[kin], gain=0.85)
            o = Scope(width=3.6, height=1.3, color=col).next_to(b, RIGHT, buff=0.9)
            o.set_wave(d[kout], gain=0.85)
            arr = VGroup(Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B, stroke_width=3), Arrow(b.get_right(), o.get_left(), buff=0.1, color=GREY_B, stroke_width=3))
            rows.add(VGroup(a, o, arr))
        v1 = label(r"a sine goes in, \ a sine comes out: \ only its size and timing change", font_size=26, color=GOOD).next_to(boxes[0], DOWN, buff=0.35)
        v2 = label(r"any other shape comes out a different shape", font_size=26, color=BAD).next_to(boxes[1], DOWN, buff=0.35)
        with self.voiceover(
            "Before the recipe, a fair question. Why sines? You could build waves out of triangles, or square "
            "pulses. What is special about this one shape? <bookmark mark='a'/> Send a sine wave through anything "
            "that rings: a string, a pipe, a room, an electrical circuit. What comes out is a sine wave of the same "
            "frequency. It may be bigger or smaller, earlier or later, but its shape is untouched. "
            "<bookmark mark='b'/> Send in any other shape, and it comes out bent. <bookmark mark='c'/> That is the "
            "reason. Sines are the only shapes that the physics of vibration leaves alone, which is why the modes "
            "of the string in Part 1 each sang a pure sine in time. Take a sound apart into sines and each piece "
            "goes through the world independently of the others."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), FadeIn(btxt[0]), FadeIn(rows[0]), FadeIn(v1))
            vo.wait_until("b")
            self.play(FadeIn(boxes[1]), FadeIn(btxt[1]), FadeIn(rows[1]), FadeIn(v2))
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def transform(self):
        d = load("square")
        head = label(r"And a sound that never repeats?", font_size=36, color=TUNE).to_edge(UP, buff=0.4)
        panels = VGroup()
        for period, name in ((4, r"a pulse every 4 widths"), (8, r"every 8"), (32, r"every 32")):
            g = axes([0, 4], [0, 1.1], x_length=3.7, y_length=2.0, xlabel=r"frequency", ylabel=r"", xticks=[], yticks=[], font_size=18)
            f, a = d[f"train_f_{period}"], d[f"train_a_{period}"]
            lines = VGroup(*[Line(g.ax.c2p(x, 0), g.ax.c2p(x, max(v, 0.005)), color=TUNE, stroke_width=3 if period < 32 else 1.5) for x, v in zip(f, a) if x <= 4])
            env = curve(g.ax, d["env_f"], d["env_a"], GREY_C, stroke_width=1.5)
            panels.add(VGroup(g, env, lines, label(name, font_size=24, color=GREY_A).next_to(g, UP, buff=0.1)))
        panels.arrange(RIGHT, buff=0.45).move_to(UP * 0.5)
        lim = VGroup(label(r"one pulse, \ once: \ the lines have merged into a curve", font_size=28, color=GOOD),
                     label(r"the Fourier \emph{transform}: \ a continuous spectrum", font_size=28, color=GREY_A),
                     label(r"a single click contains every frequency", font_size=28, color=TUNE)).arrange(DOWN, buff=0.2).move_to(DOWN * 2.2)
        with self.voiceover(
            "All of that was for a wave that repeats. Most sounds do not: a clap, a word, a whole symphony happens "
            "once. <bookmark mark='a'/> Here is the trick. Take a pulse that repeats every four of its own widths. "
            "Its recipe is a row of lines, at multiples of its repeat rate. <bookmark mark='b'/> Now let it repeat "
            "half as often. The lines move closer together, under the same outline. <bookmark mark='c'/> Repeat it "
            "more rarely still, and they crowd closer. <bookmark mark='d'/> In the limit, a pulse that happens just "
            "once, the lines merge into a smooth curve: a continuous spectrum. This is the Fourier transform. A "
            "sound that repeats has a spectrum of separate lines, and therefore a pitch. A sound that happens once "
            "has a continuous one. And the shorter the pulse, the wider its curve: a single click contains every "
            "frequency there is."
        ) as vo:
            self.play(FadeIn(head))
            for mark, pn in zip("abc", panels):
                vo.wait_until(mark)
                self.play(FadeIn(pn))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lim], lag_ratio=0.8), run_time=6.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recipe(self):
        d = load("square")
        claim = MathTex(r"f(x)", r"=", r"b_1 \sin x", r"+", r"b_2 \sin 2x", r"+", r"b_3 \sin 3x", r"+ \cdots", font_size=44).to_edge(UP, buff=0.5)
        x = np.linspace(0, 1, 400)
        sq = np.sign(np.sin(2 * np.pi * x) + 1e-9)
        panels = VGroup()
        for n in (3, 2):
            g = axes([0, 1], [-1.2, 1.2], x_length=4.6, y_length=1.9, xlabel=r"", ylabel=r"", xticks=[], yticks=[0], font_size=18)
            prod = sq * np.sin(2 * np.pi * n * x)
            pc = curve(g.ax, x, prod, GOOD if n == 3 else BAD, stroke_width=3)
            sc = curve(g.ax, x, sq, GREY_C, stroke_width=1.5)
            sn = curve(g.ax, x, np.sin(2 * np.pi * n * x), FREQ, stroke_width=1.5)
            cap = label(rf"the square $\times \sin {n}x$", font_size=24, color=GREY_A).next_to(g, UP, buff=0.1)
            res = label(rf"average: \ {d['proj'][n - 1] / 2:.3f}" if n == 3 else r"average: \ 0: \ the humps cancel", font_size=26,
                        color=GOOD if n == 3 else BAD).next_to(g, DOWN, buff=0.12)
            panels.add(VGroup(g, sc, sn, pc, cap, res))
        panels.arrange(RIGHT, buff=0.9).move_to(UP * 0.45)
        rule = MathTex(r"b_n", r"=", r"2 \times \text{the average of}\ f(x)\,\sin nx", font_size=40).move_to(DOWN * 1.9)
        rule[0].set_color(TUNE)
        table = VGroup(*[VGroup(MathTex(rf"b_{n}", font_size=30, color=TUNE),
                                label(rf"{d['proj'][n - 1]:.3f}" if abs(d["proj"][n - 1]) > 1e-6 else "0", font_size=28))
                         .arrange(DOWN, buff=0.12) for n in range(1, 8)]).arrange(RIGHT, buff=0.55).move_to(DOWN * 2.95)
        form = MathTex(r"=\ \frac{4}{\pi n}\ (n\ \text{odd})", font_size=32, color=GREY_A).next_to(table, RIGHT, buff=0.4)
        with self.voiceover(
            "Fourier's claim, for a wave that repeats: it is a sum of sines whose frequencies are one, two, three "
            "times the frequency of the wave itself. The only question is how much of each. <bookmark mark='a'/> "
            "His recipe is this. To find how much of the third sine is in a square wave, multiply the two together, "
            "point by point, and take the average. Where the square and the sine agree in sign the product is "
            "positive, and here they agree more than they disagree. <bookmark mark='b'/> Try the second sine "
            "instead, and the positive humps exactly cancel the negative ones. There is no second harmonic in a "
            "square wave. <bookmark mark='c'/> That is the whole method: each amount is twice an average. "
            f"<bookmark mark='d'/> Done numerically for the first seven, it gives {say(d['proj'][0], 3)}, nothing, "
            f"{say(d['proj'][2], 3)}, nothing, {say(d['proj'][4], 3)}: four over pi, divided by one, three, five. "
            "Only the odd ones, each weaker than the last."
        ) as vo:
            self.play(FadeIn(claim))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(rule))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(t) for t in table], lag_ratio=0.25), run_time=2.5)
            self.play(FadeIn(form))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sums(self):
        d = load("square")
        g = axes([0, 2], [-1.45, 1.45], x_length=8.4, y_length=3.6, xlabel=r"", ylabel=r"", xticks=[], yticks=[-1, 0, 1], font_size=20)
        g.move_to(LEFT * 1.9 + UP * 0.3)
        target = curve(g.ax, d["t"], d["target"], GREY_C, stroke_width=1.5)
        wave = curve(g.ax, d["t"], d["sums"][0], TUNE, stroke_width=3)
        rows = VGroup(label(r"terms \quad distance from the square", font_size=22, color=GREY_B))
        for k, r in zip(d["counts"], d["rms"]):
            rows.add(VGroup(label(str(k), font_size=28, color=TUNE), label(rf"{100 * r:.0f}\%", font_size=28)).arrange(RIGHT, buff=1.2))
        rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(RIGHT * 4.9 + UP * 0.3)
        for r in rows[1:]:
            r.set_opacity(0.2)
        note_ = label(r"the average gap shrinks for ever: \ this is the sense in which Fourier was right", font_size=26, color=GOOD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Now add them back up, and watch Lagrange's objection. With one term, a sine. With two, three, five, "
            "<bookmark mark='a'/> the flat tops fill in and the sides stand up. Every one of these curves is "
            "perfectly smooth. None of them has a corner. But measure the average gap between the sum and the "
            "square, and it keeps shrinking, towards nothing. <bookmark mark='b'/> Lagrange was thinking of a curve "
            "as a single formula. Fourier's sum does something subtler: it gets as close as you like, in the "
            "average. Making that idea exact took another twenty years, and the proof, by Dirichlet in 1829, is "
            "where the modern idea of a function comes from."
        ) as vo:
            self.play(FadeIn(g), FadeIn(target), FadeIn(wave), FadeIn(rows[0]))
            rows[1].set_opacity(1)
            self.add(rows[1])
            gap = max(vo.until("a") - 0.5, 4.0) / 5
            for i in range(1, 6):
                new = curve(g.ax, d["t"], d["sums"][i], TUNE, stroke_width=3)
                self.play(Transform(wave, new), rows[i + 1].animate.set_opacity(1), run_time=gap)
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gibbs(self):
        d = load("square")
        t = np.linspace(0.0, 0.25, 1500)
        g = axes([0, 0.25], [0.6, 1.25], x_length=7.4, y_length=3.8, xlabel=r"just after the jump", ylabel=r"", xticks=[], yticks=[0.8, 1.0, 1.2],
                 font_size=20)
        g.move_to(LEFT * 2.4 + DOWN * 0.1)
        one = DashedLine(g.ax.c2p(0, 1), g.ax.c2p(0.25, 1), color=GREY_C, stroke_width=1.5)
        curves = VGroup()
        for k, col in ((10, RATIO), (30, TUNE), (100, BAD)):
            y = sum(4 / (np.pi * n) * np.sin(2 * np.pi * n * t) for n in range(1, 2 * k, 2))
            curves.add(curve(g.ax, t, np.clip(y, 0.6, 1.25), col, stroke_width=2.5))
        leg = VGroup(*[label(rf"{k} terms", font_size=24, color=c_) for k, c_ in ((10, RATIO), (30, TUNE), (100, BAD))]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        leg.move_to(g.ax.c2p(0.2, 0.8))
        rows = VGroup(label(r"overshoot, \ as a share of the jump", font_size=24, color=GREY_B))
        for r in d["gibbs"]:
            rows.add(label(rf"{r['terms']:,} terms: \ {100 * r['overshoot']:.2f}\%".replace(",", "{,}"), font_size=30, color=TUNE))
        rows.add(label(r"it never goes away", font_size=30, color=BAD))
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.3 + UP * 0.2)
        with self.voiceover(
            "There is one place where the sum stays stubborn, and it matters for sound. Look closely just after the "
            "jump. <bookmark mark='a'/> The sum overshoots, and rings. Add more terms and the ringing squeezes "
            "closer to the jump, but the overshoot does not get smaller. <bookmark mark='b'/> It settles at about "
            f"{say(100 * d['gibbs'][-1]['overshoot'], 2)} percent of the jump, however many terms you use. This is "
            "the Gibbs phenomenon. <bookmark mark='c'/> You will meet it again whenever a sound is cut off sharply "
            "in frequency: a filter that is too steep rings, for exactly this reason."
        ) as vo:
            self.play(FadeIn(g), FadeIn(one))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in curves], lag_ratio=0.6), FadeIn(leg), run_time=4.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("square")
        c = clip("square.quiz")
        q = listen_card(r"Two tones on the same note, \ A and B. \\ One has every harmonic. \ The other has only the "
                        r"odd ones. \ Which is which?", width=9.6).to_edge(UP, buff=0.6)
        boxes = ab_boxes(y=0.2)
        with self.voiceover("A question for your ears. Two tones on the same note. One contains every harmonic. The "
                            "other contains only the odd ones. Which is which?"):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(boxes))
        with self.listen(c) as snd:
            window(snd, r"tone A, \ then tone B", kind="synthesized", tag_corner=DR)
            for key, box, end in (("A", boxes[0], snd.time_of("B") - 0.4), ("B", boxes[1], c.duration)):
                t0 = snd.time_of(key)
                snd.wait_until(t0)
                glow_on(snd, box, t0, end)
                snd.wait_until(end)
                box[1].set_color(GREY_A)
        n = np.arange(1, 13)
        saw, sq = 1.0 / n, np.where(n % 2 == 1, 1.0 / n, 0.0)
        bars = VGroup(partial_bars(saw, width=3.6, height=1.5, db=False), partial_bars(sq, width=3.6, height=1.5, db=False))
        for b, box in zip(bars, boxes):
            b.next_to(box, DOWN, buff=0.4)
        tags = VGroup(label(r"a sawtooth: \ all of them", font_size=24, color=GREY_A).next_to(bars[0], DOWN, buff=0.12),
                      label(r"a square: \ odd only", font_size=24, color=GOOD).next_to(bars[1], DOWN, buff=0.12))
        with self.voiceover(
            f"{d['quiz_answer']} was the square wave, with only the odd harmonics. It is the hollow one. You have "
            "heard that hollowness before: it was the stopped pipe of Part 2, and for the same reason. "
            "<bookmark mark='a'/> A was a sawtooth, with every harmonic: brighter, and buzzier."
        ) as vo:
            self.play(FadeIn(bars), FadeIn(tags), boxes[1][0].animate.set_stroke(GOOD, width=4))
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()
