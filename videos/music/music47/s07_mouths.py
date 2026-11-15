from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403


class Mouths(SoundScene):
    def construct(self):
        chapter(self, 6, r"A tune in simulated mouths", r"What happens to a melody passed from singer to singer?")
        self.singer()
        self.generations()
        self.quiz()
        self.measures()
        self.kinds()
        self.lab()

    # ------------------------------------------------------------------
    def singer(self):
        items = [
            (r"memory: \ what is new is what slips; \ a note with a new pitch, \ interval or length is likeliest to be lost", WHITE),
            (r"a lost note is left out, \ doubled, \ or replaced by what followed the same pitch earlier in the tune", WHITE),
            (r"hearing: \ every pitch and length a little blurred", WHITE),
            (r"pitches sorted into categories; \ lengths heard as the likeliest simple value; \ wide leaps landing short", TUNE),
            (r"singing: \ a little motor noise, \ and a pull toward a comfortable register", GREY_A),
        ]
        rows_scene(self, r"one simulated singer", items,
                   "Now let a whole melody travel. Each simulated singer hears the melody once and sings it to the next. "
                   "<bookmark mark='b'/> Memory first: what is new is what slips. A note with a pitch, an interval or a length "
                   "not heard earlier in the tune is the likeliest to be lost, <bookmark mark='c'/> and a lost note is left "
                   "out, doubled, or replaced by whatever followed the same pitch earlier in the tune. <bookmark mark='d'/> "
                   "Hearing blurs every pitch and every length a little. <bookmark mark='e'/> The singer sorts pitches into "
                   "categories, hears each length as the likeliest simple value, and lands wide leaps a little short. "
                   "<bookmark mark='f'/> Then it sings, with a little motor noise and a pull toward a comfortable register. "
                   "Nothing here mentions scales, motifs or style.", marks="bcdef")

    # ------------------------------------------------------------------
    def generations(self):
        d = load("chains")
        ex = d["example"]
        show = d["show"]
        allp = [x[0] for g in show for x in ex[str(g)]]
        rows_ = VGroup()
        for g in show:
            mel = ex[str(g)]
            tot = sum(b for _, b in mel)
            r = mroll(mel_notes(mel, base=60), width=7.6 * min(tot / 26.0, 1.4), height=0.62, lo=60 + min(allp) - 1, hi=60 + max(allp) + 1, color=TUNE if g else GREY_A, bar_h=0.085)
            rows_.add(VGroup(label(rf"singer {g}" if g else r"the start", font_size=17, color=GREY_A).set_width(1.3), r).arrange(RIGHT, buff=0.35, aligned_edge=DOWN))
        for r in rows_:
            r[0].set_width(min(r[0].width, 1.3))
        rows_.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(DOWN * 0.15)
        head = label(r"one random melody, \ after 0, \ 1, \ 5, \ 10, \ 20 and 40 singers", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        cap = label(r"height: \ pitch, \ on one scale for all rows; \ length: \ duration", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Start from a random melody: sixteen pitches anywhere in a range of seventeen semitones, lengths anywhere "
            "between a third of a beat and two and a half beats. <bookmark mark='a'/> After one singer, the lengths have "
            "snapped to simple values and the closest pitches have merged. <bookmark mark='b'/> After five, the tune has "
            "drifted, but it is the same tune. <bookmark mark='c'/> After ten, a few odd notes have been replaced by "
            "continuations heard elsewhere in it; after twenty, five pitch levels carry it, repeated, and the steps between "
            "them have halved. <bookmark mark='d'/> After forty, it circles a handful of levels with a beat you could tap."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(rows_[0]), FadeIn(VGroup(*[r[0] for r in rows_[1:]])))
            vo.wait_until("a")
            self.play(FadeIn(rows_[1][1]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[2][1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[3][1]), FadeIn(rows_[4][1]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[5][1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("chains")
        c = clip("chains.two")
        card = listen_card(r"The random melody, \ then what it became after forty singers. \ Which could you sing back after one hearing?", width=10.0)
        with self.voiceover(
            "Hear the two ends of the chain. The random melody, then what it became after forty singers. Which could you sing "
            "back after one hearing?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ex = d["example"]
        allp = [x[0] for g in ("0", "40") for x in ex[g]]
        a = mroll(mel_notes(ex["0"], base=60), width=10.0, height=1.3, lo=60 + min(allp) - 1, hi=60 + max(allp) + 1, color=GREY_A)
        b = mroll(mel_notes(ex["40"], base=60), width=10.0 * sum(x[1] for x in ex["40"]) / sum(x[1] for x in ex["0"]), height=1.3, lo=60 + min(allp) - 1, hi=60 + max(allp) + 1, color=TUNE)
        g = VGroup(VGroup(label(r"the start", font_size=19, color=GREY_A), a).arrange(DOWN, buff=0.15, aligned_edge=LEFT),
                   VGroup(label(r"after forty singers", font_size=19, color=TUNE), b).arrange(DOWN, buff=0.15, aligned_edge=LEFT)).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(UP * 0.2)
        self.play(FadeOut(card), FadeIn(g))
        st = d["starts"]
        beat = 0.42
        with self.listen(c) as snd:
            window(snd, r"singer 0, \ then singer 40", kind="synthesized", detail=r"Part 8's voice", corner=DL, tag_corner=DR)
            for key, r in (("first", a), ("last", b)):
                mel = ex["0"] if key == "first" else ex["40"]
                on = np.concatenate([[0.0], np.cumsum([x[1] for x in mel])[:-1]])
                flash(snd, r.notes, [st[key] + beat * o for o in on], hot=WHITE, base=GREY_A if key == "first" else TUNE)
        s0 = d["stats"]
        with self.voiceover(
            "Almost certainly the second. Nobody designed it; forty slightly forgetful singers did. It is not a good tune, "
            "but it is a singable one: its pitches repeat, its steps are small, and its lengths are simple. Those are three "
            "of the statistical universals of chapter three."
        ):
            self.play(Indicate(g[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measures(self):
        d = load("chains")
        s = d["stats"]
        G = d["generations"]
        def panel(key, title, lo, hi, ticks, color=TUNE, scale=1.0):
            q = s[key]
            mid = [v[1] * scale for v in q]
            band = ([v[0] * scale for v in q], [v[2] * scale for v in q])
            return line_plot([mid], width=4.3, height=1.55, ylo=lo, yhi=hi, xmax=G, colors=[color], bands=[band], ylabel=title, yticks=ticks, xticks=(0, 20, 40), size=15)
        p1 = panel("levels", r"distinct pitch levels", 0, 14, (0, 7, 14))
        p2 = panel("step", r"average step, \ semitones", 0, 7, (0, 3, 6), color=BLUE)
        p3 = panel("simple", r"lengths that are simple ratios, \ \%", 0, 100, (0, 50, 100), color=GOLD, scale=100.0)
        er = d["error"]
        eq = d["error_q"]
        p4 = line_plot([er], width=4.3, height=1.55, ylo=0, yhi=0.5, xmax=G - 1, colors=[EAR], bands=[(eq[0], eq[1])], ylabel=r"copying error, \ per note", yticks=(0, 0.25, 0.5), xticks=(0, 20, 39), size=15)
        grid = VGroup(VGroup(p1, p2).arrange(RIGHT, buff=1.4), VGroup(p3, p4).arrange(RIGHT, buff=1.4)).arrange(DOWN, buff=0.75).move_to(DOWN * 0.15)
        head = label(rf"{d['chains']} random melodies, \ {G} singers each: \ the middle line is the average, \ the band the middle half", font_size=21, color=GREY_A).to_edge(UP, buff=0.3)
        f = lambda k, i: s[k][i][1]
        with self.voiceover(
            f"Run twenty random melodies through forty singers each and measure. <bookmark mark='a'/> Distinct pitch levels "
            f"fall from about {say(f('levels', 0))} to about {say(f('levels', G), 1)}. <bookmark mark='b'/> The average step "
            f"shrinks from {say(f('step', 0), 1)} semitones to {say(f('step', G), 1)}. <bookmark mark='c'/> Lengths that are "
            f"simple ratios of the beat go from {say(100 * f('simple', 0))} per cent to {say(100 * f('simple', G))}. "
            f"<bookmark mark='d'/> And the copying error, how much each singer changes, falls from {say(er[0], 2)} to "
            f"{say(er[-1], 2)} per note: the melodies became easier to learn. That is the signature of cultural evolution "
            "in the lab: structure appears, and with it, learnability."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.copy().set_opacity(0.15)))
            for mark, p in zip("abcd", (p1, p2, p3, p4)):
                vo.wait_until(mark)
                self.play(FadeIn(p))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kinds(self):
        d = load("sampling")
        b, s = d["best"], d["sample"]
        p = line_plot([b["mean"], s["mean"]], width=8.0, height=3.0, ylo=0, yhi=0.6, xmax=30, colors=[TUNE, EAR],
                      bands=[(b["lo"], b["hi"]), (s["lo"], s["hi"])], xlabel=r"singers", ylabel=r"distance from the Tune, \ per note",
                      yticks=(0, 0.3, 0.6), xticks=(0, 10, 20, 30), size=17).move_to(DOWN * 0.2)
        k = VGroup(label(r"each length heard as the likeliest value", font_size=18, color=TUNE), label(r"each length drawn from the posterior", font_size=18, color=EAR)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(p, RIGHT, buff=-2.6).shift(UP * 1.5)
        head = label(r"the Tune through thirty singers, \ twelve times, \ two kinds of learner", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "One choice in the singer matters more than any other. Our singers take the likeliest length for each note. "
            "Chapter five's listener instead drew its answer from its posterior. <bookmark mark='a'/> Pass the Tune itself "
            f"through thirty singers of each kind, twelve times. The likeliest-value singers keep it: after thirty, it is "
            f"{say(b['mean'][-1], 2)} per note from the original. <bookmark mark='b'/> The sampling singers lose it faster: "
            f"{say(s['mean'][-1], 2)}. Griffiths and Kalish's theorem says where such a chain heads: toward the learners' prior, "
            "with nothing of the Tune left. Traditions last because singers hold on to what they heard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(p[0]), FadeIn(p[3:]), FadeIn(k))
            vo.wait_until("a")
            self.play(FadeIn(p[1]), Create(p.lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(p[2]), Create(p.lines[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lab(self):
        items = [
            (r"Simon Kirby, \ Hannah Cornish and Kenny Smith \ (2008): \ an invented language passed along chains of learners", WHITE),
            (r"it became easier to learn and gained structure: \ words built from reusable parts", WHITE),
            (r"Andrea Ravignani, \ Tania Delgado and Kirby \ (2016): \ random drumming passed along chains", WHITE),
            (r"the drumming became more regular, \ grew a beat and reused patterns: \ six features of the world's rhythms appeared", TUNE),
            (r"a universal need not be built in: \ weak biases, \ amplified by transmission, \ can produce it", GREY_A),
        ]
        rows_scene(self, r"cultural evolution in the lab", items,
                   "Real people do this too. <bookmark mark='b'/> In 2008 Simon Kirby, Hannah Cornish and Kenny Smith passed an "
                   "invented language along chains of learners. <bookmark mark='c'/> It became easier to learn and gained "
                   "structure: words built from reusable parts. <bookmark mark='d'/> In 2016 Andrea Ravignani, Tania Delgado "
                   "and Kirby did the same with random drumming. <bookmark mark='e'/> It became more regular, grew a beat and "
                   "reused patterns; six features common in the world's rhythms appeared. <bookmark mark='f'/> The lesson: a "
                   "universal need not be built in. Weak biases, amplified by transmission, can produce it.", marks="bcdef")
