from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Functions(SoundScene):
    def construct(self):
        chapter(self, 1, r"Three jobs, \ in order", r"Do chords come in an order?", extra=((1893, r"Riemann's functions"),))
        self.jobs()
        self.cycle()
        self.quiz()

    # ------------------------------------------------------------------
    def jobs(self):
        rows_ = VGroup(*[VGroup(label(a, font_size=34, color=FUNC_C[k]), label(b, font_size=24, color=WHITE)).arrange(RIGHT, buff=0.4) for k, a, b in (
            ("T", r"T", r"tonic: \ home, \ at rest \ (I, \ and vi and iii, \ which share two of its notes)"),
            ("S", r"S", r"subdominant: \ moving away \ (IV, \ and ii, \ which shares two of IV's)"),
            ("D", r"D", r"dominant: \ tension that wants home \ (V, \ and vii\textdegree)"))]).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.2)
        head = label(r"Riemann's three functions \ (Part 15)", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Part 15 sorted chords by the job they do, as Hugo Riemann did in 1893. <bookmark mark='a'/> The "
            "tonic is home. Chords that share two of its notes, six and three, can stand in for it. "
            "<bookmark mark='b'/> The subdominant moves away from home: four, and two, which shares two of "
            "four's notes. <bookmark mark='c'/> The dominant holds the tension that wants to go home: five, "
            "and seven, which is most of a five chord. The question now is whether the jobs come in an "
            "order."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cycle(self):
        d = load("functions")["major"]
        pos = {"T": UP * 1.7, "S": LEFT * 3.2 + DOWN * 1.5, "D": RIGHT * 3.2 + DOWN * 1.5}
        nodes = {k: VGroup(Circle(radius=0.55, color=FUNC_C[k], stroke_width=4), label(k, font_size=40, color=FUNC_C[k])).move_to(pos[k] + LEFT * 1.6) for k in "TSD"}
        mx = max(d.values())
        arrows = VGroup()
        texts = VGroup()
        for key, n in d.items():
            a, b = key[0], key[1]
            pa, pb = nodes[a][0].get_center(), nodes[b][0].get_center()
            off = 0.22 * np.cross(np.append((pb - pa)[:2] / np.linalg.norm((pb - pa)[:2]), 0), [0, 0, 1])
            col = TUNE if key in ("TS", "SD", "DT") else (WHITE if key == "TD" else GREY_B)
            ar = Arrow(pa + off, pb + off, buff=0.62, stroke_width=1.5 + 10 * n / mx, color=col, max_tip_length_to_length_ratio=0.12)
            arrows.add(ar)
            texts.add(label(str(n), font_size=20, color=col).move_to(ar.get_center() + 2.2 * off))
        fw = d["TS"] + d["SD"] + d["DT"]
        bw = d["ST"] + d["DS"]
        side = VGroup(label(r"T $\to$ S $\to$ D $\to$ T", font_size=30, color=TUNE),
                      label(rf"{fw:,} moves that way round".replace(",", "{,}"), font_size=24, color=WHITE),
                      label(rf"T $\to$ D, \ skipping a step: \ {d['TD']}", font_size=24, color=WHITE),
                      label(rf"against the cycle: \ {bw:,}".replace(",", "{,}"), font_size=24, color=GREY_B),
                      label(rf"D $\to$ S, \ the rarest: \ {d['DS']}", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.3 + UP * 0.6)
        head = label(r"Bach's major chorales: \ how often each job follows each", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Count, in Bach's major chorales, how often a chord with one job is followed by a chord with "
            "another. <bookmark mark='a'/> The thick gold arrows go one way round the triangle: tonic to "
            "subdominant, subdominant to dominant, dominant home to tonic. "
            f"<bookmark mark='b'/> {say(round(fw, -2))} moves go that way, and {say(round(d['TD'], -2))} more go "
            f"straight from tonic to dominant, skipping a step; only {say(round(bw, -2))} go against the cycle. The rarest move of all is from dominant back to subdominant: {say(d['DS'])} times. "
            "Once the tension of the dominant has arrived, it is almost never undone. That is the first "
            "fact of harmonic syntax: away, tension, home. The minor chorales show the same order. And the "
            "commonest move against the cycle, subdominant straight to tonic, is the plagal cadence, the Amen "
            "at the end of hymns: four to one, a softer arrival without the dominant's leading note."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(v) for v in nodes.values()])
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(texts), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("functions")
        c = clip("functions.orders")
        card = listen_card(r"The same three chords in two orders. \ Which one sounds finished: \ A or B?", width=9.0)
        with self.voiceover("Hear it. The same three chords, in two orders. Which one sounds finished, A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        sA = block_staff(d["A"], width=4.6).move_to(LEFT * 3.3 + DOWN * 0.1)
        sB = block_staff(d["B"], width=4.6).move_to(RIGHT * 3.3 + DOWN * 0.1)
        la = label(r"A", font_size=40, color=GREY_A).next_to(sA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(sB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(sA), FadeIn(sB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"a plucked string", corner=DL, tag_corner=DR)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"I \ IV \ V \ I: \ T S D T", font_size=26, color=TUNE).next_to(sA, DOWN, buff=0.35),
                     label(r"I \ V \ IV \ I: \ T D S T", font_size=26, color=GREY_A).next_to(sB, DOWN, buff=0.35))
        with self.voiceover(
            "A, for most listeners. It goes away, builds tension, and resolves it: one, four, five, one. B "
            "plays the same chords with the middle two swapped: the tension of five is raised and then "
            "abandoned for four, and the last chord arrives without having been prepared. Rock and blues "
            "use B's order freely, as the frontier will show; in Bach's style it is rare."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
