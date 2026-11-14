from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403


class ThreeTwo(SoundScene):
    def construct(self):
        chapter(self, 4, r"Three against two", r"How many beats are there, \ and who decides?")
        self.grids()
        self.hear()
        self.hemiola()
        self.debate()
        self.notations()
        self.where_one()

    # ------------------------------------------------------------------
    def grids(self):
        d = load("threetwo")
        bell = pat_row("x.x.xx.x.x.x", cell=0.45, name=r"bell", size=19)
        g4 = pat_row(["x" if i in d["four"] else "." for i in range(12)], cell=0.45, color=BLUE, name=r"4 beats of 3", size=19)
        g6 = pat_row(["x" if i in d["six"] else "." for i in range(12)], cell=0.45, color=EAR, name=r"6 beats of 2", size=19)
        g3 = pat_row(["x" if i in (0, 4, 8) else "." for i in range(12)], cell=0.45, color="#A3E635", name=r"3 beats of 4", size=19)
        rows_ = VGroup(bell, g4, g6, g3).arrange(DOWN, buff=0.3, aligned_edge=RIGHT).move_to(LEFT * 1.4 + DOWN * 0.1)
        cnt = VGroup(label(r"", font_size=18),
                     label(rf"bell on {len(d['on_four'])} of 4", font_size=18, color=BLUE),
                     label(rf"bell on {len(d['on_six'])} of 6", font_size=18, color=EAR),
                     label(rf"bell on {len(d['on_three'])} of 3", font_size=18, color="#A3E635"))
        for c_, r in zip(cnt, rows_):
            c_.next_to(r, RIGHT, buff=0.45)
        head = label(r"twelve pulses hold several beats at once", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Twelve is a generous number: it is two sixes, three fours, four threes and six twos. <bookmark mark='a'/> So a "
            "twelve-pulse cycle can carry four beats of three pulses, <bookmark mark='b'/> six beats of two, "
            "<bookmark mark='c'/> or three beats of four, all at once. <bookmark mark='d'/> The bell agrees with each only "
            "partly: it strikes on two of the four beats, three of the six, and two of the three. Against the four it "
            "pulls; against the six it sits for half a cycle and then lets go. Four against six is three against two at "
            "twice the speed, and three against two is the generating idea of much of this music: two grids heard at once, "
            "neither one the whole truth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bell))
            vo.wait_until("a")
            self.play(FadeIn(g4))
            vo.wait_until("b")
            self.play(FadeIn(g6))
            vo.wait_until("c")
            self.play(FadeIn(g3))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cnt[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("threetwo")
        c = clip("threetwo.cross")
        bell = pat_row("x.x.xx.x.x.x", cell=0.5, name=r"bell", size=20)
        g4 = pat_row(["x" if i in d["four"] else "." for i in range(12)], cell=0.5, color=BLUE, name=r"low drum: \ 4", size=20)
        g6 = pat_row(["x" if i in d["six"] else "." for i in range(12)], cell=0.5, color=EAR, name=r"high drum: \ 6", size=20)
        rows_ = VGroup(g4, g6, bell).arrange(DOWN, buff=0.35, aligned_edge=RIGHT).move_to(UP * 0.3)
        stage = VGroup(*[label(t, font_size=21, color=GREY_A) for t in (r"four", r"six", r"four and six", r"with the bell")]).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Hear it. Four beats on a low drum, then six on a high drum, then both together, which is three against two, "
            "and finally both with the bell, which belongs to neither and to both."
        ):
            self.play(FadeIn(rows_), FadeIn(stage))
        st = d["starts"]
        ks = ["four", "six", "both", "bell"]
        with self.listen(c) as snd:
            window(snd, r"four, \ six, \ both, \ bell", detail=r"membrane and bell models", corner=DL, tag_corner=DR)
            for k in ("four", "both", "bell"):
                flash_cells(snd, g4.cells, d["four"], st[k], d["pulse"], 2, 12, color=BLUE)
            for k in ("six", "both", "bell"):
                flash_cells(snd, g6.cells, d["six"], st[k], d["pulse"], 2, 12, color=EAR)
            flash_cells(snd, bell.cells, [0, 2, 4, 5, 7, 9, 11], st["bell"], d["pulse"], 2, 12)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i < 3 else c.duration
                pulse(snd, stage[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hemiola(self):
        items = [
            (r"European music knows the effect as \textit{hemiola}: \ two bars of three heard as three of two", WHITE),
            (r"Baroque cadences slow into a hemiola \ (Part 25); \ Brahms builds whole passages on it \ (Part 27)", WHITE),
            (r"there it is a moment of friction; \ here it is the ground the music stands on", WHITE),
            (r"the dancer's feet often take the four, \ while hands, \ shoulders or song take the six", TUNE),
            (r"the body holds both grids at once", GREY_A),
        ]
        rows_scene(self, r"hemiola, \ and more", items,
                   "European music knows this effect as hemiola, from the Greek for one and a half: two bars of three heard as "
                   "three of two. <bookmark mark='b'/> Baroque cadences slow into a hemiola, as Part 25 showed, and Brahms built "
                   "whole passages on it. <bookmark mark='c'/> There it is a moment of friction. Here it is the ground the music "
                   "stands on. <bookmark mark='d'/> A dancer's feet often take the four, while the hands, the shoulders or the song "
                   "take the six. <bookmark mark='e'/> The body holds both grids at once.", marks="bcde")

    # ------------------------------------------------------------------
    def debate(self):
        items = [
            (r"A. M. Jones \ (1959): \ each part with its own bar lines: \ several meters at once \ (\textit{polymeter})", WHITE),
            (r"Nketia \ (1963): \ the time line as the ensemble's guide", WHITE),
            (r"Kubik and Arom: \ a fast pulse and a cycle, \ no measures and no downbeat imposed", WHITE),
            (r"Agawu \ (2006): \ one shared meter, \ given by the dance; \ the bell is heard against it", TUNE),
            (r"Locke: \ the four main beats are felt by every player", GREY_A),
        ]
        rows_scene(self, r"how should it be written?", items,
                   "How should this be written down? The question has divided scholars for seventy years. "
                   "<bookmark mark='b'/> A. M. Jones, in his Studies in African Music of 1959, wrote each part with its own bar "
                   "lines, as though several meters ran at once: polymeter. <bookmark mark='c'/> Kwabena Nketia described the "
                   "time line as the guide for the whole ensemble. <bookmark mark='d'/> Gerhard Kubik and Simha Arom wrote a fast "
                   "pulse and a cycle, without measures or an imposed downbeat. <bookmark mark='e'/> Kofi Agawu, in 2006, "
                   "argued for one shared meter given by the dance, with the bell heard against it, <bookmark mark='f'/> close "
                   "to David Locke's view that every player feels the four main beats.", marks="cdef")

    # ------------------------------------------------------------------
    def notations(self):
        def staff(parts, bars_at, title, col):
            g = VGroup()
            for k, (name, pat) in enumerate(parts):
                r = pat_row(pat, cell=0.3, color=VOICE_C[k], name=name, size=16)
                g.add(r)
            g.arrange(DOWN, buff=0.15, aligned_edge=RIGHT)
            lines = VGroup()
            for k, r in enumerate(g):
                for b in bars_at[k]:
                    x = r.cells[b].get_left()[0] - 0.015
                    lines.add(Line([x, r.cells[b].get_top()[1] + 0.08, 0], [x, r.cells[b].get_bottom()[1] - 0.08, 0], color=col, stroke_width=4))
            t = label(title, font_size=19, color=col)
            out = VGroup(t, VGroup(g, lines)).arrange(DOWN, buff=0.25)
            return out
        bell = "x.x.xx.x.x.x" * 2
        kidi = ("..xx....xx.." * 2)
        sogo = ("x...xx" * 4)
        parts = [(r"bell", bell), (r"kidi", kidi), (r"sogo", sogo)]
        jones = staff(parts, [[0, 12], [2, 14], [4, 10, 16, 22]], r"bar lines where each part begins \ (after Jones)", EAR)
        agawu = staff(parts, [[0, 12], [0, 12], [0, 12]], r"one bar line for all, \ from the dance \ (after Agawu)", TUNE)
        g = VGroup(jones, agawu).arrange(DOWN, buff=0.6).move_to(DOWN * 0.3)
        g.scale_to_fit_height(min(g.height, 6.0))
        head = label(r"the same notes, \ written two ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is the difference in a picture, with three of our parts over two cycles. <bookmark mark='a'/> In the "
            "manner of Jones, each part is barred where its own figure begins, and the bar lines do not line up: three "
            "meters, it seems. <bookmark mark='b'/> In the manner of Agawu, one bar line serves everyone, placed by the dance, "
            "and each part is heard as off or on its beats. The notes are identical; what differs is the claim about what "
            "the players feel. Agawu's point is that this is an empirical question, about people, not about notation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            vo.wait_until("a")
            self.play(FadeIn(jones))
            vo.wait_until("b")
            self.play(FadeIn(agawu))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def where_one(self):
        items = [
            (r"even \textit{where} the cycle starts is debated: \ which bell stroke is `one'?", WHITE),
            (r"Ewe teachers, \ Cuban players and scholars do not all agree", WHITE),
            (r"motion studies of dancers' steps and players' bodies now test such claims directly", WHITE),
            (r"the answer may differ by piece, \ region and person: \ there need be no single meter", TUNE),
            (r"chapter 10 returns to measuring how this music is felt", GREY_A),
        ]
        rows_scene(self, r"where is one?", items,
                   "Even where the cycle starts is debated. <bookmark mark='b'/> Which of the bell's strokes is one? "
                   "<bookmark mark='c'/> Ewe teachers, Cuban players and scholars do not all agree. <bookmark mark='d'/> Studies "
                   "with motion capture, of dancers' steps and players' bodies, now test such claims directly. "
                   "<bookmark mark='e'/> The answer may differ by piece, by region and by person: there need be no single "
                   "meter. <bookmark mark='f'/> Chapter ten returns to measuring how this music is felt.", marks="cdef")
