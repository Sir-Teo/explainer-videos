from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403


class Claims(SoundScene):
    def construct(self):
        chapter(self, 10, r"Amusia, \ Mozart and transfer", r"What does careful testing say about music and the mind?")
        self.amusia()
        self.quiz()
        self.mozart()
        self.funnel()
        self.transfer()
        self.therapy()

    # ------------------------------------------------------------------
    def amusia(self):
        items = [
            (r"congenital amusia: \ lifelong trouble with musical pitch, \ with normal hearing and intelligence", WHITE),
            (r"Isabelle Peretz and colleagues built the Montreal Battery of Evaluation of Amusia: \ same or different?", WHITE),
            (r"many amusics cannot hear which way a small pitch change went, \ or notice a wrong note in a tune", WHITE),
            (r"Peretz and Dominique Vuvan \ (2017): \ about 1.5 per cent of people, \ not the 4 per cent long quoted", TUNE),
            (r"it runs in families; \ speech is mostly spared, \ since its pitch steps are larger", GREY_A),
        ]
        rows_scene(self, r"born without a tune", items,
                   "Some people never get music's pitch at all. <bookmark mark='b'/> Congenital amusia is lifelong trouble with "
                   "musical pitch, in people with normal hearing and intelligence. <bookmark mark='c'/> Isabelle Peretz and "
                   "colleagues built a test for it, the Montreal Battery of Evaluation of Amusia, made of same-or-different "
                   "questions. <bookmark mark='d'/> Many amusics cannot hear which way a small pitch change went, or notice a "
                   "wrong note in a tune. <bookmark mark='e'/> In 2017 Peretz and Dominique Vuvan estimated it in about one and "
                   "a half per cent of people, not the four per cent long quoted. <bookmark mark='f'/> It runs in families, "
                   "and speech is mostly spared, since its pitch movements are larger.", marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("amusia")
        c = clip("amusia.pairs")
        card = listen_card(r"Two pairs of short melodies, \ in the style of the Montreal battery. \ In one pair the two melodies "
                           r"differ by one note. \ Which pair?", width=10.0)
        with self.voiceover(
            "A question in the battery's style. Two pairs of short melodies. In one pair, the two melodies differ by a single "
            "note. Which pair?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        mel = d["melody"]
        b = [list(x) for x in mel]
        b[d["changed"]][0] = d["to"]
        def r_(m, color):
            return mroll(mel_notes(m, base=60), width=4.4, height=1.0, lo=59, hi=68, color=color)
        pairs = VGroup()
        for name in (r"first pair", r"second pair"):
            g = VGroup(r_(mel, GREY_A), r_(b if name == r"first pair" else mel, GREY_A)).arrange(RIGHT, buff=0.6)
            pairs.add(VGroup(label(name, font_size=20, color=WHITE), g).arrange(DOWN, buff=0.25))
        pairs.arrange(DOWN, buff=0.7).move_to(UP * 0.2)
        self.play(FadeOut(card), FadeIn(pairs))
        st = d["starts"]
        beat = 0.42
        on = np.concatenate([[0.0], np.cumsum([x[1] for x in mel])[:-1]])
        with self.listen(c) as snd:
            window(snd, r"two pairs", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for key in ("first", "second"):
                i = 0 if key == "first" else 1
                flash(snd, pairs[i][1][0].notes, [st[key] + beat * o for o in on], hot=WHITE, base=GREY_A)
                flash(snd, pairs[i][1][1].notes, [st[f"{key}_b"] + beat * o for o in on], hot=WHITE, base=GREY_A)
                for roll, start in ((pairs[i][1][0], st[key]), (pairs[i][1][1], st[f"{key}_b"])):
                    fr = roll.frame
                    playhead = VGroup(Line(DOWN * 0.6, UP * 0.6, color=WHITE, stroke_width=3), Dot(radius=0.09, color=WHITE))
                    def move(m, t, frame=fr, begin=start):
                        u = (t - begin) / (beat * 9)
                        m.move_to([frame.get_left()[0] + frame.width * min(max(u, 0), 1), frame.get_center()[1], 0])
                        m.set_opacity(1 if 0 <= u <= 1 else 0)
                    snd.show(playhead)
                    snd.drive(playhead, move)
        k = d["changed"]
        with self.voiceover(
            "The first pair. In its second melody the fourth note, F, became F sharp: one semitone, and out of the key. "
            "Most listeners hear it at once, as a sour note. Many amusics hear nothing; the Montreal battery asks thirty "
            "such questions, and the battery uses normative cutoffs and several subtests; one informal trial cannot diagnose amusia."
        ):
            self.play(pairs[0][1][1].notes[k].animate.set_fill(EAR, 1.0).scale(1.3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mozart(self):
        items = [
            (r"Frances Rauscher, \ Gordon Shaw and Katherine Ky \ (1993): \ ten minutes of a Mozart sonata, \ then a spatial reasoning test", WHITE),
            (r"36 students scored the equivalent of 8 or 9 IQ points higher, \ for about a quarter of an hour", WHITE),
            (r"the `Mozart effect' became a business; \ a US state governor proposed giving every newborn a classical CD", WHITE),
            (r"Jakob Pietschnig and colleagues \ (2010): \ about 40 studies and 3,000 people; \ against silence $d = 0.37$, \ against other music $d = 0.15$", TUNE),
            (r"with signs of publication bias; \ William Thompson and colleagues \ (2001) \ found mood and arousal explain it", GREY_A),
        ]
        rows_scene(self, r"the Mozart effect", items,
                   "Now a claim that went around the world. <bookmark mark='b'/> In 1993 Frances Rauscher, Gordon Shaw and "
                   "Katherine Ky played students ten minutes of a Mozart sonata, then gave them a spatial reasoning test. "
                   "<bookmark mark='c'/> Thirty-six students scored the equivalent of eight or nine IQ points higher, for about "
                   "a quarter of an hour. <bookmark mark='d'/> The Mozart effect became a business, and a US governor proposed "
                   "giving every newborn a classical CD. <bookmark mark='e'/> In 2010 Jakob Pietschnig and colleagues pooled "
                   "about forty studies and three thousand people. Against silence the effect was a standardized difference of "
                   "0.37; against other music, 0.15. <bookmark mark='f'/> There were signs of publication bias; and William "
                   "Thompson and colleagues had found in 2001 that mood and arousal explain it: any music you enjoy will do.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def funnel(self):
        d = load("mozart")["0.0"]
        rows = d["rows"]
        x0, W, H = -4.6, 8.0, 3.6
        def P(dv, se):
            return np.array([x0 + W * (np.clip(dv, -1.2, 1.2) + 1.2) / 2.4, -1.8 + H * (1 / se - 2.0) / 4.0, 0])
        LO, HI = 0.5, 1 / 6.0
        ax = VGroup(Line(P(-1.2, LO), P(1.2, LO), color=GREY_B, stroke_width=1.5),
                    DashedLine(P(0, LO), P(0, HI), color=WHITE, stroke_width=2),
                    *[label(f"{v:g}", font_size=15, color=GREY_A).next_to(P(v, LO), DOWN, buff=0.12) for v in (-1, -0.5, 0, 0.5, 1)],
                    label(r"effect found in each study \ (standardized)", font_size=16, color=GREY_A).next_to(P(0, LO), DOWN, buff=0.5),
                    label(r"$\uparrow$ \ larger studies", font_size=16, color=GREY_A).move_to(P(-1.0, 0.19)))
        unpub = VGroup(*[Dot(P(r[0], r[1]), radius=0.045, color=GREY_B, fill_opacity=0.6) for r in rows if not r[2]])
        pub = VGroup(*[Dot(P(r[0], r[1]), radius=0.065, color=EAR, fill_opacity=0.95) for r in rows if r[2]])
        mp = d["mean_published"]
        line = DashedLine(P(mp, LO), P(mp, HI), color=EAR, stroke_width=3)
        tag = label(rf"published average: \ {mp:.2f}", font_size=17, color=EAR).next_to(line, UP, buff=0.1).shift(RIGHT * 0.8)
        key = VGroup(VGroup(Dot(radius=0.05, color=GREY_B), label(r"done, \ never published", font_size=16, color=GREY_A)).arrange(RIGHT, buff=0.12),
                     VGroup(Dot(radius=0.065, color=EAR), label(r"published", font_size=16, color=EAR)).arrange(RIGHT, buff=0.12)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_corner(UR, buff=0.6).shift(DOWN * 0.6)
        head = label(r"300 small experiments of an effect that is zero", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"How does an effect appear from nothing? Simulate it. Three hundred small experiments, each with ten to sixty people per group, of a treatment whose true effect is exactly zero. <bookmark mark='a'/> Each grey dot is one study: its estimated effect across, its size up the page. They scatter around zero in a funnel, wide for small studies, narrow for large ones. <bookmark mark='b'/> Now publish every study that found a significant positive effect, and only fifteen per cent of the rest. {say(d['published'])} studies are published, and their average effect is {say(mp, 2)}: an effect, built from nothing but which studies were seen. Funnel asymmetry can flag selective reporting, but heterogeneity and other biases can also produce it; it is not proof by itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(unpub), FadeIn(pub.copy().set_color(GREY_B)))
            vo.wait_until("b")
            self.play(FadeIn(pub), Create(line), FadeIn(tag))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def transfer(self):
        items = [
            (r"a broader claim: \ music lessons make children better at other things", WHITE),
            (r"Glenn Schellenberg \ (2004): \ a year of keyboard or singing lessons, \ about 2.7 IQ points over drama or no lessons", WHITE),
            (r"Samuel Mehr and colleagues \ (2013): \ two randomized trials of preschool music classes: \ no consistent cognitive benefit", WHITE),
            (r"Giovanni Sala and Fernand Gobet \ (2020): \ 54 studies; \ the better the design, \ the smaller the effect, \ down to about zero", TUNE),
            (r"random assignment and an active control group: \ the two features that made the effect vanish", GREY_A),
        ]
        rows_scene(self, r"does music training transfer?", items,
                   "A broader claim is that music lessons make children better at other things. <bookmark mark='b'/> In 2004 "
                   "Glenn Schellenberg gave children a year of keyboard or singing lessons and found about 2.7 IQ points over "
                   "drama lessons or none. <bookmark mark='c'/> In 2013 Samuel Mehr and colleagues ran two randomized trials of "
                   "preschool music classes and found no consistent cognitive benefit. <bookmark mark='d'/> In 2020 Giovanni "
                   "Sala and Fernand Gobet pooled fifty-four studies: the better the design, the smaller the effect, down to "
                   "about zero. <bookmark mark='e'/> Random assignment and an active control group were the two features that "
                   "made it vanish. Music is worth learning for itself.", marks="bcde")

    # ------------------------------------------------------------------
    def therapy(self):
        items = [
            (r"Jenny Hole and colleagues \ (2015): \ 73 randomized trials; \ music around surgery reduced pain, \ anxiety and painkiller use", WHITE),
            (r"a Cochrane review \ (2017): \ music therapy added to usual care eased depression in the short term", WHITE),
            (r"rhythmic cueing helps people with Parkinson's disease walk more steadily", WHITE),
            (r"but the TIME-A trial \ (2017): \ 364 autistic children, \ improvisational music therapy, \ no benefit on its main measure", TUNE),
            (r"the evidence is mixed and specific: \ ask what was compared, \ with whom, \ and how it was measured", GREY_A),
        ]
        rows_scene(self, r"music as treatment", items,
                   "What about music as treatment? <bookmark mark='b'/> In 2015 Jenny Hole and colleagues pooled seventy-three "
                   "randomized trials: music around surgery reduced pain, anxiety and the use of painkillers. "
                   "<bookmark mark='c'/> A Cochrane review in 2017 found that music therapy added to usual care eased depression "
                   "in the short term. <bookmark mark='d'/> Rhythmic cueing helps people with Parkinson's disease walk more "
                   "steadily. <bookmark mark='e'/> But the TIME-A trial of 2017, with 364 autistic children, found no benefit of "
                   "improvisational music therapy on its main measure. <bookmark mark='f'/> The evidence is mixed and specific: "
                   "ask what was compared, with whom, and how it was measured.", marks="bcdef")
