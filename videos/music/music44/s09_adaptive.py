from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403

SC = {"explore": TUNE, "danger": BLUE, "combat": EAR, "victory": "#A3E635"}


class Adaptive(SoundScene):
    def construct(self):
        chapter(self, 8, r"An adaptive score, \ played", r"What does a game's score sound like as it happens?")
        self.play_game()
        self.delays()
        self.playtest()
        self.tradeoff()

    # ------------------------------------------------------------------
    def timeline(self, d, x0=-6.0, W=12.0):
        L = d["length"]
        def X(t):
            return x0 + W * t / L
        bands = VGroup()
        times = d["times"] + [L]
        for i, s in enumerate(d["states"]):
            a, b = times[i], times[i + 1]
            bands.add(Rectangle(width=X(b) - X(a), height=0.55, stroke_width=0, fill_color=SC[s], fill_opacity=0.55).move_to([(X(a) + X(b)) / 2, 1.6, 0]))
        names = VGroup(*[label(s, font_size=13, color=WHITE).move_to(bands[i]) for i, s in enumerate(d["states"]) if times[i + 1] - times[i] > 2.5])
        inten = np.array(d["intensity"])
        il = VMobject(color=WHITE, stroke_width=2).set_points_as_corners([[X(i * d["grid"]), 0.2 + 0.8 * v, 0] for i, v in enumerate(inten)])
        lay = np.array(d["layers"])
        lbars = VGroup()
        for k in range(1, 5):
            y = -1.75 + 0.42 * (k - 1)
            segs = VGroup()
            on = lay >= k
            i = 0
            while i < len(on):
                if on[i]:
                    j = i
                    while j + 1 < len(on) and on[j + 1]:
                        j += 1
                    segs.add(Rectangle(width=max(X((j + 1) * d["grid"]) - X(i * d["grid"]), 0.02), height=0.3, stroke_width=0,
                                       fill_color=[TUNE, BLUE, EAR, "#A3E635"][k - 1], fill_opacity=0.8).move_to([(X(i * d["grid"]) + X((j + 1) * d["grid"])) / 2, y, 0]))
                    i = j + 1
                else:
                    i += 1
            lbars.add(segs)
        lnames = VGroup(*[label(t, font_size=13, color=GREY_A).move_to([x0 - 0.45, -1.75 + 0.42 * k, 0]) for k, t in enumerate((r"pad", r"bass", r"drums", r"brass"))])
        sw = VGroup()
        for s in d["switches"][1:]:
            sw.add(VGroup(Line([X(s["event"]), 1.95, 0], [X(s["event"]), 1.25, 0], color=WHITE, stroke_width=2),
                          DashedLine([X(s["switch"]), 1.25, 0], [X(s["switch"]), -2.0, 0], color=GREY_B, stroke_width=1.5)))
        tl = VGroup(label(r"game state", font_size=14, color=GREY_A).move_to([x0 - 0.6, 1.6, 0]), label(r"intensity", font_size=14, color=GREY_A).move_to([x0 - 0.6, 0.6, 0]))
        g = VGroup(bands, names, il, lbars, lnames, sw, tl)
        g.X = X
        return g

    def play_game(self):
        d = load("game")
        c = clip("game.play")
        g = self.timeline(d)
        head = label(r"48 seconds of a simulated game, \ and its score", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        cap = label(r"white ticks: \ state changes \ (a stinger sounds); \ dashed: \ the next bar line, \ where the segment changes", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is forty-eight seconds of a simulated game. Across the top, its states; below, the intensity, and the four "
            "layers as they come and go. The white ticks are state changes, where a stinger sounds; the dashed lines are the "
            "next bar lines, where the new segment begins. Listen for the music following the game."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        ph = Line([g.X(0), 2.0, 0], [g.X(0), -2.1, 0], color=WHITE, stroke_width=3)
        big = label(d["states"][0], font_size=30, color=SC[d["states"][0]]).to_corner(UR, buff=0.4)
        with self.listen(c) as snd:
            window(snd, r"the game's score", kind="synthesized", detail=r"orchestra, \ piano, \ bass, \ drums", corner=DL, tag_corner=DR)
            snd.show(ph)
            snd.drive(ph, lambda m, now: m.move_to([g.X(min(now, d["length"])), 0.0, 0]))
            labels_ = {s: label(s, font_size=30, color=SC[s]).to_corner(UR, buff=0.4) for s in set(d["states"])}
            for s, lb in labels_.items():
                snd.show(lb)
                def upd(m, now, s=s):
                    i = max(k for k, t in enumerate(d["times"]) if t <= now + 1e-9)
                    m.set_opacity(1.0 if d["states"][i] == s else 0.0)
                snd.drive(lb, upd)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def delays(self):
        q = load("quantise")["quantise"]
        g = load("game")
        x0, W = -2.0, 6.5
        mx = 2.2
        bars = VGroup()
        names = {"now": r"at once", "beat": r"next beat", "bar": r"next bar", "phrase": r"next phrase \ (2 bars)"}
        for i, k in enumerate(("now", "beat", "bar", "phrase")):
            v = q[k]["mean"]
            w = W * v / mx
            y = 1.3 - 0.75 * i
            bars.add(VGroup(label(names[k], font_size=20, color=WHITE).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT),
                            Rectangle(width=max(w, 0.04), height=0.42, stroke_width=0, fill_color=TUNE, fill_opacity=0.85).move_to([x0 + w / 2, y, 0]),
                            label(rf"{v:.2f} s \ (theory {q[k]['expected']:.2f}; \ worst {q[k]['max']:.2f})", font_size=16, color=WHITE).move_to([x0 + w + 0.3, y, 0], aligned_edge=LEFT)))
        cap = label(rf"mean delay from a state change to the new music, \ {q['now']['n']:,} changes in 200 simulated games, \ 120 beats a minute", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.7)
        head = label(r"what waiting for the bar line costs", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Waiting for a musical boundary costs time. <bookmark mark='a'/> Over two hundred simulated games, a change "
            "waits on average a quarter of a second for the next beat, a second for the next bar, and two seconds for the next "
            "phrase. Theory predicts exactly half the boundary's length, because changes arrive at random moments. The worst "
            "case is the whole length: almost four seconds of the wrong music for a phrase. In our game the bar-line delay "
            f"averaged {say(g['mean_delay'], 2)} seconds; the stinger covers it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tradeoff(self):
        items = [
            (r"switch at once: \ responsive, \ but the music lurches mid-phrase", WHITE),
            (r"switch at the phrase: \ musical, \ but a fight can start in peaceful music", WHITE),
            (r"the usual answer: \ a stinger now, \ the full change at the next bar", WHITE),
            (r"the choice depends on the game: \ a rhythm game must be exact, \ an exploration game can wait", TUNE),
            (r"chapter 9: \ the machines that played the first game music", GREY_A),
        ]
        rows_scene(self, r"responsive or musical?", items,
                   "So every adaptive score trades responsiveness against musicality. <bookmark mark='b'/> Switch at once and the "
                   "music lurches mid-phrase. <bookmark mark='c'/> Switch at the phrase and a fight can start in peaceful music. "
                   "<bookmark mark='d'/> The usual answer is ours: a stinger now, and the full change at the next bar. "
                   "<bookmark mark='e'/> The right choice depends on the game: a rhythm game must be exact, an exploration game "
                   "can wait. <bookmark mark='f'/> Chapter nine turns to the machines that played the first game music.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def playtest(self):
        items = [
            (r"an adaptive score cannot be heard whole: \ every playthrough is a different piece", WHITE),
            (r"so it is tested by playing: \ hours of sessions, \ listening for wrong music and bad joins", WHITE),
            (r"logs of game states let a team replay the score's decisions offline, \ as we just did", WHITE),
            (r"repetition is the enemy: \ players hear the same loop for hours, \ so segments get variants", TUNE),
            (r"the composer becomes a designer of possibilities", GREY_A),
        ]
        rows_scene(self, r"testing a score you cannot hear whole", items,
                   "An adaptive score raises a strange problem. <bookmark mark='b'/> It can never be heard whole: every "
                   "playthrough is a different piece. <bookmark mark='c'/> So it is tested by playing, hours of sessions, "
                   "listening for wrong music and bad joins, <bookmark mark='d'/> and logs of game states let a team replay the "
                   "score's decisions offline, as we just did. <bookmark mark='e'/> Repetition is the enemy: players can hear the "
                   "same loop for hours, so segments get variants. <bookmark mark='f'/> The composer becomes a designer of "
                   "possibilities.", marks="bcdef")
