from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403

SC = {"explore": TUNE, "danger": BLUE, "combat": EAR, "victory": "#A3E635"}


class Games(SoundScene):
    def construct(self):
        chapter(self, 7, r"Music for play", r"How do you score a scene of unknown length?")
        self.history()
        self.techniques()
        self.machine()
        self.switch()
        self.layers()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"\textit{Space Invaders} \ (1978): \ a four-note bass loop that speeds up as the invaders descend", WHITE),
            (r"LucasArts' iMUSE \ (Land and McConnell, \ 1991): \ the score changes cue at musically sensible moments", WHITE),
            (r"a film cue has a known length; \ a game state lasts as long as the player takes", WHITE),
            (r"so game music is built from pieces and rules: \ the score is a program", TUNE),
            (r"Part 42's dice game, \ two centuries later, \ with a player rolling the dice", GREY_A),
        ]
        rows_scene(self, r"from loops to systems", items,
                   "Game music started as loops. <bookmark mark='b'/> Space Invaders, in 1978, played a four-note bass loop that "
                   "sped up as the invaders came down. <bookmark mark='c'/> By 1991 LucasArts' iMUSE system, designed by Michael "
                   "Land and Peter McConnell, changed cue at musically sensible moments as the player moved through a scene. "
                   "<bookmark mark='d'/> The problem is simple: a film cue has a known length, but a game state lasts as long as "
                   "the player takes. <bookmark mark='e'/> So game music is built from pieces and rules, and the score is a "
                   "program: <bookmark mark='f'/> Part 42's dice game, two centuries later, with a player rolling the dice.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def techniques(self):
        items = [
            (r"horizontal resequencing: \ short segments that can follow one another in any allowed order", WHITE),
            (r"vertical layering: \ stems that play together and fade in or out with intensity", WHITE),
            (r"transitions: \ wait for the next beat, \ bar or phrase, \ or cut at once with a bridging phrase", WHITE),
            (r"stingers: \ short phrases fired at events, \ over whatever is playing", TUNE),
            (r"middleware such as FMOD and Wwise lets composers build these rules without code", GREY_A),
        ]
        rows_scene(self, r"the techniques", items,
                   "Four techniques do most of the work. <bookmark mark='b'/> Horizontal resequencing: short segments that can "
                   "follow one another in any allowed order. <bookmark mark='c'/> Vertical layering: stems that play together and "
                   "fade in or out with the intensity. <bookmark mark='d'/> Transitions: wait for the next beat, bar or phrase, "
                   "or cut at once with a bridging phrase. <bookmark mark='e'/> And stingers: short phrases fired at events, over "
                   "whatever is playing. <bookmark mark='f'/> Middleware such as FMOD and Wwise lets composers build such rules "
                   "without writing code.", marks="bcdef")

    # ------------------------------------------------------------------
    def machine(self):
        pos = {"explore": [-3.6, 0.9, 0], "danger": [0.0, 1.9, 0], "combat": [3.6, 0.9, 0], "victory": [0.0, -1.0, 0]}
        nodes = VGroup()
        for s, p in pos.items():
            nodes.add(VGroup(RoundedRectangle(width=2.4, height=0.9, corner_radius=0.2, stroke_color=SC[s], fill_color=SC[s], fill_opacity=0.15, stroke_width=3),
                             label(s, font_size=22, color=WHITE)).arrange(ORIGIN).move_to(p))
        idx = {s: i for i, s in enumerate(pos)}
        edges = [("explore", "danger", r"enemy seen"), ("danger", "combat", r"attacked"), ("danger", "explore", r"lost them"),
                 ("combat", "victory", r"enemy beaten"), ("victory", "explore", r"after 3 s")]
        arrows = VGroup()
        for a, b, t in edges:
            A, B = nodes[idx[a]], nodes[idx[b]]
            ar = Arrow(A.get_center(), B.get_center(), buff=0.55, color=GREY_B, stroke_width=3)
            if (a, b) == ("danger", "explore"):
                ar.shift(DOWN * 0.25 + LEFT * 0.1)
            arrows.add(VGroup(ar, label(t, font_size=15, color=GREY_A).move_to(ar.get_center() + (UP * 0.25 if (a, b) != ("danger", "explore") else DOWN * 0.3))))
        cap = VGroup(label(r"each state: \ a two-bar segment in its own key and texture, \ looped", font_size=18, color=WHITE),
                     label(r"intensity: \ 1 to 4 layers \ (pad, \ bass, \ drums, \ the motive in the brass)", font_size=18, color=WHITE),
                     label(r"each change: \ a stinger at once; \ the new segment at the next bar line", font_size=18, color=TUNE)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        head = label(r"our adaptive score, \ as a state machine", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is our adaptive score as a state machine. <bookmark mark='a'/> The game has four states: exploring, "
            "danger when an enemy is seen, combat when it attacks, and victory, which lasts three seconds before exploring "
            "again. <bookmark mark='b'/> Each state has a two-bar segment in its own key and texture, looped for as long as "
            "the state lasts. Intensity, which rises and falls smoothly with the state, chooses one to four layers: a pad, a "
            "bass, drums, and the motive in the brass. At each change a stinger sounds at once, and the new segment starts "
            "at the next bar line."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(nodes).copy().set_opacity(0.15)))
            vo.wait_until("a")
            self.play(FadeIn(nodes), LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layers(self):
        items = [
            (r"these simple layers share tempo, harmonic plan and bar length", WHITE),
            (r"segments must join: \ each ends where any allowed successor can begin \ (the dice game's trick)", WHITE),
            (r"intensity changes on beat boundaries, \ so a layer never enters mid-note", WHITE),
            (r"the composer writes the pieces and the joins; \ the game decides the order", TUNE),
            (r"chapter 8: \ a game played, \ and its score heard", GREY_A),
        ]
        rows_scene(self, r"what makes it work", items,
                   "What makes such a score work? <bookmark mark='b'/> These simple layers share tempo, harmonic plan and bar length; other adaptive systems can reconcile polymeter, changing keys or asynchronous textures. <bookmark mark='c'/> Segments must join: each ends where any allowed successor can begin, the dice game's trick again. <bookmark mark='d'/> Intensity changes only on beat boundaries, which aligns entries to the selected grid, though held notes can still cross that boundary. <bookmark mark='e'/> The composer writes the pieces and the joins; the game decides the order. <bookmark mark='f'/> Chapter eight plays a game and lets us hear its score.", marks="bcdef")

    # ------------------------------------------------------------------
    def switch(self):
        d = load("switch")
        c = clip("switch.two")
        boxes = VGroup(*[VGroup(RoundedRectangle(width=4.6, height=1.3, corner_radius=0.15, stroke_color=GREY_B),
                                label(t, font_size=21, color=WHITE)).arrange(ORIGIN) for t in (r"switch at once", r"switch at the bar, \ with a stinger")]).arrange(RIGHT, buff=0.8).move_to(UP * 1.2)
        x0, W = -5.0, 10.0
        line = Line([x0, -1.2, 0], [x0 + W, -1.2, 0], color=GREY_D)
        bars = VGroup(*[Line([x0 + W * k * d["bar"] / 10, -1.35, 0], [x0 + W * k * d["bar"] / 10, -1.05, 0], color=GREY_B) for k in range(6)])
        ev = VGroup(Line([x0 + W * d["event"] / 10, -1.6, 0], [x0 + W * d["event"] / 10, -0.8, 0], color=EAR, stroke_width=4),
                    label(rf"combat starts: \ {d['event']:.1f} s", font_size=15, color=EAR).move_to([x0 + W * d["event"] / 10, -0.55, 0]))
        sw = d["cases"]["at the bar, with a stinger"]
        nb = VGroup(DashedLine([x0 + W * sw["switch"] / 10, -1.6, 0], [x0 + W * sw["switch"] / 10, -0.8, 0], color=TUNE),
                    label(rf"next bar: \ {sw['switch']:.1f} s \ ({sw['delay']:.1f} s later)", font_size=15, color=TUNE).move_to([x0 + W * sw["switch"] / 10, -1.95, 0]))
        cap = label(r"bar lines every 2 s at 120 beats a minute", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Hear the difference one transition makes. The player is exploring; at five point three seconds, combat "
            "starts. First the music switches at once, wherever it happens to be. Then it waits for the next bar line, "
            "with a stinger at the moment combat begins."
        ):
            self.play(FadeIn(boxes), FadeIn(line), FadeIn(bars), FadeIn(ev), FadeIn(nb), FadeIn(cap))
        st = d["starts"]
        ks = list(d["cases"])
        with self.listen(c) as snd:
            window(snd, r"one change, \ twice", kind="synthesized", detail=r"orchestra, \ piano, \ bass, \ drums", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st[ks[0]], st[ks[1]] - 0.4, buff=0.1)
            pulse(snd, boxes[1], st[ks[1]], c.duration, buff=0.1)
        with self.voiceover(
            "The first lurches: the new segment cuts in mid-bar. The second keeps the old music for "
            f"{say(sw['delay'], 1)} seconds, but the stinger marks the moment, and the change lands on a downbeat."
        ):
            self.play(Indicate(boxes[1]))
        self.wait(0.4)
        self.clear_scene()
