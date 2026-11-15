from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403


class Animals(SoundScene):
    def construct(self):
        chapter(self, 8, r"Birds, \ whales and a cockatoo", r"Which parts of music do other animals share?")
        self.birds()
        self.whales()
        self.snowball()
        self.quiz()
        self.test()
        self.hypothesis()

    # ------------------------------------------------------------------
    def birds(self):
        items = [
            (r"songbirds learn their song from a tutor, \ in a sensitive period, \ as children learn speech", WHITE),
            (r"a zebra finch raised alone sings an abnormal song: \ too long notes, \ odd rhythm", WHITE),
            (r"Olga Feh\'er and colleagues \ (2009): \ young birds tutored by such isolates, \ then their pupils, \ and theirs", WHITE),
            (r"within three or four generations the song drifted back toward the wild type", TUNE),
            (r"iterated learning in birds: \ the species' song is a prior, \ rebuilt by transmission", GREY_A),
        ]
        rows_scene(self, r"song, \ learned", items,
                   "Song is not only human. <bookmark mark='b'/> Songbirds learn their song from a tutor during a sensitive "
                   "period, much as children learn speech. <bookmark mark='c'/> A zebra finch raised alone sings an abnormal "
                   "song, with notes held too long and an odd rhythm. <bookmark mark='d'/> In 2009 Olga Fehér and colleagues let "
                   "young birds learn from such isolates, then let their pupils tutor the next generation, and so on. "
                   "<bookmark mark='e'/> Within three or four generations the song drifted back toward the wild type. "
                   "<bookmark mark='f'/> It is chapter six's experiment, in birds: the species' song behaves like a prior, "
                   "rebuilt by transmission.", marks="bcdef")

    # ------------------------------------------------------------------
    def whales(self):
        items = [
            (r"Roger Payne and Scott McVay \ (1971): \ humpback whales sing long songs of repeated themes", WHITE),
            (r"all the males of a population sing nearly the same song, \ and it changes gradually over a season", WHITE),
            (r"Michael Noad and colleagues \ (2000): \ east Australian humpbacks abandoned their song for the west coast's", WHITE),
            (r"within two years every singer had switched: \ a cultural revolution, \ not evolution", TUNE),
            (r"the revolutions recur, \ and they spread eastward across the South Pacific", GREY_A),
        ]
        rows_scene(self, r"songs that sweep an ocean", items,
                   "Whales sing too. <bookmark mark='b'/> In 1971 Roger Payne and Scott McVay described the songs of humpback "
                   "whales: long sequences of repeated themes. <bookmark mark='c'/> All the males of a population sing nearly "
                   "the same song, and it changes gradually through a season. <bookmark mark='d'/> In 2000 Michael Noad and "
                   "colleagues reported that humpbacks off eastern Australia had abandoned their song for the one sung off the "
                   "west coast. <bookmark mark='e'/> Within two years every singer had switched: a revolution, not an "
                   "evolution. <bookmark mark='f'/> Such revolutions recur, and new songs spread eastward across the South "
                   "Pacific from one population to the next.", marks="bcdef")

    # ------------------------------------------------------------------
    def snowball(self):
        items = [
            (r"but singing is not keeping a beat: \ most animals cannot move in time to music", WHITE),
            (r"Snowball, \ a sulphur-crested cockatoo, \ bobbed his head to the Backstreet Boys", WHITE),
            (r"Aniruddh Patel and colleagues \ (2009) \ played him the song at tempos up to 20 per cent faster or slower", WHITE),
            (r"in bouts, \ he adjusted his bobbing to the new tempo, \ between stretches out of time", TUNE),
            (r"the question was statistical: \ is a dancer on the beat more often than chance?", GREY_A),
        ]
        rows_scene(self, r"a cockatoo on the beat", items,
                   "Keeping a beat is rarer. <bookmark mark='b'/> Most animals cannot move in time to music, but in 2007 a "
                   "video spread of Snowball, a sulphur-crested cockatoo, bobbing his head to the Backstreet Boys. "
                   "<bookmark mark='c'/> Aniruddh Patel and colleagues played him the song at tempos up to twenty per cent "
                   "faster or slower. <bookmark mark='d'/> In bouts, he adjusted his bobbing to the new tempo, between "
                   "stretches out of time. <bookmark mark='e'/> So the question became statistical: is a dancer on the beat "
                   "more often than chance would allow?", marks="bcde")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("beat")
        c = clip("beat.two")
        card = listen_card(r"A beat, \ twice, \ with a high tap for every head-bob of a simulated dancer. \ "
                           r"Both dancers bob at nearly the beat's tempo. \ Which one is on the beat?", width=10.4)
        with self.voiceover(
            "Your turn to judge. A rock beat, twice, with a high tap for every head-bob of a simulated dancer. Both dancers "
            "bob at nearly the beat's tempo. Which one is on the beat?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        n = d["beats"]
        P = d["period"]
        def lane(times, color):
            W = 11.0
            T = n * P
            base = Line(LEFT * W / 2, RIGHT * W / 2, color=GREY_B, stroke_width=1.5)
            beats = VGroup(*[Line(base.get_left() + RIGHT * W * k * P / T + UP * 0.25, base.get_left() + RIGHT * W * k * P / T + DOWN * 0.25, color=GREY_B, stroke_width=2) for k in range(n)])
            bobs = VGroup(*[Dot(base.get_left() + RIGHT * W * max(t, 0) / T + UP * 0.45, radius=0.07, color=color) for t in times])
            return VGroup(base, beats, bobs)
        a = lane(d["off"]["times"], BLUE)
        b = lane(d["on"]["times"], TUNE)
        g = VGroup(VGroup(label(r"first dancer", font_size=19, color=BLUE), a).arrange(DOWN, buff=0.2), VGroup(label(r"second dancer", font_size=19, color=TUNE), b).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.7).move_to(UP * 0.4)
        cap = label(r"grey ticks: \ the beat; \ dots: \ head-bobs", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        self.play(FadeOut(card), FadeIn(g), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two dancers", detail=r"Part 40's drums, \ a wood tap per bob", corner=DL, tag_corner=DR)
            flash(snd, list(a[2]), [st["first"] + max(t, 0) for t in d["off"]["times"]], hot=WHITE, base=BLUE)
            flash(snd, list(b[2]), [st["second"] + max(t, 0) for t in d["on"]["times"]], hot=WHITE, base=TUNE)
        with self.voiceover(
            "The second. The first dancer keeps its own tempo, a little faster than the beat, so it slides through every "
            "phase of the bar: sometimes on, mostly not. The second corrects toward each beat, as Part 43's players did, and "
            "stays close. By eye the two lanes can look alike; a little statistics tells them apart."
        ):
            self.play(Indicate(g[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def test(self):
        d = load("beat")
        s = d["stats"]
        ca = phase_circle(d["off"]["phases"], s["off"]["R"], s["off"]["mean"], color=BLUE)
        cb = phase_circle(d["on"]["phases"], s["on"]["R"], s["on"]["mean"], color=TUNE)
        def p_text(p):
            return rf"$p = {p:.2f}$" if p >= 0.01 else rf"$p \approx 10^{{{int(np.floor(np.log10(p)))}}}$"
        la = VGroup(label(r"first dancer", font_size=19, color=BLUE), label(rf"$R = {s['off']['R']:.2f}$, \ {p_text(s['off']['p'])}", font_size=19, color=WHITE)).arrange(DOWN, buff=0.12)
        lb = VGroup(label(r"second dancer", font_size=19, color=TUNE), label(rf"$R = {s['on']['R']:.2f}$, \ {p_text(s['on']['p'])}", font_size=19, color=WHITE)).arrange(DOWN, buff=0.12)
        g = VGroup(VGroup(ca, la).arrange(DOWN, buff=0.35), VGroup(cb, lb).arrange(DOWN, buff=0.35)).arrange(RIGHT, buff=2.2).move_to(DOWN * 0.1)
        eq = MathTex(r"R = \Big|\tfrac{1}{n}\textstyle\sum_k e^{i\theta_k}\Big|, \qquad p \approx e^{-nR^2}", font_size=34).to_edge(UP, buff=0.9)
        head = label(r"each bob as an angle: \ where in the beat it fell", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Turn each bob into an angle: where in the beat it fell, with the top of the circle exactly on the beat. "
            "<bookmark mark='a'/> Average the bobs as arrows of length one; the length of the average, R, is near zero if "
            "they scatter round the circle and near one if they cluster. Rayleigh's test asks how likely so long an average "
            f"would be by chance: roughly e to the minus n R squared. <bookmark mark='b'/> The first dancer: R of "
            f"{say(s['off']['R'], 2)}, a p-value of {say(s['off']['p'], 2)}: no evidence of a beat. <bookmark mark='c'/> The "
            f"second: R of {say(s['on']['R'], 2)}, and a p-value below one in a trillion. Patel's team used tests of this "
            "kind on Snowball's bouts, and found more synchrony than chance at several of the tempos."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(ca[0], ca[1], cb[0], cb[1])))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(FadeIn(ca[2]), GrowArrow(ca[3]) if isinstance(ca[3], Arrow) else FadeIn(ca[3]), FadeIn(la))
            vo.wait_until("c")
            self.play(FadeIn(cb[2]), GrowArrow(cb[3]) if isinstance(cb[3], Arrow) else FadeIn(cb[3]), FadeIn(lb))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hypothesis(self):
        items = [
            (r"Patel \ (2006): \ beat-keeping may need the brain circuits of vocal learning, \ which link hearing tightly to movement", WHITE),
            (r"vocal learners: \ humans, \ parrots, \ songbirds, \ whales and dolphins, \ seals, \ bats, \ elephants", WHITE),
            (r"parrots and elephants have been seen moving in time; \ our closest relatives, \ chimpanzees, \ rarely if ever", WHITE),
            (r"but Ronan, \ a California sea lion and no vocal learner, \ learned to bob in time \ (Peter Cook and colleagues, \ 2013)", TUNE),
            (r"perhaps vocal learning helps rather than being required: \ the test cases are still coming in", GREY_A),
        ]
        rows_scene(self, r"why a parrot?", items,
                   "Why a parrot, and not a dog or a chimpanzee? <bookmark mark='b'/> Patel proposed in 2006 that keeping a "
                   "beat may need the brain circuits of vocal learning, which tie hearing tightly to movement. "
                   "<bookmark mark='c'/> The vocal learners are humans, parrots, songbirds, whales and dolphins, seals, bats "
                   "and elephants. <bookmark mark='d'/> Parrots and elephants have been seen moving in time; chimpanzees, our "
                   "closest relatives, rarely if ever. <bookmark mark='e'/> But Ronan, a California sea lion and no vocal "
                   "learner, learned to bob in time to music, as Peter Cook and colleagues showed in 2013. "
                   "<bookmark mark='f'/> Perhaps vocal learning helps rather than being required; the test cases are still "
                   "coming in.", marks="bcdef")
