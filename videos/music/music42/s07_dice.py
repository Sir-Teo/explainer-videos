from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403


class Dice(SoundScene):
    def construct(self):
        chapter(self, 6, r"Dice games", r"Can a pair of dice compose a minuet?")
        self.history()
        self.table()
        self.hear()
        self.count()
        self.probability()
        self.meaning()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Kirnberger, \ \textit{Der allezeit fertige Polonoisen- und Menuettencomponist} \ (1757): \ minuets by dice", WHITE),
            (r"C. P. E. Bach \ (1758) \ and others followed: \ a parlour game for people who could read music", WHITE),
            (r"a \textit{Musikalisches W\"urfelspiel} \ printed in 1792 under Mozart's name \ (K. 516f; \ the attribution is uncertain)", WHITE),
            (r"the trick: \ a table of bars, \ one column per bar of the piece, \ the dice choose the row", TUNE),
            (r"the composer's work is all in the table; \ the dice only choose", GREY_A),
        ]
        rows_scene(self, r"composing by dice, \ 1757", items,
                   "In 1757 Johann Philipp Kirnberger published a book whose title promises the ever-ready composer of polonaises "
                   "and minuets. <bookmark mark='b'/> Carl Philipp Emanuel Bach followed in 1758, and others after him: a parlour "
                   "game for people who could read music. <bookmark mark='c'/> The most famous, printed in 1792 under Mozart's "
                   "name, may or may not be his. <bookmark mark='d'/> The trick is a table of bars: one column for each bar of "
                   "the piece, and the dice choose the row. <bookmark mark='e'/> All the composing is in the table; the dice "
                   "only choose.", marks="bcde")

    # ------------------------------------------------------------------
    def grid(self, d, cell=0.62):
        cells = VGroup()
        for b in range(16):
            for s in range(11):
                r = Rectangle(width=cell, height=0.3, stroke_color=GREY_D, stroke_width=1, fill_color=DIM, fill_opacity=0.4)
                r.move_to([-5.0 + cell * b, 1.6 - 0.32 * s, 0])
                cells.add(r)
        rl = VGroup(*[label(rf"{s}", font_size=13, color=GREY_A).move_to([-5.0 - 0.55, 1.6 - 0.32 * (s - 2), 0]) for s in range(2, 13)])
        cl = VGroup(*[label(roman_tex(c_), font_size=12, color=GREY_A).move_to([-5.0 + cell * b, 2.0, 0]) for b, c_ in enumerate(d["plan"])])
        g = VGroup(cells, rl, cl)
        g.cell = lambda b, s: cells[b * 11 + (s - 2)]
        return g

    def table(self):
        d = load("dice")
        g = self.grid(d)
        for b in (7, 15):
            for s in range(2, 13):
                g.cell(b, s).set_fill(BLUE, 0.5)
        cap = VGroup(label(r"16 bars across, \ the dice's sums 2 to 12 down: \ 176 bars of ours over one chord plan", font_size=18, color=WHITE),
                     label(r"every bar starts on a chord tone in one register, \ so any can follow any; \ bars 8 and 16 are the same cadence in every row", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        head = label(r"our minuet table", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is our own table, in the same format. Sixteen bars of a minuet across, and down the side the sums two dice "
            "can make, two to twelve: a hundred and seventy-six bars, every one ours, over a fixed plan of chords shown along "
            "the top. <bookmark mark='a'/> The eighteenth-century trick is in how the bars are made: every option for a bar "
            "starts on a tone of that bar's chord in the same register, so any option can follow any other, and the "
            "cadence bars, eight and sixteen, are the same in every row."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("dice")
        c = clip("dice.two")
        g = self.grid(d)
        rolls = d["rolls"]
        roll_txt = VGroup(*[label(r"throws: \ " + r" \ ".join(str(x) for x in r), font_size=17, color=col) for r, col in zip(rolls, (TUNE, BLUE))]).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=1.0)
        head = label(r"two minuets, \ thrown", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Throw the dice sixteen times and you have a minuet. Hear two, thrown with a seeded random generator, the first "
            "lit in gold, the second in blue."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(roll_txt))
        st = d["starts"]
        beat = 0.4
        with self.listen(c) as snd:
            window(snd, r"two dice minuets", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            lit = {}
            for k, (key, col) in enumerate((("one", TUNE), ("two", BLUE))):
                for b in range(16):
                    t0 = st[key] + 3 * b * beat
                    pulse(snd, g.cell(b, rolls[k][b]), t0, t0 + 3 * beat, buff=0.03, color=col)
                    lit.setdefault((b, rolls[k][b]), []).append((t0, col))
            for (b, sm), evs in lit.items():
                def upd(m, now, evs=evs):
                    col = None
                    for t0, c_ in evs:
                        if now >= t0:
                            col = c_
                    m.set_fill(col if col else DIM, 0.75 if col else 0.4)
                snd.drive(g.cell(b, sm), upd)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("dice")
        n = d["count"]
        rows_ = text_rows([
            (rf"naively: \ 11 choices for each of 16 bars, \ $11^{{16}}$ \ = \ {n['naive']:,}", WHITE),
            (r"but bars 8 and 16 are the same in every row, \ and some rows repeat a bar", WHITE),
            (rf"distinct minuets: \ the product of each bar's distinct options \ = \ {n['distinct']:,}", TUNE),
            (rf"the two minuets just heard share {d['shared_bars']} of their 16 bars", WHITE),
            (r"Mozart's table is often quoted at about $7.6 \times 10^{14}$ \ distinct minuets, \ by the same reasoning", GREY_A),
        ])
        head = label(r"how many minuets?", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How many minuets does the table hold? <bookmark mark='a'/> Naively, eleven choices for each of sixteen bars: "
            "eleven to the sixteenth, about forty-six million billion. <bookmark mark='b'/> But the cadence bars are the same "
            "in every row, and in some columns two sums choose the same bar. <bookmark mark='c'/> Distinct minuets are the "
            "product of each bar's distinct options: about sixteen million million, still far more than anyone could play. "
            f"<bookmark mark='d'/> The two we just heard share {say(d['shared_bars'])} of their sixteen bars. "
            "<bookmark mark='e'/> The 1792 table attributed to Mozart is usually quoted at about seven hundred and sixty "
            "million million, by the same reasoning."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def probability(self):
        d = load("dice")
        p = d["p"]
        n = d["count"]
        x0 = -5.6
        bars = VGroup()
        for i, s in enumerate(range(2, 13)):
            h = 3.0 * p[str(s)] / max(p.values())
            bars.add(VGroup(Rectangle(width=0.42, height=h, stroke_width=0, fill_color=EAR if s == 7 else BLUE, fill_opacity=0.85).move_to([x0 + 0.5 * i, -1.6 + h / 2, 0]),
                            label(rf"{s}", font_size=15, color=GREY_A).move_to([x0 + 0.5 * i, -1.9, 0])))
        side = VGroup(label(r"two dice do not choose evenly: \ 7 comes 6 times in 36, \ 2 and 12 once", font_size=19, color=WHITE),
                      label(rf"so some minuets are likelier: \ the likeliest has probability {n['p_likeliest']:.1e}", font_size=19, color=WHITE),
                      label(rf"the game's entropy: \ {n['entropy_bits']:.1f} bits, \ against {n['uniform_bits']:.1f} if every minuet were equally likely", font_size=19, color=TUNE),
                      label(r"bits: \ how many yes-or-no questions it takes, \ on average, \ to name the minuet thrown", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 2.2 + UP * 0.2)
        head = label(r"what the dice favour", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "There is a subtlety the games' printers ignored. <bookmark mark='a'/> Two dice do not choose evenly: a sum of "
            "seven comes six times in thirty-six, a two or a twelve once. <bookmark mark='b'/> So the bars in the middle row "
            "come up far more often, and some minuets are much likelier than others. <bookmark mark='c'/> Information "
            f"theory gives one number for the game's variety, its entropy: {say(n['entropy_bits'], 1)} bits, against "
            f"{say(n['uniform_bits'], 1)} if every distinct minuet were equally likely. A bit is one yes-or-no "
            "question; it would take about forty-one, on average, to name the minuet you threw."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        items = [
            (r"the dice game is a grammar with one rule per bar: \ the composer wrote the grammar", WHITE),
            (r"every output is good because every bar was made to fit every neighbour", WHITE),
            (r"nothing is judged after the throw: \ generate, \ never test", WHITE),
            (r"the next step, \ two centuries later: \ generate freely, \ then test", TUNE),
            (r"chapter 7: \ a computer in Illinois, \ 1957", GREY_A),
        ]
        rows_scene(self, r"what the dice game is", items,
                   "What is a dice game, as a method? <bookmark mark='b'/> It is a grammar with one rule per bar, and the "
                   "composer wrote the grammar. <bookmark mark='c'/> Every output is acceptable because every bar was made to fit "
                   "every neighbour, <bookmark mark='d'/> so nothing is judged after the throw: generate, and never test. "
                   "<bookmark mark='e'/> The next step came two centuries later: generate freely, and then test. "
                   "<bookmark mark='f'/> Chapter seven goes to a computer in Illinois, in 1957.", marks="cdef")
