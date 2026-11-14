from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403

A_, B_, C_ = np.array([-2.6, -1.9, 0.0]), np.array([2.6, -1.9, 0.0]), np.array([0.0, 2.6, 0.0])


def place(p, shift=ORIGIN, scale: float = 1.0) -> np.ndarray:
    """A rhythm of three intervals (fractions that add to one) as a point of a triangle."""
    return (p[0] * A_ + p[1] * B_ + p[2] * C_) * scale + shift


def triangle(shift=ORIGIN, scale: float = 1.0) -> VGroup:
    g = VGroup(Polygon(A_ * scale + shift, B_ * scale + shift, C_ * scale + shift, color=GREY_C, stroke_width=2))
    for v, t, d in ((A_, r"first interval long", DOWN), (B_, r"second long", DOWN), (C_, r"third long", UP)):
        g.add(label(t, font_size=20, color=GREY_B).next_to(v * scale + shift, d, buff=0.12))
    return g


def cloud(points, shift=ORIGIN, scale: float = 1.0, color=WHITE, radius: float = 0.035) -> VGroup:
    return VGroup(*[Dot(place(p, shift, scale), radius=radius, color=color, fill_opacity=0.8) for p in points])


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ what the listener expects", r"Are the simple ratios in the music, \ or in us?", extra=((2017, r"rhythms by the telephone game"),),
                spoken="Chapter 10. The frontier: what the listener expects.")
        self.game()
        self.two()
        self.animals()
        self.open()

    # ------------------------------------------------------------------
    def game(self):
        d = load("frontier")
        c = clip("frontier.chain")
        sh = LEFT * 3.4 + DOWN * 0.2
        tri = triangle(sh)
        pk = np.asarray(d["peaks"])
        marks = VGroup(*[Circle(radius=0.11, color=TUNE, stroke_width=1.5).move_to(place(p, sh)) for p in pk[:7]])
        names = VGroup(*[label(":".join(str(x) for x in r), font_size=18, color=TUNE).next_to(place(p, sh), UP, buff=0.14) for r, p in list(zip(d["ratios"], pk))[:7]])
        seeds = cloud(np.asarray(d["a"])[0], sh, color=GREY_B)
        steps = VGroup(label(r"1 \ \ play a random rhythm of three intervals", font_size=26, color=GREY_A), label(r"2 \ \ the listener taps it back", font_size=26, color=GREY_A),
                       label(r"3 \ \ play the tapping to the listener; \ repeat", font_size=26, color=GREY_A),
                       label(r"errors pile up in the direction \\ of what the listener expects", font_size=26, color=EAR)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.3 + UP * 0.6)
        with self.voiceover(
            "Simple ratios everywhere: two to one, three to two. Are they in the music, or in us? One "
            "way to ask is a game of telephone, invented for rhythm by Nori Jacoby and Josh McDermott. "
            "<bookmark mark='a'/> Play a listener a rhythm of three intervals, chosen at random. Every "
            "such rhythm is a point in this triangle: near a corner, one interval is long; in the "
            "middle, all three are equal. <bookmark mark='b'/> The listener taps it back, not quite "
            "right. <bookmark mark='c'/> Play the tapping to the listener as the next rhythm, and go "
            "round again. <bookmark mark='d'/> Each time, the errors lean toward what the listener "
            "expects a rhythm to be. After a few rounds the rhythm has drifted to one of those "
            "expectations. Here is a simulated listener, and one rhythm going down the chain."
        ) as vo:
            self.play(FadeIn(tri))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), LaggedStart(*[FadeIn(s) for s in seeds], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]), FadeIn(marks), FadeIn(names))
        chain = np.asarray(d["chain"])
        dot = Dot(place(chain[0], sh), radius=0.12, color=BAD)
        trail = VGroup()
        self.play(seeds.animate.set_opacity(0.25), FadeIn(dot))
        with self.listen(c) as snd:
            window(snd, r"one rhythm, \ rounds 0, 1, 2 and 5", detail=r"a clave, \ modelled; \ a simulated chain", corner=DL, tag_corner=DR)
            for j, k in enumerate(d["rounds_heard"]):
                snd.wait_until(d["starts"][j])
                if j:
                    seg = Line(dot.get_center(), place(chain[k], sh), color=BAD, stroke_width=2)
                    trail.add(seg)
                    self.play(Create(seg), dot.animate.move_to(place(chain[k], sh)), run_time=0.5)
                t0 = d["starts"][j]
                snd.drive(dot, lambda m, t, t0=t0: m.set_fill(opacity=0.55 + 0.45 * np.cos(14 * (t - t0))))
        end = ":".join(str(x) for x in d["chain_end"])
        with self.voiceover(
            f"It began as a lopsided rhythm, with intervals of {say(round(d['chain_start_ms'][0], -1))}, "
            f"{say(round(d['chain_start_ms'][1], -1))} and {say(round(d['chain_start_ms'][2], -1))} milliseconds. Five rounds "
            f"later it is {say(round(d['chain_end_ms'][0], -1))}, {say(round(d['chain_end_ms'][1], -1))} and "
            f"{say(round(d['chain_end_ms'][2], -1))}: very nearly two to one to one. Nobody told the listener to "
            "tidy it."
        ):
            self.play(Indicate(dot, color=TUNE, scale_factor=1.6))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two(self):
        d = load("frontier")
        a = np.asarray(d["a"])
        L, Rr = LEFT * 3.4 + DOWN * 0.5, RIGHT * 3.4 + DOWN * 0.5
        ta, tb = triangle(L, 0.85), triangle(Rr, 0.85)
        start_a, start_b = cloud(a[0], L, 0.85, GREY_B), cloud(a[0], Rr, 0.85, GREY_B)
        end_a, end_b = cloud(a[5], L, 0.85, TUNE), cloud(np.asarray(d["b5"]), Rr, 0.85, LOW)
        la = label(r"listener A", font_size=28, color=TUNE).next_to(ta, UP, buff=0.5)
        lb = label(r"listener B", font_size=28, color=LOW).next_to(tb, UP, buff=0.5)
        toy = label(r"a simulation: \ these two listeners' expectations were put in by hand", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now do that with two hundred random rhythms at once, for two simulated listeners who expect "
            "different things. <bookmark mark='a'/> After five rounds the cloud has collapsed into "
            "clusters, and the clusters show what each listener expects: for A, rhythms made of ones and "
            "twos; for B, rhythms with a three in them. <bookmark mark='b'/> That is a toy, and we put "
            "the expectations in by hand. The real experiment reads them out of real people. In 2017 it "
            "was run with listeners in Boston and with the Tsimane, in the Bolivian Amazon. In 2024 it "
            "was run with thirty-nine groups of people in fifteen countries. <bookmark mark='c'/> Every "
            "group had clusters, and the clusters were at ratios of small whole numbers. But which "
            "ratios were strongest differed from group to group, and matched the music each group knew. "
            "The grid of small ratios seems to be common to people. Where each culture puts its weight "
            "on that grid is learned."
        ) as vo:
            self.play(FadeIn(ta), FadeIn(tb), FadeIn(la), FadeIn(lb), FadeIn(start_a), FadeIn(start_b), FadeIn(toy))
            vo.wait_until("a")
            self.play(*[s.animate.move_to(e) for s, e in zip(start_a, end_a)], *[s.animate.move_to(e) for s, e in zip(start_b, end_b)], run_time=3.0)
            self.play(start_a.animate.set_color(TUNE), start_b.animate.set_color(LOW))
            vo.wait_until("c")
            found = label(r"Jacoby and others (2024): \ 39 groups, \ 15 countries. \ Small whole-number ratios everywhere; \ which ones, \ by culture.", font_size=24, color=LIMIT).to_edge(UP, buff=0.3)
            self.play(FadeIn(found))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def animals(self):
        head = label(r"Who else keeps a beat?", font_size=36, color=LIMIT).to_edge(UP, buff=0.5)
        rows = rows_card([
            (r"a cockatoo, \\ 2009", r"Snowball danced to pop songs, \ and when the music was sped up \\ or slowed down, \ he changed the speed of his dancing to match."),
            (r"a sea lion, \\ 2013", r"Ronan was trained to bob her head to a metronome, \\ and then kept the beat of music she had never heard."),
            (r"apes and \\ monkeys", r"our nearest relatives do it poorly, \ if at all: \\ they tap after the beat, \ reacting to it, \ not ahead of it."),
        ], left=-6.2, text_left=-2.8, top=1.4, step=1.5, name_size=28, text_size=25, color=LIMIT)
        with self.voiceover(
            "And who else keeps a beat? For a long time the answer seemed to be nobody. "
            "<bookmark mark='a'/> Then, in 2009, a cockatoo named Snowball was tested. He danced to pop "
            "songs, and when the experimenters sped the music up or slowed it down, he adjusted. "
            "<bookmark mark='b'/> In 2013 a sea lion named Ronan was trained to bob her head to a "
            "metronome, and then kept time to music she had never heard. <bookmark mark='c'/> Monkeys "
            "and apes, our nearest relatives, do it poorly: their taps follow the beat instead of "
            "anticipating it. Predicting a beat is rare among animals, and why these animals can, and "
            "those cannot, is argued over."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        head = label(r"What is not known", font_size=38, color=LIMIT).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"where the ratios \\ come from", r"from the ear's and the body's own clocks, \ or from the music heard since birth? \\ The telephone game shows the expectations, \ not their source."),
            (r"microtiming \\ and groove", r"do notes played a few milliseconds off the grid make music feel better? \\ Players say yes; \ several listening experiments have found no, \ or the reverse."),
            (r"why we move", r"syncopation and the urge to move make an arch; \ why the body should \\ enjoy filling in a missing beat is an open question."),
            (r"machines", r"finding the beat of a pop song is nearly solved; \ finding the metre of a \\ Balkan dance, \ or of a free solo, \ is not. \ Part 62 takes this up."),
        ], left=-6.5, text_left=-2.9, top=1.9, step=1.42, name_size=26, text_size=23, color=LIMIT)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "What is not known is a good deal. <bookmark mark='a'/> Where the small ratios come from: "
            "from the timing machinery of ears and limbs, or from the music a child hears from birth. "
            "The telephone game shows the expectations. It cannot show their source. "
            "<bookmark mark='b'/> Whether microtiming matters. Players are sure that notes placed a few "
            "milliseconds off the grid give music its feel. Several careful listening experiments have "
            "found that listeners prefer the exact version, or cannot tell. Both may be true of "
            "different music. <bookmark mark='c'/> Why we move at all. Syncopation and the urge to move "
            "make an arch, but nobody can yet say why a body should enjoy supplying a missing beat. "
            "<bookmark mark='d'/> And machines. Finding the beat of a pop song is nearly a solved "
            "problem. Finding the meter of a Balkan dance, or the pulse of a free solo, is not, and we "
            "return to that in Part 62."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
