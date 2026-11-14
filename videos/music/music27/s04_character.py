from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403


class Character(SoundScene):
    def construct(self):
        chapter(self, 3, r"Small pieces, \ large feelings", r"Why does a mazurka limp?", extra=((1830, r"Chopin leaves Warsaw"),))
        self.miniatures()
        self.mazurka()
        self.beats()
        self.chopin()

    # ------------------------------------------------------------------
    def miniatures(self):
        items = [
            (r"the character piece: \ a short piano piece with a mood and often a title", WHITE),
            (r"John Field's nocturnes \ (from 1812): \ a singing melody over wide, \ pedalled arpeggios", WHITE),
            (r"Mendelssohn's \textit{Songs without Words}; \ Schumann's \textit{Carnaval} \ (1835), \ a ball in masks", WHITE),
            (r"Chopin: \ nocturnes, \ études, \ preludes, \ and about sixty mazurkas", TUNE),
            (r"the large feeling in the small form: \ a Romantic paradox", GREY_A),
        ]
        rows_scene(self, r"the character piece", items,
                   "Beside the song, the century loved the short piano piece. <bookmark mark='b'/> A character piece is a few "
                   "minutes long, has a single mood, and often a title. <bookmark mark='c'/> The Irish pianist John Field "
                   "published the first nocturnes from 1812: a singing melody over wide arpeggios held in the pedal. "
                   "<bookmark mark='d'/> Mendelssohn wrote Songs without Words, and Schumann's Carnaval of 1835 is a masked "
                   "ball in twenty-odd short scenes. <bookmark mark='e'/> Chopin wrote nocturnes, études and preludes, and "
                   "about sixty mazurkas, the dance of his native Poland. <bookmark mark='f'/> The large feeling in a small "
                   "form is one of the century's paradoxes.", marks="cdef")

    # ------------------------------------------------------------------
    def mazurka(self):
        d = load("mazurka")
        c = clip("mazurka.two")
        unit = d["unit"]
        parts = d["parts"]
        g1 = voices_roll(parts[::-1], width=5.4, height=2.8, colors=[TUNE, GREY_A], lo=40, hi=86, bar_h=0.08).move_to(LEFT * 3.3 + DOWN * 0.3)
        g2 = voices_roll(parts[::-1], width=5.4, height=2.8, colors=[TUNE, GREY_A], lo=40, hi=86, bar_h=0.08).move_to(RIGHT * 3.3 + DOWN * 0.3)
        warp = d["shift"]
        for g in (g2,):
            for part, v in zip(g.parts, parts[::-1]):
                for b, n in zip(part.notes, v):
                    k = int(n[1])
                    sh = warp[min(k, len(warp) - 1)] + (n[1] - k) * 0.0
                    b.shift(RIGHT * g.frame.width * sh / g.total)
        l1 = label(r"A", font_size=40, color=GREY_A).next_to(g1, UP, buff=0.3)
        l2 = label(r"B", font_size=40, color=GREY_A).next_to(g2, UP, buff=0.3)
        head = label(r"Chopin, \ Mazurka in C$\sharp$ minor, \ Op. 6 No. 2: \ bars 9 to 16", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        card = listen_card(r"Chopin's Mazurka Op. 6 No. 2, \ its theme, \ twice. \ In one the three beats of each bar are equal; \ "
                           r"in the other they are not. \ Which one dances, \ A or B?", width=10.4)
        with self.voiceover(
            "Here is Chopin's Mazurka in C sharp minor, Opus 6 Number 2, published in 1832, its theme read from the "
            "encoding and played twice. In one performance the three beats of every bar are exactly equal, as the "
            "notation says. In the other they are not. Which one dances, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        self.play(FadeOut(card), FadeIn(head), FadeIn(g1), FadeIn(g2), FadeIn(l1), FadeIn(l2))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash_voices(snd, g1, parts[::-1], d["starts"]["strict"], unit, colors=[TUNE, GREY_A])
            pulse(snd, l1, d["starts"]["strict"], d["starts"]["mazurka"] - 0.5, buff=0.1)
            pulse(snd, l2, d["starts"]["mazurka"], c.duration, buff=0.1)
            for part, v, col in zip(g2.parts, parts[::-1], (TUNE, GREY_A)):
                if part.notes:
                    times = [d["starts"]["mazurka"] + unit * (n[1] + warp[min(int(n[1]), len(warp) - 1)]) for n in v]
                    flash(snd, part.notes, times, hot=WHITE, base=col)
        ans = VGroup(label(r"A: \ three equal beats, \ as written", font_size=21, color=GREY_A).next_to(g1, DOWN, buff=0.35),
                     label(r"B: \ beat 1 short, \ beat 2 long: \ the mazurka", font_size=21, color=TUNE).next_to(g2, DOWN, buff=0.35))
        with self.voiceover(
            "B is the mazurka. The notes are identical; only their timing differs. The first beat is a little short, the "
            "second a little long, and the bar begins to limp the way the dance does, the accent falling on the second "
            "or third beat rather than the first."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beats(self):
        d = load("mazurka")
        bl = d["beat_lengths"]
        tot = sum(bl)
        W = 9.0
        x0 = -W / 2
        strict = VGroup()
        bent = VGroup()
        for i in range(3):
            strict.add(Rectangle(width=W / 3 - 0.06, height=0.55, stroke_width=0, fill_color=GREY_B, fill_opacity=0.7).move_to([x0 + W / 3 * (i + 0.5), 1.0, 0]))
        a = x0
        for i, b in enumerate(bl):
            w = W * b / tot
            bent.add(Rectangle(width=w - 0.06, height=0.55, stroke_width=0, fill_color=[BLUE, TUNE, EAR][i], fill_opacity=0.85).move_to([a + w / 2, -0.3, 0]))
            a += w
        nums = VGroup(*[label(str(i + 1), font_size=24, color=WHITE).move_to(r) for i, r in enumerate(strict)],
                      *[label(rf"{3 * b / tot:.2f}", font_size=22, color=WHITE).move_to(r) for b, r in zip(bl, bent)])
        lab = VGroup(label(r"written", font_size=22, color=GREY_A).next_to(strict, LEFT, buff=0.3),
                     label(r"played", font_size=22, color=TUNE).next_to(bent, LEFT, buff=0.3))
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (r"the beat lengths here are an illustration, \ not a measurement", GREY_A),
            (r"recordings show many patterns: \ pianists differ, \ and so do mazurkas", WHITE),
            (r"what is constant: \ the notation is regular and the performance is not", TUNE))]).arrange(DOWN, buff=0.28).move_to(DOWN * 2.0)
        with self.voiceover(
            "Drawn as lengths, the written bar has three equal beats, and the played bar here gives them 0.85, 1.2 and 0.95 "
            "of a beat. <bookmark mark='a'/> Those numbers are the film's illustration, not a measurement. "
            "<bookmark mark='b'/> When researchers measured the beats in thousands of recorded mazurkas, they found many "
            "patterns: pianists differ, and so do the dances. <bookmark mark='c'/> What is constant is the gap between "
            "a regular notation and an irregular performance. The score is not the music."
        ) as vo:
            self.play(FadeIn(strict), FadeIn(bent), FadeIn(nums), FadeIn(lab))
            for mark, r in zip("abc", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chopin(self):
        items = [
            (r"Chopin, \ 1810--1849: \ born near Warsaw, \ in Paris from 1831", WHITE),
            (r"after the failed Polish rising of 1830--31 he never went home", WHITE),
            (r"mazurkas and polonaises: \ Polish dances as a national voice in exile", WHITE),
            (r"the drone of the opening: \ village bagpipes, \ open fifths in the bass", TUNE),
            (r"a style of the salon, \ heard in Poland as a style of the nation", GREY_A),
        ]
        rows_scene(self, r"a nation in a dance", items,
                   "Chopin's dances carry a nation. <bookmark mark='b'/> He was born near Warsaw in 1810 and settled in Paris "
                   "in 1831. <bookmark mark='c'/> After the Polish rising against Russia failed that year, he never went "
                   "home. <bookmark mark='d'/> His mazurkas and polonaises turned Polish dances into a national voice in "
                   "exile. <bookmark mark='e'/> This mazurka opens over open fifths held in the bass, like a village "
                   "bagpipe's drone. <bookmark mark='f'/> Music written for Parisian salons was heard in Poland as the sound "
                   "of the nation, a theme chapter eight takes further.", marks="cdef")
