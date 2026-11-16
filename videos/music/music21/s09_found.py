from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


class Found(SoundScene):
    def construct(self):
        chapter(self, 8, r"Form from sound", r"Can a program find a piece's sections by listening?")
        self.sonata()
        self.scores()
        self.limits()

    # ------------------------------------------------------------------
    def sonata(self):
        d = load("sonata")
        c = clip("sonata.whole")
        total = d["total"]
        n = len(d["novelty"])
        img = ssm_image(d["ssm"], size=3.6).move_to(LEFT * 4.6 + DOWN * 0.1)
        cv = curve(d["novelty"], width=8.0, height=1.4, color=TUNE).move_to(RIGHT * 1.8 + UP * 0.9)
        truth = VGroup(*[tick(cv, b, n, color=GREY_B, height=1.6) for b in d["truth"]])
        found = VGroup(*[Dot([cv[0].get_left()[0] + cv[0].width * b / (n - 1), cv[0].get_y() + 1.55, 0], radius=0.08, color=EAR) for b in d["found"]])
        big = d["big"]
        st = strip([big[k][0] for k in big], list(big), total, width=8.0, height=0.4, colors={"exposition": "#F5C542", "development": "#7DD3FC", "recapitulation": "#A3E635"}, font_size=18).next_to(cv, DOWN, buff=0.4)
        sc = d["score"]
        cap = label(rf"{sc['hits']} of the {len(d['truth'])} places where the material changes found within two beats; \ {len(d['found']) - sc['hits']} false alarms", font_size=22, color=TUNE).to_edge(DOWN, buff=0.55)
        cur = Line(ORIGIN, ORIGIN, color=WHITE, stroke_width=2.5)
        with self.voiceover(
            "Now give the program the whole miniature sonata, about three-quarters of a minute of piano, and nothing "
            "else: no score, no bar lines, no idea what a sonata is. Its picture is on the left; its novelty curve, with a "
            "checkerboard eight beats wide, on the right. Grey lines mark where the music really changes section; pink "
            "dots are where the program thinks it does."
        ):
            self.play(FadeIn(img), FadeIn(cv), FadeIn(truth), FadeIn(st))
        with self.listen(c) as snd:
            window(snd, r"the miniature sonata", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, list(found), [b * d["beat"] for b in d["found"]], hot=WHITE, base=EAR, hold=0.6)

            def upd(m, t):
                b = min(max(t / d["beat"], 0.0), n - 1)
                x = cv[0].get_left()[0] + cv[0].width * b / (n - 1)
                m.put_start_and_end_on([x, cv[0].get_y(), 0], [x, cv[0].get_y() + 1.7, 0])

            snd.drive(cur, upd)
            self.add(cur, found)
        with self.voiceover(
            f"It finds {say(sc['hits'])} of the {say(len(d['truth']))} boundaries within two beats, with "
            f"{say(len(d['found']) - sc['hits'])} false alarms. Where the music changes key, the change in its notes is "
            "large, and the picture shows it plainly."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scores(self):
        d = load("segment")
        names = ["sonata", "rondo", "ternary", "verse-chorus", "AABA", "binary", "variations"]
        vals = [100 * max(x["f"] for x in d["pieces"][k]["by_width"].values()) for k in names]
        ch = columns(vals, names, width=9.0, height=2.6, color=WEAK, hot=(0,), hot_color=TUNE, fmt="{:.0f}", font_size=18, top=100).move_to(LEFT * 1.4 + DOWN * 0.5)
        t = label(r"F-score of the boundaries found, \ in a hundred \ (the best of three checkerboard widths)", font_size=21, color=GREY_A).next_to(ch, UP, buff=0.4)
        s = d["summary"]
        side = VGroup(label(r"high where sections change key", font_size=22, color=TUNE),
                      label(r"variations: \\ same harmony, \\ weak seams", font_size=22, color=EAR),
                      label(rf"same collection, \\ selected setting: \ {round(100 * s[d['best_width']]['f'])} in a hundred", font_size=22, color=WHITE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 3.8))
        side.move_to(RIGHT * 5.0 + DOWN * 0.2)
        with self.voiceover(
            "Run it on every piece in this part, scoring the boundaries it finds by the F-score, which combines how many "
            "true boundaries it found with how many of its finds were true. <bookmark mark='a'/> The sonata scores best, "
            "because its sections change key. <bookmark mark='b'/> The set of variations scores lowest: every variation "
            "keeps the theme's harmony, so in a picture made of notes there is hardly a seam to find, although a listener "
            "hears each new variation begin at once. <bookmark mark='c'/> With one of three settings selected on this same collection, the program "
            f"scores about {say(round(100 * s[d['best_width']]['f']))} in a hundred: better than nothing, with no human baseline measured here."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(t))
            for mark, r in zip("abc", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"novelty sees contrast: \ a change of key, \ of harmony, \ of texture", WHITE),
            (r"repetition needs the stripes: \ A A B B has a seam between the two A's that novelty cannot see", WHITE),
            (r"real systems add timbre, \ rhythm and loudness, \ and look for stripes as well as blocks", WHITE),
            (r"and a listener hears a new variation begin by its new figure, \ not its notes", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"what the picture misses", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "So what does the picture miss? <bookmark mark='a'/> Novelty sees contrast: a change of key, of harmony, of "
            "texture. <bookmark mark='b'/> It cannot see a seam between a passage and its own repeat: in A A B B, the two "
            "A's join without a change. Finding those needs the stripes, the diagonals, as well as the blocks. "
            "<bookmark mark='c'/> Practical systems measure timbre, rhythm and loudness too, and search for stripes and "
            "blocks together. <bookmark mark='d'/> And a listener hears a new variation begin by its new figure, a "
            "change of surface that a picture made of pitch classes throws away."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
