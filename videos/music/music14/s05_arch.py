from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Arch(SoundScene):
    def construct(self):
        chapter(self, 4, r"The arch", r"What shape is a phrase?", extra=((1996, r"Huron's melodic arch"),))
        self.ode()
        self.average()
        self.peak()

    # ------------------------------------------------------------------
    def ode(self):
        d = load("arch")
        c = clip("arch.ode")
        o = d["ode"]
        r = roll(o["pitches"], o["beats"], width=11.0, height=2.6, lines=(0,), phrase_ends=o["phrase_ends"], color=TUNE).move_to(UP * 0.5)
        head = label(r"two phrases of Beethoven's \textit{Ode to Joy}", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Melodies come in phrases, each about one breath long. Here are two phrases of Beethoven's "
            "Ode to Joy. Watch the shape of each."
        ):
            self.play(FadeIn(head), FadeIn(r))
        with self.listen(c) as snd:
            window(snd, r"two phrases", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, r, d["times"])
        e = o["phrase_ends"][0]
        arcs = VGroup()
        for a, b in ((0, e), (e, len(o["pitches"]))):
            xs = [r.notes[k].get_center()[0] for k in range(a, b)]
            ys = [r.notes[k].get_center()[1] + 0.35 for k in range(a, b)]
            arcs.add(VMobject(color=EAR, stroke_width=4).set_points_smoothly([np.array([x, y, 0.0]) for x, y in zip(xs, ys)]))
        cap = label(r"up, \ and back down; \ and a second, \ smaller arch", font_size=30, color=EAR).to_edge(DOWN, buff=0.9)
        with self.voiceover("Up, and back down. And then a second, smaller arch, which stops one step short of home."):
            self.play(Create(arcs[0]), run_time=1.2)
            self.play(Create(arcs[1]), FadeIn(cap), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def average(self):
        d = load("arch")
        sh = d["shapes"]
        names = ["falling", "arch", "rising", "valley"]
        ch = columns([sh[n] for n in names], names, width=5.0, height=2.2, color=WEAK, hot=(1,), hot_color=TUNE, fmt="{:.0f}", font_size=24).move_to(LEFT * 3.8 + DOWN * 0.9)
        g = axes([0, 8], [-1.2, 0.8], x_length=5.6, y_length=3.0, xlabel=r"from the start of a phrase to its end", ylabel=r"semitones above the phrase's mean", yticks=[-1, 0], font_size=20).move_to(RIGHT * 3.3 + DOWN * 0.7)
        faint = VGroup(*[curve_from(g, np.arange(9), np.clip(s, -1.2, 0.8), WEAK, stroke_width=1).set_stroke(opacity=0.25) for s in d["sample"][:24]])
        mean = curve_from(g, np.arange(9), d["arch"], TUNE, stroke_width=5)
        head = label(rf"the shapes of {d['phrases']} phrases", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"Is that typical? Our tunes have {say(d['phrases'])} phrases. Sort each one by comparing "
            "its first note, the average of its middle, and its last note. <bookmark mark='a'/> The "
            f"commonest shapes are falling, {say(sh['falling'])}, and the arch, {say(sh['arch'])}. Then "
            f"rising, {say(sh['rising'])}. The valley, down and then up, is the rarest of the four."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch))
        with self.voiceover(
            "Now average all the phrases together. <bookmark mark='a'/> What emerges is an arch: up by "
            "about a semitone in the first third, then down, ending half a semitone below where it "
            "began. David Huron found the same arch in 1996, in six thousand European folk songs. "
            "<bookmark mark='b'/> Speech does it too. The pitch of a spoken sentence drifts downward as "
            "the air in the lungs runs out. A phrase of melody is shaped like a breath: it rises as it "
            "sets out, and it sinks as it ends."
        ) as vo:
            self.play(FadeIn(g), FadeIn(faint))
            vo.wait_until("a")
            self.play(Create(mean), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(label(r"a phrase is shaped like a breath", font_size=30, color=TUNE).next_to(head, DOWN, buff=0.3)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def peak(self):
        d = load("more")["peak"]
        ch = columns(d["fifths"], [r"first fifth", r"second", r"third", r"fourth", r"last fifth"], width=8.0, height=2.4, color=WEAK, hot=(0,), hot_color=TUNE, fmt="{:.0f}", font_size=22).move_to(DOWN * 1.0)
        xl = label(r"where in the tune its highest note first arrives", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        head = label(r"``save the high note for two thirds of the way through''?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(rf"in the middle tune, \ a quarter of the way through; \ {d['second_half']} of {d['of']} wait for the second half", font_size=26, color=WHITE).next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Here is a piece of advice that is often given with the arch: save the highest note of a "
            "melody for about two thirds of the way through. Test it. <bookmark mark='a'/> In our "
            "tunes, the top note first arrives, in the middle case, only a quarter of the way through. "
            f"In {say(d['fifths'][0])} of the {say(d['of'])} it comes in the first fifth of the tune, "
            f"and only {say(d['second_half'])} wait until the second half. These tunes climb early, and "
            "spend the rest of their time coming down. The advice may suit a symphony. It does not "
            "describe the songs that everyone knows."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(xl), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
