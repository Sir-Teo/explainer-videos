from __future__ import annotations

import numpy as np

from videos.music.music65.common import *  # noqa: F403


class Counting(SoundScene):
    def construct(self):
        chapter(self, 2, r"Counting what comes next", r"How far back should a machine remember?")
        self.idea()
        self.bits()
        self.surprise()
        self.heard()

    # ------------------------------------------------------------------
    def idea(self):
        lines = VGroup(
            label(r"a note is its pitch, \ its length, \ and whether a phrase ends on it", font_size=20, color=WHITE),
            MathTex(r"P(x_t \mid x_{t-1}, \dots, x_{t-k}) \approx \frac{\#(x_{t-k} \dots x_{t-1}\, x_t)}{\#(x_{t-k} \dots x_{t-1})}", font_size=36, color=TUNE),
            label(r"order $k$: \ how many notes back the machine remembers; \ order 0 knows only how common each note is", font_size=19, color=WHITE),
            label(r"contexts never seen fall back to shorter ones \ (as Part 14's model of the next note did)", font_size=18, color=GREY_A),
            label(r"to compose: \ draw a note from the counts, \ append it, \ repeat", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.38)
        head = label(r"a Markov chain", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The simplest learner counts. <bookmark mark='a'/> Treat each note as one symbol: its pitch, its length, and "
            "whether a phrase ends on it. <bookmark mark='b'/> The chance of the next note, given the last few, is estimated "
            "by how often that continuation followed those notes in the corpus. <bookmark mark='c'/> The order is how many "
            "notes back the machine remembers; order nought knows only how common each note is. <bookmark mark='d'/> When a "
            "context was never seen, it falls back to shorter ones, as Part 14's model of the next note did. "
            "<bookmark mark='e'/> And to compose, draw a note from the counts, append it, and repeat."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bits(self):
        d = load("markov")
        b = d["bits"]
        o = np.arange(9)
        v = np.array([b[str(k)] for k in o])
        ax = frame_axes(width=8.0, height=3.2, xlo=0, xhi=8, ylo=3.0, yhi=5.5, center=DOWN * 0.4 + LEFT * 0.6)
        cv = curve(o, v, ax.to, color=TUNE, width=3)
        dots = VGroup(*[Dot(ax.to(x, y), radius=0.06, color=TUNE) for x, y in zip(o, v)])
        ticks = VGroup(*[label(str(k), font_size=14, color=GREY_A).move_to(ax.to(k, 3.0) + DOWN * 0.25) for k in o])
        xl = label(r"order: \ notes remembered", font_size=14, color=GREY_A).next_to(ticks, DOWN, buff=0.15)
        yl = label(r"bits per note on the tunes kept back \ (lower: \ better prediction)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        best = d["best"]
        mark = Circle(radius=0.16, color=EAR).move_to(ax.to(best, b[str(best)]))
        head = label(r"how well each order predicts Bach", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How good is each order? Measure it on the tunes kept back, in bits per note: how surprised the model is by each "
            f"note Bach actually wrote. <bookmark mark='a'/> Order nought needs {say(b['0'], 1)} bits a note; remembering one "
            f"note brings it to {say(b['1'], 1)}; <bookmark mark='b'/> two notes, {say(b[str(best)], 2)}, the best. "
            "<bookmark mark='c'/> Beyond that the curve rises again. Longer contexts are rarer: most four-note contexts in a "
            "new tune were seen once or never, and what was seen once is a poor guide. The model knows its training tunes "
            "better and better, and new tunes worse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(dots), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(mark))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("markov")
        c = clip("orders.three")
        rolls = VGroup(*[tune_roll(d["samples"][k][:28], width=3.6, height=1.3) for k in ("1", "2", "8")]).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.6)
        boxes = choice_boxes([r"order 1", r"order 2", r"order 8"], width=3.4, height=0.8, buff=0.7, size=18).move_to(UP * 1.4)
        head = label(r"three orders, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the first two phrases of a tune drawn from orders one, two and eight."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(rolls))
        st = d["starts"]
        ks = ["o1", "o2", "o8"]
        with self.listen(c) as snd:
            window(snd, r"orders 1, \ 2, \ 8", kind="synthesized", detail=r"Markov chains on Bach's tunes", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            "Order one wanders: every step is plausible, and the whole goes nowhere. Order two sounds more like a hymn. Order "
            "eight sounds most like Bach of all. The next chapter shows why that is not the compliment it seems."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def surprise(self):
        d = load("surprise")
        notes = d["notes"]
        n = len(notes)
        mk = np.minimum(np.array(d["markov"]), 12)
        tf = np.minimum(np.array(d["transformer"]), 12)
        roll = tune_roll(notes, width=11.0, height=1.2).move_to(UP * 1.5)
        ax = frame_axes(width=11.0, height=2.2, xlo=-0.5, xhi=n - 0.5, ylo=0, yhi=12, center=DOWN * 1.1)
        bars = VGroup(*[Rectangle(width=11.0 / n * 0.7, height=max(0.02, 2.2 * v / 12), stroke_width=0, fill_color=TUNE, fill_opacity=0.85)
                        .move_to(ax.to(i, v / 2)) for i, v in enumerate(mk)])
        ends = VGroup(*[DashedLine(ax.to(i, 0), ax.to(i, 12), color=GREY_D, stroke_width=1) for i in d["ends"]])
        yl = label(r"bits for each note, \ order-2 chain \ (tall: \ surprising)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        note = label(r"dashed: \ the fermatas, \ where phrases end", font_size=14, color=GREY_A).to_edge(DOWN, buff=0.25)
        head = label(rf"where {bwv(d['name'])} surprises", font_size=26, color=GREY_A).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Bits per note is an average; note by note it shows where the music surprises. Here is a tune kept back, and how "
            "many bits the order-two chain needed for each of its notes. <bookmark mark='a'/> Inside a phrase most notes are "
            f"cheap. <bookmark mark='b'/> The expensive ones sit at the boundaries: the note that ends a phrase, "
            f"{say(d['markov_at_ends'], 1)} bits on average against {say(d['markov_mean'], 1)} overall, because the machine "
            "must decide that the phrase ends there, and the note that begins the next, which can start almost anywhere. A "
            "listener's expectations, Part 46 found, are least sure in the same places."
        ) as vo:
            self.play(FadeIn(head), FadeIn(roll), FadeIn(ax), FadeIn(yl), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ends))
        self.wait(0.6)
        self.clear_scene()
