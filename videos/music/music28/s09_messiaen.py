from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403


class Messiaen(SoundScene):
    def construct(self):
        chapter(self, 8, r"Messiaen: \ modes and palindromes", r"What is a rhythm that cannot be reversed?", extra=((1941, r"\textit{Quartet for the End of Time}"),))
        self.quartet()
        self.hear()
        self.count()
        self.added_heard()
        self.added()

    # ------------------------------------------------------------------
    def quartet(self):
        items = [
            (r"Olivier Messiaen, \ 1908--1992: \ organist in Paris for sixty years, \ a devout Catholic", WHITE),
            (r"a prisoner of war in 1940--41: \ the \textit{Quartet for the End of Time}, \ first played in the camp", WHITE),
            (r"birdsong transcribed in the field, \ rhythms from Greek metre and Indian \textit{deśītālas}", WHITE),
            (r"modes of limited transposition \ (chapter two) \ and non-retrogradable rhythms", TUNE),
            (r"his music is in copyright: \ the example is ours, \ built with his rules", GREY_A),
        ]
        rows_scene(self, r"Messiaen", items,
                   "Olivier Messiaen turned symmetry into a whole language. <bookmark mark='b'/> He was organist of a Paris "
                   "church for some sixty years and a devout Catholic, <bookmark mark='c'/> and in 1940, as a prisoner of "
                   "war, he wrote the Quartet for the End of Time, first played in the camp in January 1941. "
                   "<bookmark mark='d'/> He transcribed birdsong in the field and took rhythms from Greek metres and from a "
                   "medieval Indian list of rhythms, the deśītālas. <bookmark mark='e'/> To his symmetric modes he added "
                   "symmetric rhythms. <bookmark mark='f'/> His music is in copyright, so the example is ours, built by his "
                   "rules.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("messiaen")
        c = clip("messiaen.mode2")
        rh = d["rhythm"]
        W = 9.0
        total = sum(rh)
        boxes = VGroup()
        x = -W / 2
        for r in rh:
            w = W * r / total
            boxes.add(Rectangle(width=w - 0.06, height=0.6, stroke_width=0, fill_color=TUNE, fill_opacity=0.8).move_to([x + w / 2, 1.2, 0]))
            x += w
        nums = VGroup(*[label(str(r), font_size=24, color=WHITE).move_to(b) for r, b in zip(rh, boxes)])
        mirror = DashedLine([0, 1.75, 0], [0, 0.65, 0], color=EAR, stroke_width=3)
        g = mroll(d["notes"], width=9.0, height=2.0, lo=58, hi=82, color=TUNE).move_to(DOWN * 1.3)
        head = label(r"a rhythm that reads the same backwards, \ with chords from the second mode \ (ours)", font_size=24, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A non-retrogradable rhythm is a palindrome: it reads the same forwards and backwards, so playing it in reverse "
            "changes nothing. Here, durations of one, two, three, two and one sixteenths, mirrored about the middle. Each "
            "duration carries a chord drawn from Messiaen's second mode, the octatonic, and the whole figure is played "
            "twice."
        ):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(nums), FadeIn(mirror), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"a palindrome, \ twice", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in d["notes"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("messiaen")
        ks = list(range(2, 17, 2))
        pal = [d["palindromes"][str(k)] for k in ks]
        allc = [d["all"][str(k)] for k in ks]
        ax = Axes(x_range=[0, 16, 2], y_range=[0, 5, 1], x_length=7.4, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 18}, x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": False}).move_to(LEFT * 2.0 + DOWN * 0.3)
        ylabels = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v, t in ((1, "10"), (2, "100"), (3, "1,000"), (4, "10,000"))])
        c1 = ax.plot_line_graph(ks, [np.log10(v) for v in allc], line_color=GREY_A, add_vertex_dots=True, stroke_width=3)
        c2 = ax.plot_line_graph(ks, [np.log10(v) for v in pal], line_color=TUNE, add_vertex_dots=True, stroke_width=4)
        xl = label(r"length, \ in sixteenths \ (durations of 1 to 4)", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (rf"16 sixteenths: \ {d['all']['16']:,} rhythms".replace(",", "{,}"), GREY_A),
            (rf"palindromes among them: \ {d['palindromes']['16']}", TUNE),
            (r"a palindrome is half a rhythm, \ mirrored: \ about the square root of the count", WHITE),
            (r"rare, \ and so audible as a shape", EAR))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.6))
        side.move_to(RIGHT * 4.3 + DOWN * 0.2)
        with self.voiceover(
            "How rare are they? Count every rhythm of a given length made of durations from one to four sixteenths, on a "
            "logarithmic scale. <bookmark mark='a'/> Sixteen sixteenths, one four-four bar, can be filled in "
            f"{say(d['all']['16'])} ways. <bookmark mark='b'/> Only {say(d['palindromes']['16'])} of them are palindromes. "
            "<bookmark mark='c'/> A palindrome is decided by its first half alone, so their number grows like the square "
            "root of the total. <bookmark mark='d'/> That rarity is what makes the mirror audible: a listener who hears the "
            "middle can predict the rest."
        ) as vo:
            self.play(Create(ax), FadeIn(ylabels), FadeIn(xl), Create(c1), Create(c2))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def added(self):
        items = [
            (r"added values: \ a short note, \ a dot or a rest added to a regular rhythm, \ to unbalance it", WHITE),
            (r"rhythmic canons, \ augmentation by uneven ratios", WHITE),
            (r"birdsong: \ \textit{Catalogue d'oiseaux} \ (1956--58), \ each bird transcribed and harmonized", WHITE),
            (r"his pupils: \ Boulez, \ Stockhausen, \ Xenakis: \ the next part's serialism and Part 30's sound itself", TUNE),
            (r"a theorem in pitch, \ a palindrome in time: \ symmetry as a composer's material", GREY_A),
        ]
        rows_scene(self, r"more of Messiaen's techniques", items,
                   "He had other techniques. <bookmark mark='b'/> Added values: a short note, a dot or a rest added to a "
                   "regular rhythm to throw it off balance. <bookmark mark='c'/> Rhythmic canons, with augmentation by uneven "
                   "ratios. <bookmark mark='d'/> And birdsong, transcribed in the field and harmonized, in the Catalogue of "
                   "Birds of the 1950s. <bookmark mark='e'/> His pupils included Pierre Boulez, Karlheinz Stockhausen and Iannis "
                   "Xenakis, who lead into the next part's serialism and Part 30's sound itself. <bookmark mark='f'/> Symmetry, "
                   "a theorem in pitch and a palindrome in time, had become a composer's material.", marks="cdef")

    # ------------------------------------------------------------------
    def added_heard(self):
        d = load("added")
        c = clip("added.two")
        def row(durs, col):
            g = VGroup()
            x = -5.0
            for k, du in enumerate(durs):
                w = 0.55 * du
                g.add(Rectangle(width=w - 0.06, height=0.5, stroke_width=0, fill_color=col if du == 2 else EAR, fill_opacity=0.85).move_to([x + w / 2, 0, 0]))
                x += w
            return g
        r1 = row(d["regular"], GREY_A).shift(UP * 0.9)
        r2 = row(d["added"], TUNE).shift(DOWN * 0.9)
        l1 = label(r"regular", font_size=22, color=GREY_A).next_to(r1, LEFT, buff=0.3)
        l2 = label(r"two added values", font_size=22, color=TUNE).next_to(r2, LEFT, buff=0.3)
        head = label(r"Messiaen's added value: \ a sixteenth slipped in", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "And his added value, heard. Eight even notes on a woodblock. Then the same eight with a sixteenth slipped into "
            "two of them, in pink. Nothing else changes, but the even pattern is broken twice, and the second version will "
            "not settle into a bar."
        ):
            self.play(FadeIn(head), FadeIn(r1), FadeIn(r2), FadeIn(l1), FadeIn(l2))
        with self.listen(c) as snd:
            window(snd, r"even, \ then added", detail=r"Part 9's bars", corner=DL, tag_corner=DR)
            on1 = np.concatenate([[0], np.cumsum(d["regular"])[:-1]])
            on2 = np.concatenate([[0], np.cumsum(d["added"])[:-1]])
            flash(snd, list(r1), [d["starts"]["regular"] + t * d["unit"] for t in on1], hot=WHITE, base=GREY_A)
            flash(snd, list(r2), [d["starts"]["added"] + t * d["unit"] for t in on2], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()
