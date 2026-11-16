from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403


class Rag(SoundScene):
    def construct(self):
        chapter(self, 4, r"Ragtime and stride", r"What is `ragged' about ragtime?")
        self.history()
        self.strain()
        self.hands()
        self.counted()
        self.form()
        self.stride()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"ragtime: \ piano music of the 1890s to the 1910s, \ sold as sheet music for the parlour", WHITE),
            (r"Scott Joplin \ (1868--1917) \ published \textit{Maple Leaf Rag} in Sedalia, \ Missouri, \ in 1899", WHITE),
            (r"`ragged time': \ a syncopated right hand over a steady, \ march-like left hand", WHITE),
            (r"Joplin: \ `it is never right to play ragtime fast' \ (\textit{School of Ragtime}, \ 1908)", TUNE),
            (r"the music is in the public domain: \ we play it from an encoding of the score", GREY_A),
        ]
        rows_scene(self, r"ragtime", items,
                   "Alongside the blues grew ragtime, piano music of the 1890s to the 1910s, sold as sheet music for the parlour "
                   "piano. <bookmark mark='b'/> Its master, Scott Joplin, published the Maple Leaf Rag in Sedalia, Missouri, in "
                   "1899, and it sold for years. <bookmark mark='c'/> The name means ragged time: a syncopated right hand over a "
                   "steady, march-like left hand. <bookmark mark='d'/> Joplin warned in his School of Ragtime of 1908 that it is "
                   "never right to play ragtime fast. <bookmark mark='e'/> The rag is in the public domain, and we play it from "
                   "an encoding of the score in the music21 corpus.", marks="bcde")

    # ------------------------------------------------------------------
    def strain(self):
        d = load("rag")
        c = clip("rag.strain")
        bar = d["bar"]
        rh = [[p, o / 24.0, du / 24.0] for p, o, du in d["right"]]
        lh = [[p, o / 24.0, du / 24.0] for p, o, du in d["left"]]
        roll = voices_roll([rh, lh], width=12.0, height=3.6, colors=[TUNE, BLUE], total=16 * bar / 24.0, lo=36, hi=88, bar_h=0.07).move_to(DOWN * 0.1)
        leg = VGroup(label(r"upper-register proxy (above C$\sharp$4)", font_size=18, color=TUNE), label(r"lower-register proxy", font_size=18, color=BLUE)).arrange(RIGHT, buff=0.8).next_to(roll, UP, buff=0.3)
        head = label(r"Joplin, \ \textit{Maple Leaf Rag} \ (1899), \ bars 1--16", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is the first strain of the Maple Leaf Rag, sixteen bars, played by Part 7's piano model from the score, at "
            "a moderate march tempo. Right hand in gold, left hand in blue."
        ):
            self.play(FadeIn(head), FadeIn(leg), FadeIn(roll))
        unit = d["unit"] * 24.0
        with self.listen(c) as snd:
            window(snd, r"\textit{Maple Leaf Rag}, \ first strain", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            cursor(snd, roll, 0.0, unit)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hands(self):
        d = load("rag")
        c = clip("rag.hands")
        bar = d["bar"]
        rh = [[p, o / 24.0, du / 24.0] for p, o, du in d["right"] if o < 4 * bar]
        lh = [[p, o / 24.0, du / 24.0] for p, o, du in d["left"] if o < 4 * bar]
        total = 4 * bar / 24.0
        grid = VGroup()
        roll = voices_roll([rh, lh], width=11.0, height=3.4, colors=[TUNE, BLUE], total=total, lo=36, hi=88, bar_h=0.1).move_to(DOWN * 0.2)
        fr = roll.frame
        for q in range(int(total) + 1):
            x = fr.get_left()[0] + fr.width * q / total
            grid.add(Line([x, fr.get_bottom()[1], 0], [x, fr.get_top()[1], 0], color=GREY_D if q % 2 else GREY_B, stroke_width=1))
        stage = VGroup(*[label(t, font_size=20, color=GREY_A) for t in (r"right hand", r"left hand", r"both")]).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.7)
        head = label(r"bars 1--4, pitch-split proxies; grey lines: beats", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Take the first four bars apart. First the right hand alone: notes that start between the beats and run across "
            "them. Then the left hand alone: a bass note on each beat and a chord between, like a march band's tuba and "
            "snare. Then both, and the friction between them is the rag."
        ):
            self.play(FadeIn(head), FadeIn(grid), FadeIn(roll), FadeIn(stage))
        unit = d["unit"] * 24.0
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"right, \ left, \ both", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, roll.parts[0].notes, [st["right"] + n[1] * unit for n in rh], hot=WHITE, base=TUNE)
            flash(snd, roll.parts[1].notes, [st["left"] + n[1] * unit for n in lh], hot=WHITE, base=BLUE)
            flash(snd, roll.parts[0].notes, [st["both"] + n[1] * unit for n in rh], hot=WHITE, base=TUNE)
            flash(snd, roll.parts[1].notes, [st["both"] + n[1] * unit for n in lh], hot=WHITE, base=BLUE)
            ks = ["right", "left", "both"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, stage[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counted(self):
        d = load("rag")
        R_, L_ = d["sync_right"], d["sync_left"]
        cats = [(r"on the beat", "on_beat"), (r"on the half-beat", "on_half"), (r"between \ (sixteenths)", "between")]
        bars = VGroup()
        mx = max(R_["onsets"], L_["onsets"])
        for i, (name, key) in enumerate(cats):
            row = VGroup(label(name, font_size=19, color=WHITE))
            for j, (S, col) in enumerate(((R_, TUNE), (L_, BLUE))):
                w = 6.0 * S[key] / mx
                b = Rectangle(width=max(w, 0.02), height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.85)
                row.add(VGroup(b, label(str(S[key]), font_size=17, color=col)))
            bars.add(row)
        for i, row in enumerate(bars):
            y = 1.6 - 1.05 * i
            row[0].move_to([-3.2, y, 0], aligned_edge=RIGHT)
            for j in (1, 2):
                row[j][0].move_to([-2.9, y + (0.17 if j == 1 else -0.17), 0], aligned_edge=LEFT)
                row[j][1].next_to(row[j][0], RIGHT, buff=0.12)
        leg = VGroup(label(rf"upper register: \ {R_['onsets']} attack times", font_size=18, color=TUNE), label(rf"lower register: \ {L_['onsets']}", font_size=18, color=BLUE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.9)
        note = label(rf"held across the next stronger position, with nothing new there: \\ upper {R_['syncopated']}, \ lower {L_['syncopated']}", font_size=19, color=EAR).to_edge(DOWN, buff=0.9)
        head = label(r"bars 1--16: pitch-split proxy counts", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Monochord splits the encoded notes by a pitch threshold at MIDI sixty-one, a register proxy rather than verified score hand labels, then counts attacks in each group. <bookmark mark='a'/> The left hand plays almost entirely "
            f"on beats and half-beats: only {say(L_['between'])} of its {say(L_['onsets'])} attacks fall between. The right "
            f"hand puts {say(R_['between'])} of its {say(R_['onsets'])} attacks between the eighth notes, on sixteenths. "
            f"<bookmark mark='b'/> And {say(R_['syncopated'])} times a right-hand note starts off the beat and is held across "
            "the next stronger position, with nothing new played there: the classic syncopation, the accent arriving early."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def form(self):
        items = [
            (r"a rag is built like a march: \ sixteen-bar strains, \ each repeated", WHITE),
            (r"\textit{Maple Leaf Rag}: \ AA BB A CC DD, \ the C strain \ (the trio) \ in the subdominant, \ D$\flat$", WHITE),
            (r"published rags are composed; oral ragging also involved improvisation", WHITE),
            (r"player pianos and piano rolls spread it, \ and fixed performances in paper", TUNE),
            (r"Part 21's forms, \ in a new dress", GREY_A),
        ]
        rows_scene(self, r"the form of a rag", items,
                   "A rag is built like a march. <bookmark mark='b'/> Its sections are sixteen-bar strains, each repeated: the "
                   "Maple Leaf Rag runs A A, B B, A, C C, D D, with the C strain, the trio, in the subdominant, D flat. "
                   "<bookmark mark='c'/> Published piano rags are composed works; ragtime also developed through oral performance, improvised ragging and practices not preserved on the printed page. <bookmark mark='d'/> Player pianos and "
                   "their paper rolls spread it, and fixed performances in paper. <bookmark mark='e'/> Part 21's forms, in a new "
                   "dress.", marks="bcde")

    # ------------------------------------------------------------------
    def stride(self):
        items = [
            (r"stride: \ Harlem piano of the 1920s and 30s, \ from ragtime but faster, \ improvised and swung", WHITE),
            (r"the left hand `strides': \ a low bass note, \ then a chord in the middle, \ leaping every beat", WHITE),
            (r"James P. Johnson, \ Fats Waller, \ Willie `The Lion' Smith; \ then Art Tatum's virtuosity", WHITE),
            (r"the even eighths of ragtime become swung eighths", TUNE),
            (r"chapter 5 measures that swing", GREY_A),
        ]
        rows_scene(self, r"stride", items,
                   "From ragtime came stride, the Harlem piano style of the 1920s and 30s: faster, improvised, and swung. "
                   "<bookmark mark='b'/> The left hand strides, a low bass note then a chord in the middle, leaping on every "
                   "beat. <bookmark mark='c'/> Its masters were James P. Johnson, Fats Waller and Willie The Lion Smith, and "
                   "then Art Tatum. <bookmark mark='d'/> And the even eighths of ragtime became swung eighths. "
                   "<bookmark mark='e'/> Chapter five measures that swing.", marks="bcde")
