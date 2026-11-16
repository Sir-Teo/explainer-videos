from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403


class Quartet(SoundScene):
    def construct(self):
        chapter(self, 7, r"Quartets and conductors", r"Who leads a string quartet?")
        self.wing()
        self.two()
        self.hear()
        self.conductor()
        self.beyond()

    # ------------------------------------------------------------------
    def wing(self):
        items = [
            (r"Wing, \ Endo, \ Bradbury and Vorberg \ (2014) \ recorded two professional string quartets", WHITE),
            (r"from every note's onset they estimated each player's correction to each other player: \ a 4 $\times$ 4 matrix", WHITE),
            (r"one quartet was `autocratic': \ the first violin corrected little, \ the others corrected towards it", WHITE),
            (r"the other was `democratic': \ everyone corrected towards everyone", TUNE),
            (r"both stayed together; \ they differed in who adjusts", GREY_A),
        ]
        rows_scene(self, r"two quartets, \ measured", items,
                   "In 2014 Alan Wing, Satoshi Endo, Adrian Bradbury and Dirk Vorberg recorded two professional string quartets. "
                   "<bookmark mark='b'/> From every note's onset they estimated how much each player corrected towards each "
                   "other player: a four by four matrix of alphas. <bookmark mark='c'/> One quartet was, in their word, "
                   "autocratic: the first violin corrected little, and the others corrected towards the first violin. "
                   "<bookmark mark='d'/> The other was democratic: everyone corrected towards everyone. <bookmark mark='e'/> Both "
                   "stayed together. They differed in who does the adjusting.", marks="bcde")

    # ------------------------------------------------------------------
    def net(self, M, title, col):
        names = [r"vn 1", r"vn 2", r"va", r"vc"]
        pos = [np.array(p) for p in ([0, 1.2, 0], [1.3, 0, 0], [0, -1.2, 0], [-1.3, 0, 0])]
        nodes = VGroup(*[VGroup(Circle(radius=0.32, color=col, fill_color=col, fill_opacity=0.3), label(n, font_size=16, color=WHITE)).move_to(p) for n, p in zip(names, pos)])
        arrows = VGroup()
        for i in range(4):
            for j in range(4):
                a = M[i][j]
                if i == j or a < 0.02:
                    continue
                d = pos[j] - pos[i]
                u = d / np.linalg.norm(d)
                perp = np.array([-u[1], u[0], 0]) * 0.1
                arrows.add(Arrow(pos[i] + 0.38 * u + perp, pos[j] - 0.38 * u + perp, buff=0, stroke_width=1 + 14 * a, color=col,
                                 max_tip_length_to_length_ratio=0.12))
        return VGroup(label(title, font_size=20, color=col), VGroup(arrows, nodes)).arrange(DOWN, buff=0.35)

    def two(self):
        d = load("quartet")
        a = self.net(d["democratic"]["M"], r"democratic", TUNE)
        b = self.net(d["autocratic"]["M"], r"autocratic", BLUE)
        g = VGroup(a, b).arrange(RIGHT, buff=2.2).move_to(UP * 0.3)
        sp = VGroup(label(rf"spread: \ {d['democratic']['spread_ms']:.0f} ms", font_size=18, color=TUNE).next_to(a, DOWN, buff=0.3),
                    label(rf"spread: \ {d['autocratic']['spread_ms']:.0f} ms", font_size=18, color=BLUE).next_to(b, DOWN, buff=0.3))
        cap = label(r"an arrow from A to B: \ A corrects towards B; \ thickness: \ how much \ (our models, \ not the measured values)", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"two model quartets", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are two model quartets of ours in that spirit. An arrow from one player to another means the first corrects "
            "towards the second, and its thickness says how much. <bookmark mark='a'/> In the democratic quartet every player "
            "corrects a little towards every other. <bookmark mark='b'/> In the autocratic one, the second violin, viola and "
            "cello correct strongly towards the first violin, which hardly listens back. <bookmark mark='c'/> Simulated over "
            f"four thousand beats, their average spread from earliest to latest player is almost the same, "
            f"{say(d['democratic']['spread_ms'])} and {say(d['autocratic']['spread_ms'])} milliseconds. The structure of "
            "listening differs; the togetherness does not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(sp))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def conductor(self):
        items = [
            (r"an orchestra is too large to listen around: \ sound takes 30 ms to cross ten metres", WHITE),
            (r"the conductor adds a shared visual reference; \ players still listen", WHITE),
            (r"studies of conductors' gestures find players lock to the bottom of the beat and to sharp changes in speed", WHITE),
            (r"orchestras still play slightly after the beat, \ by an amount each orchestra learns", TUNE),
            (r"the conductor also shapes tempo, \ balance and phrasing: \ the interpretation, \ not only the clock", GREY_A),
        ]
        rows_scene(self, r"the conductor", items,
                   "What about a full orchestra? <bookmark mark='b'/> It is too large to listen around: sound takes thirty milliseconds to cross ten metres, more than a duo's whole asynchrony. <bookmark mark='c'/> The conductor supplies a shared visual reference while players continue listening to one another. <bookmark mark='d'/> Studies of conductors' gestures find players lock to the lowest point of the beat and to sharp changes in the hand's speed. <bookmark mark='e'/> Orchestras still play slightly after the beat, by an amount each orchestra learns. <bookmark mark='f'/> And a conductor shapes tempo, balance and phrasing: the interpretation, not only the clock.", marks="bcdef")

    # ------------------------------------------------------------------
    def beyond(self):
        items = [
            (r"West African drumming \ (Part 37): \ players lock to a timeline, \ not to each other alone", WHITE),
            (r"jazz rhythm sections: \ the drummer and bassist hold slightly different places on the beat on purpose", WHITE),
            (r"duos clapping over a network \ (Chafe and colleagues, \ 2010): \ delays above about 25 ms make them slow down", WHITE),
            (r"machines that accompany a soloist must estimate the soloist's tempo and correct, \ like a partner", TUNE),
            (r"chapter 8: \ timing as a signature", GREY_A),
        ]
        rows_scene(self, r"other ways to stay together", items,
                   "Other traditions stay together in other ways. <bookmark mark='b'/> In West African drumming, Part 37, "
                   "players lock to a timeline, not only to each other. <bookmark mark='c'/> In jazz rhythm sections the "
                   "drummer and bassist hold slightly different places on the beat, on purpose. <bookmark mark='d'/> Duos clapping over a network, in Chris Chafe's experiments of 2010, slowed down steadily "
                   "once the delay passed about twenty-five milliseconds, each waiting for a partner who seemed late. "
                   "<bookmark mark='e'/> And machines that accompany a soloist must "
                   "estimate the soloist's tempo and correct, like a partner. <bookmark mark='f'/> Chapter eight treats timing "
                   "as a signature.", marks="bcdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("quartet")
        c = clip("quartet.two")
        a = self.net(d["democratic"]["M"], r"democratic", TUNE)
        b = self.net(d["autocratic"]["M"], r"autocratic", BLUE)
        g = VGroup(a, b).arrange(RIGHT, buff=2.2).move_to(UP * 0.3)
        cap = label(r"each player a piano voice, \ sixteen chords; \ can you tell which is which?", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Hear both, each player as one voice of a piano chord, sixteen chords each. Listen for any difference in how "
            "together they sound."
        ):
            self.play(FadeIn(g), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two quartets", detail=r"Part 7's piano, \ model players", corner=DL, tag_corner=DR)
            pulse(snd, a, st["democratic"], st["autocratic"] - 0.4, buff=0.15)
            pulse(snd, b, st["autocratic"], c.duration, buff=0.15)
        with self.voiceover(
            f"They are very hard to tell apart by ear: the spreads in these two clips are {say(d['democratic']['clip_spread_ms'])} and {say(d['autocratic']['clip_spread_ms'])} milliseconds. Similar onset spreads do not uniquely reveal leadership; estimating correction patterns requires a model and suitable data; that is why Wing and his colleagues had to estimate it."
        ):
            self.play(Indicate(a[0]), Indicate(b[0]))
        self.wait(0.4)
        self.clear_scene()
